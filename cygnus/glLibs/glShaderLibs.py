from OpenGL.GL import *
from OpenGL.GL.shaders import *
#from OpenGL.GL.ARB.shader_objects import *
#from OpenGL.GL.ARB.vertex_shader import *
#from OpenGL.GL.ARB.fragment_shader import *
from OpenGL.GL.ARB.uniform_buffer_object import *
from OpenGL.GL.ARB.geometry_shader4 import *
from OpenGL.GL.NV.transform_feedback import *
import numpy as np
import ctypes as c
import os
from gl_custom_wrapper import wrapper_glTransformFeedbackVaryings

ShaderType={GL_VERTEX_SHADER:"GL_VERTEX_SHADER",GL_FRAGMENT_SHADER:"GL_FRAGMENT_SHADER",GL_GEOMETRY_SHADER:'GL_GEOMETRY_SHADER' }

TransformFeedbackType = { 'Interleaved':GL_INTERLEAVED_ATTRIBS_NV, GL_INTERLEAVED_ATTRIBS_NV:GL_INTERLEAVED_ATTRIBS_NV, 'Separate':GL_SEPARATE_ATTRIBS_NV, GL_SEPARATE_ATTRIBS_NV:GL_SEPARATE_ATTRIBS_NV}


def CompileShader(code=None, shader_type=None, geom_param=None ):
    
    if not code:
        raise ValueError("Shader Code Invalide")
    
    try:
            
        if shader_type not in [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_GEOMETRY_SHADER]:
            raise ValueError("Type de Shader Inconnu. ( GL_VERTEX_SHADER, GL_FRAGMENT_SHADER ou GL_GEOMETRY_SHADER uniquement) ")
            
        elif shader_type == GL_VERTEX_SHADER:   shader = glCreateShader(GL_VERTEX_SHADER)
        elif shader_type == GL_FRAGMENT_SHADER: shader = glCreateShader(GL_FRAGMENT_SHADER)
        elif shader_type == GL_GEOMETRY_SHADER: shader = glCreateShader(GL_GEOMETRY_SHADER_ARB)
        
        glShaderSource(shader, code)
        
        glCompileShader(shader)
    
    except (OpenGL.error.GLError):pass
    
    shader_status_ok=glGetShaderiv(shader, GL_COMPILE_STATUS)
    if shader_status_ok:
        return shader
    print glGetShaderInfoLog( shader )

    raise ValueError("Erreur de Compilation sur le Shader "+ShaderType[shader_type]+"\n"+code )
    
def CompileProgram(name, vertexShader, fragmentShader, geomShader=None, geom_param=None):
    
    try:
        program = glCreateProgram()
        
        if vertexShader: glAttachShader(program, vertexShader)    
        if fragmentShader: glAttachShader(program, fragmentShader)
        if geomShader: glAttachShader(program, geomShader)
        
        glValidateProgram(program)        
        glLinkProgram(program)
        
        
        if vertexShader: glDeleteShader(vertexShader)
        if fragmentShader: glDeleteShader(fragmentShader)
        if geomShader: glDeleteShader(geomShader)
    
    except (OpenGL.error.GLError):pass
        
    validate_status_ok=glGetProgramiv(program, GL_VALIDATE_STATUS)
    link_status_ok=glGetProgramiv(program, GL_LINK_STATUS)
    
    if validate_status_ok and link_status_ok:
        #print "~~~~~~~~~~~~~~~~\nShader '%s' Compiled\n~~~~~~~~~~~~~~~~" % (str(name))
        return program
    
    
    print glGetProgramInfoLog( program )
    
    raise ValueError("Erreur sur sur le Programme '%s' Validate Status: %s, Link Stats: %s" % (name, bool(validate_status_ok), bool(link_status_ok) ) )

def RelinkProgram(program):
    try:
        glLinkProgram(program)
    except (OpenGL.error.GLError):pass
        
    validate_status_ok=glGetProgramiv(program, GL_VALIDATE_STATUS)
    link_status_ok=glGetProgramiv(program, GL_LINK_STATUS)
    
    if validate_status_ok and link_status_ok:
        #print "~~~~~~~~~~~~~~~~\nShader '%s' Compiled\n~~~~~~~~~~~~~~~~" % (str(name))
        return program
    
    
    print glGetProgramInfoLog( program )
    
    raise ValueError("Erreur sur sur le Programme '%s' Validate Status: %s, Link Stats: %s" % (name, bool(validate_status_ok), bool(link_status_ok) ) )


