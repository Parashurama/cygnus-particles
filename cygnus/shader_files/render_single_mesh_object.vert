#version 330

in vec3 Vertex_Position ;
in vec2 Vertex_TexCoords ;

uniform mat4 ModelView;
uniform mat4 ModelViewProjection;

out vec2 TexCoords0 ;



void main()
{
    TexCoords0 = Vertex_TexCoords ;
    
    // Set the position of the current vertex 
    gl_Position = ModelViewProjection* vec4( Vertex_Position, 1.0) ;
    
    /*
    // fix of the clipping bug for both Nvidia and ATi
    #ifdef __GLSL_CG_DATA_TYPES
    gl_ClipVertex = gl_ModelViewMatrix * gl_Vertex;
    #endif
    */
}
