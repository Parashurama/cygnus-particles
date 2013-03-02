#version 330

uniform sampler2D Diffuse_Texture0;
uniform bool hasDiffuseTexture;

in vec2 TexCoords0  ;

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
    
    gl_FragColor = TexColor*0.001 + vec4(1.0);
} 
