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

from cygnus import Particle, Template, Texture2D, AnimatedTexture
from cygnus.particle_domain     import Triangle, Square, Line, Disc, Sphere
from cygnus.particle_controller import LifeTime, Collector, Gravity, ColorBlender, Growth, Magnet, Bounce
from cygnus.particle_renderer   import PointRenderer, PointSpriteRenderer, AnimatedPointSpriteRenderer#, MeshRenderer
from cygnus.particle_emitter    import Emitter, PerParticleEmitter

if __name__ == '__main__':
    
    window = PygletWindow(1440,800, caption='TestParticles7 AnimatedSpriteEmitter', vsync=False)   
    cygnus.Init()
    
    CAMERA_0 = CameraObject(translation = (0.0, 0.0, -1472.0),
                            rotation    = (-119.0, -105.0, -30.0))
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
            cygnus.GetObjectfromName('Test1').Emit(150)
        
    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):
        if button == 4: # RIGHT_DRAG
            CAMERA_0.RotateCamera(a=dx, c=dy)
        
    @window.event
    def on_mouse_release(x, y, button, modifiers):
        pass
    
    @window.event
    def on_mouse_scroll(self, x, y, scroll_y):
        CAMERA_0.ZoomCamera(dz=-scroll_y)
        
    @window.event
    def on_key_press(symbol, modifiers):
        if modifiers & key.MOD_ALT: 
            if symbol == key.F4: raise SystemExit
            if symbol == key.ENTER: window.ToggleFullscreen()
    
    DOMAIN_CONTROLLERS=[ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                        (1.0, (0.0, 0.0, 0.5, 0.7)), 
                                        (3.0, (0.0, 0.5, 1.0, 1.0)), 
                                        (5.0, (1.0, 1.0, 0.0, 1.0)),
                                        (8.0, (0.0, 0.5, 0.0, 0.7)),
                                        (10.0,(0.5, 0.0, 0.5, 0.0))]) ]
    Emitter(name='Test1',
            position=Triangle((650.0, 100.0, 0.0), (250.0, 100.0, 0.0), (150.0, 400.0, 0.0)),
            fire_rate=200,
            particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0) ),#, color = (1.0,0.4,1.0,0.7)
            particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                            velocity= (250.0, 250.0, 250.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                            age = 0.0 ),
            controllers = DOMAIN_CONTROLLERS+[ LifeTime(10.0), Growth(10.0) ],
            
            renderer = AnimatedPointSpriteRenderer( AnimatedTexture('ressources/textures/Dark_1.png', 5, 5), point_size=64.0, feather = 0.0,
                                                    blending=(gl.GL_SRC_ALPHA, gl.GL_ONE),
                                                    distance_attenuation=True),
            
            )
    
    
    pyglet.app.run()

