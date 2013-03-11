#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from __globals__ import cVars

from particle_system import ParticleSystem
from glLibs.media_manager import ImagesManager

default_particle_system = ParticleSystem()
cVars.default_image_manager = ImagesManager()

def InitializeSystem():
    import particle_shaders
    from utils import RandomTexture
    
    cVars.RandomLookup = RandomTexture(8092)    
    particle_shaders.BuildShaders()
    cVars.isCygnusInitialized = True

def Set_Camera(camera_object):
    cVars.Current_Camera = camera_object


def GenId(obj):
    cVars.id+=1    
    cVars.__objects_by_Id__[cVars.id]=obj
        
    return cVars.id

def ReferenceName(obj,Name):
    print Name
    
    assert isinstance(Name, basestring), "Invalid name type. '{}' of type {}: (must be string)".format(Name, type(Name) )
    
    if not Name in cVars.__objects_by_Name__:
        cVars.__objects_by_Name__[Name]=obj
        
    else: raise NameError("Nom de Reference '%s' deja utilise" %(Name))

    
def GetObjectfromId(id):
    obj=cVars.__objects_by_Id__.get(id, None)
    
    assert (obj is not None), "No Object for id '{0}'".format(id)    
    return obj
    
def GetObjectfromName(Name):
    obj=cVars.__objects_by_Name__.get(Name, None)
    
    assert (obj is not None), "No Object named '{0}'".format(Name)    
    return obj
