#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *

from root import InitializeSystem, cVars, GenId, ReferenceName
from particle_renderer import PointRenderer, PointSpriteRenderer, AnimatedPointSpriteRenderer
from particle_structs import Particle
from particle_emitter_structs import BasicEmitter
from particle_emitter_utils import *
from particle_emitter_vars import *

from glLibs.glObjects import BufferObject, VertexArrayObject, TransformFeedback, QueryObject

import random

class PerParticleEmitter(BasicEmitter):
    def __init__(self, name, fire_rate=None, velocity=(0.0,0.0,0.0), color=(1.0,1.0,1.0,1.0), particle_template=None, particle_deviation={}, controllers=[], renderer=None):
        
        self.__id__ = GenId(self)
        
        self.select_particle_renderer(renderer)
        
        if not isinstance(particle_template, Particle):
            raise TypeError("Invalid Particle Template Argument. Must be 'Particle' instance")
        
        self.emitter_name = name ; ReferenceName(self, name)
        self.emitter_fire_rate = fire_rate
        
        self.position = (0.0,0.0,0.0)
        self.velocity = velocity
        self.color = color
        self.age = 0.0
        self.point_size = None
        
        self.parent_emitter = None
        self.particle_template = particle_template
        self.particle_deviation = particle_deviation
        
        self.particle_controllers = controllers
        self.particle_renderer = renderer
        
        self.update_shader = cVars.UpdateShader
        self.emitter_shader = cVars.PerParticleEmitterShader
        
        self.parse_controllers()
        
        self.setup_emitter_uniforms_buffer()
        self.setup_updater_uniforms_buffer()
        
        ##### Create Particle Data        
        self.VBO_Geometry= BufferObject(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW, size=DEFAULT_MAX_PARTICLE_BUFFER_SIZE*8)
        self.VBO_FeedBack= BufferObject(GL_ARRAY_BUFFER, None, GL_STREAM_DRAW, size=DEFAULT_MAX_PARTICLE_BUFFER_SIZE*8)
        
        self.QO_Geometry = QueryObject()
        self.QO_FeedBack = QueryObject()
        
        
        self.particle_renderer.BuildRenderState(self.VBO_Geometry,self.VBO_FeedBack)
        self.emitted_particles = 0
        self.emission_time=0.0
        self.real_emitted_particles=0
    
    def select_particle_renderer(self, renderer):
        
        if   isinstance(renderer, PointRenderer) : self.renderer_flag = 'PointRenderer'
        elif isinstance(renderer, PointSpriteRenderer) : self.renderer_flag = 'PointSpriteRenderer'
        elif isinstance(renderer, AnimatedPointSpriteRenderer) : self.renderer_flag = 'AnimatedPointSpriteRenderer'
        #elif isinstance(renderer, MeshRenderer) : self.renderer_flag = 'MeshRenderer'
        else: raise ValueError("Invalid Renderer Type {},{}".format(type(renderer), renderer))
        
        renderer.set_parent_emitter(self)
    
    def set_parent_emitter(self, parent_emitter):
        self.parent_emitter = parent_emitter
        
        self.create_emitter_shader_states()
        self.create_update_shader_states()
    
    def update_emitter_uniforms_buffer(self):
        BLOCK_EMITTER_UNIFORMS = self.set_emitter_uniforms()
        
        BUFFER, OffsetInfo = self.emitter_shader.GetUniformBuffer('PER_PARTICLE_EMITTER_UNIFORMS')
        
        FillUniformBuffer(BLOCK_EMITTER_UNIFORMS, BUFFER, OffsetInfo)
        
        if self.UBO_EmitterUniforms is not None:
            self.UBO_EmitterUniforms.FastUpdate(BUFFER)
        else:
            self.UBO_EmitterUniforms = BufferObject(GL_UNIFORM_BUFFER, BUFFER, GL_DYNAMIC_DRAW)
    
    def set_emitter_uniforms(self):
        BLOCK_EMITTER_UNIFORMS = EMITTER_SECONDARY_UNIFORMS_SRC_DATA.copy()
        
        BLOCK_EMITTER_UNIFORMS['PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION'][1] = list(self.particle_deviation['position'])
        BLOCK_EMITTER_UNIFORMS['PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION'][1] = list(self.particle_deviation['velocity'])
        BLOCK_EMITTER_UNIFORMS['PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION'][1] = [self.particle_deviation['age']]
        
        BLOCK_EMITTER_UNIFORMS['PER_PARTICLE_EMITTER_PARTICLE_VELOCITY'][1] = list(self.particle_template.velocity)        

        return BLOCK_EMITTER_UNIFORMS    
    
    def create_emitter_shader_states(self):
        VBO_STRIDE=PARTICLE_DATA_SIZE
                
        self.VAO_A_Emit=VertexArrayObject()
        self.VAO_A_Emit.bind()
        
        self.parent_emitter.VBO_Geometry.bind()
        
        Attributes = self.emitter_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Position'] )
        
        glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
        
        ##########################
        
        self.VAO_B_Emit=VertexArrayObject()
        self.VAO_B_Emit.bind()
        
        self.parent_emitter.VBO_FeedBack.bind()
        
        Attributes = self.emitter_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Position'] )
        
        glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
        
        self.VAO_B_Emit.unbind()
    
    def update(self, dt):
        self.update_emitter_uniforms_buffer()        
        emit_new_subparticles(self, dt)
        
        self.update_updater_uniforms_buffer()
        update_particles(self, dt)
    
    def render(self):
        with self.particle_renderer:
            
            glDrawArrays(GL_POINTS, 0, self.particles_count)
        
        
def emit_new_subparticles(self, dt):
    
    Uniforms = self.emitter_shader.Uniforms
    
    self.emission_time+=dt
    if self.emission_time>1.0:
        self.emission_time=0.0
        self.real_emitted_particles=0
    
    virtual_emitted_particles = int(self.emitter_fire_rate*self.emission_time)
    particles_to_emit = (virtual_emitted_particles-self.real_emitted_particles)
    
    self.emitter_shader.Set()
    
    self.UBO_EmitterUniforms.bind_asUniformBuffer(self.emitter_shader.UniformBlocks['PER_PARTICLE_EMITTER_UNIFORMS'])
    
    rnd = random.random
    n_parent_emitter_particles = self.parent_emitter.particles_count
    
    glUniform1f( Uniforms['ParticleSystemcount'], particles_to_emit*n_parent_emitter_particles)
    
    with TransformFeedback(self.VBO_FeedBack, GL_POINTS, query=False):
        with self.VAO_A_Emit:
            for i in xrange(particles_to_emit):
                glUniform2f( Uniforms['seed'], rnd(), rnd())
                glDrawArrays(GL_POINTS, 0, n_parent_emitter_particles )
    
    # End Emission
    self.emitted_particles = particles_to_emit*n_parent_emitter_particles
    self.real_emitted_particles +=particles_to_emit

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
