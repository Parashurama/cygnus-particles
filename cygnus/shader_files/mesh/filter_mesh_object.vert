#version 330

layout (location = 0) in vec3 Position;
layout (location = 1) in float Type;
layout (location = 2) in float Age;

out ParticleData
{
    vec3 position;
    float type;
    float age;
    
} Particle;

void main()
{
    Particle.position = Position;
    Particle.type = Type;
    Particle.age = Age;
}

