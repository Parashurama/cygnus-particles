#! /usr/bin/env python
# *-* coding: UTF-8 *-*

import numpy as np
import os


class ModelLoadingError(Exception):
    pass

class MaterialFileLoadingError(Exception):
    pass

############### LOAD MESH UTILS #####################

MATERIAL_COMPONENTS = { 'Ka':'ambient',
                        'Kd':'diffuse',
                        'Ks':'specular',
                        'd':'tranparency',
                        'Tr':'tranparency',
                        'Ns':'shininess',
                        'Ni':'refraction_indice',
                        'illum':'illumination_mode',
                        'map_Ka':'ambiant_texture',
                        'map_Kd':'diffuse_texture',
                        'map_Ks':'specular_texture',
                        'bump' : 'bump_texture',
                        'map_bump':'bump_texture',
                        'face_culling':'face_culling'}

def LoadMaterialsFile(filename, folder, use_default_material=True, alternate_file_name=None):
    contents = {}
    mtl = None
    
    if alternate_file_name is not None:
        
        alternate_file_name = os.path.join(filename,alternate_file_name)
        
        if not os.path.exists(alternate_file_name):
            alternate_file_name = filename+'.mtl'
        
        mtlfilename=alternate_file_name
    else:
        if not filename.endswith('.mtl'):
            mtlfilename = os.path.normpath(os.path.join(folder, filename+'.mtl'))
        else:
            mtlfilename = os.path.normpath(os.path.join(folder, filename))
        
    try:
        material_file = open(mtlfilename, "r")
    except IOError:
        if use_default_material:
            # If Material not Found Use Default Material
            return {'DEFAULT_MATERIAL':{'name':'DEFAULT_MATERIAL'}}
        else:
            raise MaterialFileLoadingError("Invalid Material Filename '{}' in Model File".format(mtlfilename))
    
    for line in open(mtlfilename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if len(values) in (0,1): continue
        
        component = values[0]
        
        # New Material definition
        if component == 'newmtl':
            mtl = {}
            contents[values[1]]=mtl
            mtl['name'] = values[1]
            
        # Assert mtl file contains material definitions
        elif mtl is None:
            raise MaterialFileLoadingError("'.mtl' file doesn't start with newmtl statement")
        
        # Diffuse map component
        elif component == 'map_Kd':
            Texturefile = os.path.relpath(os.path.join(folder,values[1]))
            mtl[MATERIAL_COMPONENTS[component]] = Texturefile
            assert os.path.isfile(Texturefile), "Diffuse Texture file '{}' does not exists".format(Texturefile)
        
        # Specular map component
        elif component == 'map_Ks':
            Texturefile = os.path.relpath(os.path.join(folder,values[1]))
            mtl[MATERIAL_COMPONENTS[component]] = Texturefile
            assert os.path.isfile(Texturefile), "Specular Texture file '{}' does not exists".format(Texturefile)
        
        # Bump map component
        elif component in ("bump","map_bump"):
            Texturefile = os.path.relpath(os.path.join(folder,values[1]))
            mtl[MATERIAL_COMPONENTS[component]] = Texturefile
            assert os.path.isfile(Texturefile), "Bump Texture file '{}' does not exists".format(Texturefile)
            
            if len(values) > 2 and values[2] == '-bm':
                mtl['bump_multiplier'] = float(values[3])
            else:
                mtl['bump_multiplier'] = 1.0
            
        else:
            COMPONENT = MATERIAL_COMPONENTS[component]
            mtl[COMPONENT] = map(float, values[1:])
            if len(mtl[COMPONENT]) == 3: mtl[COMPONENT] = mtl[COMPONENT]+[1.0]
            if len(mtl[COMPONENT]) == 1: mtl[COMPONENT] = mtl[COMPONENT][0]
    
    contents['DEFAULT_MATERIAL']={'name':'DEFAULT_MATERIAL'}
    
    return contents

def Pack_VertexData(vertices, normals=None, texcoords=None):
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
    
    return vertex_data, data_format

def tesselate_face(faces, vertices):
    tri1 = [faces[0],faces[1], faces[3]]
    tri2 = [faces[3],faces[1], faces[2]]
    
    return [get_triangle_data(tri1), get_triangle_data(tri2)]

def get_triangle_data(face):
    triangle = []
    for v in face:
        w = v.split('/')
        point = []
        # structure: vertex_indice/texcoords_indice/normal_indice
        point.append(int(w[0]))
        if len(w) >= 2 and len(w[1]) > 0: point.append(int(w[1]))# texcoords
        else:                             point.append(-1)
        if len(w) == 3 and len(w[2]) > 0: point.append(int(w[2]))# normals
        else:                             point.append(-1)
        triangle.append(tuple(point))
    
    return triangle



def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens                
    return arr

# https://sites.google.com/site/dlampetest/python/calculating-normals-of-a-triangle-mesh-using-numpy
def calculateMeshNormals(faces, vertices):
    #Then we create our new normal array:

    #Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal
    norm = np.zeros( vertices.shape, dtype=vertices.dtype )
    #Create an indexed view into the vertex array using the array of three indices for triangles
    tris = vertices[faces]
    #Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
    n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )# n is now an array of normals per triangle. The length of each normal is dependent the vertices, # we need to normalize these, so that our next step weights each normal equally.normalize_v3(n)
    # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
    # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle, 
    # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
    # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
    
    norm[ faces[:,0] ] += n
    norm[ faces[:,1] ] += n
    norm[ faces[:,2] ] += n
    
    normalize_v3(norm)
    
    return norm

    

