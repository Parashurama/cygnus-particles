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
    
    #DOMAIN_CONTROLLERS=[]
    Emitter(name='Test1',
            position=Sphere((720.0, 450.0, 0.0), 0, 75),#(720.0, 450.0),
            #position=Square(450.0, 450.0, 650.0, 650.0, 0.0),
            #position=(650.0, 100.0, 0.0),
            fire_rate=200000,
            particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0), color = (1.0,0.4,1.0,0.7) ),
            particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                            velocity= (5.0, 5.0, 5.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                            age = 1.0 ),
            controllers = [ LifeTime(1.0) ],
            
            #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/Images/_Dark_1.png', 5, 5),
            #                                        point_size=64.1,
            #                                        feather = 0.0,
            #                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE) )
            #renderer = PointSpriteRenderer( Texture('Media/Images/bubble.png'), point_size=32.0, feather = 0.0,
            #                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
            renderer = PointRenderer( point_size=4.0, feather = 2.0,
                                   blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
            
            #renderer = MeshRenderer( ParticleMesh('Media/Models/book_open', 'Media/Models/book.png') )
            )
    
    
    pyglet.app.run()
