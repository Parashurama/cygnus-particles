#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
#from OpenGL.GL.NV.transform_feedback import *
#from OpenGL.GL.ARB.instanced_arrays import glVertexAttribDivisorARB
#from OpenGL.GL.ARB.draw_instanced import glInitDrawInstancedARB,glDrawArraysInstancedARB,glDrawElementsInstancedARB

from glLibs.glObjects import BufferObject, VertexArrayObject, TransformFeedback, QueryObject

from particle_system import ParticleSystem
from particle_structs import Particle
from particle_domain import Disc, Line, Triangle, Square, Sphere
from particle_emitter import Emitter, update_particles
from particle_emitter_structs import BasicEmitter
from particle_emitter_utils import FillUniformBuffer, Unpack
from particle_emitter_2nd import PerParticleEmitter

from particle_emitter_vars import DEFAULT_MAX_PARTICLE_BUFFER_SIZE,\
                                  PARTICLE_DATA_SIZE,\
                                  EMITTER_TYPE_REF,\
                                  EMITTER_UNIFORMS_SRC_DATA,\
                                  EMITTER_UNIFORMS_LIST,\
                                  DOMAIN_REF

from root import cVars, default_particle_system, GenId, ReferenceName

import random

class MeshEmitter(Emitter):
    def __init__(self, name, position, mesh, fire_rate, particle_template, particle_deviation={}, controllers=[], renderer=None, system=default_particle_system):
        Emitter.__init__(self, name, position, fire_rate, particle_template, particle_deviation=particle_deviation, controllers=controllers, renderer=renderer, system=system)
        
        self.mesh = mesh
        
    def select_emitter_type(self, position, particle_template):
        
        if   isinstance(position, tuple):
            self.emitter_type=EMITTER_TYPE_REF['PointEmitter'];
            self.emitter_position = tuple(position)
            
        else:
            raise ValueError("Invalid Emitter Type {},{}".format(type(position), position))
            
        if   isinstance(particle_template, Particle):
            self.emitter_type_flag = 'Basic'
            self.emitter_shader = cVars.MeshEmitterShader
            self.update_shader = cVars.UpdateShader
            self.update_function = update_simple_particle_emitter
            
            if self.renderer_flag == 'MeshRenderer':
                raise NotImplementedError('')
                self.render_function = simple_render_mesh
            else:
                self.render = self.render_simple
                
        elif isinstance(particle_template, PerParticleEmitter):
            raise NotImplementedError('')
            self.emitter_type_flag = 'PerParticle'
            self.emitter_shader = cVars.MeshEmitterShader
            self.update_shader = cVars.UpdateShader
            self.update_function = update_complex_particle_emitter
            
            if self.renderer_flag == 'MeshRenderer':
                  raise NotImplementedError('')
            else:
                self.render = self.render_complex
            
        else:
            raise ValueError("Invalid Template Type {},{}".format(type(particle_template), particle_template))
        
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
        
        return BLOCK_EMITTER_UNIFORMS






########## MESH PARTICLE EMITTER ################
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
        self.mesh.vertexes_buffer.bind_asTextureBuffer(1, 'R32F')
        
        glUniform1i( Uniforms['vertex_count'], self.mesh.vertex_count)
        glUniform1f( Uniforms['ModelScale'], 2)
        
        glUniform1f( Uniforms['ParticleSystemcount'], particles_to_emit)
        glUniform2f( Uniforms['seed'], random.random(), random.random())
        
        with TransformFeedback(self.VBO_FeedBack, GL_POINTS, query=False):
            with self.VAO_A_Emit:
                glDrawArrays(GL_POINTS, 0, particles_to_emit )

    self.emitted_particles = particles_to_emit
