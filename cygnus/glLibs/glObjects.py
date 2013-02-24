#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from OpenGL.GL.ARB.map_buffer_range import *
from OpenGL.GL.ARB.vertex_array_object import *
from OpenGL.GL.ARB.uniform_buffer_object import *
from OpenGL.GL.ARB.texture_buffer_object import *
from OpenGL.GL.NV.transform_feedback import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.ARB.texture_float import *
from OpenGL.GL.ARB.texture_rg import *

import numpy as np
import ctypes
import ctypes as c

class BufferObject(object):
    def __init__(self, target, data, usage, size=None):
        self.__buffer__ = int(glGenBuffers(1))
        #self.__query__ = None #int(glGenQueries(1))
        
        self.isTextureBufferObject = False
        self.isUniformBufferObject = False
        self.primitive_count_query_result = None
        self.default_target = target
        self.usage = usage
  
        glBindBuffer(self.default_target, self.__buffer__)
        
        if data is None : 
            assert size is not None
            self.data_size=size
            self.data_type='float32'
            self.data_type_size=4
            self.data_byte_size= self.data_size*self.data_type_size
            
            glBufferData(self.default_target, self.data_byte_size, data, usage)
            
        else:
            glBufferData(self.default_target, data, usage)
            
            self.data_size=data.shape[0]
            self.data_type=data.dtype.name
            self.data_type_size=data.dtype.itemsize
            self.data_byte_size= self.data_size*data.dtype.itemsize
            assert self.data_type == 'float32'
        
        #if self.data_size>16 : print self.GetData(size=16)
        
        glBindBuffer(self.default_target, 0)
        
    def bind(self):
        glBindBuffer(self.default_target, self.__buffer__)
    
    def bind_asUniformBuffer(self, emplacement=0):        
        glBindBufferBase( GL_UNIFORM_BUFFER, emplacement, self.__buffer__)
        
    def bind_asTextureBuffer(self, emplacement=0):
        glBindBuffer(GL_TEXTURE_BUFFER_ARB, self.__buffer__)

        if not self.isTextureBufferObject:            
            self.__texid__ = glGenTextures(1)
            
            glBindTexture(GL_TEXTURE_BUFFER_ARB, self.__texid__);            
            glTexBufferARB(GL_TEXTURE_BUFFER_ARB, GL_RGBA32F_ARB, self.__buffer__);
            self.isTextureBufferObject=True
            
        else:
            glBindTexture(GL_TEXTURE_BUFFER_ARB, self.__texid__)
        
        glBindTexture(GL_TEXTURE_BUFFER_ARB, 0);
        glBindBuffer(GL_TEXTURE_BUFFER_ARB, 0)

    def MajorUpdate(self, data, usage, target=None):        
        if data.ndim >1:  data=data.ravel()
        glBindVertexArray(0)
        glBindBuffer(target or self.default_target, self.__buffer__)
        
        self.data_size=data.shape[0]
        self.data_type=data.dtype
        self.data_type_size=data.dtype.itemsize
        self.default_target = target or self.default_target
        assert self.data_type == 'float32'
        
        self.data_byte_size= self.data_size*self.data_type_size
        self.usage=usage
        glBufferData(self.default_target, data, usage)

    def FastUpdate(self, data, target=None, range=None):
        if data.ndim >1:  data=data.ravel()
        
        data_byte_size = data.shape[0]*data.dtype.itemsize
        
        assert self.data_type == data.dtype.name
        
        assert (0<data_byte_size<=self.data_byte_size), "Error in 'FastUpdate' function of Buffer Object: 'Invalid Data byte size' ( 0 < data_byte_size <= {0}) , was {1}".format( self.data_byte_size, data_byte_size)
        
        glBindBuffer(target or self.default_target, self.__buffer__)
        
        if range is None: ctypes_MapBufferRangeData(target or self.default_target, data, 0, data.dtype.itemsize*data.shape[0])
        else: ctypes_MapBufferRangeData(target or self.default_target, data, range[0]*data.dtype.itemsize, range[1]*data.dtype.itemsize)
    
    def C_Pointer(self, offset=0):        
        return ctypes.c_void_p(offset)
        
    def GetData(self, byte_offset=None, offset=None, byte_size=None, size=None, row=None, dtype='float32'):
        glBindBuffer(self.default_target, self.__buffer__)
        assert byte_size or size , "Must specify 'byte_size' or 'size'"
        
        if offset is not None:     byte_offset = self.data_type_size*offset
        elif byte_offset is None:  byte_offset = 0
        
        if size is not None: byte_size = size*self.data_type_size
        else:                size = byte_size/self.data_type_size
        
        NUMPY_ARRAY = np.empty(size, np.dtype(dtype))#self.data_type)
        
        ctypes_GetDataMapBufferRange(self.default_target, NUMPY_ARRAY, byte_offset, byte_size)
        
        if row is None: return NUMPY_ARRAY
        else: return NUMPY_ARRAY.reshape(-1,int(row))
    
    def delete(self):
        """
        Delete Buffer Object and any associated query object
        """
        if self.__buffer__ is not None:
            glDeleteBuffers(1,[self.__buffer__])
            self.__buffer__=None
            
        if self.__query__ is not None:
            glDeleteQueries(1, [self.__query__])
            self.__query__=None

