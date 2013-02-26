#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *

from glLibs.glObjects import BufferObject, VertexArrayObject, TransformFeedback, QueryObject
from particle_emitter_utils import FillUniformBuffer, Unpack
from particle_renderer import PointRenderer, PointSpriteRenderer, AnimatedPointSpriteRenderer, ParticleMeshRenderer
from particle_emitter_vars import UPDATER_UNIFORMS_SRC_DATA,\
                                  DOMAIN_REF,\
                                  PARTICLE_DATA_SIZE

class BasicEmitter(object):    
    @property
    def particles_count(self):
        return self.QO_Geometry.primitive_count+self.emitted_particles
    
    def parse_controllers(self):
        self.controller_flags={}
        
        for flag, controller in ( (controller.controller_flag, controller) for controller in self.particle_controllers):
            if not flag in self.controller_flags:
                self.controller_flags[flag]=[controller]
            else:
                self.controller_flags[flag].append(controller)
        
        for flag, controller in self.controller_flags.items():
            if isinstance(controller, list) and len(controller) < 2 and flag not in ('COLLECTOR_CONTROLLER', 'MAGNETIC_CONTROLLER', 'BOUNCE_CONTROLLER') :
                self.controller_flags[flag]=controller[0]

        self.RefParticleDomains = {'TRIANGLE_DOMAIN':[], 'SQUARE_DOMAIN':[], 'CIRCLE_DOMAIN':[]}
        
        if 'COLLECTOR_CONTROLLER' in self.controller_flags:
            for collector in self.controller_flags['COLLECTOR_CONTROLLER']:
                self.RefParticleDomains[collector.domain.domain_flag].append(collector.domain)

        if 'BOUNCE_CONTROLLER' in self.controller_flags:
            for collector in self.controller_flags['BOUNCE_CONTROLLER']:
                self.RefParticleDomains[collector.domain.domain_flag].append(collector.domain)
        
        if 'COLOR_CONTROLLER' in self.controller_flags:
            self.particle_renderer.color_blender = self.controller_flags['COLOR_CONTROLLER']
        
        if 'GROWTH_CONTROLLER' in self.controller_flags:
            self.particle_renderer.growth_controller = self.controller_flags['GROWTH_CONTROLLER']
    
    def select_particle_renderer(self, renderer):
        
        if   isinstance(renderer, PointRenderer) : self.renderer_flag = 'PointRenderer'
        elif isinstance(renderer, PointSpriteRenderer) : self.renderer_flag = 'PointSpriteRenderer'
        elif isinstance(renderer, AnimatedPointSpriteRenderer) : self.renderer_flag = 'AnimatedPointSpriteRenderer'
        elif isinstance(renderer, ParticleMeshRenderer) : self.renderer_flag = 'MeshRenderer'
        else: raise ValueError("Invalid Renderer Type: '{}'".format(renderer.__class__.__name__))
        
        renderer.set_parent_emitter(self)
    
    def create_update_shader_states(self):
        VBO_STRIDE=PARTICLE_DATA_SIZE
                
        self.VAO_A_Update=VertexArrayObject()
        self.VAO_A_Update.bind()
        
        self.VBO_Geometry.bind()
        
        Attributes = self.update_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Position'] )
        glEnableVertexAttribArray( Attributes['Velocity'] )
        glEnableVertexAttribArray( Attributes['Type'] )
        glEnableVertexAttribArray( Attributes['Age'])
        
        glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
        glVertexAttribPointer( Attributes['Velocity'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(12) )
        glVertexAttribPointer( Attributes['Type'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(24) )
        glVertexAttribPointer( Attributes['Age'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(28) )

        ##########################
        
        self.VAO_B_Update=VertexArrayObject()
        self.VAO_B_Update.bind()
        
        self.VBO_FeedBack.bind()
        
        Attributes = self.update_shader.Attributes
        
        glEnableVertexAttribArray( Attributes['Position'] )
        glEnableVertexAttribArray( Attributes['Velocity'] )
        glEnableVertexAttribArray( Attributes['Type'] )
        glEnableVertexAttribArray( Attributes['Age'])
        
        glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
        glVertexAttribPointer( Attributes['Velocity'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(12) )
        glVertexAttribPointer( Attributes['Type'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(24) )
        glVertexAttribPointer( Attributes['Age'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(28) )
    
        self.VAO_B_Update.unbind()
    
    def setup_emitter_uniforms_buffer(self):
        
        self.UBO_EmitterUniforms = None # Placeholder for Uniform Buffer Object created later
        
        self.update_emitter_uniforms_buffer()
    
    def setup_updater_uniforms_buffer(self):
        
        self.UBO_UpdaterUniforms = None # Placeholder for Uniform Buffer Object created later
        
        self.update_updater_uniforms_buffer()
        
    def update_updater_uniforms_buffer(self):
        BLOCK_EMITTER_UNIFORMS = self.set_updater_uniforms()
        
        BUFFER, OffsetInfo = self.update_shader.GetUniformBuffer('UPDATER_UNIFORMS')
        
        FillUniformBuffer(BLOCK_EMITTER_UNIFORMS, BUFFER, OffsetInfo)
        
        if self.UBO_UpdaterUniforms is not None:
            self.UBO_UpdaterUniforms.FastUpdate(BUFFER)
        else:
            self.UBO_UpdaterUniforms = BufferObject(GL_UNIFORM_BUFFER, BUFFER, GL_DYNAMIC_DRAW)
    
    def set_updater_uniforms(self):
        BLOCK_EMITTER_UNIFORMS = UPDATER_UNIFORMS_SRC_DATA.copy()
        
        if 'LIFETIME_CONTROLLER' in self.controller_flags:
              BLOCK_EMITTER_UNIFORMS['PARTICLE_LIFETIME'][1] = [self.controller_flags['LIFETIME_CONTROLLER'].lifetime]
        else: BLOCK_EMITTER_UNIFORMS['PARTICLE_LIFETIME'][1] = [1800]
        
        bool_COLLECTORS = 0
        bool_BOUNCERS = 0
        
        for DOMAIN_TYPE, LIST in self.RefParticleDomains.iteritems():
            basename, uniform_list = DOMAIN_REF[DOMAIN_TYPE]
            n_bouncer=0
            n_controller=0
            for i, domain in enumerate(LIST):
                for attr, l in uniform_list:
                    uniform_name = basename.format(i,attr)
                    try :  BLOCK_EMITTER_UNIFORMS[uniform_name][1] = list(getattr(domain, attr))
                    except TypeError: BLOCK_EMITTER_UNIFORMS[uniform_name][1] = [getattr(domain, attr)]
                    
                if   domain.controller_flag == 'BOUNCE_CONTROLLER' : n_bouncer+=1 ; bool_BOUNCERS = 1
                elif domain.controller_flag == 'COLLECTOR_CONTROLLER' : n_controller+=1 ; bool_COLLECTORS = 1                
            
            if   DOMAIN_TYPE == 'CIRCLE_DOMAIN':
                BLOCK_EMITTER_UNIFORMS['N_CIRCLE_COLLECTOR'][1] = [n_controller]
                BLOCK_EMITTER_UNIFORMS['N_CIRCLE_BOUNCER'][1] = [n_controller+n_bouncer ]
                BLOCK_EMITTER_UNIFORMS['I_CIRCLE_BOUNCER'][1] = [n_controller]
                
            elif DOMAIN_TYPE == 'TRIANGLE_DOMAIN':
                BLOCK_EMITTER_UNIFORMS['N_TRIANGLE_COLLECTOR'][1] = [n_controller]
                BLOCK_EMITTER_UNIFORMS['N_TRIANGLE_BOUNCER'][1] = [n_controller+n_bouncer ]
                BLOCK_EMITTER_UNIFORMS['I_TRIANGLE_BOUNCER'][1] = [n_controller]
                
            elif DOMAIN_TYPE == 'SQUARE_DOMAIN':
                BLOCK_EMITTER_UNIFORMS['N_SQUARE_COLLECTOR'][1] = [n_controller]
                BLOCK_EMITTER_UNIFORMS['N_SQUARE_BOUNCER'][1] = [n_controller+n_bouncer ]
                BLOCK_EMITTER_UNIFORMS['I_SQUARE_BOUNCER'][1] = [n_controller]
        
        BLOCK_EMITTER_UNIFORMS['PARTICLE_COLLECTORS'][1] = [bool_COLLECTORS]
        BLOCK_EMITTER_UNIFORMS['PARTICLE_BOUNCERS'][1] = [bool_BOUNCERS]
        
        i=-1
        if 'MAGNETIC_CONTROLLER' in self.controller_flags:

            basename= 'uMagneticCon[{0}].{1}'
            uniform_list = [('origin',3) , ('sqr_cutoff_distance',1), ('charge', 1), ('epsilon',1) ]
            for i, controller in enumerate(self.controller_flags['MAGNETIC_CONTROLLER']):
                for attr, l in uniform_list:                    
                    uniform_name = basename.format(i,attr)
                    try :  BLOCK_EMITTER_UNIFORMS[uniform_name][1] = list(getattr(controller, attr) )
                    except TypeError: BLOCK_EMITTER_UNIFORMS[uniform_name][1] = [getattr(controller, attr)]
        
        BLOCK_EMITTER_UNIFORMS['N_MAGNETIC_CONTROLLER'][1] = [i+1]
        
        return BLOCK_EMITTER_UNIFORMS
