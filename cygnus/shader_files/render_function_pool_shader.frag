#version 330
#extension GL_EXT_gpu_shader4 : enable

in vec3 color;

void main()
{
    
    gl_FragColor = vec4(color.rgb,1.0);

} 
