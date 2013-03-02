
from OpenGL.GL import *
from math_module import Vec3

class Environnement(object):
    def __init__(self):
        self.env_light={}
        
        self.env_light['ambient']  = (0.2, 0.1, 0.0, 1.0)
        self.env_light['diffuse']  = (1.0, 1.0, 1.0, 1.0)
        self.env_light['specular'] = (1.0, 1.0, 1.0, 1.0)
        self.env_light['direction']=  Vec3(0.0, 1.0, 0.0).normalized()
        
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
