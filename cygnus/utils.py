#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
import numpy as np

class ColorBlendTexture(object):
    def __init__(self, color_data, precision=0.1):
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, self.id)
        
        pColorData = ComputeColorInterpolation(color_data, precision)
        
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, pColorData.shape[0], 0, GL_RGBA, GL_FLOAT, pColorData);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP);
        
        glBindTexture(GL_TEXTURE_1D, 0)


def ComputeColorInterpolation(color_data, precision):
    ARRAY=None
    
    for i,(t, color) in enumerate(color_data):
        
        color = np.array(color, 'float32')
        if i ==0: prev_t=t ; prev_color = color ; continue

        VAL = np.linspace(0, 1.0, int((t-prev_t)/precision)).reshape(-1,1)
        ARR = prev_color + VAL *(color -prev_color)
        
        if ARRAY is None:
            ARRAY=ARR
        else:
            ARRAY = np.vstack((ARRAY, ARR))        
        
        prev_t=t ; prev_color = color
    
    return ARRAY

class RandomTexture(object):
    def __init__(self, size):
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, self.id)
        
        pRandomData = np.random.random(size*4).astype('float32')
        
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, size, 0, GL_RGBA, GL_FLOAT, pRandomData);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        
        glBindTexture(GL_TEXTURE_1D, 0)

DATA_FORMAT_REFERENCE = {'v':'position', 'n':'normal', 't':'texcoord'}
DATA_TYPE_REFERENCE = {'f':'float', 'i':'int'}

def ParseBufferData_format(data_format):
    struct_size = 0
    DATA_INFO = {}
    
    for data_struct in data_format:
        
        data = DATA_FORMAT_REFERENCE[data_struct[0]]
        size = int(data_struct[1])
        data_type = DATA_TYPE_REFERENCE[data_struct[2]]
        
        DATA_INFO['struct_'+data+'_offset'] = struct_size
        struct_size+= size
    
    DATA_INFO['struct_size'] = struct_size
    
    return DATA_INFO
    
    
#class Transform(object):
#    def __init__(self, size):
