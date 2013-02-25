#version 330

layout (location = 0) in float Type;


#define PI 3.14159265f
#define PI2 6.2831853f


uniform vec2 seed;
uniform sampler1D RandomTexture;
uniform float ParticleSystemcount;

//uniform usamplerBuffer MeshTriangleIndice;
uniform samplerBuffer MeshTriangleVertices;
uniform int vertex_count;
uniform float ModelScale;

uniform EMITTER_UNIFORMS
{
    int EMITTER_TYPE;
    float EMITTER_PARTICLE_FIRERATE;
    vec3 EMITTER_PARTICLE_POSITION;
    vec3 EMITTER_PARTICLE_VELOCITY;
    vec3 EMITTER_PARTICLE_POSITION_DEVIATION;
    vec3 EMITTER_PARTICLE_VELOCITY_DEVIATION;
    float EMITTER_PARTICLE_AGE_DEVIATION;
    
    
    float PARTICLE_TYPE_TO_EMIT;
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
    vec2 rn_value = seed + 1.0/(seed*(0.5+seed)) +  gl_VertexID/ParticleSystemcount+Type*0.1; 
    
    vec4 rndfloats0 = GetRandomDir(rn_value.x);
    vec4 rndfloats1 = GetRandomDir(rn_value.y);
    vec4 rndhalffloats0 = rndfloats0*0.5 +0.5 ;
    vec4 rndhalffloats1 = rndfloats1*0.5 +0.5 ;
    
    //uvec3 indices = texelFetch(MeshTriangleIndice, int(MeshSize*rndhalffloats0.x));
    
    // if using texture buffer internal format R32F
    int INDEX = int(vertex_count*rndhalffloats1.y)*3; //three component
    vec3 EMIT_POSITION = EMITTER_PARTICLE_POSITION + vec3(texelFetch(MeshTriangleVertices, INDEX).x,
                                                          texelFetch(MeshTriangleVertices, INDEX+1).x,
                                                          texelFetch(MeshTriangleVertices, INDEX+2).x)*ModelScale;
    
    
    Position_out = EMIT_POSITION + EMITTER_PARTICLE_POSITION_DEVIATION * vec3(rndfloats0.xy, rndfloats1.x);
    Velocity_out = EMITTER_PARTICLE_VELOCITY + EMITTER_PARTICLE_VELOCITY_DEVIATION * vec3(rndfloats1.zx,rndfloats0.z);
    Age_out      = EMITTER_PARTICLE_AGE_DEVIATION*rndfloats0.w;
    Type_out = PARTICLE_TYPE_TO_EMIT;
                
}
    
    /*
    // if using texture buffer internal format RGBA32F
    vec3 EMIT_POSITION = EMITTER_PARTICLE_POSITION + texelFetch(MeshTriangleVertices, int(vertex_count*rndhalffloats1.y)).xyz*ModelScale;
    */
