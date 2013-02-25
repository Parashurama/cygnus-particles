
EMITTER_UNIFORMS_LIST = [
'EMITTER_TYPE',
'EMITTER_PARTICLE_FIRERATE',
'EMITTER_PARTICLE_POSITION',
'EMITTER_PARTICLE_VELOCITY',
'EMITTER_PARTICLE_POSITION_DEVIATION',
'EMITTER_PARTICLE_VELOCITY_DEVIATION',
'EMITTER_PARTICLE_AGE_DEVIATION',

'CIRCLE_EMITTER_RADIUS',
'DISC_EMITTER_RADII',
'LINE_EMITTER_POINTS',
'TRIANGLE_EMITTER_POINTS',
'SQUARE_EMITTER_POINTS',
'SPHERE_EMITTER_RADII',

'PARTICLE_TYPE_TO_EMIT'
]

MESH_EMITTER_UNIFORMS_LIST = [
'EMITTER_TYPE',
'EMITTER_PARTICLE_FIRERATE',
'EMITTER_PARTICLE_POSITION',
'EMITTER_PARTICLE_VELOCITY',
'EMITTER_PARTICLE_POSITION_DEVIATION',
'EMITTER_PARTICLE_VELOCITY_DEVIATION',
'EMITTER_PARTICLE_AGE_DEVIATION',

'PARTICLE_TYPE_TO_EMIT'
]

EMITTER_SECONDARY_UNIFORMS_LIST = [
'PER_PARTICLE_EMITTER_PARTICLE_FIRERATE',
'PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION',
'PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION',
'PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION',
#'PER_PARTICLE_EMITTER_MIN_AGE_EMISSION', 
'PER_PARTICLE_EMITTER_PARTICLE_VELOCITY',
'PER_PARTICLE_EMITTER_PARTICLE_AGE'
]

UPDATER_UNIFORMS_LIST = [
'EMITTER_TYPE',
'PARTICLE_COLLECTORS',
'N_CIRCLE_COLLECTOR',
'N_TRIANGLE_COLLECTOR',
'N_SQUARE_COLLECTOR',

'PARTICLE_BOUNCERS',
'N_CIRCLE_BOUNCER',
'N_TRIANGLE_BOUNCER',
'N_SQUARE_BOUNCER',

'I_CIRCLE_BOUNCER',
'I_SQUARE_BOUNCER',
'I_TRIANGLE_BOUNCER',

'N_MAGNETIC_CONTROLLER',

'PARTICLE_LIFETIME',

'uCircleDom[0].center',
'uCircleDom[0].radius',
'uCircleDom[1].center',
'uCircleDom[1].radius',
'uCircleDom[2].center',
'uCircleDom[2].radius',

'uSquareDom[0].square',
'uSquareDom[0].A',
'uSquareDom[0].B',
'uSquareDom[0].C',
'uSquareDom[0].D',
'uSquareDom[1].square',
'uSquareDom[1].A',
'uSquareDom[1].B',
'uSquareDom[1].C',
'uSquareDom[1].D',
'uSquareDom[2].square',
'uSquareDom[2].A',
'uSquareDom[2].B',
'uSquareDom[2].C',
'uSquareDom[2].D',

'uTriangleDom[0].A',
'uTriangleDom[0].B',
'uTriangleDom[0].C',
'uTriangleDom[1].A',
'uTriangleDom[1].B',
'uTriangleDom[1].C',
'uTriangleDom[2].A',
'uTriangleDom[2].B',
'uTriangleDom[2].C',

'uMagneticCon[0].origin',
'uMagneticCon[0].sqr_cutoff_distance',
'uMagneticCon[0].charge',
'uMagneticCon[0].epsilon',
'uMagneticCon[1].origin',
'uMagneticCon[1].sqr_cutoff_distance',
'uMagneticCon[1].charge',
'uMagneticCon[1].epsilon',
'uMagneticCon[2].origin',
'uMagneticCon[2].sqr_cutoff_distance',
'uMagneticCon[2].charge',
'uMagneticCon[2].epsilon'
]



DEFAULT_MAX_PARTICLE_BUFFER_SIZE=1000000
PARTICLE_DATA_SIZE = 32 #bytes

EMITTER_TYPE_REF = { 'PointEmitter':0,'CircleEmitter':1,'SquareEmitter':2, 'TriangleEmitter':3,'LineEmitter':4    }

MAIN_PARTICLE_EMITTER = 0.0
PARTICLE_TYPE_1 = 10.0
PER_PARTICLE_EMITTER =20.0



EMITTER_UNIFORMS_SRC_DATA = {
                'EMITTER_TYPE':['int',[0]],
                'EMITTER_PARTICLE_FIRERATE':['float',[0]],
                'EMITTER_PARTICLE_POSITION':['float',[0,0,0]],
                'EMITTER_PARTICLE_VELOCITY':['float',[0,0,0]],
                'EMITTER_PARTICLE_POSITION_DEVIATION':['float',[0,0,0]],
                'EMITTER_PARTICLE_VELOCITY_DEVIATION':['float',[0,0,0]],
                'EMITTER_PARTICLE_AGE_DEVIATION':['float',[0]],
                
                'CIRCLE_EMITTER_RADIUS':['float',[0]],
                'DISC_EMITTER_RADII':['float',[0,0]],
                'LINE_EMITTER_POINTS':['float',[0,0,0,0, 0,0,0,0]],
                'TRIANGLE_EMITTER_POINTS':['float',[0,0,0,0, 0,0,0,0, 0,0,0,0]],
                'SQUARE_EMITTER_POINTS':['float',[0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]],
                'SPHERE_EMITTER_RADII':['float',[0,0]],
                'PARTICLE_TYPE_TO_EMIT':['float',[0]]
                
                }


