#version 330

layout (location = 0) in vec3 Position;
layout (location = 1) in vec3 Velocity;
layout (location = 2) in float Type;
layout (location = 3) in float Age;

out ParticleData
{
    vec3 position;
    vec3 velocity;
    float type;
    float age;
    
} Particle;

void main()
{
    Particle.position = Position;
    Particle.velocity = Velocity;
    Particle.type = Type;
    Particle.age = Age;
}