class VertexArrayObject(object):
    def __init__(self):
        #self.__buffer__ = np.zeros(1,'uint32')
        #glGenVertexArrays(1,self.__buffer__ )
        self.__buffer__ = glGenVertexArrays(1)
    
    def bind(self):
        glBindVertexArray(self.__buffer__)
        
    def unbind(self, *args):
        glBindVertexArray(0)
        
    __enter__ = bind
    __exit__ = unbind
    
    def delete(self):
        """
        Delete VertexArray Object
        """
        if self.__buffer__ is not None:
            glDeleteVertexArrays(1,[self.__buffer__])
            self.__buffer__=None

class QueryObject(object):
    def __init__(self):
        self.__query__ = int(glGenQueries(1))
        self._primitive_count = 0
        
    def reset_query(self, query_type):
        if query_type=='primitive_count':
            self._primitive_count =None
        else:
            raise NotImplementedError()
    
    def get_primitive_count(self):
        if self._primitive_count is None:
            self._primitive_count = glGetQueryObjectuiv(self.__query__, GL_QUERY_RESULT)
        return self._primitive_count
        
    primitive_count = property(fget=get_primitive_count)
            
    def delete(self):
        if self.__query__ is not None:
            glDeleteQueries(1, [self.__query__])
            self.__query__=None

class TransformFeedbackObject(object):
    def __init__(self):
        self.buffer_object = None
        self.primitive_type = None
        self.query_object = None
    
    def __call__(self, buffer_object, primitive, emplacement=0, byte_offset=0, byte_size=None, query=False):
        self.buffer_object  = buffer_object
        self.primitive_type = primitive
        self.emplacement    = emplacement
        self.byte_offset    = byte_offset
        
        if byte_size is None:
            byte_size = buffer_object.data_byte_size-byte_offset
            
        self.byte_size  = byte_size
        self.query_object = query
        
        return self
        
    def __enter__(self):        
        #glBindBufferBaseNV(GL_TRANSFORM_FEEDBACK_BUFFER_NV, 0, self.buffer_object.__buffer__)
        
        glBindBufferRangeNV(GL_TRANSFORM_FEEDBACK_BUFFER_NV, self.emplacement, self.buffer_object.__buffer__, self.byte_offset, self.byte_size)
        
        if self.query_object is not False:
            self.query_object.reset_query('primitive_count')
            glBeginQuery(GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN_NV, self.query_object.__query__)
            
        glBeginTransformFeedbackNV(self.primitive_type)
    
    def __exit__(self, type, value, traceback):
        glEndTransformFeedbackNV()
        
        if self.query_object is not False:
            glEndQuery(GL_TRANSFORM_FEEDBACK_PRIMITIVES_WRITTEN_NV)

TransformFeedback = TransformFeedbackObject()

