#! /usr/bin/env python
# *-* coding: UTF-8 *-*
import sys
sys.path.append('..')

import cygnus
import OpenGL.GL as gl

from cygnus.particle_domain import Triangle, Square, Line, Disc, Sphere
from cygnus.particle_controller import LifeTime, Collector, Gravity, ColorBlender, Growth, Magnet, Bounce
from cygnus.particle_renderer import PointRenderer, PointSpriteRenderer, AnimatedPointSpriteRenderer, MeshRenderer
from cygnus.particle_emitter import BasicEmitter, PerParticleEmitter
#from Cygnus.particle_pool import ParticlePool
from cygnus import Particle, Template, Texture2D, AnimatedTexture, ParticleMesh, GetObjectfromName

def Cloud(i, circle, color):
    DOMAIN_CONTROLLERS = [  Gravity(0.0, 295.81, 0.0),
                            #Growth(1.0),
                            Collector(domain = Circle((750, 350, 0.0), 96) ),
                            Magnet( origin=(600, 550, 0),
                                            charge=-0.01,
                                            cutoff=250,
                                            name='MoveMagnet',
                                            epsilon=5.0),
                            #Bounce(domain = Circle((750, 650, 0.0), 32) ),
                            #Bounce(domain = Circle((450, 550, 0.0), 32) )
                            ]
    
    E = BasicEmitter( name='Test{}'.format(i),
                  #position=Disc(*circle),
                  position=(650.0, 100.0, 0.0),
                  fire_rate=10000,
                  particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0), color = color ),
                    
                  particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                  velocity= (50.0, 50.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                  age = 0.5 ),
                  controllers = DOMAIN_CONTROLLERS+[ LifeTime(10.0) ],
                  
                  renderer = PointRenderer( point_size=4.0, feather = 2.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                                
                )

def Fire(i,position):
    
    DOMAIN_CONTROLLERS = [  Gravity(0.0, 60.81, 0.0),
                            Growth(5.0),
                            ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                            (0.5, (0.0, 0.0, 0.5, 0.2)), 
                                            (0.9, (0.0, 0.5, 1.0, 0.6)), 
                                            (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                            (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                            (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                            (4.0, (0.8, 0.8, 0.8, 0.01)),
                                            (6.0, (0.8, 0.8, 0.8, 0.0)) ]),

                            ]
    """                            ColorBlender([  (0.0, (1.0, 0.0, 0.0, 1.0)),
                                            (3.0, (0.0, 1.0, 0.0, 1.0)),
                                            (6.0, (0.0, 0.0, 1.0, 1.0)) ]),
                            """
    E = BasicEmitter( name='TestFire{}'.format(i),
                  position=Line(*position),
                  #position=(650.0, 100.0, 0.0),
                  fire_rate=5000,
                  particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0) ),#, color = (1.0,0.4,1.0,0.7)
                    
                  particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                  velocity= (5.0, 10.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                  age = 0.8 ),
                  controllers = DOMAIN_CONTROLLERS+[ LifeTime(4.0) ],
                  
                  renderer = PointRenderer( point_size=32.0, feather = 128.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                                
                )
    """
    E = BasicEmitter( name='TestFire{}'.format(i),
                  position=Circle(position, 50),
                  #position=(650.0, 100.0, 0.0),
                  fire_rate=1000,
                  particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0) ),#, color = (1.0,0.4,1.0,0.7)
                    
                  particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                  velocity= (5.0, 5.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                  age = 0.5 ),
                  controllers = DOMAIN_CONTROLLERS+[ LifeTime(6.0) ],
                  
                  renderer = PointRenderer( point_size=64.0, feather = 128.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                                
                )
    """
def Plasma():
        
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
    #DOMAIN_CONTROLLERS=[]
    BasicEmitter(   name='Test1',
                    #position=Disc((720, 150, 0.0), 45, 75),#(720.0, 450.0),
                    position=(650.0, 100.0, 0.0),
                    fire_rate=20000,
                    particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0), color = (1.0,0.4,1.0,0.7) ),
                    
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
                    renderer = PointRenderer( point_size=4.0, feather = 2.0,
                                           blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                    
                    #renderer = MeshRenderer( ParticleMesh('Media/Models/book_open', 'Media/Models/book.png') )
                    )

