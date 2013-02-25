import numpy as np

def LoadRawMesh(mesh_file):
    
    indices = np.asarray(map(int, open('{}/faces'.format(mesh_file)).read().strip().split()), dtype='uint16').reshape(-1, 3)#.tolist()
    vertices = np.asarray(map(float, open('{}/vertices'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 3)#.tolist()
    
    return indices, vertices
    
    
    
