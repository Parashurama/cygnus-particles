#! /usr/bin/env python
# *-* coding: UTF-8 *-*

from OpenGL.GL import *
from __globals__ import cVars

from glLibs.glShaderLibs import BasicShaderObject

from particle_emitter_vars import EMITTER_UNIFORMS_LIST, UPDATER_UNIFORMS_LIST, EMITTER_SECONDARY_UNIFORMS_LIST, MESH_EMITTER_UNIFORMS_LIST

def SetupSimplePointRenderShader(ShaderObject, *args):
        
        UNIFORM_LIST= [ 'ModelViewProjection', 'ModelView','animation_fps',
                        'nFrames', 'ColorBlendTexture',
                        'ColorBlendLifeTime', 'COLOR_BLENDING',
                        'GROWTH_FACTOR', 'PARTICLE_SIZE',#'PARTICLE_TYPE_TO_RENDER',
                        'TEXTURE_TYPE', 'PARTICLE_FEATHER_RADIUS',
                        'DEFAULT_PARTICLE_COLOR', 'SimpleTexture0',
                        'AnimatedTexture0']
        
        ATTRIBUTE_LIST= ( 'Position','Age')#'Type',
        
        ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ATTRIBUTE_LIST, False)

        glUniform1i(ShaderObject.Uniforms['ColorBlendTexture'], 0)
        glUniform1i(ShaderObject.Uniforms['SimpleTexture0'], 0)
        glUniform1i(ShaderObject.Uniforms['AnimatedTexture0'], 0)
        
        glUseProgram(0)

def SetupEmitterShader(ShaderObject, *args):
    UNIFORM_LIST= [ 'seed',
                    'RandomTexture',
                    'ParticleSystemcount']
    
    ATTRIBUTE_LIST= ('Type',)
            
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ATTRIBUTE_LIST, False)

    glUniform1i(ShaderObject.Uniforms['RandomTexture'], 0)

    glUseProgram(0)

def SetupMeshEmitterShader(ShaderObject, *args):
    UNIFORM_LIST= [ 'seed','MeshVertexCount','ModelScale',
                    'RandomTexture', 'MeshTriangleVertices',
                    'MESH_DATA_STRUCT_SIZE', 'MESH_DATA_STRUCT_POSITION_OFFSET',
                    'ParticleSystemcount']
    
    ATTRIBUTE_LIST= ('Type',)
    
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ATTRIBUTE_LIST, False)

    glUniform1i(ShaderObject.Uniforms['RandomTexture'], 0)
    glUniform1i(ShaderObject.Uniforms['MeshTriangleVertices'], 1)

    glUseProgram(0)

def SetupUpdateShader(ShaderObject, *args):
    UNIFORM_LIST= [ 'VISCOUS_DRAG', 'GRAVITY','dtime']
    
    ATTRIBUTE_LIST= ( 'Position','Velocity','Type','Age')
            
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ATTRIBUTE_LIST, False)

    glUseProgram(0)

def SetupPerParticleEmitterShader(ShaderObject, *args):
    UNIFORM_LIST= [ 'seed',
                    'RandomTexture',
                    'ParticleSystemcount']
    
    ATTRIBUTE_LIST= ('Position',)
            
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ATTRIBUTE_LIST, False)

    glUniform1i(ShaderObject.Uniforms['RandomTexture'], 0)

    glUseProgram(0)

def SetupSimplePoolRenderShader(ShaderObject, *args):
    ShaderObject.SetupAttributesAndUniforms(['ModelViewProjection','ModelView'], ( 'Position',), True)


def SetupMeshRenderShader(ShaderObject, *args):
    UNIFORM_LIST = ['ModelView',
                    'ModelViewProjection',
                    'Diffuse_Texture0',
                    'DEFAULT_PARTICLE_COLOR',
                    'ColorBlendTexture',
                    'ColorBlendLifeTime',
                    'COLOR_BLENDING',
                    'GROWTH_FACTOR',
                    'PARTICLE_SIZE',
                    'hasDiffuseTexture']
    
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ( 'Vertex_Position','Vertex_TexCoords', 'Instance_Position', 'Instance_Age'), False)
    
    glUniform1i(ShaderObject.Uniforms['Diffuse_Texture0'], 0)
    glUseProgram(0)

def SetupSingleMeshRenderShader(ShaderObject, *args):
    UNIFORM_LIST = ['ModelView',
                    'ModelViewProjection',
                    'Diffuse_Texture0',
                    'hasDiffuseTexture']
    
    ShaderObject.SetupAttributesAndUniforms(UNIFORM_LIST, ( 'Vertex_Position','Vertex_TexCoords'), False)
    
    glUniform1i(ShaderObject.Uniforms['Diffuse_Texture0'], 0)
    glUseProgram(0)

