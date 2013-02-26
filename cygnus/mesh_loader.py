import numpy as np

def LoadRawMesh(mesh_file):
    
    indices = np.asarray(map(int, open('{}/faces'.format(mesh_file)).read().strip().split()), dtype='uint16').reshape(-1, 3)
    vertices = np.asarray(map(float, open('{}/vertices'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 3)
    
    try: normals = np.asarray(map(float, open('{}/normals'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 3)
    except IOError: normals = None
    
    try: texcoords = np.asarray(map(float, open('{}/texcoords'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 2)
    except IOError: texcoords = None
    
    if   normals is None:
        if   texcoords is None:
            vertex_data = vertices
            data_format=('v3f',)
        else:
            vertex_data = np.hstack((vertices, texcoords))
            data_format=('v3f','t2f')         
    else:
        if   texcoords is None:
            vertex_data = np.hstack((vertices, normals))
            data_format=('v3f','n3f')  
        else:
            vertex_data = np.hstack((vertices, normals, texcoords))
            data_format=('v3f','n3f','t2f')  
    
    return indices, vertex_data, data_format
    
    
    
