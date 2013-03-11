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
        faces_data, faces_materials, material_reference, vertex_data, data_format = LoadMesh(filename)
        
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
        
        mesh.mesh_materials = MaterialManager(faces_materials, material_reference)
        
        mesh.vertex_count = len(vertex_data)
        mesh.indice_count = len(faces_data)
        
        mesh.IBO_Vertex_Indices = BufferObject(GL_ELEMENT_ARRAY_BUFFER, faces_data, GL_STATIC_DRAW)
        mesh.VBO_Vertex_Data = BufferObject(GL_ARRAY_BUFFER, vertex_data, GL_STATIC_DRAW)
        
        return mesh