MESH_EMITTER_UNIFORMS_SRC_DATA = {
                'EMITTER_TYPE':['int',[0]],
                'EMITTER_PARTICLE_FIRERATE':['float',[0]],
                'EMITTER_PARTICLE_POSITION':['float',[0,0,0]],
                'EMITTER_PARTICLE_VELOCITY':['float',[0,0,0]],
                'EMITTER_PARTICLE_POSITION_DEVIATION':['float',[0,0,0]],
                'EMITTER_PARTICLE_VELOCITY_DEVIATION':['float',[0,0,0]],
                'EMITTER_PARTICLE_AGE_DEVIATION':['float',[0]],
                

                'PARTICLE_TYPE_TO_EMIT':['float',[0]]
                }

EMITTER_SECONDARY_UNIFORMS_SRC_DATA = {
                'PER_PARTICLE_EMITTER_PARTICLE_FIRERATE':['float',[0]],
                'PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION':['float',[0,0,0]],
                'PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION':['float',[0,0,0]],
                'PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION':['float',[0]],
                #'PER_PARTICLE_EMITTER_MIN_AGE_EMISSION':['float',[0]], 
                'PER_PARTICLE_EMITTER_PARTICLE_VELOCITY':['float',[0,0,0]],
                'PER_PARTICLE_EMITTER_PARTICLE_AGE':['float',[0]],
                }

UPDATER_UNIFORMS_SRC_DATA = {
                
                'PARTICLE_LIFETIME':['float',[0]],
                'EMITTER_TYPE':['int',[0]],
                
                'PARTICLE_COLLECTORS':['int',[0]],
                'N_CIRCLE_COLLECTOR':['int',[0]],
                'N_TRIANGLE_COLLECTOR':['int',[0]],
                'N_SQUARE_COLLECTOR':['int',[0]],
                
                'PARTICLE_BOUNCERS':['int',[0]],
                'N_CIRCLE_BOUNCER':['int',[0]],
                'N_TRIANGLE_BOUNCER':['int',[0]],
                'N_SQUARE_BOUNCER':['int',[0]],
                'I_CIRCLE_BOUNCER':['int',[0]],
                'I_SQUARE_BOUNCER':['int',[0]],
                'I_TRIANGLE_BOUNCER':['int',[0]],
                'N_MAGNETIC_CONTROLLER':['int',[0]],

                'uTriangleDom[0].A':['float',[0,0,0]],
                'uTriangleDom[0].B':['float',[0,0,0]],
                'uTriangleDom[0].C':['float',[0,0,0]],
                'uTriangleDom[1].A':['float',[0,0,0]],
                'uTriangleDom[1].B':['float',[0,0,0]],
                'uTriangleDom[1].C':['float',[0,0,0]],
                'uTriangleDom[2].A':['float',[0,0,0]],
                'uTriangleDom[2].B':['float',[0,0,0]],
                'uTriangleDom[2].C':['float',[0,0,0]],
                'uSquareDom[0].square':['float',[0,0,0,0]],
                'uSquareDom[0].A':['float',[0,0,0]],
                'uSquareDom[0].B':['float',[0,0,0]],
                'uSquareDom[0].C':['float',[0,0,0]],
                'uSquareDom[0].D':['float',[0,0,0]],
                'uSquareDom[1].square':['float',[0,0,0,0]],
                'uSquareDom[1].A':['float',[0,0,0]],
                'uSquareDom[1].B':['float',[0,0,0]],
                'uSquareDom[1].C':['float',[0,0,0]],
                'uSquareDom[1].D':['float',[0,0,0]],
                'uSquareDom[2].square':['float',[0,0,0,0]],
                'uSquareDom[2].A':['float',[0,0,0]],
                'uSquareDom[2].B':['float',[0,0,0]],
                'uSquareDom[2].C':['float',[0,0,0]],
                'uSquareDom[2].D':['float',[0,0,0]],
                'uCircleDom[0].center':['float',[0,0,0]],
                'uCircleDom[0].radius':['float',[0]],
                'uCircleDom[1].center':['float',[0,0,0]],
                'uCircleDom[1].radius':['float',[0]],
                'uCircleDom[2].center':['float',[0,0,0]],
                'uCircleDom[2].radius':['float',[0]],

                'uMagneticCon[0].origin':['float',[0,0,0]],
                'uMagneticCon[0].sqr_cutoff_distance':['float',[0]],
                'uMagneticCon[0].charge':['float',[0]],
                'uMagneticCon[0].epsilon':['float',[0]],
                'uMagneticCon[1].origin':['float',[0,0,0]],
                'uMagneticCon[1].sqr_cutoff_distance':['float',[0]],
                'uMagneticCon[1].charge':['float',[0]],
                'uMagneticCon[1].epsilon':['float',[0]],
                'uMagneticCon[2].origin':['float',[0,0,0]],
                'uMagneticCon[2].sqr_cutoff_distance':['float',[0]],
                'uMagneticCon[2].charge':['float',[0]],
                'uMagneticCon[2].epsilon':['float',[0]]
                }

                
DOMAIN_REF = {  'TRIANGLE_DOMAIN':('uTriangleDom[{0}].{1}', (('A',3), ('B',3), ('C',3))),
                'SQUARE_DOMAIN': ('uSquareDom[{0}].{1}', (('square',4), ('A',3), ('B',3), ('C',3), ('D',3) )),
                'CIRCLE_DOMAIN': ('uCircleDom[{0}].{1}', (('radius',1),('center',3))) }
