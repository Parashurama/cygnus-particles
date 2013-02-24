#version 330

uniform sampler2D ObjTexture;

in vec2 TexCoords0  ;
flat in vec4 vLColor ;

uniform vec4 DEFAULT_PARTICLE_COLOR;

void main() {
    // Set the output color of our current pixel
    
    vec4 TexColor= texture2D(ObjTexture, TexCoords0) ;
    
    if (TexColor.a < 0.30 )
        discard;
    
    gl_FragColor = DEFAULT_PARTICLE_COLOR*TexColor*vLColor;//*0.00001+vec4(1.0);
} 
