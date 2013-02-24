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

"""
import cPickle
from root import cVars
import numpy as np

from glLibs.glObjects import BufferObject, VertexArrayObject
from glLibs.textures import GLTexture as Texture

from OpenGL.GL import *
from OpenGL.GL.ARB.instanced_arrays import glVertexAttribDivisorARB
from OpenGL.GL.ARB.draw_instanced import glInitDrawInstancedARB,glDrawArraysInstancedARB,glDrawElementsInstancedARB

class ParticleMesh(object):
    def __init__(self,  mesh_file=None,
                        texture=None):
        
        _3dfile = open(mesh_file+".3d", "rb")
            
        vertex=cPickle.load(_3dfile).astype('float32')
        texcoords=cPickle.load(_3dfile)
        
        if    isinstance(texture, str): self.texture = Texture(texture)
        elif  isinstance(texture, Texture): self.texture = texture
        else: raise ValueError("Invalid Texture Type {},{}".format(type(texture), texture))
        
        self.Vertex_Position_VBO = BufferObject(GL_ARRAY_BUFFER, vertex, GL_STATIC_DRAW)
        self.Vertex_TexCoords_VBO = BufferObject(GL_ARRAY_BUFFER, texcoords, GL_STATIC_DRAW)
        self.Vertex_Count = vertex.shape[0]
        self.shader = cVars.render_mesh_objects

        #self.CreateVAO()
        #print self.BoundingBox(vertex)
        '''
    def BoundingBox(self, vertex):
        ul = np.maximum.reduce([ np.maximum.reduce(vertex)])
        ll = np.minimum.reduce([ np.minimum.reduce(vertex)])
            
        return ul,ll
        
    def CreateVAO(self):
        
        self.Mesh_VAO=VertexArrayObject()
        self.Mesh_VAO.bind()
        
        Attributes = cVars.render_mesh_objects.Attributes
        
        glEnableVertexAttribArray( Attributes['Vertex_Position'] )
        glEnableVertexAttribArray( Attributes['Vertex_TexCoords'] )
        glEnableVertexAttribArray( Attributes['Instance_Position'] )
        
        self.Vertex_Position_VBO.bind()
        glVertexAttribPointer( Attributes['Vertex_Position'], 3, GL_FLOAT,False, 0, ctypes.c_void_p(0) )
        
        self.Vertex_TexCoords_VBO.bind()
        glVertexAttribPointer( Attributes['Vertex_TexCoords'], 2, GL_FLOAT,False, 0, ctypes.c_void_p(0) )

        self.Instance_Position_VBO.bind()
        glVertexAttribPointer( Attributes['Instance_Position'], 3, GL_FLOAT,False, 0, ctypes.c_void_p(0) )
        glVertexAttribDivisorARB( Attributes['Instance_Position'], 1)
        
        self.Mesh_VAO.unbind()
        
    def draw(self):
        
        glUseProgram(self.shader.program)
        
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glUniformMatrix4fv(self.shader.Uniforms['ModelView'], 1, False, cVars.ModelViewProjectionMatrix)
        
        self.Mesh_VAO.bind()
        
        glDrawArraysInstancedARB( GL_TRIANGLES, 0 , self.Vertex_Count, self.InstanceCount ) 
        
        self.Mesh_VAO.unbind()
        glUseProgram(0)
        '''
"""
