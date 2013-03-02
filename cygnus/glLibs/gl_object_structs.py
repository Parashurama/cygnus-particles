#! /usr/bin/env python
# *-* coding: UTF-8 *-*
from OpenGL.GL import *
from ..__globals__ import cVars
from glObjects import BufferObject
from textures import GLTexture2D
# illumination_mode:
# 0 : no_lighting
# 1 : lambert_shading
# 2 : phong_shading

class glMaterial(object):
    def __init__(self, data={}):
        assert hasattr(data, 'get'), '{}\n{}'.format(type(data),data)
        self.name = data.get('name')
        
        self.shininess = float(data.get('shininess', 0.0))
        self.diffuse = tuple(data.get('diffuse', (1.0, 1.0, 1.0, 1.0)))
        self.ambient = tuple(data.get('ambient', (1.0, 1.0, 1.0, 1.0)))
        self.specular = tuple(data.get('specular', (1.0, 1.0, 1.0, 1.0)))
        self.diffuse_texture = data.get('diffuse_texture', None)
        self.specular_texture = data.get('specular_texture', None)
        self.bump_texture = data.get('bump_texture', None)
        self.bump_multiplier = float(data.get('bump_multiplier', 1.0))
        self.illumination_mode = int(data.get('illumination_mode', 0))
        self.backface_culling = int(data.get('cull_face', 1))
        self.isTextured = False
        
        if self.diffuse_texture is not None:
            self.diffuse_texture = cVars.default_image_manager.GetTexture( self.diffuse_texture, GLTexture2D,repeat_texture=True)
            self.isTextured = True
        
        if self.illumination_mode:
            if self.bump_texture is not None:
                self.bump_texture = cVars.default_image_manager.GetTexture( self.bump_texture, GLTexture2D, anisotropic=True, repeat_texture=True)
                self.isTextured = True
            self.setup_material = self.setup_lighting
        else:
            self.bump_texture = None
            self.setup_material = self.setup_no_lighting
    
    def setup_no_lighting(self, Uniforms):
        if self.isTextured is True:
            if self.diffuse_texture is not None:
                glUniform1i(Uniforms["hasDiffuseTexture"], 1)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture( GL_TEXTURE_2D, self.diffuse_texture.id)
            else:
                glUniform1i(Uniforms["hasDiffuseTexture"], 0)
    
    def setup_lighting(self, Uniforms):
        
        if self.isTextured is True:
            if self.diffuse_texture is not None:
                glUniform1i(Uniforms["hasDiffuseTexture"], 1)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture( GL_TEXTURE_2D, self.diffuse_texture.id)
            else:
                glUniform1i(Uniforms["hasDiffuseTexture"], 0)
            
            if self.bump_texture is not None:
                glUniform1i(Uniforms["hasNormalTexture"], 1)
                glUniform1f(Uniforms["NormalMultiplier"], self.bump_multiplier)
                glActiveTexture(GL_TEXTURE1)
                glBindTexture( GL_TEXTURE_2D, self.bump_texture.id)
                glActiveTexture(GL_TEXTURE0)
            else:
                glUniform1i(Uniforms["hasNormalTexture"], 0)
        
        glUniform4f(Uniforms["material.ambient"], *self.ambient)
        glUniform4f(Uniforms["material.diffuse"], *self.diffuse)
        glUniform4f(Uniforms["material.specular"], *self.specular)
        glUniform1f(Uniforms["material.shininess"], self.shininess)

class glMaterialSubMesh(glMaterial):
    def __init__(self, data, indices):
        glMaterial.__init__(self, data)
        
        assert indices.dtype == 'uint16' and indices.ndim == 1 and indices.shape[0]%3==0
        self.primitive_type = GL_TRIANGLES
        
        self.indices_count = indices.shape[0]
        self.indices_type = GL_UNSIGNED_SHORT
        self.indices_offset = 0
        
        self.IBO_Vertex_Indices = BufferObject(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW )
        
    def setup(self, Uniforms):
        self.setup_material(Uniforms)
        self.IBO_Vertex_Indices.bind()

# Pseudo Iterator Object
class MaterialManager(object):
    def __init__(self, faces_materials, material_definitions):
        self.materials = [ glMaterialSubMesh(material_definitions[material_name], material_faces) for material_name, material_faces in faces_materials.iteritems() ]
        
        self.use_texturing = any([ material.isTextured for material in self.materials])
        self.use_lighting = any([ material.illumination_mode for material in self.materials])
        
        
    def __iter__(self):
        """
        Iterating through the mesh materials and return the corresponding submesh
        """
        return iter(self.materials)
        
    
