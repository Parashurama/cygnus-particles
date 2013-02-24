#version 330

layout (location = 0) in float Type;


#define PI 3.14159265f
#define PI2 6.2831853f
/*
#define MAIN_PARTICLE_EMITTER 0.0f
#define PARTICLE_TYPE_1 10.0f
#define PER_PARTICLE_EMITTER 20.0f
*/
#define POINT_EMITTER 0
#define CIRCLE_EMITTER 1
#define DISC_EMITTER 2
#define LINE_EMITTER 3
#define TRIANGLE_EMITTER 4
#define SQUARE_EMITTER 5
#define SPHERE_EMITTER 6

uniform vec2 seed;
uniform sampler1D RandomTexture;
uniform float ParticleSystemcount;


uniform EMITTER_UNIFORMS
{
    int EMITTER_TYPE;
    float EMITTER_PARTICLE_FIRERATE;
    vec3 EMITTER_PARTICLE_POSITION;
    vec3 EMITTER_PARTICLE_VELOCITY;
    vec3 EMITTER_PARTICLE_POSITION_DEVIATION;
    vec3 EMITTER_PARTICLE_VELOCITY_DEVIATION;
    float EMITTER_PARTICLE_AGE_DEVIATION;

    float CIRCLE_EMITTER_RADIUS;
    vec2 DISC_EMITTER_RADII; // inner radius & outer_radius
    vec3 LINE_EMITTER_POINTS[2];
    vec3 TRIANGLE_EMITTER_POINTS[3];
    vec3 SQUARE_EMITTER_POINTS[4];
    vec2 SPHERE_EMITTER_RADII;
    
    float PARTICLE_TYPE_TO_EMIT;
};

/////////////////////////////////
out vec3 Position_out;
out vec3 Velocity_out;
out float Type_out;
out float Age_out;
/////////////////////////////////





//////////////////////////////////////////////////////////////////
////////////////////// Random Point Functions ////////////////////
//////////////////////////////////////////////////////////////////

vec3 RandomPointOnCircle(vec3 center, float radius, float randomfloat) {
    vec3 point;
    float theta = randomfloat*PI2;
    point.x = center.x + cos(theta)*radius;
    point.y = center.y + sin(theta)*radius;
    point.z = center.z;
    
    return point;
}

vec3 RandomPointOnDisc(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats) {
    vec3 point;
    float theta = randomfloats.x*PI2;    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloats.y);
    point.x = center.x + cos(theta)*radius;
    point.y = center.y + sin(theta)*radius;
    point.z = center.z;
    return point;
}

vec3 RandomPointOnLine(vec3 center, float randomfloat) {
    vec3 pt1 = LINE_EMITTER_POINTS[0];
    vec3 pt2 = LINE_EMITTER_POINTS[1];
    
    vec3 point = mix(pt1, pt2, randomfloat );
    
    return center + point;
}

vec3 RandomPointOnTriangle(vec3 center, vec2 randomfloats) {
    int rnd1 = int(floor(9*(randomfloats.x)));  rnd1  = rnd1 % 3;
    
    
    int rnd2 = rnd1== 2 ? 0 :rnd1+1 ;
    vec3 pt1 = TRIANGLE_EMITTER_POINTS[rnd1];
    vec3 pt2 = TRIANGLE_EMITTER_POINTS[rnd2];
    
    vec3 point = mix(pt1, pt2, randomfloats.y );
    
    return center + point;
}

vec3 RandomPointOnSquare(vec3 center, vec2 randomfloats) {   
    int rnd1 = int(floor(12*(randomfloats.x)));  rnd1  = rnd1 % 4;
    
    
    int rnd2 = rnd1== 3 ? 0 :rnd1+1 ;
    vec3 pt1 = SQUARE_EMITTER_POINTS[rnd1];
    vec3 pt2 = SQUARE_EMITTER_POINTS[rnd2];
    
    vec3 point = mix(pt1, pt2, randomfloats.y );
    
    return center + point;


}

vec3 RandomPointInWhatever(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats, float randomfloat) {
    vec3 point;
    float theta = randomfloats.x*PI2;    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloats.y);
    float omega = randomfloat;
    
    float factor = sqrt(radius*radius-omega*omega);
    
    point.x = center.x + factor*cos(theta);
    point.y = center.y + factor*sin(theta);
    point.z = center.z + omega*radius;
    
    return point;
}

