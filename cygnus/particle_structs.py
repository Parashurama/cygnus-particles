#! /usr/bin/env python
# *-* coding: UTF-8 *-*

class Particle(object):
    def __init__(self, position, velocity, color=(1.0,1.0,1.0,1.0), mass=1.0):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.age = 0.0
        self.mass = mass
        self.point_size = None
        
    def set_parent_emitter(self, parent):
        pass

class Template(dict):
    def __init__(self, *args, **kwargs ):        
        self['position']=(0.0,0.0,0.0)
        self['velocity']=(0.0,0.0,0.0)
        self['age']=0.0
        self['mass']=0.0
        
        dict.__init__(self, *args, **kwargs )

from OpenGL.GL import GL_ELEMENT_ARRAY_BUFFER,\
                      GL_ARRAY_BUFFER,\
                      GL_STATIC_DRAW

from glLibs.glObjects import BufferObject#, VertexArrayObject
from mesh_loader import LoadMesh
from utils import ParseBufferData_format
from glLibs.gl_object_structs import MaterialManager
import numpy as np

class Mesh(object):
    @classmethod
    def fromMeshFile(cls, filename):
        mesh = cls.__new__(cls)
        faces_material, material_reference, vertex_data, data_format = LoadMesh(filename)
        
        mesh.data_format = ParseBufferData_format(data_format)
        
        if not 'position' in mesh.data_format['struct_info']:
            raise AssertionError('invalid buffer data format')
        
        if not 'texcoord' in mesh.data_format['struct_info']:
            mesh.hasTexturing = False
        else:
            mesh.hasTexturing = True
        
        if not 'normal' in mesh.data_format['struct_info']:
            mesh.hasLighting = False
        else:
            mesh.hasLighting = True
        
        mesh.mesh_materials = MaterialManager(faces_material, material_reference)
        
        mesh.vertex_count = len(vertex_data)
        mesh.VBO_Vertex_Data = BufferObject(GL_ARRAY_BUFFER, np.asarray(vertex_data, dtype='float32'), GL_STATIC_DRAW)
        
        return mesh
    """
        #self.indice_count = len(INDICES)
        #INDICES = np.asarray(indices, dtype='uint16').ravel()
        
        #self.IBO_Vertex_Indices = BufferObject(GL_ELEMENT_ARRAY_BUFFER, INDICES, GL_STATIC_DRAW)
    
    def create_from_buffer(self, indices_buffer,vertexes_buffer, vertex_count, indice_count, data_format):
        self.IBO_Vertex_Indices = indices_buffer
        self.VBO_Vertex_Data = vertexes_buffer
        self.vertex_count = vertex_count
    
    
        return cls.fromData()
    
    @classmethod
    def fromData(cls, indices, vertexes, data_format):
        mesh = cls.__new__(cls)
        mesh.create(indices, vertexes, data_format)
        
        return mesh
        
    @classmethod
    def fromBuffers(cls, indices_buffer, vertexes_buffer, vertex_count, indice_count, data_format):
        mesh = cls.__new__(cls)
        mesh.create_from_buffer(indices_buffer,vertexes_buffer, vertex_count, indice_count, data_format)
        return mesh
    """
"""
class Mesh(object):
    
    def create(self, indices, vertexes, data_format):
        
        self.data_format = ParseBufferData_format(data_format)
        assert 'position' in self.data_format['struct_info'], 'invalid buffer data format'
        
        INDICES = np.asarray(indices, dtype='uint16').ravel()
        VERTEXES = np.asarray(vertexes, dtype='float32')
        self.vertex_count = len(vertexes)
        self.indice_count = len(INDICES)
        
        self.IBO_Vertex_Indices = BufferObject(GL_ELEMENT_ARRAY_BUFFER, INDICES, GL_STATIC_DRAW)
        self.VBO_Vertex_Data = BufferObject(GL_ARRAY_BUFFER, VERTEXES, GL_STATIC_DRAW)
    
    def create_from_buffer(self, indices_buffer,vertexes_buffer, vertex_count, indice_count, data_format):
        self.IBO_Vertex_Indices = indices_buffer
        self.VBO_Vertex_Data = vertexes_buffer
        self.vertex_count = vertex_count
        
    @classmethod
    def fromMeshFile(cls, filename):
        return cls.fromData(*LoadMesh(filename))
    
    @classmethod
    def fromData(cls, indices, vertexes, data_format):
        mesh = cls.__new__(cls)
        mesh.create(indices, vertexes, data_format)
        
        return mesh
        
    @classmethod
    def fromBuffers(cls, indices_buffer, vertexes_buffer, vertex_count, indice_count, data_format):
        mesh = cls.__new__(cls)
        mesh.create_from_buffer(indices_buffer,vertexes_buffer, vertex_count, indice_count, data_format)
        return mesh
"""
