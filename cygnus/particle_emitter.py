#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
#from OpenGL.GL.NV.transform_feedback import *
from OpenGL.GL.ARB.instanced_arrays import glVertexAttribDivisorARB
from OpenGL.GL.ARB.draw_instanced import glInitDrawInstancedARB,glDrawArraysInstancedARB,glDrawElementsInstancedARB

from glLibs.glObjects import BufferObject, VertexArrayObject, TransformFeedback, QueryObject

from particle_system import ParticleSystem
from particle_structs import Particle
from particle_domain import Disc, Line, Triangle, Square, Sphere
from particle_emitter_structs import BasicEmitter
from particle_emitter_utils import FillUniformBuffer, Unpack
from particle_emitter_2nd import PerParticleEmitter

from particle_emitter_vars import DEFAULT_MAX_PARTICLE_BUFFER_SIZE,\
                                  PARTICLE_DATA_SIZE,\
                                  EMITTER_UNIFORMS_SRC_DATA,\
                                  EMITTER_UNIFORMS_LIST,\
                                  DOMAIN_REF,\
                                  EMITTER_TYPE_REF

from root import cVars, default_particle_system, GenId, ReferenceName

import numpy as np
import time
import weakref
import random

class Emitter(BasicEmitter):
    def __init__(self, name, position, fire_rate, particle_template, particle_deviation={}, controllers=[], renderer=None, system=default_particle_system):
        
        self.__id__ = GenId(self)
        assert isinstance(system, ParticleSystem) , 'Invalid Particle System Argument. Must be ParticleSystem instance.'
        assert isinstance(particle_template, Particle) or isinstance(particle_template, PerParticleEmitter) , 'Invalid Particle Template Argument. Must be Particle or PerParticleEmitter instance'
        
        self.select_particle_renderer(renderer)
        self.select_emitter_type(position, particle_template)
        
        # Set emitter variables
        self.emitter_name = name ; ReferenceName(self, name)
        self.emitter_fire_rate = fire_rate
        self.particle_template = particle_template
        self.particle_deviation = particle_deviation
        
        self.particle_controllers = controllers
        self.particle_renderer = renderer
        self.particle_system = weakref.proxy(system)
        self.particle_system.add_group(self)

        # Set controllers
        self.lifetime_controller = None
        self.gravity_controller = None
        self.drag_controller = None
        
        self.particle_controllers.extend(self.particle_system.global_controllers)        
        self.parse_controllers()
        
        self.setup_emitter_uniforms_buffer()
        self.setup_updater_uniforms_buffer()
        
        ##### Create Particle Data        
        self.VBO_Geometry= BufferObject(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW, size=DEFAULT_MAX_PARTICLE_BUFFER_SIZE*8)
        self.VBO_FeedBack= BufferObject(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW, size=DEFAULT_MAX_PARTICLE_BUFFER_SIZE*8)
        
        self.QO_Geometry = QueryObject()
        self.QO_FeedBack = QueryObject()
                
        self.create_emitter_shader_states()
        self.create_update_shader_states()
        
        self.particle_template.set_parent_emitter(self)
        
        self.particle_renderer.BuildRenderState(self.VBO_Geometry,self.VBO_FeedBack)
        self.emitted_particles = 0
        self.emission_time=0.0
        self.real_emitted_particles=0
        self.particles_burst =None
        
    def select_emitter_type(self, position, particle_template):
        
        if   isinstance(position, tuple):   self.emitter_type=EMITTER_TYPE_REF['PointEmitter']; self.emitter_position = tuple(position)
        elif isinstance(position, Square):  self.emitter_type=EMITTER_TYPE_REF['SquareEmitter']; self.emitter_domain = position ; self.emitter_position = position.center
        elif isinstance(position, Line):    self.emitter_type=EMITTER_TYPE_REF['LineEmitter']; self.emitter_domain = position ; self.emitter_position = position.center
        elif isinstance(position, Triangle):self.emitter_type=EMITTER_TYPE_REF['TriangleEmitter']; self.emitter_domain = position ; self.emitter_position = position.center
        elif isinstance(position, Disc):    self.emitter_type=EMITTER_TYPE_REF['CircleEmitter'] if position.inner_radius==position.outer_radius else EMITTER_TYPE_REF['DiscEmitter']; self.emitter_domain = position ; self.emitter_position = position.center
        elif isinstance(position, Sphere):  self.emitter_type=EMITTER_TYPE_REF['SphereEmitter']; self.emitter_domain = position ; self.emitter_position = position.center
        else: raise ValueError("Invalid Emitter Type {},{}".format(position.__class__.__name__, position))
        
        if   isinstance(particle_template, Particle):
            self.emitter_type_flag = 'Basic'
            self.emitter_shader = cVars.EmitterShader
            self.update_shader = cVars.UpdateShader
            self.update_function = update_simple_particle_emitter
            
            if self.renderer_flag == 'MeshRenderer':
                #raise NotImplementedError('')
                self.render = self.render_mesh_simple
            else:
                self.render = self.render_simple
                
        elif isinstance(particle_template, PerParticleEmitter):
            self.emitter_type_flag = 'PerParticle'
            self.emitter_shader = cVars.EmitterShader
            self.update_shader = cVars.UpdateShader
            self.update_function = update_complex_particle_emitter
            
            if self.renderer_flag == 'MeshRenderer':
                  raise NotImplementedError('')
            else:
                self.render = self.render_complex
            
        else:
            raise ValueError("Invalid Template Type {},{}".format(type(particle_template), particle_template))
    
    def update_emitter_uniforms_buffer(self):
        
        BLOCK_EMITTER_UNIFORMS = self.set_emitter_uniforms()
        
        BUFFER, OffsetInfo = self.emitter_shader.GetUniformBuffer('EMITTER_UNIFORMS')
        
        FillUniformBuffer(BLOCK_EMITTER_UNIFORMS, BUFFER, OffsetInfo)
        
        if self.UBO_EmitterUniforms is not None:
            self.UBO_EmitterUniforms.FastUpdate(BUFFER)
        else:
            self.UBO_EmitterUniforms = BufferObject(GL_UNIFORM_BUFFER, BUFFER, GL_DYNAMIC_DRAW)
    
    def set_emitter_uniforms(self):
        BLOCK_EMITTER_UNIFORMS = EMITTER_UNIFORMS_SRC_DATA.copy()
        
        if   self.emitter_type_flag == 'Basic':
            BLOCK_EMITTER_UNIFORMS['PARTICLE_TYPE_TO_EMIT'][1]=[10.0]
           
        elif self.emitter_type_flag == 'PerParticle':
            BLOCK_EMITTER_UNIFORMS['PARTICLE_TYPE_TO_EMIT'][1]=[20.0]
        
        EMITTER_TYPE = self.emitter_type
        
        BLOCK_EMITTER_UNIFORMS['EMITTER_TYPE'][1] = [EMITTER_TYPE]
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_FIRERATE'][1] = [1/float(self.emitter_fire_rate)]
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_POSITION'][1] = list(self.emitter_position)
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_VELOCITY'][1] = list(self.particle_template.velocity)
        
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_POSITION_DEVIATION'][1] = list(self.particle_deviation['position'])
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_VELOCITY_DEVIATION'][1] = list(self.particle_deviation['velocity'])
        BLOCK_EMITTER_UNIFORMS['EMITTER_PARTICLE_AGE_DEVIATION'][1] = [self.particle_deviation['age']]
        
        if   EMITTER_TYPE == 1: #CircleEmitter
            BLOCK_EMITTER_UNIFORMS['CIRCLE_EMITTER_RADIUS'][1] = [self.emitter_domain.radius]
            
        if   EMITTER_TYPE == 2: #DiscEmitter
            BLOCK_EMITTER_UNIFORMS['DISC_EMITTER_RADII'][1] = [self.emitter_domain.inner_radius, self.emitter_domain.outer_radius]
            
        elif EMITTER_TYPE == 3: #LineEmitter
            BLOCK_EMITTER_UNIFORMS['LINE_EMITTER_POINTS'][1] = Unpack(self.emitter_domain.A, self.emitter_domain.B)
            
        elif EMITTER_TYPE == 4: #TriangleEmitter
            BLOCK_EMITTER_UNIFORMS['TRIANGLE_EMITTER_POINTS'][1] = Unpack(self.emitter_domain.A, self.emitter_domain.B, self.emitter_domain.C)
            
        elif EMITTER_TYPE == 5: #SquareEmitter
            BLOCK_EMITTER_UNIFORMS['SQUARE_EMITTER_POINTS'][1] = Unpack(self.emitter_domain.A, self.emitter_domain.B, self.emitter_domain.C, self.emitter_domain.D)
        
        elif EMITTER_TYPE == 6: #SphereEmitter
            
            BLOCK_EMITTER_UNIFORMS['SPHERE_EMITTER_RADII'][1] = [self.emitter_domain.inner_radius, self.emitter_domain.outer_radius]
        
        return BLOCK_EMITTER_UNIFORMS
    
    def Emit(self, n_particles):
        self.particles_burst = (n_particles,)
    
    def create_emitter_shader_states(self):
        VBO_STRIDE=32
        
        self.VAO_A_Emit=VertexArrayObject()
        self.VAO_A_Emit.bind()
        
        self.VBO_Geometry.bind()
        
        Attributes = self.update_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Type'] )        
        glVertexAttribPointer( Attributes['Type'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(24) )
        
        ###################################
        self.VAO_B_Emit=VertexArrayObject()
        self.VAO_B_Emit.bind()
        
        self.VBO_FeedBack.bind()
        
        Attributes = self.update_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Type'] )        
        glVertexAttribPointer( Attributes['Type'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(24) )
        
        self.VAO_B_Emit.unbind()
        
    def update(self, dt):
        self.update_function(self, dt)
        
    def render_simple(self):
        # render with Particle Template
        
        with self.particle_renderer:

            glDrawArrays(GL_POINTS, 0, self.particles_count)
    
    def render_complex(self):
        # render with PerParticleEmitter Template
        
        with self.particle_renderer:

            glDrawArrays(GL_POINTS, 0, self.particles_count)
        
        self.particle_template.render()
    
    #"""
    def render_mesh_simple(self):
        # render Mesh with ParticleMesh Template
        MESH_OBJECT = self.particle_renderer.mesh_object
        
        with self.particle_renderer:
            glDrawElementsInstancedARB(GL_TRIANGLES, MESH_OBJECT.indice_count*3, GL_UNSIGNED_SHORT, MESH_OBJECT.IBO_Vertex_Indices.C_Pointer(0), self.particles_count )
    
    def render_single_mesh_simple(self):
        # render Mesh with ParticleMesh Template
        MESH_OBJECT = self.particle_renderer.mesh_object
        
        with self.particle_renderer:
            glDrawElements(GL_TRIANGLES,  MESH_OBJECT.indice_count*3, GL_UNSIGNED_SHORT,  MESH_OBJECT.IBO_Vertex_Indices.C_Pointer(0))
    
########## BASIC PARTICLE EMITTER ################
def update_simple_particle_emitter(self, dt):
    self.update_emitter_uniforms_buffer()
    emit_new_particles(self, dt)
    
    self.update_updater_uniforms_buffer()
    update_particles(self, dt)

def emit_new_particles(self, dt):
    
    Uniforms = self.emitter_shader.Uniforms
    
    self.emission_time+=dt
    
    virtual_emitted_particles = int(self.emitter_fire_rate*self.emission_time)
    particles_to_emit = (virtual_emitted_particles-self.real_emitted_particles)
    
    if self.particles_burst is not None:
        particles_to_emit = self.particles_burst[0]
        self.particles_burst = None
        print "Emit", particles_to_emit
        
    else:
        self.real_emitted_particles +=particles_to_emit
    
    
    if particles_to_emit:
        
        self.emitter_shader.Set()
        
        self.UBO_EmitterUniforms.bind_asUniformBuffer(self.emitter_shader.UniformBlocks['EMITTER_UNIFORMS'])
    
        glUniform1f( Uniforms['ParticleSystemcount'], particles_to_emit)
        glUniform2f( Uniforms['seed'], random.random(), random.random())
        
        with TransformFeedback(self.VBO_FeedBack, GL_POINTS, query=False):
            with self.VAO_A_Emit:
                glDrawArrays(GL_POINTS, 0, particles_to_emit )

    self.emitted_particles = particles_to_emit
    

def update_particles(self, dt):
    
    byte_offset = PARTICLE_DATA_SIZE*self.emitted_particles 
    
    Uniforms = self.update_shader.Uniforms
    
    self.update_shader.Set()
    
    self.UBO_UpdaterUniforms.bind_asUniformBuffer(self.update_shader.UniformBlocks['UPDATER_UNIFORMS'])
    
    if 'DRAG_CONTROLLER' in self.controller_flags:
          glUniform3f( Uniforms['VISCOUS_DRAG'], 0.0, 0.0, 0.0)
    else: glUniform3f( Uniforms['VISCOUS_DRAG'], 0.0, 0.0, 0.0 )
    
    if 'GRAVITY_CONTROLLER' in self.controller_flags:
          glUniform3f( Uniforms['GRAVITY'], *self.controller_flags['GRAVITY_CONTROLLER'].gravity )
    else: glUniform3f( Uniforms['GRAVITY'], 0.0, 0.0, 0.0 )
        
    glUniform1f( Uniforms['dtime'], dt)
    
    with TransformFeedback(self.VBO_FeedBack, GL_POINTS, byte_offset=byte_offset, query=self.QO_FeedBack):
        with self.VAO_A_Update:
            
            glDrawArrays(GL_POINTS, 0, self.particles_count)
    
    #Ping Pong between VAO
    self.VAO_B_Update, self.VAO_A_Update = self.VAO_A_Update, self.VAO_B_Update
    #Ping Pong between VBO
    self.VBO_Geometry, self.VBO_FeedBack = self.VBO_FeedBack, self.VBO_Geometry
    #Ping Pong between QueryObjects
    self.QO_Geometry, self.QO_FeedBack = self.QO_FeedBack, self.QO_Geometry
    #Ping Pong between Emitter VAO
    self.VAO_A_Emit, self.VAO_B_Emit = self.VAO_B_Emit, self.VAO_A_Emit
    
    glUseProgram(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


########## PER PARTICLE EMITTER ################
def update_complex_particle_emitter(self, dt):
    
    self.particle_template.update(dt)
    
    self.update_emitter_uniforms_buffer()
    emit_new_particles(self, dt)
        
    self.update_updater_uniforms_buffer()
    update_particles(self, dt)