###############################################################
##################### LOAD MESH FUNCTIONS #####################
###############################################################

def LoadMesh(mesh_file):
    filename = os.path.basename(mesh_file)
    
    if '.' in filename:
        file_extension = filename.split('.')[-1]
    else:
        file_extension = 'raw'
    
    if   file_extension == 'obj':
        return LoadObjMesh(mesh_file)
        
    elif file_extension == 'raw':
        return LoadRawMesh(mesh_file)
    
    raise ValueError()


def LoadRawMesh(mesh_file):
    
    indices = np.asarray(map(int, open('{}/faces'.format(mesh_file)).read().strip().split()), dtype='uint16')
    vertices = np.asarray(map(float, open('{}/vertices'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 3)
    
    try: normals = np.asarray(map(float, open('{}/normals'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 3)
    except IOError: normals = None
    
    try: texcoords = np.asarray(map(float, open('{}/texcoords'.format(mesh_file)).read().strip().split()), dtype='float32').reshape(-1, 2)
    except IOError: texcoords = None
    
    materials_reference = LoadMaterialsFile(mesh_file, mesh_file, alternate_file_name='materials')
    
    # get arbitrary dictionary key
    current_material_name = next(materials_reference.iterkeys(), None)
    
    vertex_data, data_format = Pack_VertexData(vertices, normals, texcoords)
    faces_data=indices                       # indice_count, offset, byte_offset, indice_dtype
    faces_materials = {current_material_name:(indices.shape[0],   0,           0, indices.dtype)}
    
    return faces_data, faces_materials, materials_reference, vertex_data, data_format

def LoadObjMesh(mesh_filename):
    vertices = []
    normals = []
    texcoords = []
    faces = {}
    
    folder = os.path.dirname(mesh_filename)
    materials_ref_file = mesh_filename[:-3]+'.mtl'
    
    hasnormals = False
    hastexcoords = False
    hasmaterial = True
    material = 'DEFAULT_MATERIAL'
    
    with open(mesh_filename,"r") as file:
        for line in file.readlines():
            line = line.strip()
            if line.startswith('#'): continue
            values = line.split()
            
            if not values: continue
            first_word = values[0]
            
            if   first_word == 'v' :  # mesh vertexes
                vertices.append (map(float,values[1:4])); continue
            
            elif first_word == 'vn': # mesh vertexes normals
                normals.append  (map(float,values[1:4])); hasnormals = True; continue
            
            elif first_word == 'vt':# mesh vertexes texcoords
                texcoords.append(map(float,values[1:3])); hastexcoords = True; continue
            
            elif first_word == 'f' :# mesh vertexes faces
                
                if not len(values[1:]) == 3:
                    if not len(values[1:]) == 4:
                        raise ModelLoadingError("OBJ Model '{}': Unsupported polygons at Face {}. (must be Triangles or Quads)".format(mesh_filename, values[1:]))
                    triangles = tesselate_face(values[1:], vertices)
                    
                else:
                    triangles = [get_triangle_data(values[1:])]
                
                if not material in faces:
                    #if  material is None:
                    #    raise ModelLoadingError("OBJ Model '{}': Undefined Material at Face {}.".format(mesh_filename, values[1:])) # assert face info in Defined Material
                    #assert material in materials_reference, "Unknow Material '{}' definition at Face {}".format(material, values[1:])
                    faces[material]=[]
                
                for triangle in triangles:
                    faces[material].append(triangle)
                
                continue
                
            elif first_word in ('usemtl','usemat'):
                material = values[1]
                if 'null' in material:
                    material='DEFAULT_MATERIAL'
                    
                continue
            elif first_word == 'mtllib':
                materials_ref_file = values[1] if (values[1].endswith('.mtl')) else values[1]+'.mtl'
    
    materials_reference = LoadMaterialsFile(materials_ref_file, folder, use_default_material=False)
    #if current_material_name is None:
    #    raise MaterialFileLoadingError("OBJ Model '{}': Empty material file.")
        
    for material in faces:
        if not material in materials_reference:
            raise ModelLoadingError("OBJ Model '{}': Material Name {} not referenced in {}.".format(mesh_filename, material, materials_ref_file) )
    
    VERTICES = []
    NORMALS  = []
    TEXCOORDS = []
    
    INDICE_REF = {}
    INDICE=0
    has_normals = True
    
    for material in faces:
        for triangle in faces[material]:
            for i, vertex_data in enumerate(triangle):
                if vertex_data in INDICE_REF:
                    triangle[i]=INDICE_REF[vertex_data]
                else:
                    a,b,c = vertex_data
                    
                    VERTICES.append(vertices[a-1]) # OBJ file index start at 1
                    if b is not -1:
                        TEXCOORDS.append(texcoords[b-1]) # OBJ file index start at 1
                    
                    if c is not -1: # OBJ file has normals
                        NORMALS.append(normals[c-1]) # OBJ file index start at 1
                    
                    INDICE_REF[vertex_data] = INDICE
                    triangle[i]= INDICE
                    
                    INDICE+=1
    
    faces_materials = {}
    
    offset = 0
    byte_offset = 0
    
    for material in faces:
        faces[material] = array = np.asarray(faces[material], 'uint16').ravel()
        faces_materials[material] = (array.shape[0], offset, byte_offset, array.dtype)
        
        offset+= array.shape[0]
        byte_offset+= array.shape[0]*array.dtype.itemsize
    
    faces_data = np.vstack([ faces[material].reshape(-1,3) for material in faces])
    
    VERTICES  = np.asarray(VERTICES, 'float32')
    
    if not NORMALS:
        NORMALS = calculateMeshNormals(faces_data, VERTICES)
    else:
        NORMALS = np.asarray(NORMALS, 'float32')
    
    if not TEXCOORDS:
        TEXCOORDS = None
    else:
        TEXCOORDS = np.asarray(TEXCOORDS, 'float32')
    
    vertex_data, data_format = Pack_VertexData(VERTICES, NORMALS, TEXCOORDS)
    
    return faces_data, faces_materials, materials_reference, vertex_data, data_format
    
"""
def Load3dsMesh(mesh_filename):
    import dom3ds
    
    DOMFILE = dom3ds.read_3ds_file(meshfilename,tight=False, recover=True)
    
    def CreateMaterial(mat):
        #  "transparency", _pctf(mat.transparency.pct, 1.0)
        return {"shininess": _pctf(mat.shininess.pct, 0.0),
                "ambient":_colorf(mat.ambient.color, 1.0, 1.0),
                "diffuse": _colorf(mat.diffuse.color, 1.0, 1.0),
                "specular": _colorf(mat.specular.color, 1.0, 1.0),
                "diffuse_texture": mat.texmap.filename.value,
                "cull_face": mat.two_side is None,
                "illumination_mode": 2}
    
    materials_reference = {}
    for mat in DOM.mdata.materials:
        materials_reference[mat.name.value]=CreateMaterial(mat)
    
    
    def CreateMesh(name, obj):
        facearray = np.array(obj.faces.array[:,:3])
        # face smoothin boolean
        #obj.faces.smoothing.array
        pointarray = obj.points.array
        tvertarray = obj.texverts.array
        print facearray.shape, facearray.dtype
        print pointarray.shape, pointarray.dtype
        print tvertarray.shape, tvertarray.dtype
        
        faces_materials = {}
        
        offset = 0
        byte_offset = 0
        
        for material in obj.faces.materials:
            array = m.array
            print material.name , (array.shape[0], offset, byte_offset, array.dtype)
            faces_materials[material.name] = (array.shape[0], offset, byte_offset, array.dtype)
            
            offset+= array.shape[0]
            byte_offset+= array.shape[0]*array.dtype.itemsize
        
        
    for i,nobj in enumerate(DOM.mdata.objects):
        obj = nobj.obj
        if type(obj) is not dom3ds.N_TRI_OBJECT:
            continue
        if obj.faces is None:
            continue
        if obj.faces.nfaces < 1:
            continue
        print 'OBJECT{}'.format(i), nobj.name
        #kfnode = kfobj.get(nobj.name)
        CreateMesh(nobj.name,obj)
        print


###########################

def _colorf(color,alpha,default):
    if color is None:
        return (default,default,default,alpha)
    
    if isinstance(color, dom3ds.COLOR_24):
        return (color.red*0.0039215, color.green*0.0039215, color.blue*0.0039215, alpha)
    
    return (color.red,color.green,color.blue,alpha)


def _pctf(pct,default):
    if pct is None:
        return default
    
    if isinstance(pct, dom3ds.INT_PERCENTAGE):
        return pct.value*0.01
    
    return pct.value
"""
