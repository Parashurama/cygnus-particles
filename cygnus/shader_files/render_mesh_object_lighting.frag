#version 330
//#define BLINN_PHONG_LIGHTING
#define PHONG_LIGHTING

#define SPECULAR_COLOR_HACK_CORRECTION 0.5

smooth in vec3 vNormals;
smooth in vec3 vLightVec;
smooth in vec3 vEyeVec;
smooth in vec2 vTexCoords0;
flat   in vec4 vLColor;

uniform sampler2D Diffuse_Texture0;
uniform sampler2D Normal_Texture0;

uniform vec4 DEFAULT_PARTICLE_COLOR;
uniform bool hasDiffuseTexture;
uniform bool hasNormalTexture;

uniform float NormalMultiplier;

struct Light
{
    vec4 ambient;              // Aclarri   
    vec4 diffuse;              // Dcli   
    vec4 specular;             // Scli
    vec3 direction;
};

uniform Light light;

struct Material
{  
   vec4 ambient;     // Acm   
   vec4 diffuse;     // Dcm   
   vec4 specular;    // Scm   
   float shininess;  // Srm  
};

uniform Material material;

void main()
{   
    // Set the output color of our current pixel
    vec4 TexColor, Ispec;
    vec3 normalAdjusted;
    
    if (hasDiffuseTexture)
    {
        TexColor=texture2D(Diffuse_Texture0, vTexCoords0) ;
    }
    else
    {
        TexColor=vec4(1.0);
    }
    
    if (hasNormalTexture)
    {   // Mess around with this value to increase/decrease normal perturbation
        float maxVariance = 2.0 * NormalMultiplier; 
        float minVariance = maxVariance *0.5;
        
        normalAdjusted = normalize(vNormals + (texture2D(Normal_Texture0, vTexCoords0).xyz * maxVariance - minVariance));
    }
    else
    {
        normalAdjusted = normalize(vNormals);
    }
    
    vec3 lVec = normalize(vLightVec);
    vec3 vVec = normalize(vEyeVec);// we are in Eye Coordinates, so EyePos is (0,0,0)
    
    float cosTheta = dot(lVec, normalAdjusted); // for Diffuse componnent
    
    
    //calculate Ambient Term:
    vec4 Iamb = light.ambient*material.ambient;
    
    //calculate Diffuse Term:
    vec4 Idiff = light.diffuse * max( cosTheta, 0.0 ) *material.diffuse;
    
    // calculate Specular Term:
    if  ( material.shininess > 0.0001 )
    {   
        #if   defined(PHONG_LIGHTING)
        float cosAlpha = dot(reflect(-lVec, normalAdjusted), vVec); // for Phong Specular componnent
        
        #elif defined(BLINN_PHONG_LIGHTING)
        vec3 halfVector = normalize(lVec+vVec);
        float cosAlpha = dot(halfVector,  normalAdjusted);
        
        #endif
        
        Ispec = light.specular * pow(clamp(cosAlpha, 0.0, 1.0), material.shininess ) * material.specular;
    }
    else
    {
        Ispec = vec4(0.0);
    }
    
    gl_FragColor = (DEFAULT_PARTICLE_COLOR*vLColor*TexColor*(Iamb + Idiff) + Ispec*SPECULAR_COLOR_HACK_CORRECTION);
    
} 
