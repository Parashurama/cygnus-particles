#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from OpenGL.GL.ARB.instanced_arrays import glVertexAttribDivisorARB

from __globals__ import cVars

from particle_structs  import Mesh
from glLibs.gl_object_structs import glMaterial
from glLibs.glObjects  import BufferObject, VertexArrayObject
from mesh_loader       import LoadMaterialsFile

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
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
                        distance_attenuation=False):
        self.feather_radius = feather
        self.point_size = point_size
        self.blending = blending
        self.distance_attenuation = distance_attenuation
        
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
        
        if self.distance_attenuation:
            glUniform1i(Uniforms['hasDistanceAttenuation'], True)
        else:
            glUniform1i(Uniforms['hasDistanceAttenuation'], False)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        if self.blending is None:
            glDisable(GL_BLEND)
        else:
            glDisable(GL_DEPTH_TEST)
            glBlendFunc(*self.blending)
        
        self.render_state.bind()
        
    __enter__ = SetState

class PointSpriteRenderer(PointRenderer):
    flag='POINT_SPRITE_RENDERER'
    def __init__(self,  texture,
                        point_size=None,
                        feather = 0.0,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
                        distance_attenuation=False):
        self.texture = texture
        self.feather_radius = feather
        self.point_size =  point_size or max( texture.width, texture.height )
        self.blending = blending
        self.distance_attenuation = distance_attenuation
        
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
        
        if self.distance_attenuation:
            glUniform1i(Uniforms['hasDistanceAttenuation'], True)
        else:
            glUniform1i(Uniforms['hasDistanceAttenuation'], False)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        if self.blending is None:
            glDisable(GL_BLEND)
        else:
            glDisable(GL_DEPTH_TEST)
            glBlendFunc(*self.blending)
        
        
        self.render_state.bind()
        
    __enter__ = SetState
    