class FrameBufferObject(object):
    framebuffers = []
    current_framebuffer = 0
    errors = {
        GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT:'GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT',
        GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT:'GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT: no image is attached',
        GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS:'GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS: attached images dont have the same size',
        GL_FRAMEBUFFER_INCOMPLETE_FORMATS:'GL_FRAMEBUFFER_INCOMPLETE_FORMATS: the attached images dont have the same format',
        GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER:'GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER',
        GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER:'GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER',
        GL_FRAMEBUFFER_UNSUPPORTED:'GL_FRAMEBUFFER_UNSUPPORTED',
    }
    def __init__(self):
        # create the framebuffer
        self.__buffer__ = glGenFramebuffers(1)
        self.attached_textures = dict( (i,-1) for i in xrange(8))
    
    @staticmethod
    def Push():
        FrameBufferObject.framebuffers.append(FrameBufferObject.current_framebuffer)
        if not len(FrameBufferObject.framebuffers) <= 32:
            raise Exception('GL_STACK_OVERFLOW: Framebuffer stack full')
    
    @staticmethod
    def Pop():
        try:
            framebuffer = FrameBufferObject.framebuffers.pop(0)
        except IndexError:
            raise Exception('GL_STACK_UNDERFLOW: Framebuffer stack empty')
        
        FrameBufferObject._bind(framebuffer)

    @staticmethod
    def _bind(buffer):
        FrameBufferObject.current_framebuffer = buffer
        glBindFramebuffer(GL_FRAMEBUFFER, buffer)
        
    def bind(self):
        FrameBufferObject._bind(self.__buffer__)
    
    def isCurrent(self):
        return self.__buffer__ == FrameBufferObject.current_framebuffer
    
    @staticmethod
    def _check():
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        description = FrameBufferObject.errors.get(status, None)
        if description  is not None:
            print("Error on Framebuffer({})".format(description))
            raise SystemExit
                
    def check(self):
        if not self.isCurrent():
            FrameBufferObject.Push()            
            self.bind()
            FrameBufferObject._check()
            
            FrameBufferObject.Pop()
    
    def bindTexture2D(self, texture, attachment=0, viewport=False, clear=True):
        
        glFramebufferTexture2D(GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0+attachment, GL_TEXTURE_2D, texture.id, 0)
        
        if viewport is True:
            glViewport(0, 0, texture.width, texture.height)
        
        FrameBufferObject._check()
        
        if clear is True:
            glClear(GL_COLOR_BUFFER_BIT)
            
    # start rendering to this framebuffer
    def activate(self):
        
        FrameBufferObject._bind(self.__buffer__)#glBindFramebuffer(GL_FRAMEBUFFER, self.__buffer__)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        
        glPushAttrib(GL_VIEWPORT_BIT)
        
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # stop rendering to this framebuffer
    def deactivate(self, *args):
        
        FrameBufferObject._bind(0)#glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        
        glPopAttrib(GL_VIEWPORT_BIT)
    
    __enter__ = activate
    __exit__ = deactivate
    """
    def Render(self, texture_index):
        glBindTexture(GL_TEXTURE_2D, getattr(self, 'RGB_INFO_{}'.format(int(texture_index))))
            
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)     ; glVertex3f(0, 0, 0)
        glTexCoord2f(1.0,0.0)  ; glVertex3f(self.width, 0, 0)
        glTexCoord2f(1.0, 1.0) ; glVertex3f(self.width , self.height, 0)
        glTexCoord2f(0.0, 1.0) ; glVertex3f(0, self.height, 0)
        glEnd()
        
        glBindTexture(GL_TEXTURE_2D, 0)
    """


DTYPE_EQUIVALENCY = {np.dtype('float32'):GL_FLOAT,
                     np.dtype('uint8'):GL_UNSIGNED_BYTE}

FORMATS = {'RGBA'   :GL_RGBA,
           'RGB'    :GL_RGB,
           'RG'     :GL_RG,
           'R'      :GL_RED}

INTERNAL_FORMATS = {'R8'      :GL_R8,
                    'R32F'   :GL_R32F,
                    'RG8'     :GL_RG8,
                    'RG32F'  :GL_RG32F,
                    'RGB8'    :GL_RGB8,
                    'RGB32F' :GL_RGB32F_ARB,
                    'RGBA8'   :GL_RGBA8,
                    'RGBA32F':GL_RGBA32F_ARB}

