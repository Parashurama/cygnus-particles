#version 330

layout (location = 0) in vec3 Position;
//layout (location = 1) in vec3 Velocity;
//layout (location = 2) in float Type;
//layout (location = 3) in float Age;


#define MAIN_PARTICLE_EMITTER 0.0f
#define PARTICLE_TYPE_1 10.0f
#define PER_PARTICLE_EMITTER 20.0f

uniform vec2 seed;
uniform sampler1D RandomTexture;
uniform float ParticleSystemcount;


uniform PER_PARTICLE_EMITTER_UNIFORMS
{
    float PER_PARTICLE_EMITTER_PARTICLE_FIRERATE;
    vec3 PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION;
    vec3 PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION;
    float PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION;
    //float PER_PARTICLE_EMITTER_MIN_AGE_EMISSION;
    
    vec3 PER_PARTICLE_EMITTER_PARTICLE_VELOCITY;
    float PER_PARTICLE_EMITTER_PARTICLE_AGE;
    
};

/////////////////////////////////
out vec3 Position_out;
out vec3 Velocity_out;
out float Type_out;
out float Age_out;
/////////////////////////////////
//////////////////////////////////////////////////////////////////

vec4 GetRandomDir(float TexCoord)
{
    vec4 Dir = texture(RandomTexture, TexCoord);
    Dir -= vec4(0.5);
    return 2*Dir;
} 
//////////////////////////////////////////////////////////////////


void main()
{
    vec2 rn_value;
    vec4 rndfloats0;
    vec4 rndfloats1;
    
    rn_value = seed + 1.0/(seed*(0.5+seed)) +  gl_VertexID/ParticleSystemcount; 
    
    rndfloats0 = GetRandomDir(rn_value.x);
    rndfloats1 = GetRandomDir(rn_value.y);
    
    Position_out = Position + PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION * rndfloats0.xyz;
    Velocity_out = PER_PARTICLE_EMITTER_PARTICLE_VELOCITY + PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION * rndfloats1.zwx;
    Age_out      = PER_PARTICLE_EMITTER_PARTICLE_AGE + PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION*rndfloats0.w;
    Type_out     = PARTICLE_TYPE_1;
    
}

    /*
    if (Age > PER_PARTICLE_EMITTER_MIN_AGE_EMISSION)
    {
        rn_value = seed + 1.0/(seed*(0.5+seed)) +  gl_VertexID/ParticleSystemcount+Type*0.1; 
        
        rndfloats0 = GetRandomDir(rn_value.x);
        rndfloats1 = GetRandomDir(rn_value.y);

        Position_out = Pos + PER_PARTICLE_EMITTER_PARTICLE_POSITION_DEVIATION * rndfloats0.xyz;
        Velocity_out = PER_PARTICLE_EMITTER_PARTICLE_VELOCITY + PER_PARTICLE_EMITTER_PARTICLE_VELOCITY_DEVIATION * rndfloats1.zwx;
        Age_out      = PER_PARTICLE_EMITTER_PARTICLE_AGE + PER_PARTICLE_EMITTER_PARTICLE_AGE_DEVIATION*rndfloats0.w;
        Type_out     = PARTICLE_TYPE_1; 
    }*/
