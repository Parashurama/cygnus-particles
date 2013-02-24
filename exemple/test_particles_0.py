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
    
    window = PygletWindow(1440,800, caption='TestParticles0', vsync=False)   
    cygnus.Init()
    
    CAMERA_0 = CameraObject(translation = (0.0,0.0,0.0),
                            rotation= (0.0,0.0,0.0))
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
    
    
    trail = PerParticleEmitter( name='Trail0',
                                fire_rate=500,
                                velocity = (0.0,0.0,0.0),
                                color = (0.0,0.8,1.0,0.7),
                                particle_template=Particle( position = (0.0, 0.0, 0.0),
                                                            velocity = (0.0, 0.0, 0.0),
                                                            #color = (1.0,0.4,1.0,0.7)
                                                          ),
                                particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                                velocity= (5.0,5.0, 5.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                                age = 0.5 ),
                                controllers = [ LifeTime(20.0),
                                                #Growth(1.0),
                                                ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                (1.0, (0.0, 0.0, 0.5, 0.7)), 
                                                                (3.0, (0.0, 0.5, 1.0, 1.0)), 
                                                                (5.0, (1.0, 1.0, 0.0, 1.0)), 
                                                                (10.7, (0.9, 0.2, 0.0, 1.0)), 
                                                                (15.0, (0.6, 0.1, 0.05, 0.8)), 
                                                                (19.0, (0.8, 0.8, 0.8, 0.5)),
                                                                (20.0, (0.8, 0.8, 0.8, 0.3)) ])
                                                ],
                                renderer = PointRenderer( point_size=8.0, feather = 8.0,
                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                                )
    
    DOMAIN_CONTROLLERS = [Gravity(0.0, 95.81, 0.0),
                                    Magnet( origin=(750, 550, 0),
                                            charge=0.05,
                                            cutoff=250,
                                            name='MoveMagnet',
                                            epsilon=1.0),
                                    Bounce(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0), friction=0.7 ),
                                    Magnet( origin=(220, 450, 0),
                                            charge=0.01,
                                            cutoff=150,
                                            epsilon=1.0),
                                    Magnet( origin=(720, 250, 0),
                                            charge=0.01,
                                            cutoff=150,
                                            epsilon=1.0)]
    
    Emitter(name='Test1',
            #position=Disc((720, 150, 0.0), 45, 75),#(720.0, 450.0),
            position=(650.0, 100.0, 0.0),
            fire_rate=5,
            particle_template=trail,
            
            particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                            velocity= (150.0, 150.0, 150.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                            age = 1.0 ),
            controllers = DOMAIN_CONTROLLERS+[ LifeTime(15.0) ],
            
            #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/Images/_Dark_1.png', 5, 5),
            #                                        point_size=64.1,
            #                                        feather = 0.0,
            #                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE) )
            #renderer = PointSpriteRenderer( Texture('Media/Images/bubble.png'), point_size=32.0, feather = 0.0,
            #                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
            renderer = PointRenderer( point_size=16.0, feather = 2.0,
                                   blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
            
            #renderer = MeshRenderer( ParticleMesh('Media/Models/book_open', 'Media/Models/book.png') )
            )
    
    
    pyglet.app.run()
