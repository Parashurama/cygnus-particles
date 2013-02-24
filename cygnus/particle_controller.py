#! /usr/bin/env python
# *-* coding: UTF-8 *-*
from root import ReferenceName
from utils import ColorBlendTexture

class Collector(object):
    controller_flag = 'COLLECTOR_CONTROLLER'
    def __init__(self, domain, collect_inside=True):
        self.domain = domain
        self.domain.controller_flag='COLLECTOR_CONTROLLER'
        self.bool_collect_inside  = collect_inside

class Bounce(object):
    controller_flag = 'BOUNCE_CONTROLLER'
    def __init__(self, domain, friction=True):
        self.domain = domain
        self.domain.controller_flag='BOUNCE_CONTROLLER'
        self.friction = friction

class LifeTime(object):
    controller_flag = 'LIFETIME_CONTROLLER'
    def __init__(self, lifetime):
        self.lifetime = lifetime

class Gravity(object):
    controller_flag = 'GRAVITY_CONTROLLER'
    def __init__(self, gx, gy, gz):
        self.gravity=[gx, gy, gz]

class ColorBlender(object):
    controller_flag = 'COLOR_CONTROLLER'
    def __init__(self, color_info):
        self.start_time = color_info[0][0]
        self.end_time = color_info[-1][0]
        
        self.ColorBlendLookup = ColorBlendTexture(color_info, precision=0.1)

class Growth(object):
    controller_flag = 'GROWTH_CONTROLLER'
    def __init__(self, growth=0.0, damping=1.0):
        self.growth = growth
        self.damping = damping

class Magnet(object):
    controller_flag = 'MAGNETIC_CONTROLLER'
    def __init__(self, origin, charge=0.0, cutoff=150, epsilon=1.0, name=None):
        self.origin = origin
        self.charge = charge
        self.sqr_cutoff_distance = cutoff*cutoff
        self.epsilon = epsilon
        self.name = name
        if name is not None:ReferenceName(self, name)
        
    def Set(self, attr, value):
        setattr(self, attr, value)

class Mass(object):
    def __init__(self, position, mass):
        self.position=position
        self.mass=mass
        