class TextureObject(object):
    def __init__(self, data, size, format='RGBA', internalformat='RGBA', mipmap=True, nearest=False, anisotropic=False, repeat_texture=True):
        assert format in internalformat
        
        self.id = glGenTextures(1)
        
        ndim = len(size)
        dtype = data.dtype
        self.data_type = DTYPE_EQUIVALENCY[dtype]
        self.format = FORMATS[format]
        self.internal_format = INTERNAL_FORMATS[internalformat]
        self.ndim = ndim
        
        if   ndim == 3:
            self.target = GL_TEXTURE_3D
            self.width,self.height,self.depth =  size
            
        elif ndim == 2:
            self.target = GL_TEXTURE_2D
            self.width,self.height=  size
            
        elif ndim == 1:
            self.target = GL_TEXTURE_1D
            self.width= float(size)
            
        else:
            raise TypeError('Invalid number of dimensions in TextureObject : {}'.format(ndim))
        
        
        glBindTexture(self.target, self.id)
        
        if   ndim == 3:
            glTexImage3D(GL_TEXTURE_3D, 0, self.internal_format, self.width,self.height,self.depth, 0, self.format, self.data_type, data)
            
        elif   ndim == 2:
            glTexImage2D(GL_TEXTURE_2D, 0, self.internal_format, self.width,self.height, 0, self.format, self.data_type, data)
            
        elif   ndim == 1:
            glTexImage2D(GL_TEXTURE_2D, 0, self.internal_format, self.width, 0, self.format, self.data_type, data)

        
        if repeat_texture is True:
            glTexParameteri(self.target, GL_TEXTURE_WRAP_S,  GL_REPEAT);
            if ndim > 1:
                glTexParameteri(self.target, GL_TEXTURE_WRAP_T,  GL_REPEAT);
            if ndim > 2:
                glTexParameteri(self.target, GL_TEXTURE_WRAP_R,  GL_REPEAT);
        else:
            glTexParameteri(self.target, GL_TEXTURE_WRAP_S,  GL_CLAMP_TO_EDGE);
            if ndim > 1:
                glTexParameteri(self.target, GL_TEXTURE_WRAP_T,  GL_CLAMP_TO_EDGE);
            if ndim > 2:
                glTexParameteri(self.target, GL_TEXTURE_WRAP_R,  GL_CLAMP_TO_EDGE);
                
        if nearest is True: glTexParameteri(self.target,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        else:               glTexParameteri(self.target,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        
        if   mipmap:
            glTexParameteri(self.target,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
            glGenerateMipmap(self.target)
            
        elif nearest: glTexParameteri(self.target,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
        else:         glTexParameteri(self.target,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        
        if anisotropic: glTexParameterf(self.target, GL_TEXTURE_MAX_ANISOTROPY_EXT, 4.0)
        
        glBindTexture(self.target, 0)
    
    def bind(self, emplacement=0):
        
        glActiveTexture(GL_TEXTURE0+emplacement)
        glBindTexture(self.target, self.id)
        glActiveTexture(GL_TEXTURE0)
        
    def resize(self, size):
        
        ndim = len(size)
        
        assert  (ndim == self.ndim), 'Invalid dimension resize'
        
        glBindTexture(self.target, self.id)
        
        if   ndim == 3:
            self.width,self.height,self.depth =  size
            glTexImage3D(self.target, 0, GL_RGBA, self.width, self.height, self.depth, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
            
        elif ndim == 2:
            self.width,self.height = size
            glTexImage2D(self.target, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
            
        elif ndim == 1:
            self.width = float(size)
            glTexImage1D(self.target, 0, GL_RGBA, self.width, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        else:
            raise TypeError('Invalid number of dimensions in TextureObject : {}'.format(ndim))
        
        glBindTexture(self.target, 0)
        
        
    def delete(self):        
        glDeleteTextures(1, [self.id])


def ctypes_MapBufferRangeData(target, numpy_data, start_offset, end_offset):
    
    ptr = glMapBufferRange( target, start_offset, end_offset, GL_MAP_WRITE_BIT | GL_MAP_INVALIDATE_BUFFER_BIT )
    ctypes.memmove(ptr, numpy_data.ctypes.data, end_offset-start_offset)
    
    glUnmapBuffer( target )

def ctypes_GetDataMapBufferRange(target, numpy_destination, start_offset, end_offset):
    ptr = glMapBufferRange( target, start_offset, end_offset, GL_MAP_READ_BIT )
    ctypes.memmove(numpy_destination.ctypes.data, ptr, end_offset-start_offset)
    
    glUnmapBuffer( target )
