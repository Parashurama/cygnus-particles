#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from OpenGL.GL.NV.transform_feedback import GL_RASTERIZER_DISCARD_NV

from particle_environnement import Environnement
class ParticleSystem(object):
    
    def __init__(self, global_controllers=()):
        self.global_controllers = tuple(global_controllers)
        self.groups = []
        self.default_env = Environnement()
    
    def add_global_controller(self, *controllers):
        """Add a global controller applied to all groups on update"""
        self.global_controllers += controllers
    
    def add_group(self, group):
        """Add a particle group to the system"""
        self.groups.append(group)
    
    def update(self, dt):
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, cVars.RandomLookup.id)
        glEnable(GL_RASTERIZER_DISCARD_NV)
        
        for group in  self.groups:
            group.update(dt)
        
        glDisable(GL_RASTERIZER_DISCARD)
        
    def render(self):
        #self.default_env.RenderLight()
        
        glActiveTexture(GL_TEXTURE0)            
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        
        glEnable(GL_POINT_SPRITE);   
        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE)
        
        for group in  self.groups:
            group.render()

        glTexEnvi(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_FALSE)
        glDisable(GL_POINT_SPRITE);   
        
        glDisable(GL_VERTEX_PROGRAM_POINT_SIZE)



from root import cVars
