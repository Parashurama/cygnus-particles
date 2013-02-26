#version 330

uniform sampler2D Diffuse_Texture0;

in vec2 TexCoords0  ;
flat in vec4 vLColor ;

uniform vec4 DEFAULT_PARTICLE_COLOR;
uniform bool hasDiffuseTexture;

void main() {
    // Set the output color of our current pixel
    vec4 TexColor;
    
    if (hasDiffuseTexture)
    {
        TexColor=texture2D(Diffuse_Texture0, TexCoords0) ;
    }
    else
    {
        TexColor=vec4(1.0);
    }
    
    if (TexColor.a < 0.30 )
        discard;
    
    gl_FragColor = DEFAULT_PARTICLE_COLOR*TexColor*vLColor;//*0.00001+vec4(1.0);
} 