def BuildShaders():
    import os, cygnus
    __dir__ = os.path.join(cygnus.__path__[0],'shader_files/')
    
    cVars.SimplePointRenderShader = BasicShaderObject('SimplePointRenderShader', directory=__dir__, fragment_file='simple_point_render_function.frag', vertex_file='simple_point_render_function.vert')       
    
    cVars.SimplePointRenderShader.init_params = SetupSimplePointRenderShader
    cVars.SimplePointRenderShader.set_uniforms=dummy
    cVars.SimplePointRenderShader.set_params=dummy
    
    cVars.SimplePointRenderShader.InitShaderParams()
    
    
    
    cVars.EmitterShader = BasicShaderObject('EmitterShader', directory=__dir__, vertex_file='emit_function_shader.vert')       
    cVars.EmitterShader.SetupUniformBufferInfo("EMITTER_UNIFORMS", EMITTER_UNIFORMS_LIST )
    
    cVars.EmitterShader.init_params = SetupEmitterShader
    cVars.EmitterShader.set_uniforms=dummy
    cVars.EmitterShader.set_params=dummy
    cVars.EmitterShader.SetTransformFeedbackAttributes(["Position_out", "Velocity_out", "Type_out", "Age_out"], 'Interleaved') # GL_SEPARATE_ATTRIBS_NV,
    
    
    cVars.MeshEmitterShader = BasicShaderObject('MeshEmitterShader', directory=__dir__, vertex_file='emit_mesh_function_shader.vert')       
    cVars.MeshEmitterShader.SetupUniformBufferInfo("EMITTER_UNIFORMS", MESH_EMITTER_UNIFORMS_LIST )
    
    cVars.MeshEmitterShader.init_params = SetupMeshEmitterShader
    cVars.MeshEmitterShader.set_uniforms=dummy
    cVars.MeshEmitterShader.set_params=dummy
    cVars.MeshEmitterShader.SetTransformFeedbackAttributes(["Position_out", "Velocity_out", "Type_out", "Age_out"], 'Interleaved') # GL_SEPARATE_ATTRIBS_NV,
    
    
    cVars.PerParticleEmitterShader = BasicShaderObject('PerParticleEmitterShader', directory=__dir__, vertex_file='emit_secondary_function_shader.vert')       
    cVars.PerParticleEmitterShader.SetupUniformBufferInfo("PER_PARTICLE_EMITTER_UNIFORMS", EMITTER_SECONDARY_UNIFORMS_LIST )
    
    cVars.PerParticleEmitterShader.init_params = SetupPerParticleEmitterShader
    cVars.PerParticleEmitterShader.set_uniforms=dummy
    cVars.PerParticleEmitterShader.set_params=dummy
    cVars.PerParticleEmitterShader.SetTransformFeedbackAttributes(["Position_out", "Velocity_out", "Type_out", "Age_out"], 'Interleaved') # GL_SEPARATE_ATTRIBS_NV,
    
    
    cVars.UpdateShader = BasicShaderObject('UpdaterShader', directory=__dir__, vertex_file='update_function_shader.vert', geometry_file='update_function_shader.glsl' )       
    cVars.UpdateShader.SetupUniformBufferInfo("UPDATER_UNIFORMS", UPDATER_UNIFORMS_LIST )
    
    cVars.UpdateShader.init_params = SetupUpdateShader
    cVars.UpdateShader.set_uniforms=dummy
    cVars.UpdateShader.set_params=dummy
    cVars.UpdateShader.SetTransformFeedbackAttributes(["Position_out", "Velocity_out", "Type_out", "Age_out"], 'Interleaved') # GL_SEPARATE_ATTRIBS_NV,
    
    cVars.SimplePoolRenderShader = BasicShaderObject('PoolSimpleRenderShader', directory=__dir__, vertex_file='render_function_pool_shader.vert', fragment_file='render_function_pool_shader.frag' )       
    
    cVars.SimplePoolRenderShader.init_params = SetupSimplePoolRenderShader
    cVars.SimplePoolRenderShader.set_uniforms=dummy
    cVars.SimplePoolRenderShader.set_params=dummy
    cVars.SimplePoolRenderShader.InitShaderParams()
    
    
    cVars.MeshRenderShader = BasicShaderObject('MeshRenderShader', directory=__dir__, vertex_file='render_mesh_object.vert', fragment_file='render_mesh_object.frag' )       
    
    cVars.MeshRenderShader.init_params = SetupMeshRenderShader
    cVars.MeshRenderShader.set_uniforms=dummy
    cVars.MeshRenderShader.set_params=dummy
    cVars.MeshRenderShader.InitShaderParams()
    
    
    cVars.SingleMeshRenderShader = BasicShaderObject('SingleMeshRenderShader', directory=__dir__, vertex_file='render_single_mesh_object.vert', fragment_file='render_single_mesh_object.frag' )       
    
    cVars.SingleMeshRenderShader.init_params = SetupSingleMeshRenderShader
    cVars.SingleMeshRenderShader.set_uniforms=dummy
    cVars.SingleMeshRenderShader.set_params=dummy
    cVars.SingleMeshRenderShader.InitShaderParams()
    
def dummy(*args):pass