def Nebulae():
    
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
                                renderer = PointRenderer( point_size=4.0, feather = 8.0,
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
    #DOMAIN_CONTROLLERS=[]
    BasicEmitter(   name='Test1',
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
                    renderer = PointRenderer( point_size=3.0, feather = 2.0,
                                           blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                    
                    #renderer = MeshRenderer( ParticleMesh('Media/Models/book_open', 'Media/Models/book.png') )
                    )
    
def Fireworks():
    trail = PerParticleEmitter( name='Trail0',
                                fire_rate=500,
                                velocity = (0.0,0.0,0.0),
                                color = (0.0,0.8,1.0,0.7),
                                particle_template=Particle( position = (0.0, 0.0, 0.0),
                                                            velocity = (0.0, 0.0, 0.0),
                                                            #color = (1.0,0.4,1.0,0.7)
                                                          ),
                                particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                                velocity= (5.0,5.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                                age = 0.5 ),
                                controllers = [ LifeTime(1.0),
                                                #Growth(1.0),
                                                ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                (0.1, (0.0, 0.0, 0.5, 0.7)), 
                                                                (0.2, (0.0, 0.5, 1.0, 1.0)), 
                                                                (0.5, (1.0, 1.0, 0.0, 1.0)), 
                                                                (0.7, (0.9, 0.2, 0.0, 1.0)), 
                                                                (0.9, (0.6, 0.1, 0.05, 0.8)), 
                                                                (0.95, (0.8, 0.8, 0.8, 0.5)),
                                                                (1.0, (0.8, 0.8, 0.8, 0.0)) ])
                                                ],
                                renderer = PointRenderer( point_size=4.0, feather = 8.0,
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
    #DOMAIN_CONTROLLERS=[]
    BasicEmitter(   name='Test1',
                    #position=Disc((720, 150, 0.0), 45, 75),#(720.0, 450.0),
                    position=(650.0, 100.0, 0.0),
                    fire_rate=40,
                    particle_template=trail,
                    
                    particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                    velocity= (150.0, 150.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
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

def GravityFun():
    
    ParticlePool(name='POLL0',
                n_particles = 2500,
                particle_template = Particle( position = (750.0, 450.0, 0.0),
                                              velocity = (0.0, 0.0, 0.0),
                                              mass= 6#color = (1.0,0.4,1.0,0.7)
                                          ),
                particle_deviation = Template(  position = (300.0, 300.0, 0.0),#(0.0, 0.0, 0.0),
                                                velocity= (2.0, 2.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                age = 0.5,
                                                mass = 2 ),
                renderer = PointRenderer( point_size=64.0, feather = 0.0,
                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                                )

def Burst():
    #DOMAIN_CONTROLLERS=[]
    BasicEmitter(   name='Test1',
                    position=Sphere((720.0, 450.0, 0.0), 0, 75),#(720.0, 450.0),
                    #position=Square(450.0, 450.0, 650.0, 650.0, 0.0),
                    #position=(650.0, 100.0, 0.0),
                    fire_rate=400000,
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
    
def SetupParticles():
    Burst()
    #Nebulae()
    #Plasma()
    #Fireworks()
    #GravityFun()
    #Fire(1, ((370, 250, 0.0),(770, 250, 0.0)))
    #Cloud(0, ((750, 450, 0.0),0, 128), (0.0,1.0,1.0,0.7))
    return 
    
    """
    ParticlePool(name='POLL0',
                n_particles = 2500,
                particle_template = Particle( position = (750.0, 450.0, 0.0),
                                              velocity = (0.0, 0.0, 0.0),
                                              mass= 6#color = (1.0,0.4,1.0,0.7)
                                          ),
                particle_deviation = Template(  position = (300.0, 300.0, 0.0),#(0.0, 0.0, 0.0),
                                                velocity= (10.0, 10.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                age = 0.5,
                                                mass = 5 ),
                renderer = PointRenderer( point_size=64.0, feather = 0.0,
                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                                )
    
    
    trail = PerParticleEmitter( name='Trail0',
                                fire_rate=505,
                                velocity = (0.0,0.0,0.0),
                                #color = (0.0,0.8,1.0,0.7),
                                particle_template=Particle( position = (0.0, 0.0, 0.0),
                                                            velocity = (0.0, 0.0, 0.0),
                                                            #color = (1.0,0.4,1.0,0.7)
                                                          ),
                                particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                                velocity= (5.0,5.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                                age = 0.5 ),
                                controllers = [ LifeTime(2.0),
                                                Growth(2.0),
                                                ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                (0.5, (0.0, 0.0, 0.5, 0.2)), 
                                                                (0.9, (0.0, 0.5, 1.0, 0.6)), 
                                                                (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                                                (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                (6.0, (0.8, 0.8, 0.8, 0.0)) ]),
                                                ],
                                renderer = PointRenderer( point_size=4.0, feather = 8.0,
                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                                #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/_Dark_1.png', 5, 5),
                                #                                        point_size=64.1,
                                #                                        feather = 0.0,)
                                )
    #"""
    #"""
    """
    DOMAIN_CONTROLLERS = [Gravity(0.0, 95.81, 0.0)],
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
    """
    DOMAIN_CONTROLLERS = [ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                (0.5, (0.0, 0.0, 0.5, 0.2)), 
                                                                (0.9, (0.0, 0.5, 1.0, 0.6)), 
                                                                (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                                                (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                (6.0, (0.8, 0.8, 0.8, 0.0)) ])]#Gravity(0.0, 95.81, 0.0)]
    
    
    BasicEmitter(   name='Test1',
                    #position=Circle((750, 450, 0.0), 50),
                    #position=Triangle( (150, 150, 0.0),(250, 250, 0.0),(150, 250, 0.0)),
                    #position=Line((600, 100, 0.0), (950, 100, 0.0)),
                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                    #position=Square(450.0, 450.0, 650.0, 650.0, 0.0),
                    position=Disc((720, 150, 0.0), 45, 75),#(720.0, 450.0),
                    #position=(650.0, 100.0, 0.0),
                    fire_rate=200000,
                    #particle_template=trail,
                    particle_template = Particle( position = (0.0, 0.0, 0.0), velocity = (0.0, 0.0, 0.0)),#, color = (1.0,0.4,1.0,0.7) ),
                    
                    particle_deviation = Template(  position = (20.0, 20.0, 0.0),#(0.0, 0.0, 0.0),
                                                    velocity= (5.0, 5.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                    age = 1.0 ),
                    controllers = DOMAIN_CONTROLLERS+[ LifeTime(2.0) ],
                    
                    #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/Images/_Dark_1.png', 5, 5),
                    #                                        point_size=64.1,
                    #                                        feather = 0.0,)
                                                            #blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)
                    #renderer = PointSpriteRenderer( Texture('Media/Images/bubble.png'), point_size=128.1, feather = 0.0,
                    #                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                    renderer = PointRenderer( point_size=4.0, feather = 2.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                    
                    #renderer = MeshRenderer( ParticleMesh('Media/Models/book_open', 'Media/Models/book.png') )
                    )
    #"""
    """
    BasicEmitter(   name='Test2',
                    position=(650.0, 100.0, 0.0),
                    fire_rate=16000,
                    particle_template = Particle( position = (0.0, 0.0, 0.0),
                                                  velocity = (0.0, 0.0, 0.0),
                                                  color = (0.0,0.9,1.0,0.7) ),
                    particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                    velocity= (50.0, 50.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                    age = 0.5 ),
                    controllers = DOMAIN_CONTROLLERS + [ LifeTime(25.0) ],
                    
                    renderer = PointRenderer( point_size=4.0, feather = 2.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                    
                    )


                                                        ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.0)), 
                                                                        (3.0, (1.0, 1.0, 1.5, 1.2)) ]),
                                                                        
                                                        ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                        (0.5, (0.0, 0.0, 0.5, 0.2)), 
                                                                        (0.9, (0.0, 0.5, 1.0, 0.6)), 
                                                                        (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                        (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                                                        (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                        (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                        (6.0, (0.8, 0.8, 0.8, 0.0)) ]),

################## PSEUDO-FIRE #####################"

   
    ShVarsX.Test = StaticEmitter(   #position=Triangle( (250, 150, 0.0),(350, 150, 0.0),(300, 350, 0.0)),
                                    #position=Circle((750, 430, 0.0), 15),
                                    position=Line((600, 100, 0.0), (750, 100, 0.0)),
                                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                                    #position=Circle((720, 150, 0.0), 75),#(720.0, 450.0),
                                    #position=(720.0, 450.0, 0.0),
                                    fire_rate=25,
                                    template=Particle( position = (0.0, 0.0, 0.0),
                                                       velocity = (0.0, 0.0, 0.0) ),
                                    deviation = Holder( position = (5.0, 5.0, 0.0),
                                                        velocity=(7.0,0.0, 0.0),
                                                        age=0.1 )
                                    )
    ShVarsX.TestGroup = ParticleGroup(emitter=ShVarsX.Test,
                                      controllers = [   LifeTime(7),
                                                        Gravity(0.0, 55.81, 0.0),
                                                        Growth(35.0),
                                                        #Magnet( origin=(720, 550, 0),
                                                        #        charge=1500,
                                                        #        cutoff=150,
                                                        #        epsilon=0.01),
                                                        Collector(domain = Circle((450, 130, 0.0), 35) ),
                                                        ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                        (0.5, (0.0, 0.0, 0.5, 0.1)), 
                                                                        (0.9, (0.0, 0.5, 1.0, 0.05)), 
                                                                        (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                        (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                                                        (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                        (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                        (6.0, (0.8, 0.8, 0.8, 0.0)) ]),
                                                        #Collector(domain = Circle((750, 430, 0.0), 15) ),
                                                        #Collector(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0),  ),
                                                        #Collector(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), ),
                                                    ],
                                        renderer = PointRendererObject( point_size=44.1, feather = 25.0,
                                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                      )

    
    ShVarsX.Test = StaticEmitter(   #position=Triangle( (250, 150, 0.0),(350, 150, 0.0),(300, 350, 0.0)),
                                    #position=Circle((750, 430, 0.0), 15),
                                    #position=Line((600, 100, 0.0), (750, 100, 0.0)),
                                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                                    #position=Circle((720, 150, 0.0), 75),#(720.0, 450.0),
                                    position=(650.0, 100.0, 0.0),
                                    fire_rate=20,
                                    template=Particle( position = (0.0, 0.0, 0.0),
                                                       velocity = (0.0, 0.0, 0.0) ),
                                    deviation = Holder( position = (15.0, 15.0, 0.0),
                                                        velocity=(7.0,0.0, 0.0),
                                                        age=0.1 )
                                    )
    ShVarsX.TestGroup = ParticleGroup(emitter=ShVarsX.Test,
                                      controllers = [   LifeTime(7),
                                                        Gravity(0.0, 55.81, 0.0),
                                                        Growth(35.0),
                                                        #Magnet( origin=(720, 550, 0),
                                                        #        charge=1500,
                                                        #        cutoff=150,
                                                        #        epsilon=0.01),
                                                        Collector(domain = Circle((450, 130, 0.0), 35) ),
                                                        ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                        (0.5, (0.0, 0.0, 0.5, 0.1)), 
                                                                        (0.9, (0.0, 0.5, 1.0, 0.05)), 
                                                                        (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                        (2.1, (0.9, 0.2, 0.0, 0.4)), 
                                                                        (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                        (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                        (6.0, (0.8, 0.8, 0.8, 0.0)) ]),
                                                        #Collector(domain = Circle((750, 430, 0.0), 15) ),
                                                        #Collector(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0),  ),
                                                        #Collector(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), ),
                                                    ],
                                        renderer = PointRendererObject( point_size=44.1, feather = 25.0,
                                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                      )



################ pARTICLE fIELD

    
    ShVarsX.Test = StaticEmitter(   #position=Triangle( (250, 150, 0.0),(350, 150, 0.0),(300, 350, 0.0)),
                                    #position=Circle((750, 430, 0.0), 15),
                                    #position=Line((600, 100, 0.0), (750, 100, 0.0)),
                                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                                    #position=Circle((720, 150, 0.0), 75),#(720.0, 450.0),
                                    position=(650.0, 100.0, 0.0),
                                    fire_rate=30500,
                                    template=Particle( position = (0.0, 0.0, 0.0),
                                                       velocity = (0.0, 0.0, 0.0),
                                                       color = (1.0,0.4,1.0,0.7)
                                                    ),
                                    deviation = Holder( position = (150.0, 15.0, 0.0),
                                                        velocity=(35.0,35.0, 0.0),
                                                        age=0.1 )
                                    )
    ShVarsX.TestGroup = ParticleGroup(emitter=ShVarsX.Test,
                                      controllers = [   LifeTime(10),
                                                        Gravity(0.0, 155.81, 0.0),
                                                        #Growth(5.0),
                                                        Magnet( origin=(720, 550, 0),
                                                                charge=0.01,
                                                                cutoff=350,
                                                                epsilon=1.0),
                                                        Magnet( origin=(220, 450, 0),
                                                                charge=0.01,
                                                                cutoff=350,
                                                                epsilon=1.0),
                                                       Magnet( origin=(720, 250, 0),
                                                                charge=0.01,
                                                                cutoff=350,
                                                                epsilon=1.0),
                                                        Magnet( origin=(500, 350, 0),
                                                                charge=-0.005,
                                                                cutoff=350,
                                                                epsilon=1.0),
                                                        Collector(domain = Circle((500, 350, 0.0), 5) ),
                                                        #Collector(domain = Circle((750, 430, 0.0), 15) ),
                                                        #Collector(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0),  ),
                                                        #Collector(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), ),
                                                    ],
                                        renderer = PointRendererObject( point_size=2.1, feather = 2.0,
                                                                        blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                      )
    

    ShVarsX.Test = StaticEmitter(   #position=Triangle( (250, 150, 0.0),(350, 150, 0.0),(300, 350, 0.0)),
                                    position=Circle((750, 430, 0.0), 15),
                                    #position=Line((600, 100, 0.0), (750, 100, 0.0)),
                                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                                    #position=Circle((720, 150, 0.0), 75),#(720.0, 450.0),
                                    #position=(650.0, 100.0, 0.0),
                                    fire_rate=150000,
                                    template=Particle( position = (0.0, 0.0, 0.0),
                                                       velocity = (0.0, 0.0, 0.0),
                                                       #color = (1.0,0.4,1.0,1.0)
                                                    ),
                                    deviation = Template(   position = (5.0, 5.0, 0.0),#(0.0, 0.0, 0.0),
                                                            velocity= (50.0,50.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                            age=0.5 )
                                    )
    
    ShVarsX.TestGroup = ParticleGroup(emitter=ShVarsX.Test,
                                      controllers = [   LifeTime(3),
                                                        Gravity(0.0, 55.81, 0.0),
                                                        #Growth(0.0),
                                                        #Bounce(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0), friction=0.7 ),
                                                        #Bounce(domain = Circle((350, 350, 0.0), 20), friction=0.7 ),
                                                        #Bounce(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), friction=0.7 ),
                                                        ColorBlender([  (0,   (0.0, 0.0, 0.2, 0.1)), 
                                                                        (0.5, (0.0, 0.0, 0.5, 0.1)), 
                                                                        (0.9, (0.0, 0.5, 1.0, 0.05)), 
                                                                        (1.5, (1.0, 1.0, 0.0, 0.2)), 
                                                                        (2.7, (0.9, 0.2, 0.0, 0.4)), 
                                                                        (3.2, (0.6, 0.1, 0.05, 0.2)), 
                                                                        (4.0, (0.8, 0.8, 0.8, 0.01)),
                                                                        (6.0, (0.8, 0.8, 0.8, 0.0)) ]),
                                                        Magnet( origin=(720, 550, 0),
                                                                charge=0.05,
                                                                cutoff=250,
                                                                epsilon=1.0),
                                                        Magnet( origin=(220, 450, 0),
                                                                charge=0.01,
                                                                cutoff=150,
                                                                epsilon=1.0),
                                                        Magnet( origin=(720, 250, 0),
                                                                charge=0.01,
                                                                cutoff=150,
                                                                epsilon=1.0),
                                                        #Collector(domain = Circle((750, 430, 0.0), 35) ),
                                                        #Collector(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0),  ),
                                                        #Collector(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), ),
                                                    ],
                                        #renderer = PointSpriteRenderer( Texture('Media/bubble.png'), point_size=128.1, feather = 0.0,
                                        #                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),
                                        
                                        #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/_Dark_1.png', 5, 5),
                                        #                                        point_size=1.1,
                                        #                                        feather = 0.0,
                                        #                                        #blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)
                                        #                                        )
                                        renderer = PointRenderer( point_size=4.0, feather = 1.0,
                                                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                                      )

    

    BasicEmitter(   name='Test1',
                    #position=Circle((750, 430, 0.0), 15),
                    position=Triangle( (250, 150, 0.0),(350, 150, 0.0),(300, 350, 0.0)),
                    #position=Line((600, 100, 0.0), (750, 100, 0.0)),
                    #position=Square(350.0, 250.0, 650.0, 550.0, 0.0),
                    #position=Circle((720, 150, 0.0), 75),#(720.0, 450.0),
                    #position=(650.0, 100.0, 0.0),
                    fire_rate=70000,
                    particle_template=Particle( position = (0.0, 0.0, 0.0),
                                                velocity = (0.0, 0.0, 0.0),
                                                color = (1.0,0.4,1.0,0.7)
                                              ),
                    particle_deviation = Template(  position = (0.0, 0.0, 0.0),#(0.0, 0.0, 0.0),
                                                    velocity= (3.0,3.0, 0.0),#(35.0,35.0, 0.0),#(0.0,0.0, 0.0),#
                                                    age = 0.5 ),
                    controllers = [   LifeTime(10.1),
                                    Gravity(0.0, 355.81, 0.0),
                                    #Growth(0.0),
                                    #Bounce(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0), friction=0.7 ),
                                    #Bounce(domain = Circle((350, 350, 0.0), 20), friction=0.7 ),
                                    #Bounce(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), friction=0.7 ),
                                    
                                    Magnet( origin=(750, 550, 0),
                                            charge=0.05,
                                            cutoff=250,
                                            name='MoveMagnet',
                                            epsilon=1.0),
                                    Magnet( origin=(220, 450, 0),
                                            charge=0.01,
                                            cutoff=150,
                                            epsilon=1.0),
                                    Magnet( origin=(720, 250, 0),
                                            charge=0.01,
                                            cutoff=150,
                                            epsilon=1.0),
                                    #Collector(domain = Circle((750, 430, 0.0), 35) ),
                                    #Collector(domain = Square(550.0, 450.0, 650.0, 550.0, 0.0),  ),
                                    #Collector(domain = Triangle( (250, 150, 0.0),(650, 650, 0.0),(850, 350, 0.0)), ),
                                ],
                    #renderer = PointSpriteRenderer( Texture('Media/bubble.png'), point_size=128.1, feather = 0.0,
                    #                                blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)),

                    #renderer = AnimatedPointSpriteRenderer( AnimatedTexture('Media/_Dark_1.png', 5, 5),
                    #                                        point_size=1.1,
                    #                                        feather = 0.0,
                    #                                        #blending=(gl.GL_SRC_ALPHA, gl.GL_ONE)
                    #                                        )
                    renderer = PointRenderer( point_size=2.0, feather = 0.0,
                                            blending=(gl.GL_SRC_ALPHA, gl.GL_ONE))
                    
                    )
"""