class BasicShaderObject(object):
    def __init__(self, name, directory, vertex_file=None, fragment_file=None, geometry_file=None, vlibs='', flibs='', transform_param=None):
        
        if vertex_file:
            vertex_shader_code=open(os.path.join(directory,vertex_file)).read()
            VERTEX_SHADER = CompileShader( vlibs + vertex_shader_code, GL_VERTEX_SHADER)
        else: VERTEX_SHADER=None
        
        if fragment_file:
            fragment_shader_code=open(os.path.join(directory,fragment_file)).read()
            FRAGMENT_SHADER = CompileShader( flibs + fragment_shader_code, GL_FRAGMENT_SHADER)
        else: FRAGMENT_SHADER=None
        
        if geometry_file:
            geometry_shader_code=open(os.path.join(directory,geometry_file)).read()
            GEOMETRY_SHADER = CompileShader( '' + geometry_shader_code, GL_GEOMETRY_SHADER)
        else: GEOMETRY_SHADER=None
        
        self.program=CompileProgram(name, VERTEX_SHADER, FRAGMENT_SHADER , GEOMETRY_SHADER)
        
        self.name=name
        self.__initialized__=False
        self.UniformToUpdate=True
        self.UniformBlocks={}
        self.UniformBlocksInfo={}
        
        self.Uniforms={}
        self.Attributes={}
        
    def SetupAttributesAndUniforms(self, uniform_name_list, attribute_name_list, off_shader=True):
        glUseProgram(self.program)

        for uniform in uniform_name_list:
            location = glGetUniformLocation( self.program, uniform )
            if location in (None,-1):
                print 'Warning, no uniform: {0} in Shader {1}'.format( uniform, self.name )
            self.Uniforms[uniform] = location    
        
        for attribute in attribute_name_list:        
            location = glGetAttribLocation( self.program, attribute )
            if location in (None,-1):
                print 'Warning, no attribute:  {0} in Shader {1}'.format( attribute, self.name )
            self.Attributes[attribute]=location
        
        if off_shader is True:
            glUseProgram(0)
        
    def SetupUniformBufferInfo(self, uniformBlockName, uniformNameList):
        assert (uniformBlockName not in self.UniformBlocks)
        
        uniformIndices  = ctypes_glGetUniformIndices(self.program, uniformNameList, debug=self)    
        uniformOffset = ctypes_glGetActiveUniformsiv(self.program, uniformIndices, GL_UNIFORM_OFFSET, uniformNameList, debug=self)    
        
        uniformBlockIndex = ctypes_glGetUniformBlockIndex (self.program, uniformBlockName, debug=self)
        
        uniformBlockSize  = ctypes_glGetActiveUniformBlockiv (self.program, uniformBlockIndex, GL_UNIFORM_BLOCK_DATA_SIZE)
        
        uniformOffsetInfo = [ (l,o) for l,o in zip(uniformNameList,uniformOffset) ]
        
        glUniformBlockBinding(self.program, uniformBlockIndex, len(self.UniformBlocks) )
        
        
        self.UniformBlocks[uniformBlockName]=len(self.UniformBlocks)        
        self.UniformBlocksInfo[uniformBlockName] = (uniformOffsetInfo, uniformBlockSize)
        
    def GetUniformBuffer(self, uniformBlockName):
        
        assert (uniformBlockName in self.UniformBlocksInfo)
        
        uniformOffsetInfo, uniformBlockSize = self.UniformBlocksInfo[uniformBlockName]
        
        uniform_buffer_data = np.zeros(uniformBlockSize/4, 'float32')
        
        return uniform_buffer_data, uniformOffsetInfo
    
    def SetTransformFeedbackAttributes(self, varyings_name, bufferMode):
        glUseProgram(0) # Need to disable eventual 'in-use' Shaders
        
        for attrib in varyings_name:
            glActiveVaryingNV(self.program, attrib)
        
        RelinkProgram(self.program)
        self.InitShaderParams()

        ctypes_glTransformFeedbackVaryings( self.program, varyings_name, TransformFeedbackType[bufferMode])

    def Set(self, *args, **kwargs):
        glUseProgram(self.program)
        
        if not self.__initialized__: 
            self.set_uniforms(self)
            self.__initialized__=True

        self.set_params(self, *args, **kwargs)
        
    def InitShaderParams(self,*args):
        self.init_params(self,*args)

