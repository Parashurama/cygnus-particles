#! /usr/bin/env python
# *-* coding: UTF-8 *-*
import sys
sys.path.append('..')

import pyglet
import pyglet.window.key as key

from exemple_framework_pyglet import PygletWindow, Timer
from exemple_camera_class     import CameraObject

import cygnus
import OpenGL.GL as gl

from cygnus import Particle, Mesh, Template, Texture2D, AnimatedTexture
from cygnus.particle_domain     import Triangle, Square, Line, Disc, Sphere
from cygnus.particle_controller import LifeTime, Collector, Gravity, ColorBlender, Growth, Magnet, Bounce
from cygnus.particle_renderer   import PointRenderer, PointSpriteRenderer, AnimatedPointSpriteRenderer, ParticleMeshRenderer
from cygnus.particle_emitter    import Emitter, PerParticleEmitter
from cygnus.particle_mesh_emitter import MeshEmitter

if __name__ == '__main__':
    
    window = PygletWindow(1440,800, caption='TestParticles5', vsync=False, resizable=True)   
    cygnus.Init()
    
    CAMERA_0 = CameraObject(translation = (0.0, 0.0, -128.0),
                            rotation= (-28.0, -14.0, 0.0))
    cygnus.Set_Camera(CAMERA_0)
    
    GetTick = Timer()
    
    @window.event
    def on_draw(*args):
        window.clear()
        dt=GetTick(draw_fps=True)
        
        with CAMERA_0:
            cygnus.default_particle_system.render()
            cygnus.default_particle_system.update(dt)
        
    @window.event
    def on_resize(width, height):        
        CAMERA_0.SetProjection(45.0, float(width)/float(height),  10., 10000.0)
    
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == 1: # LEFT_CLICK
            cygnus.GetObjectfromName('Test1').Emit(10)
        
    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        if button == 4: # RIGHT_DRAG
            CAMERA_0.RotateCamera(a=dx, c=dy)
        
    @window.event
    def on_mouse_release(x, y, button, modifiers):
        pass
    
    @window.event
    def on_mouse_scroll(self, x, y, scroll_y):
        CAMERA_0.ZoomCamera(dz=-scroll_y*0.2)
        
    @window.event
    def on_key_press(symbol, modifiers):
        if modifiers & key.MOD_ALT: 
            if symbol == key.F4: raise SystemExit
            if symbol == key.ENTER: window.ToggleFullscreen()
    
    DOMAIN_CONTROLLERS=[ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                (1.0, (0.0, 0.0, 0.5, 0.7)), 
                                                                (3.0, (0.0, 0.5, 1.0, 1.0)), 
                                                                (5.0, (1.0, 1.0, 0.0, 1.0)), 
                                                                (10.7, (0.9, 0.2, 0.0, 1.0)), 
                                                                (15.0, (0.6, 0.1, 0.05, 0.8)), 
                                                                (19.0, (0.8, 0.8, 0.8, 0.5)),
                                                                (20.0, (0.8, 0.8, 0.8, 0.3)) ])
                                                
                                ]
    Emitter(name='Test1',
            position=(720.0, 450.0),
            fire_rate=0.1,
            particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0)),#, color = (1.0,0.4,1.0,0.7) ),
            particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                            velocity= (0.0, 0.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                            age = 1.0 ),
            controllers = [ LifeTime(10.0) ],#+DOMAIN_CONTROLLERS,
            
            
            #renderer = ParticleMeshRenderer('ressources/meshes/connor/Connor_Kenway.obj', blending=None, size=1)
            #renderer = ParticleMeshRenderer('ressources/meshes/dragon/dragon.obj', blending=None, size=1)
            #renderer = ParticleMeshRenderer('ressources/meshes/bunny_watertight_s.obj', blending=None)
            #renderer = ParticleMeshRenderer('ressources/meshes/bunny2', blending=None)
            renderer = ParticleMeshRenderer('ressources/meshes/raptor/raptor.obj', blending=None)
            #renderer = ParticleMeshRenderer('ressources/meshes/darkelf_f_armor/DarkElf11.obj', blending=None, size=3)
            )
    
    
    pyglet.app.run()
