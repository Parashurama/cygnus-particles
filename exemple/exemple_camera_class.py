
from OpenGL.GL import *
import numpy as np

from cygnus.math_module import Vec3, cross3
from math import cos, sin, tan, pi

PI_OVER_180 =pi/180.

def Mat4_RotationMatrix(phi, theta, psi):
    
    # NEGATE ALL ANGLE to MATCH OPENGL ROTATIONS & convert to RADIANS
    phi   *= -PI_OVER_180 ; theta *= -PI_OVER_180 ; psi   *= -PI_OVER_180;
    
    sx = sin(phi) ; cx = cos(phi)
    sy = sin(theta) ; cy = cos(theta)
    sz = sin(psi) ; cz = cos(psi)
    
    return np.array([(cz*cy, -sz*cx + cz*sy*sx, -sz*-sx + cz*sy*cx, 0.0),
                     (sz*cy,  cz*cx + sz*sy*sx,  cz*-sx + sz*sy*cx, 0.0),
                     (-sy,               cy*sx,              cy*cx, 0.0),
                     (0.0,                 0.0,                0.0, 1.0)], dtype='float32')

def Mat4_TranslationMatrix(dx, dy, dz):
    return np.array([(1.0, 0.0, 0.0, 0.0),
                     (0.0, 1.0, 0.0, 0.0),
                     (0.0, 0.0, 1.0, 0.0),
                     (dx,   dy,  dz, 1.0)], dtype='float32')

def Mat4_PerspectiveMatrix(fovy, aspect, zNear, zFar):
    deltaZ = float(zFar - zNear);
    
    if ((deltaZ == 0) or (aspect == 0)):
        raise ValueError();
                                     # Convert to RADIANS
    cotangent = 1.0 / tan((fovy *0.5)*PI_OVER_180);
    
    return np.array([(cotangent/aspect,       0.0,                      0.0,  0.0),
                     (             0.0, cotangent,                      0.0,  0.0),
                     (             0.0,       0.0, -(zFar + zNear) / deltaZ, -1.0),
                     (0.0,         0.0, -(2.0 * zFar * zNear) / deltaZ, 0.0)], dtype='float32')

def Mat4_to_Mat3(matrix):
    return np.ascontiguousarray(matrix[:3,:3])

class CameraObject(object):
    def __init__(self, translation=(0,0,0), rotation=(0,0,0)):
        self.camera_translation = Vec3(*translation)
        self.camera_rotation = Vec3(*rotation)
        self.DefaultViewVector=Vec3( 0.0, 0.0, -1.0 )
        self.ViewVector = self.DefaultViewVector.copy()
        self._has_moved = False
        self.RotateCamera() # Update ViewVector
        #self.CalculateFrustum() # Update FrustumCenter
        
    def __enter__(self): # Use with Python "with statement"
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadMatrixf(self.projection_matrix)
        
        if self._to_update is True:
            self.UpdateFrustum()
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadMatrixf(self.view_matrix)
        
        
    def __exit__(self, *args): # Use with Python "with statement"
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    
    def SetProjection(self, fov, aspect_ratio, near, far):
        self.projection_matrix= Mat4_PerspectiveMatrix(fov, aspect_ratio, near, far)
        
    def MoveCamera(self,dx=0,dy=0):    
        
        if   dy:
            self.camera_translation+=self.ViewVector*dy*64
            
        elif dx:
            crossViewVector = cross3(self.ViewVector, Vec3(0.0,1.0,0.0))
            self.camera_translation+=crossViewVector*dx*64
        
        self._to_update = True
        
    def ZoomCamera(self,dz=None):
        if   dz:
            self.camera_translation.z+=dz*64
        
        self._to_update = True
    
    #def CalculateFrustum(self):
    #    near = 50. # near plane 
    #    far = 50000.0 # far plane 
    #    
    #    camera_position = -self.camera_translation
    #    self.FrustumCenter = camera_position+self.ViewVector*((far-near)*0.5)
    
    def UpdateFrustum(self):
        print self.camera_translation, self.camera_rotation
        translation_matrix = Mat4_TranslationMatrix(*self.camera_translation)
        rotation_matrix    = Mat4_RotationMatrix(*self.camera_rotation)
        
        self.normal_matrix = Mat4_to_Mat3(rotation_matrix)
        self.view_matrix = np.dot(Mat4_TranslationMatrix(-700.0, -450.0, 0.0) , np.dot(rotation_matrix, translation_matrix))
        #self.view_matrix = Mat4_TranslationMatrix(*self.camera_translation)*Mat4_RotationMatrix(*self.camera_rotation)*Mat4_TranslationMatrix(-700.0, -450.0, 0.0)
        
        self.projection_view_matrix = np.dot(self.view_matrix,self.projection_matrix)
        
        self._to_update = False
        self._has_moved = True
        
    def RotateCamera(self,a=None,b=None,c=None):
        
        if a: self.camera_rotation.y+=a
        if c: self.camera_rotation.x+=c
        
        #Rotation = Mat4_RotationMatrix(*self.camera_rotation)
        #self.ViewVector=Rotation * (self.DefaultViewVector)
        self._to_update = True

