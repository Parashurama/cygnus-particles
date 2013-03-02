#version 330

in vec3 Vertex_Position ;
in vec3 Vertex_Normals ;
in vec2 Vertex_TexCoords ;
in vec3 Instance_Position ;
in float Instance_Age ;

uniform mat3 NormalMatrix;
uniform mat4 ModelView;
uniform mat4 ModelViewProjection;

uniform sampler1D ColorBlendTexture;
uniform float ColorBlendLifeTime;

uniform bool COLOR_BLENDING;
uniform float GROWTH_FACTOR;
uniform float PARTICLE_SIZE;


struct Light
{
    vec4 ambient;              // Aclarri   
    vec4 diffuse;              // Dcli   
    vec4 specular;             // Scli
    vec3 direction;
};

uniform Light light;

smooth out vec3 vNormals;
smooth out vec3 vLightVec;
smooth out vec3 vEyeVec;
smooth out vec2 vTexCoords0;
flat   out vec4 vLColor;



void main()
{
    
    
    float vObjectSize = PARTICLE_SIZE + Instance_Age * GROWTH_FACTOR;
    
    if ( COLOR_BLENDING)
        vLColor = texture(ColorBlendTexture, Instance_Age/ColorBlendLifeTime);    
    else
        vLColor = vec4(1.0);
    
    vTexCoords0 = Vertex_TexCoords ;
    
    // gl_NormalMatrix = transpose(inverse(modelview_matrix))
    // since modelview_matrix is orthogonal : inverse(modelview_matrix) ==transpose(modelview_matrix)
    // ==> transpose(inverse(modelview_matrix)) == modelview_matrix
    
    // matrix multiplication order is reversed because RotationMatrix is row major instead of column major
    // see : http://www.opengl.org/wiki/GLSL_Types#Matrix_constructors  
    vNormals = (NormalMatrix * Vertex_Normals ).xyz;
    
    vec4 Vertex = vec4( Vertex_Position*vObjectSize+Instance_Position, 1.0);
    vec3 mVertex = (ModelView * Vertex).xyz;
    
    vLightVec = normalize(ModelView * vec4(light.direction.xyz,0.0)).xyz;
    vEyeVec = vec3(0,0,0)-mVertex;
    
    // Set the position of the current vertex 
    gl_Position = ModelViewProjection*Vertex ;
    
    /*
    // fix of the clipping bug for both Nvidia and ATi
    #ifdef __GLSL_CG_DATA_TYPES
    gl_ClipVertex = gl_ModelViewMatrix * gl_Vertex;
    #endif
    */
}
