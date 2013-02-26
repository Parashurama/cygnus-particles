import pyglet

import OpenGL.GL as gl
import time


def HackFunction(window):# Update as often as possible (limited by vsync, if not disabled)
    window.register_event_type('on_update')
    def update(dt):
        window.dispatch_event('on_update', dt)        
    pyglet.clock.schedule(update)

def SetupOpenGLContext():

    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)  ;#gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)    
    
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glClearDepth(1.0)
    
    gl.glDisable(gl.GL_SCISSOR_TEST) ; gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_STENCIL_TEST) ; gl.glDisable(gl.GL_DITHER)    

    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_FASTEST)
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT,gl.GL_FASTEST)
    gl.glHint(gl.GL_GENERATE_MIPMAP_HINT,gl.GL_FASTEST)
    gl.glShadeModel(gl.GL_SMOOTH)    
    
    gl.glDisable(gl.GL_FOG)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_BLEND)
    #gl.glEnable( gl.GL_POINT_SMOOTH )

    gl.glPolygonMode( gl.GL_FRONT, gl.GL_FILL )

class PygletWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        
        self.set_exclusive_keyboard( exclusive=False)
        self.set_exclusive_mouse( exclusive=False)
        
        HackFunction(self)
        SetupOpenGLContext()
    
    def ToggleFullscreen(self):
        self.set_fullscreen(not self.fullscreen)




class Timer(object):
    def __init__(self):
        self.last_time=time.time()
        self.n_cycles = 0
        self.cumuled_time = 0
        self.delay=1.
        
    def Reset(self):
        self.last_time=time.time()
    
    def __call__(self, draw_fps=False):
        curent_time=time.time()
        
        dt = curent_time-self.last_time
        self.last_time= curent_time
        
        self.cumuled_time+=dt
        self.n_cycles+=1
        
        if draw_fps and self.cumuled_time>self.delay:
            frame =  self.cumuled_time/self.n_cycles
            self.cumuled_time = 0.
            self.n_cycles=0.
            
            print "Average time per frames {:.5f}, FPS: {:.2f}".format(frame, 1/frame)
            
            
        return dt


    
