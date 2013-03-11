#version 330

in vec3 Position;
in float Age;
//in float Type;

flat out float SpriteAnimationFrame;
flat out vec4 vLColor;
flat out float vPointSize;

uniform mat4 ModelViewProjection;
uniform mat4 ModelView;

uniform sampler1D ColorBlendTexture;
uniform float ColorBlendLifeTime;

uniform int COLOR_BLENDING;

uniform float GROWTH_FACTOR;
uniform float PARTICLE_SIZE;

uniform float animation_fps = 1/15.0;
uniform int nFrames = 25;


uniform bool hasDistanceAttenuation;
uniform vec3 DISTANCE_ATTENUATION = vec3( 1.0, 0.0001, 0.000001);
//uniform vec3 DISTANCE_ATTENUATION = vec3( 1.0, 0.0, 0.00001);
//uniform vec3 DISTANCE_ATTENUATION = vec3( 1.0, 0.0, 0.0);

void main()
{   float attenuation_factor;
    SpriteAnimationFrame = float(int(Age/animation_fps)% nFrames);
    
    if ( COLOR_BLENDING == 1)
            vLColor = texture(ColorBlendTexture, Age/ColorBlendLifeTime);    
    else
        vLColor = vec4(1.0);
    
    if (hasDistanceAttenuation)
    {
        float Distance = -(ModelView*vec4(Position, 1.0 )).z; // Calculate Eye vector (z component is distance from camera)
        attenuation_factor = sqrt(1.0 / (DISTANCE_ATTENUATION.x + (DISTANCE_ATTENUATION.y + DISTANCE_ATTENUATION.z*Distance)*Distance ));
    }
    
    else
    {
        attenuation_factor = 1.0;
    }
    
    // Set current vertex point size (needs 'glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)' to work)
    gl_PointSize = vPointSize = attenuation_factor * (PARTICLE_SIZE + Age * GROWTH_FACTOR);
    
    // Set the position of the current vertex     
    gl_Position = ModelViewProjection * vec4(Position, 1.0 );
}