class BasicShaderObjectFromtext(BasicShaderObject):
    def __init__(self, name, vertex_code=None, fragment_code=None, geometry_code=None, vlibs='', flibs='', transform_param=None):
        
        if vertex_code:
            VERTEX_SHADER = CompileShader( vlibs + vertex_code, GL_VERTEX_SHADER)
        else: VERTEX_SHADER=None
        
        if fragment_code:
            FRAGMENT_SHADER = CompileShader( flibs + fragment_code, GL_FRAGMENT_SHADER)
        else: FRAGMENT_SHADER=None
        
        if geometry_code:
            GEOMETRY_SHADER = CompileShader( '' + geometry_code, GL_GEOMETRY_SHADER)
        else: GEOMETRY_SHADER=None
        
        self.program=CompileProgram(name, VERTEX_SHADER, FRAGMENT_SHADER , GEOMETRY_SHADER)

        self.name=name
        self.__initialized__=False
        self.UniformToUpdate=True
        self.UniformBlocks={}
        self.UniformBlocksInfo={}


#####################################################################
################ TransformFeedback Setup Functions ##################
#####################################################################


def ctypes_glTransformFeedbackVaryings( program, varyings_name, bufferMode, debug=False):
    
    varyings_location=np.array([ glGetVaryingLocationNV(program, attrib) for attrib in varyings_name ], 'int32')        
    
    if debug is not False:
        for n, l, in zip(varyings_name, varyings_location):
            if l == -1: print "No Transform FeedBack Varying Attribute named '{}' in Shader '{}'".format(n, debug.name)
        
    wrapper_glTransformFeedbackVaryings(program, varyings_location.shape[0], varyings_location.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), bufferMode)


#####################################################################
################### Uniform Buffer Setup Functions ##################
#####################################################################

def ctypes_glGetUniformIndices(program, uniformNames, debug=False):
    
    uniformCount = len(uniformNames)
    
    c_uniformNames = (c.POINTER(c.c_char) *uniformCount )()

    for i,name in enumerate(uniformNames):
        buff = c.create_string_buffer(name)
        c_uniformNames[i] = c.cast(c.pointer(buff), c.POINTER(c.c_char))
        
    uniformIndices = (ctypes.c_int32 * uniformCount)()
    
    glGetUniformIndices (program, uniformCount, c_uniformNames,  ctypes.byref(uniformIndices))
    
    if debug is not False:
        for l, o in [ (l,o) for l,o in zip(uniformNames,uniformIndices) ]:
            if o ==-1: print "No uniform named '{}' in UniformBlock in Shader '{}'".format(l, debug.name)
    
    return uniformIndices

def ctypes_glGetActiveUniformsiv(program, uniformIndices, pname, uniformNames, debug=False):
    uniformCount = len(uniformIndices)
    uniformOffsets = (ctypes.c_int32 * uniformCount)()
    
    glGetActiveUniformsiv (program, uniformCount, uniformIndices, pname, ctypes.byref(uniformOffsets))
    
    if debug is not False:
        for l, o in [ (l,o) for l,o in zip(uniformNames,uniformOffsets) ]:                                       # shader_name
            if o ==-1: print "No Uniform Offset for uniform named '{}' in UniformBlock in Shader '{}'".format(l, debug.name)
        
    return uniformOffsets
    
def ctypes_glGetUniformBlockIndex (program, uniformBlockName, debug=False):
    c_uniformBlockName = c.create_string_buffer(uniformBlockName)
    c_uniformBlockName = c.cast(c.pointer(c_uniformBlockName), c.POINTER(c.c_char))
    
    retvalue =  glGetUniformBlockIndex(program, c_uniformBlockName)
    
    if debug is not False and retvalue in ( -1, 4294967295L):
        raise ValueError("Invalid Uniform Block Name: {} in shader '{}'".format(uniformBlockName, debug.name) )
    
    return retvalue
                                                                #GL_UNIFORM_BLOCK_DATA_SIZE
def ctypes_glGetActiveUniformBlockiv (program, uniformBlockIndex, pname):
    
    uniformBlockSize  = (ctypes.c_int32 * 1)()
    glGetActiveUniformBlockiv( program, uniformBlockIndex, pname, ctypes.byref(uniformBlockSize) )

    return uniformBlockSize[0]

