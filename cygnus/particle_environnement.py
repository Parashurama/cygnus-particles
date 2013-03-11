#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from math_module import Vec3

class Environnement(object):
    def __init__(self):
        self.env_light={}
        
        self.env_light['ambient']  = (0.2, 0.1, 0.0, 1.0)
        self.env_light['diffuse']  = (0.8, 0.7, 0.6, 1.0)
        self.env_light['specular'] = (0.8, 0.7, 0.6, 1.0)
        self.env_light['direction']=  Vec3(12000,6000,0.0).normalized()
        
    def SetDirectionalLight(self, ambient=None, diffuse=None, specular=None, direction=None):
        if ambient is not None: self.env_light['ambient']  = ambient
        if diffuse is not None: self.env_light['diffuse']  = diffuse
        if specular is not None: self.env_light['specular'] = specular
        if direction is not None: self.env_light['direction']= Vec3(*direction).normalized()
    
    def SetupLightProperties(self, uniforms):
        glUniform4f(uniforms["light.ambient"], *self.env_light['ambient'])
        glUniform4f(uniforms["light.diffuse"], *self.env_light['diffuse'])
        glUniform4f(uniforms["light.specular"], *self.env_light['specular'])
        glUniform3f(uniforms["light.direction"], *self.env_light['direction'])
        
    def RenderLight(self):
        RenderCube(self.env_light['direction']*1500, 64)


def RenderCube((x,y,z), size, offset=(0,0,0)):
    (dx,dy,dz) = offset
    glPushMatrix()
    glTranslatef(x+dx,y+dy,z+dz)
    
    glDisable(GL_TEXTURE_2D)
    glColor4f(0.8,0.3,0.6,1.0)
    
    glBegin(GL_QUADS)
    
    # Front Face (note that the texture's corners have to match the quad's corners)
    glVertex3f(-size, -size,  size) # Bottom Left Of The Texture and Quad
    glVertex3f( size, -size,  size) # Bottom Right Of The Texture and Quad
    glVertex3f( size,  size,  size) # Top Right Of The Texture and Quad
    glVertex3f(-size,  size,  size) # Top Left Of The Texture and Quad
    
    # Back Face
    glVertex3f(-size, -size, -size) # Bottom Right Of The Texture and Quad
    glVertex3f(-size,  size, -size) # Top Right Of The Texture and Quad
    glVertex3f( size,  size, -size) # Top Left Of The Texture and Quad
    glVertex3f( size, -size, -size) # Bottom Left Of The Texture and Quad
    
    # Top Face
    glVertex3f(-size,  size, -size) # Top Left Of The Texture and Quad
    glVertex3f(-size,  size,  size) # Bottom Left Of The Texture and Quad
    glVertex3f( size,  size,  size) # Bottom Right Of The Texture and Quad
    glVertex3f( size,  size, -size) # Top Right Of The Texture and Quad
    
    # Bottom Face       
    glVertex3f(-size, -size, -size) # Top Right Of The Texture and Quad
    glVertex3f( size, -size, -size) # Top Left Of The Texture and Quad
    glVertex3f( size, -size,  size) # Bottom Left Of The Texture and Quad
    glVertex3f(-size, -size,  size) # Bottom Right Of The Texture and Quad
    
    # Right face
    glVertex3f( size, -size, -size) # Bottom Right Of The Texture and Quad
    glVertex3f( size,  size, -size) # Top Right Of The Texture and Quad
    glVertex3f( size,  size,  size) # Top Left Of The Texture and Quad
    glVertex3f( size, -size,  size) # Bottom Left Of The Texture and Quad
    
    # Left Face
    glVertex3f(-size, -size, -size) # Bottom Left Of The Texture and Quad
    glVertex3f(-size, -size,  size) # Bottom Right Of The Texture and Quad
    glVertex3f(-size,  size,  size) # Top Right Of The Texture and Quad
    glVertex3f(-size,  size, -size) # Top Left Of The Texture and Quad
    
    glEnd();
    glEnable(GL_TEXTURE_2D)
    glPopMatrix()
    
    glColor4f(1.0,1.0,1.0,1.0)