// http://mathworld.wolfram.com/SpherePointPicking.html
// SPERICAL COORDINATES
vec3 RandomPointInSphere1(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats, float randomfloat) {
    vec3 point;
    float theta = randomfloats.x*PI2;    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloats.y);
    float omega = randomfloat;
    
    float factor = sqrt(1.0-omega*omega);
    
    point.x = center.x + factor*cos(theta)*radius;
    point.y = center.y + factor*sin(theta)*radius;
    point.z = center.z + omega*radius;
    
    return point;
}

//http://mathworld.wolfram.com/SpherePointPicking.html
// Marsaglia 1972
vec3 RandomPointInSphere2(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats, float randomfloat) {
    vec3 point;
    float x1 = randomfloats.x;
    float x2 = randomfloats.y;  
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloat);
    
    float factor = sqrt(1.0 - x1*x1 - x2*x2);
    
    point.x = center.x + (2.0*x1*factor)*radius;
    point.y = center.y + (2.0*x2*factor)*radius;
    point.z = center.z + (1.0 - 2.0*(x1*x1 + x2*x2))*radius;
    
    return point;
}

/*
//http://andy.moonbase.net/archives/416
vec3 RandomPointInSphere3(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats, float randomfloat) {
    vec3 point;
    float theta = randomfloats.x;
    float phi = (0.5+0.5*randomfloats.y)*PI2;  
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloat);
    
    float costheta = cos(theta);
    float sinphi = sin(phi);
    
    point.x = center.x + costheta*cos(phi)*radius;
    point.y = center.y + sinphi*radius;
    point.z = center.z + costheta*sinphi*radius;
    
    return point;
}
*/

//http://mathworld.wolfram.com/SpherePointPicking.html
// Marsaglia 1972 Reworked
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec3 randomfloats, float randomfloat) {
    vec3 point;
    
    point = normalize(randomfloats);
    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloat);
    point *= radius;
    point += center;
    
    return point;
}
/*
//http://stackoverflow.com/questions/7280184/fast-uniformly-distributed-random-points-on-the-surface-of-a-unit-hemisphere
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec3 randomhalffloats) {
    vec3 point;
    
    float azimuthal = (randomhalffloats.x)*PI2;  
    float zenith = sqrt(randomhalffloats.y);
    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(randomhalffloats.z);
    
    point.x = center.x + sin(zenith)*cos(azimuthal)*radius;
    point.y = center.y + sin(zenith)*sin(azimuthal)*radius;
    point.z = center.z + cos(zenith)*radius;
    
    return point;
}
*/

/*
//http://andy.moonbase.net/archives/416
* // BUGGED
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec2 randomfloats, float randomfloat) {
    vec3 point;
    float theta = randomfloats.x;
    float phi = (0.5+0.5*randomfloats.y)*PI2;  
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloat);
    
    float costheta = cos(theta);
    float sinphi = sin(phi);
    
    point.x = center.x + costheta*cos(phi)*radius;
    point.y = center.y + sinphi*radius;
    point.z = center.z + costheta*sinphi*radius;
    
    return point;
}
*/

/*
 * // ORIGINAL
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec3 randomfloats) {
    vec3 point;
    float theta = randomfloats.x*PI2;    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(0.5+0.5*randomfloats.y);
    float omega = randomfloats.z;
    
    float factor = sqrt(1-omega*omega);
    
    point.x = center.x + factor*cos(theta)*radius;
    point.y = center.y + factor*sin(theta)*radius;
    point.z = center.z + omega*radius;
    
    return point;
}
*/

/*
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec2 randomhalffloats, float randomfloat) {
    vec3 point;
    float theta = randomhalffloats.x*PI2*2.0-1.0;    
    float radius = inner_radius + (outer_radius-inner_radius)*sqrt(randomhalffloats.y);
    float omega = randomfloat;
    
    float factor = sqrt(radius*radius-omega*omega);
    
    point.x = center.x + factor*cos(theta);
    point.y = center.y + factor*sin(theta);
    point.z = center.z + omega;
    
    return point;
}*/

