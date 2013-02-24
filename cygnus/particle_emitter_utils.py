#! /usr/bin/env python
# *-* coding: UTF-8 *-*

def dummy(*args):pass

def Unpack(*args):
    LIST=[]
    for arg in args:
        try:
            LIST+=list(arg)
        except TypeError:
            LIST.append(arg)
    return LIST

def FillUniformBuffer(UNIFORMS_DATA, BUFFER, OffsetInfo):

    F_BUFFER = BUFFER
    I_BUFFER = BUFFER.view(dtype='int32')
    DTYPE_SIZE=4
    
    for uniform, offset in OffsetInfo:
        dtype, uniform_data = UNIFORMS_DATA[uniform]
        if dtype == 'float': buffer = F_BUFFER
        else               : buffer = I_BUFFER
        for i, d in enumerate(uniform_data):
            buffer[offset/DTYPE_SIZE+i] = d

def UpdateUniformBuffer(UNIFORMS_DATA, UNIFORM_LIST_TO_UPDATE, BUFFER, OffsetInfo):

    F_BUFFER = BUFFER
    I_BUFFER = BUFFER.view(dtype='int32')
    DTYPE_SIZE=4
            
        
    for uniform, offset in OffsetInfo:
        if not uniform in UNIFORM_LIST_TO_UPDATE: continue
        
        dtype, uniform_data = UNIFORMS_DATA[uniform]
        if dtype == 'float': buffer = F_BUFFER
        else               : buffer = I_BUFFER
        for i, d in enumerate(uniform_data):
            buffer[offset/DTYPE_SIZE+i] = d
