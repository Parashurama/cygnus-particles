#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from __globals__ import cVars
#from particle_structs import ParticleMesh

from glLibs.glObjects import BufferObject, VertexArrayObject

class Renderer(object):
    color_blender = None
    growth_controller = None
    
    def set_parent_emitter(self, emitter):
        self.parent_emitter = emitter
    
    def SwitchState(self):
        if self.render_state is self.VAO0:
            self.render_state = self.VAO1
        else:
            self.render_state = self.VAO0
    
    def SetState(self):
        raise NotImplementedError('')
        
    def UnsetState(self, *args):
        
        glUseProgram(0)        
        glBindVertexArray(0)
        self.SwitchState()
        
    __enter__ = SetState
    __exit__ = UnsetState
    
class PointRenderer(Renderer):
    flag='POINT_RENDERER'
    def __init__(self,  point_size=1.0,
                        feather = 0.0,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
        self.feather_radius = feather
        self.point_size = point_size
        self.blending = blending
        
    def BuildRenderState(self, *buffer_objects):
        
        cVars.SimplePointRenderShader.Set()
        
        for i,buffer_object in enumerate(buffer_objects):
            setattr(self, 'VAO{}'.format(i), VertexArrayObject() ) 
            with getattr(self, 'VAO{}'.format(i)):
                
                VBO_STRIDE=32
                
                buffer_object.bind()
                
                Attributes=cVars.SimplePointRenderShader.Attributes

                glEnableVertexAttribArray( Attributes['Position'] )
                #glEnableVertexAttribArray( Attributes['Type'])
                glEnableVertexAttribArray( Attributes['Age'])
                
                glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
                #glVertexAttribPointer( Attributes['Type'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(24) )
                glVertexAttribPointer( Attributes['Age'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(28) )
    
        self.render_state = self.VAO0
        
        glUseProgram(0)
        
    def SetState(self):
        
        # render_shader
        cVars.SimplePointRenderShader.Set()
        Uniforms = cVars.SimplePointRenderShader.Uniforms
        
        emitter = self.parent_emitter
        
        if self.color_blender is not None:
            glUniform1f( Uniforms['ColorBlendLifeTime'], self.color_blender.end_time -self.color_blender.start_time)           
            glUniform1i( Uniforms['COLOR_BLENDING'], 1)
            glBindTexture(GL_TEXTURE_1D, self.color_blender.ColorBlendLookup.id)
            
        else:
            glUniform1f( Uniforms['ColorBlendLifeTime'], 0.0)
            glUniform1i( Uniforms['COLOR_BLENDING'], 0)
        
        if self.growth_controller is not None:
              glUniform1f( Uniforms['GROWTH_FACTOR'], self.growth_controller.growth)
        else: glUniform1f( Uniforms['GROWTH_FACTOR'], 0.0)
        
        glUniform1i( Uniforms['TEXTURE_TYPE'], 0)  
        
        glUniform1f( Uniforms['PARTICLE_SIZE'], (emitter.particle_template.point_size or self.point_size)/2)
        glUniform1f( Uniforms['PARTICLE_FEATHER_RADIUS'], self.feather_radius)
        glUniform4f( Uniforms['DEFAULT_PARTICLE_COLOR'], *emitter.particle_template.color)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        glBlendFunc(*self.blending)
        
        self.render_state.bind()
        
    __enter__ = SetState

class PointSpriteRenderer(PointRenderer):
    flag='POINT_SPRITE_RENDERER'
    def __init__(self,  texture,
                        point_size=None,
                        feather = 0.0,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
        self.texture = texture
        self.feather_radius = feather
        self.point_size =  point_size or max( texture.width, texture.height )
        self.blending = blending
        
    def SetState(self):
        
        # render_shader
        cVars.SimplePointRenderShader.Set()
        Uniforms = cVars.SimplePointRenderShader.Uniforms
        
        emitter = self.parent_emitter
        
        if self.color_blender is not None:
            glUniform1f( Uniforms['ColorBlendLifeTime'], self.color_blender.end_time -self.color_blender.start_time)           
            glUniform1i( Uniforms['COLOR_BLENDING'], 1)
            glBindTexture(GL_TEXTURE_1D, self.color_blender.ColorBlendLookup.id)
            
        else:
            glUniform1f( Uniforms['ColorBlendLifeTime'], 0.0)
            glUniform1i( Uniforms['COLOR_BLENDING'], 0)
        
        if self.growth_controller is not None:
              glUniform1f( Uniforms['GROWTH_FACTOR'], self.growth_controller.growth)
        else: glUniform1f( Uniforms['GROWTH_FACTOR'], 0.0)
        
        glUniform1i( Uniforms['TEXTURE_TYPE'], 1)  
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glUniform1f( Uniforms['PARTICLE_SIZE'], (emitter.particle_template.point_size or self.point_size)/2)
        glUniform1f( Uniforms['PARTICLE_FEATHER_RADIUS'], self.feather_radius)
        glUniform4f( Uniforms['DEFAULT_PARTICLE_COLOR'], *emitter.particle_template.color)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        glBlendFunc(*self.blending)
        
        self.render_state.bind()
        
    __enter__ = SetState
    
class AnimatedPointSpriteRenderer(PointRenderer):
    flag='ANIMATED_POINT_SPRITE_RENDERER'
    def __init__(self,  texture,
                        point_size=None,
                        feather = 0.0,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
                            
        self.texture = texture
        self.feather_radius = feather
        self.point_size =  point_size or max( texture.width, texture.height )
        self.blending = blending
        
    def SetState(self):
        
        # render_shader
        cVars.SimplePointRenderShader.Set()
        Uniforms = cVars.SimplePointRenderShader.Uniforms
        
        emitter = self.parent_emitter
        
        if self.color_blender is not None:
            glUniform1f( Uniforms['ColorBlendLifeTime'], self.color_blender.end_time -self.color_blender.start_time)           
            glUniform1i( Uniforms['COLOR_BLENDING'], 1)
            glBindTexture(GL_TEXTURE_1D, self.color_blender.ColorBlendLookup.id)
            
        else:
            glUniform1f( Uniforms['ColorBlendLifeTime'], 0.0)
            glUniform1i( Uniforms['COLOR_BLENDING'], 0)
        
        if self.growth_controller is not None:
              glUniform1f( Uniforms['GROWTH_FACTOR'], self.growth_controller.growth)
        else: glUniform1f( Uniforms['GROWTH_FACTOR'], 0.0)
        
        glUniform1i( Uniforms['TEXTURE_TYPE'], 2)  
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture.id)
        
        glUniform1f( Uniforms['PARTICLE_SIZE'], (emitter.particle_template.point_size or self.point_size)/2)
        glUniform1f( Uniforms['PARTICLE_FEATHER_RADIUS'], self.feather_radius)
        glUniform4f( Uniforms['DEFAULT_PARTICLE_COLOR'], *emitter.particle_template.color)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        glBlendFunc(*self.blending)
        
        self.render_state.bind()
        
    __enter__ = SetState
    
"""
class MeshRenderer(object):
    flag='MESH_RENDERER'
    def __init__(self,  mesh_object,
                        size=1,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
        
        assert (isinstance(mesh_object, ParticleMesh) )
        
        self.mesh_object = mesh_object
        self.texture = mesh_object.texture
        self.point_size =  size
        self.blending = blending
"""