/*
vec3 RandomPointInSphere(vec3 center, float inner_radius, float outer_radius, vec2 randomhalffloats, float randomfloat) {
    vec3 point;
    float theta = randomhalffloats.x*PI2;
    float radius = inner_radius + (outer_radius-inner_radius)*randomhalffloats.y;
    float omega = randomfloat*radius;
    
    float factor = sqrt(radius*radius-omega*omega);
    
    point.x = center.x + factor*cos(theta);
    point.y = center.y + factor*sin(theta);
    point.z = center.z + omega;
    
    return point;
}
*/
//////////////////////////////////////////////////////////////////

vec4 GetRandomDir(float TexCoord)
{
    vec4 Dir = texture(RandomTexture, TexCoord);
    Dir -= vec4(0.5);
    return 2*Dir;
} 
//////////////////////////////////////////////////////////////////


void main()
{
    
    vec3 EMIT_POSITION;
    vec2 rn_value = seed + 1.0/(seed*(0.5+seed)) +  gl_VertexID/ParticleSystemcount+Type*0.1; 
    
    vec4 rndfloats0 = GetRandomDir(rn_value.x);
    vec4 rndfloats1 = GetRandomDir(rn_value.y);
    vec4 rndhalffloats0 = rndfloats0*0.5 +0.5 ;
    vec4 rndhalffloats1 = rndfloats1*0.5 +0.5 ;
    
    if      ( EMITTER_TYPE == POINT_EMITTER)   { EMIT_POSITION = EMITTER_PARTICLE_POSITION;}
    else if ( EMITTER_TYPE == CIRCLE_EMITTER)  { EMIT_POSITION = RandomPointOnCircle(EMITTER_PARTICLE_POSITION, CIRCLE_EMITTER_RADIUS, rndfloats1.w);}
    else if ( EMITTER_TYPE == DISC_EMITTER)    { EMIT_POSITION = RandomPointOnDisc(EMITTER_PARTICLE_POSITION, DISC_EMITTER_RADII.x, DISC_EMITTER_RADII.y, rndfloats1.wy);}
    else if ( EMITTER_TYPE == SQUARE_EMITTER)  { EMIT_POSITION = RandomPointOnSquare(EMITTER_PARTICLE_POSITION, rndhalffloats1.wy);}
    else if ( EMITTER_TYPE == LINE_EMITTER)    { EMIT_POSITION = RandomPointOnLine(EMITTER_PARTICLE_POSITION, rndhalffloats1.w); }
    else if ( EMITTER_TYPE == TRIANGLE_EMITTER){ EMIT_POSITION = RandomPointOnTriangle(EMITTER_PARTICLE_POSITION, rndhalffloats1.wy);}
    //else if ( EMITTER_TYPE == SPHERE_EMITTER)  { EMIT_POSITION = RandomPointInSphere(EMITTER_PARTICLE_POSITION, SPHERE_EMITTER_RADII.x, SPHERE_EMITTER_RADII.y, rndhalffloats1.ywx);}
    else if ( EMITTER_TYPE == SPHERE_EMITTER)  { EMIT_POSITION = RandomPointInSphere(EMITTER_PARTICLE_POSITION, SPHERE_EMITTER_RADII.x, SPHERE_EMITTER_RADII.y, rndfloats1.ywx, rndfloats1.z*rndfloats0.z);}
    //else if ( EMITTER_TYPE == SPHERE_EMITTER)  { EMIT_POSITION = RandomPointInSphere(EMITTER_PARTICLE_POSITION, SPHERE_EMITTER_RADII.x, SPHERE_EMITTER_RADII.y, rndfloats1.yw, rndfloats1.x);}
    
    Position_out = EMIT_POSITION + EMITTER_PARTICLE_POSITION_DEVIATION * vec3(rndfloats0.xy, rndfloats1.x);
    Velocity_out = EMITTER_PARTICLE_VELOCITY + EMITTER_PARTICLE_VELOCITY_DEVIATION * vec3(rndfloats1.zx,rndfloats0.z);
    Age_out      = EMITTER_PARTICLE_AGE_DEVIATION*rndfloats0.w;
    Type_out = PARTICLE_TYPE_TO_EMIT;
                
}
