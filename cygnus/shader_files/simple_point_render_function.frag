#version 330
#extension GL_EXT_gpu_shader4 : enable

flat in vec4 vLColor;
flat in float SpriteAnimationFrame;
flat in float vPointSize;

# define NO_TEXTURE       0
# define SIMPLE_TEXTURE   1
# define ANIMATED_TEXTURE 2

uniform int TEXTURE_TYPE;
uniform float PARTICLE_FEATHER_RADIUS;
uniform vec4 DEFAULT_PARTICLE_COLOR;

uniform sampler2D SimpleTexture0;
uniform sampler2DArray AnimatedTexture0;

void main()
{
    vec4 TexColor = vec4(1.0);
    
    if ( TEXTURE_TYPE == SIMPLE_TEXTURE )
    {
        TexColor = texture(SimpleTexture0, gl_PointCoord.xy);
    }
    
    else if ( TEXTURE_TYPE == ANIMATED_TEXTURE )
    {
        TexColor = texture2DArray(AnimatedTexture0, vec3(gl_PointCoord.xy, SpriteAnimationFrame));
    }
    
    float PARTICLE_SIZE = vPointSize;
    
    vec2 gVector = ((gl_PointCoord -0.5))*2;
    float Distance = length(gVector)*PARTICLE_SIZE; // Optimize without sqrt
    
    gl_FragColor = DEFAULT_PARTICLE_COLOR*vLColor*TexColor;    
    gl_FragColor.a *= clamp((PARTICLE_SIZE-Distance)/PARTICLE_FEATHER_RADIUS,0.0,1.0);

} 
