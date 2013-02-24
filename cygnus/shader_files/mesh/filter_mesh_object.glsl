#version 330
#extension GL_EXT_gpu_shader4 : enable

layout(points) in;
layout(points) out;
layout(max_vertices = 1) out;


/////////////////////////////////
in ParticleData
{
    vec3 position;
    float type;
    float age;
} Particle[];

out vec3 Position_out;
out float Age_out;

uniform float PARTICLE_TYPE_TO_RENDER;

void main()
{   
    gl_Position = vec4(1.0); // HACK
    
    if (Particle[0].type == PARTICLE_TYPE_TO_RENDER)
    {   
        Position_out= Particle[0].position;
        Age_out= Particle[0].type;
        
        EmitVertex();
        EndPrimitive();
    }
}
