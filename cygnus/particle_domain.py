#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from root import ReferenceName
from math_module import Vec3, lerp3

class Domain(object):
    controller_flag=None

class Disc(Domain):
    domain_flag = 'DISC_DOMAIN'
    def __init__(self, center, inner_radius, outer_radius, name=None):
        '''
        '''
        self.center = Vec3(*center)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.radius = self.outer_radius
        
        self.name = name
        if name is not None:ReferenceName(self, name)

class Sphere(Domain):
    domain_flag = 'SPHERE_DOMAIN'
    def __init__(self, center, inner_radius, outer_radius, name=None):
        '''
        '''
        self.center = Vec3(*center)
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.radius = self.outer_radius
        
        self.name = name
        if name is not None:ReferenceName(self, name)

class Square(Domain):
    domain_flag = 'SQUARE_DOMAIN'
    def __init__(self, x0, y0, x1, y1, z, name=None):
        '''
        '''
        A=Vec3(x0, y0, z) ; B =Vec3(x1, y0, z) ; C =Vec3(x1, y1, z); D =Vec3(x0, y1, z)
        
        cAB = lerp3(A,B, 0.5)
        cDC = lerp3(D,C, 0.5)
        self.center = lerp3(cAB,cDC, 0.5)
        
        self.A=A-self.center ; self.B=B-self.center
        self.C=C-self.center ; self.D=D-self.center
        
        self.square=[x0,y0, x1,y1]
        
        self.name = name
        if name is not None:ReferenceName(self, name)
        #self.square_data=[x0-self.center.x, y0self.center.y, x1-self.center.x, y1-self.center.y]

class Triangle(Domain):
    domain_flag = 'TRIANGLE_DOMAIN'
    def __init__(self, A, B, C, name=None):
        '''
        '''
        A=Vec3(*A) ; B =Vec3(*B) ; C =Vec3(*C)
        
        Ap = lerp3(B,C, 0.5)
        
        self.center = lerp3(Ap, A, 0.333)
        
        self.A = A - self.center
        self.B = B - self.center
        self.C = C - self.center
        self.name = name
        if name is not None:ReferenceName(self, name)
        

class Line(Domain):
    domain_flag = 'LINE_DOMAIN'
    def __init__(self, A, B, name=None):
        '''
        '''
        A=Vec3(*A) ; B =Vec3(*B)
        
        self.center = lerp3(A,B, 0.5)        
        self.A = A - self.center
        self.B = B - self.center
        self.name = name
        if name is not None:ReferenceName(self, name)


"""
RANDOM POINT IN SPHERE

z = 2.0 * randomfloat() - 1.0;
t = 2.0 * M_PI * randomfloat();

w = sqrt( 1 - z*z );
x = w * cos( t );
y = w * sin( t );
"""

  
