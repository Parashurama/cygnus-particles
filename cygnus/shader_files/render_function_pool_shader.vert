#version 330

in vec3 Position;

uniform mat4 ModelView;
uniform mat4 ModelViewProjection;
out vec3 color;

float scale= 1/10;

void main()
{   

    float val= sqrt(Position.z)*0.002;
    
    color.r=min(val, 1.0);
    color.g=min((val),0.5);
    color.b=min((1.0-val),0.5);
    
    gl_Position = ModelViewProjection * vec4(Position.xy, 0.0, 1.0 );
}
