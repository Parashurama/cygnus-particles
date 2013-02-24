#version 330

in vec3 Vertex_Position ;
in vec2 Vertex_TexCoords ;
in vec3 Instance_Position ;
in float Instance_Age ;

uniform mat4 ModelView;

uniform sampler1D ColorBlendTexture;
uniform float ColorBlendLifeTime;

uniform float COLOR_BLENDING;
uniform float GROWTH_FACTOR;
uniform float PARTICLE_SIZE;

out vec2 TexCoords0 ;
flat out vec4 vLColor;



void main()
{            
    TexCoords0 = Vertex_TexCoords ;
    
    
    float vObjectSize = PARTICLE_SIZE + Instance_Age * GROWTH_FACTOR;
    
    if ( COLOR_BLENDING == 1.0)
        vLColor = texture(ColorBlendTexture, Instance_Age/ColorBlendLifeTime);    
    else
        vLColor = vec4(1.0);
        
    // Set the position of the current vertex 
    gl_Position = ModelView* vec4( Vertex_Position*vObjectSize+Instance_Position, 1.0) ; //+Instance_Position
    
    /*
    // fix of the clipping bug for both Nvidia and ATi
    #ifdef __GLSL_CG_DATA_TYPES
    gl_ClipVertex = gl_ModelViewMatrix * gl_Vertex;
    #endif
    */
}