class AnimatedPointSpriteRenderer(PointRenderer):
    flag='ANIMATED_POINT_SPRITE_RENDERER'
    def __init__(self,  texture,
                        point_size=None,
                        feather = 0.0,
                        blending =(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
                        distance_attenuation=False):
                            
        self.texture = texture
        self.feather_radius = feather
        self.point_size =  point_size or max( texture.width, texture.height )
        self.blending = blending
        self.distance_attenuation = distance_attenuation
        
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
        
        if self.distance_attenuation:
            glUniform1i(Uniforms['hasDistanceAttenuation'], True)
        else:
            glUniform1i(Uniforms['hasDistanceAttenuation'], False)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        
        if self.blending is None:
            glDisable(GL_BLEND)
        else:
            glDisable(GL_DEPTH_TEST)
            glBlendFunc(*self.blending)
        
        
        self.render_state.bind()
        
    __enter__ = SetState


MESH_ATTRIBUTES_LIST_NO_TEXTURE_NO_LIGHTING = {'position':'Vertex_Position'}
MESH_ATTRIBUTES_LIST_NO_TEXTURE_LIGHTING = {'position':'Vertex_Position', 'normal':'Vertex_Normals'}

MESH_ATTRIBUTES_LIST_TEXTURED_NO_LIGHTING = {'position':'Vertex_Position', 'texcoord':'Vertex_TexCoords'}
MESH_ATTRIBUTES_LIST_TEXTURED_LIGHTING = {'position':'Vertex_Position', 'texcoord':'Vertex_TexCoords', 'normal':'Vertex_Normals'}

class ParticleMeshRenderer(Renderer):
    flag='MESH_RENDERER'
    def __init__(self,  mesh_file,
                        size=1,
                        blending=None):
        
        self.mesh_object = Mesh.fromMeshFile(mesh_file)
        self.mesh_hasTexturing = (self.mesh_object.hasTexturing and self.mesh_object.mesh_materials.use_texturing)
        self.mesh_hasLighting  = (self.mesh_object.hasLighting and self.mesh_object.mesh_materials.use_lighting)
        
        if self.mesh_hasLighting:
            self.set_state_function = self.SetState_withMaterial
            self.render_shader = cVars.MeshRenderShaderLighting
        else:
            self.set_state_function = self.SetState_noMaterial
            self.render_shader = cVars.MeshRenderShader
        
        self.point_size =  size
        self.blending = blending
        
    def BuildRenderState(self, *buffer_objects):
        
        if self.mesh_hasTexturing:
            if self.mesh_hasLighting:
                Mesh_AttributesList = MESH_ATTRIBUTES_LIST_TEXTURED_LIGHTING
            else:
                Mesh_AttributesList = MESH_ATTRIBUTES_LIST_TEXTURED_NO_LIGHTING
        else:
            if self.mesh_hasLighting:
                Mesh_AttributesList = MESH_ATTRIBUTES_LIST_NO_TEXTURE_LIGHTING
            else:
                Mesh_AttributesList = MESH_ATTRIBUTES_LIST_NO_TEXTURE_NO_LIGHTING
        
        MESH_OBJ_DATA_FORMAT = self.mesh_object.data_format
        
        for i,buffer_object in enumerate(buffer_objects):
            setattr(self, 'VAO{}'.format(i), VertexArrayObject() ) 
            with getattr(self, 'VAO{}'.format(i)):
                
                Attributes=self.render_shader.Attributes
                
                VBO_STRIDE=MESH_OBJ_DATA_FORMAT['struct_byte_size']
                
                self.mesh_object.VBO_Vertex_Data.bind()
                
                for attribute, shader_attribute_name in Mesh_AttributesList.iteritems():
                    glEnableVertexAttribArray( Attributes[shader_attribute_name] )                    
                    glVertexAttribPointer( Attributes[shader_attribute_name], MESH_OBJ_DATA_FORMAT['struct_{}_size'.format(attribute)], GL_FLOAT,False, VBO_STRIDE, ctypes.c_void_p(MESH_OBJ_DATA_FORMAT['struct_{}_byte_offset'.format(attribute)]) )
                
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
    
    def SetState_noMaterial(self):

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
        
        if self.blending is not None:
            glBlendFunc(*self.blending)
            glDisable(GL_CULL_FACE)
        else:
            glDisable(GL_BLEND)
            glEnable(GL_CULL_FACE)
        
        self.render_state.bind()
    
    def SetState_withMaterial(self):
        
        # render_shader
        cVars.MeshRenderShaderLighting.Set()
        Uniforms = cVars.MeshRenderShaderLighting.Uniforms
        
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
        
        glUniform1f( Uniforms['PARTICLE_SIZE'], self.point_size)#(emitter.particle_template.point_size or self.point_size)/2)
        glUniform4f( Uniforms['DEFAULT_PARTICLE_COLOR'], *emitter.particle_template.color)
        
        glUniformMatrix4fv(Uniforms['ModelViewProjection'], 1, False, cVars.Current_Camera.projection_view_matrix)
        glUniformMatrix4fv(Uniforms['ModelView'], 1, False, cVars.Current_Camera.view_matrix)
        glUniformMatrix3fv(Uniforms['NormalMatrix'], 1, False, cVars.Current_Camera.normal_matrix)
        
        emitter.particle_system.default_env.SetupLightProperties(Uniforms)
        
        if self.blending is not None:
            glBlendFunc(*self.blending)
            glDisable(GL_CULL_FACE)
        else:
            glDisable(GL_BLEND)
            glEnable(GL_CULL_FACE)
        
        self.render_state.bind()
        
        
    def SetState(self):
        self.set_state_function()
        
    __enter__ = SetState
    
    def UnsetState(self, *args):
        if self.blending is None:
            glEnable(GL_BLEND)
            glDisable(GL_CULL_FACE)
            
        glUseProgram(0)        
        glBindVertexArray(0)
        self.SwitchState()
        
    __exit__ = UnsetState

