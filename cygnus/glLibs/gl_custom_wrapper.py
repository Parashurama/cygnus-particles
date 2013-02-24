
import ctypes
from OpenGL import platform, constants, constant, arrays

_DEPRECATED = False

c_GLintptr = ctypes.POINTER(ctypes.c_int)

wrapper_glTransformFeedbackVaryings = platform.createExtensionFunction( 
'glTransformFeedbackVaryingsNV',dll=platform.GL,
extension='GL_NV_transform_feedback',
resultType=None, 
argTypes=(constants.GLuint,constants.GLsizei, c_GLintptr,constants.GLenum,),
doc='glTransformFeedbackVaryingsNV(GLuint(program), GLsizei(count), GLintptr(locations), GLenum(bufferMode)) -> None',
argNames=('program','count','locations','bufferMode',),
deprecated=_DEPRECATED,
)

