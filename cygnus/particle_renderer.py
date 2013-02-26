#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from OpenGL.GL.ARB.instanced_arrays import glVertexAttribDivisorARB

from __globals__ import cVars
from particle_structs import ParticleMesh

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
                glEnableVertexAttribArray( Attributes['Age'])
                
                glVertexAttribPointer( Attributes['Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
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
    
#"""
class ParticleMeshRenderer(Renderer):
    flag='MESH_RENDERER'
    def __init__(self,  mesh_file,
                        texture_file=None,
                        size=1,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
        
        self.mesh_object = ParticleMesh(mesh_file)
        self.texture = None
        self.point_size =  size
        self.blending = blending
    
    def BuildRenderState(self, *buffer_objects):
        
        cVars.MeshRenderShader.Set()
        
        for i,buffer_object in enumerate(buffer_objects):
            setattr(self, 'VAO{}'.format(i), VertexArrayObject() ) 
            with getattr(self, 'VAO{}'.format(i)):
                
                Attributes=cVars.MeshRenderShader.Attributes
                
                VBO_STRIDE=24
                self.mesh_object.VBO_Vertex_Data.bind()
                
                glEnableVertexAttribArray( Attributes['Vertex_Position'] )
                #glEnableVertexAttribArray( Attributes['Vertex_TexCoords'] )
                
                glVertexAttribPointer( Attributes['Vertex_Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
                #glVertexAttribPointer( Attributes['Vertex_TexCoords'], 2, GL_FLOAT,False, 0, ctypes.c_void_p(0) )

                # Instance Attributes # Buffer used with transform feedback
                buffer_object.bind()
                
                VBO_STRIDE=32
                
                glEnableVertexAttribArray( Attributes['Instance_Position'] )
                glEnableVertexAttribArray( Attributes['Instance_Age'] )
                
                glVertexAttribPointer( Attributes['Instance_Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
                glVertexAttribDivisorARB( Attributes['Instance_Position'], 1)

                glVertexAttribPointer( Attributes['Instance_Age'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(28) )
                glVertexAttribDivisorARB( Attributes['Instance_Age'], 1)
                
                self.mesh_object.IBO_Vertex_Indices.bind()
                
        self.render_state = self.VAO0
        
        glUseProgram(0)
    
    def SetState(self):

        # render_shader
        cVars.MeshRenderShader.Set()
        Uniforms = cVars.MeshRenderShader.Uniforms
        
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
        
        glUniform1f( Uniforms['PARTICLE_SIZE'], 0.1)#(emitter.particle_template.point_size or self.point_size)/2)
        glUniform4f( Uniforms['DEFAULT_PARTICLE_COLOR'], *emitter.particle_template.color)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        if self.mesh_object.texture is not None:
            glBindTexture(GL_TEXTURE_2D, self.mesh_object.texture.id)
            glUniform1i( Uniforms['hasDiffuseTexture'], True)
        else:
            glUniform1i( Uniforms['hasDiffuseTexture'], False)
        
        if self.blending is not None:
            glBlendFunc(*self.blending)
        else:
            glDisable(GL_BLEND)
        
        self.render_state.bind()
        
    __enter__ = SetState

"""
class ParticleMeshRenderer(Renderer):
    flag='MESH_RENDERER'
    def __init__(self,  mesh_file,
                        texture_file=None,
                        size=1,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)):
        
        self.mesh_object = ParticleMesh(mesh_file)
        self.texture = None
        self.point_size =  size
        self.blending = blending
    
    def BuildRenderState(self, *buffer_objects):
        
        cVars.SingleMeshRenderShader.Set()
        
        for i,buffer_object in enumerate(buffer_objects):
            setattr(self, 'VAO{}'.format(i), VertexArrayObject() ) 
            with getattr(self, 'VAO{}'.format(i)):
                
                Attributes=cVars.SingleMeshRenderShader.Attributes
                
                VBO_STRIDE=24
                self.mesh_object.VBO_Vertex_Data.bind()
                
                glEnableVertexAttribArray( Attributes['Vertex_Position'] )
                #glEnableVertexAttribArray( Attributes['Vertex_TexCoords'] )
                
                glVertexAttribPointer( Attributes['Vertex_Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
                #glVertexAttribPointer( Attributes['Vertex_TexCoords'], 2, GL_FLOAT,False, 0, ctypes.c_void_p(0) )
                
                self.mesh_object.IBO_Vertex_Indices.bind()
                
        self.render_state = self.VAO0
        
        glUseProgram(0)
    
    def SetState(self):

        # render_shader
        cVars.SingleMeshRenderShader.Set()
        Uniforms = cVars.SingleMeshRenderShader.Uniforms
        
        emitter = self.parent_emitter
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        if self.mesh_object.texture is not None:
            glBindTexture(GL_TEXTURE_2D, self.mesh_object.texture.id)
            glUniform1i( Uniforms['hasDiffuseTexture'], True)
        else:
            glUniform1i( Uniforms['hasDiffuseTexture'], False)
        
        glBlendFunc(*self.blending)
        
        self.render_state.bind()
        
    __enter__ = SetState
"""
"""

def simple_render_mesh(self):
    VBO_STRIDE=32
    glUseProgram(self.render_mesh_shader.program)
    
    
    glUniformMatrix4fv(self.render_mesh_shader.Uniforms['ModelView'], 1, False, cVars.ModelViewProjectionMatrix)
    
    UpdateMeshRenderState(self, self.render_mesh_shader.Uniforms)
    Attributes = cVars.render_mesh_objects.Attributes
    MESH_OBJECT = self.particle_renderer.mesh_object
    
    glBindTexture(GL_TEXTURE_2D, MESH_OBJECT.texture.id)
    
    glEnableVertexAttribArray( Attributes['Vertex_Position'] )
    glEnableVertexAttribArray( Attributes['Vertex_TexCoords'] )
    glEnableVertexAttribArray( Attributes['Instance_Position'] )
    glEnableVertexAttribArray( Attributes['Instance_Age'] )
    
    MESH_OBJECT.Vertex_Position_VBO.bind()
    glVertexAttribPointer( Attributes['Vertex_Position'], 3, GL_FLOAT,False, 0, ctypes.c_void_p(0) )
    
    MESH_OBJECT.Vertex_TexCoords_VBO.bind()
    glVertexAttribPointer( Attributes['Vertex_TexCoords'], 2, GL_FLOAT,False, 0, ctypes.c_void_p(0) )

    self.VBO_Geometry.bind()
    glVertexAttribPointer( Attributes['Instance_Position'], 3, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(0) )
    glVertexAttribDivisorARB( Attributes['Instance_Position'], 1)

    glVertexAttribPointer( Attributes['Instance_Age'], 1, GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(28) )
    glVertexAttribDivisorARB( Attributes['Instance_Age'], 1)
    
    glDrawArraysInstancedARB( GL_TRIANGLES, 0 , MESH_OBJECT.Vertex_Count, self.VBO_Geometry.GetPrimitiveCount() ) 
    
    
    glVertexAttribDivisorARB( Attributes['Instance_Position'], 0)
    glVertexAttribDivisorARB( Attributes['Instance_Age'], 0)
    
    glDisableVertexAttribArray( Attributes['Vertex_Position'] )
    glDisableVertexAttribArray( Attributes['Vertex_TexCoords'] )
    glDisableVertexAttribArray( Attributes['Instance_Position'] )
    glDisableVertexAttribArray( Attributes['Instance_Age'] )
    
    glUseProgram(0)


"""
