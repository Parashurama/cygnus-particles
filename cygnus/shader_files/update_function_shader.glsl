#version 330
#extension GL_EXT_gpu_shader4 : enable

layout(points) in;
layout(points) out;
layout(max_vertices = 1) out;

#define PI 3.14159265f
#define PI2 6.2831853f
#define MAIN_PARTICLE_EMITTER 0.0f
#define PARTICLE_TYPE_1 10.0f
#define PER_PARTICLE_EMITTER 20.0f
#define G 6.67428E4
#define Ke 8.987551E9

#define BOUNCING_COEFFICIENT 0.35

/////////////////////////////////
in ParticleData
{
    vec3 position;
    vec3 velocity;
    float type;
    float age;
} Particle[];

/////////////////////////////////
out vec3 Position_out;
out vec3 Velocity_out;
out float Type_out;
out float Age_out;
/////////////////////////////////

uniform float dtime;

uniform vec3 VISCOUS_DRAG = vec3(0.0, 0.0, 0.0);
uniform vec3 GRAVITY = vec3(0.0, 0.0, 0.0);


struct CircleDomain {
  vec3 center;
  float radius;
  
};

struct SquareDomain {
  vec4 square;
  vec3 A, B, C, D;
  vec3 center;
  
};

struct TriangleDomain {
  //vec2 Points[3];
  vec3 center;
  vec3 A, B, C;
  
};


struct MagneticController {
  vec3 origin;
  float charge;
  float sqr_cutoff_distance;
  float epsilon;
  
};


uniform UPDATER_UNIFORMS {
    int EMITTER_TYPE;
    int PARTICLE_COLLECTORS;
    int N_CIRCLE_COLLECTOR;
    int N_TRIANGLE_COLLECTOR;
    int N_SQUARE_COLLECTOR;

    int PARTICLE_BOUNCERS;
    int N_CIRCLE_BOUNCER;
    int N_TRIANGLE_BOUNCER;
    int N_SQUARE_BOUNCER;

    int I_CIRCLE_BOUNCER;
    int I_TRIANGLE_BOUNCER;
    int I_SQUARE_BOUNCER;

    int N_MAGNETIC_CONTROLLER;

    float PARTICLE_LIFETIME;
    
    CircleDomain uCircleDom[3];
    SquareDomain uSquareDom[3];
    TriangleDomain uTriangleDom[3];
    MagneticController uMagneticCon[3];
};


bool IntersectionLinewithLine(in vec3 P0, in vec3 gVec0, in vec3 P1, in vec3 gVec1, inout vec3 iPoint, inout vec3 iNormal) {
    
    vec3 gVector, tVec;
    float dx, dy;
    float ua, ub;
    
    //gVec1*= 3; // HACK to LIMIT BLEED-THROUGH
    float d = gVec1.y*gVec0.x - gVec1.x*gVec0.y;
    
    if ( abs(d) < 0.00001 )
        return false;
    
    dy = P0.y - P1.y;    
    dx = P0.x - P1.x;
    
    ua = (gVec1.x *dy - gVec1.y*dx)/d ;
    ub = (gVec0.x *dy - gVec0.y*dx)/d ;
    
    if (  !(ua >= 0.0 && ua <= 1.0)  || !(ub >= 0.0 && ub <= 1.0) )
        return false;
    
    iPoint  = P0 + ua * gVec0;
    
    // Compute Line-Segment Normal (90° Rotation)
    iNormal = vec3(-gVec0.y, gVec0.x, gVec0.z);
    
    return true;
/*
bool IntersectionLinewithLine(in vec3 P0, in vec3 gVec0, in vec3 P1, in vec3 gVec1, inout vec3 iPoint, inout vec3 iNormal)
{   //return ((vector1.x * vector2.y) - (vector1.y * vector2.x))
    vec3 gVector, tVec;
    float dx, dy;
    float ua, ub;
    float d = gVec1.y*gVec0.x - gVec1.x*gVec0.y;
    
    if ( abs(d) < 0.00001 )
        return false;
        
    gVector.x = (P0-P1).yxz/ d;
    
    tVec = gVec1 * gVector;    
    ua = tVec.x - tVec.y;
    
    tVec = gVec0 * gVector;    
    ub = tVec.x - tVec.y;
    
    if (  !(ua >= 0.0 && ua <= 0.0)  || !(ub >= 0.0 && ub <= 1.0) )
        return false;
    
    iPoint  = P0 + ua * gVec0;
    
    // Compute Line-Segment Normal (90° Rotation)
    iNormal = vec3(-gVec0.y, gVec0.x, gVec0.z);
    
    return true;
*/
}

void BounceOffTriangle(in vec3 A, in vec3 B, in vec3 C, in vec3 OldPos, inout vec3 Pos, inout vec3 Velocity) {
    vec3 iNormal, nNormal;
    vec3 iPoint = vec3(0.0,0.0,0.0);
    vec3 gVec1 = Pos-OldPos;
    
    if ( IntersectionLinewithLine( A, B-A, OldPos, gVec1, iPoint, iNormal) ||
         IntersectionLinewithLine( B, C-B, OldPos, gVec1, iPoint, iNormal) ||
         IntersectionLinewithLine( C, A-C, OldPos, gVec1, iPoint, iNormal) )
    {
        nNormal = normalize(iNormal);
        Velocity = BOUNCING_COEFFICIENT*reflect(Velocity, nNormal);//vec3(0.0,0.0,0.0);//
        Pos+= (iPoint-Pos)*(6.0-BOUNCING_COEFFICIENT);
        
    }
}

void BounceOffSquare(in vec3 A, in vec3 B, in vec3 C, in vec3 D, in vec3 OldPos, inout vec3 Pos, inout vec3 Velocity) {
    vec3 iNormal, nNormal;
    vec3 iPoint = vec3(0.0,0.0,0.0);
    vec3 gVec1 = Pos-OldPos;
    
    if ( IntersectionLinewithLine( A, B-A, OldPos, gVec1, iPoint, iNormal) ||
         IntersectionLinewithLine( B, C-B, OldPos, gVec1, iPoint, iNormal) ||
         IntersectionLinewithLine( C, D-C, OldPos, gVec1, iPoint, iNormal) ||
         IntersectionLinewithLine( D, A-D, OldPos, gVec1, iPoint, iNormal) )
    {
        nNormal = normalize(iNormal);
        Velocity = BOUNCING_COEFFICIENT*reflect(Velocity, nNormal);//vec3(0.0,0.0,0.0);//
        Pos+= (iPoint-Pos)*(6.0-BOUNCING_COEFFICIENT);
        
    }
}


bool IntersectionSegmentwithCircle(in vec3 center, in float radius, in vec3 S0, in vec3 S1, inout vec3 iPoint) {
    vec3 gVector = S1-S0;
    float a = dot(gVector,gVector);
    
    float b = 2 * (gVector.x * (S0.x-center.x) + gVector.y * (S0.y-center.y) );
    float c = dot(center,center) + dot(S0,S0) - 2 * dot(center, S0) - radius*radius;
    float det = b*b - 4*a*c ;
    
    if (det < 0.0)
        return false;
    
    float u = (-b - sqrt(det)) / (2 * a);
    
    if ( !( (0.0<=u) || (u<=1.0) ) )
        return false;
    
    iPoint =  S0 + u * gVector ;
    return true;
    
}


void BounceOffCircle(in vec3 center, in float radius, in vec3 OldPos, inout vec3 Pos, inout vec3 Velocity) {
    vec3 iPoint = vec3(0.0,0.0,0.0);
    if ( IntersectionSegmentwithCircle( center, radius, OldPos, Pos, iPoint) )
    {
        vec3 gVector = iPoint-center ;
        vec3 nVector = normalize(gVector);
        //vec3 Tangent = vec3( nVector
        Velocity = BOUNCING_COEFFICIENT*reflect(Velocity, nVector);
        Pos+= iPoint-Pos;
        
    }
}

bool PointInCircle(vec3 center, float radius, vec3 pt) {
    vec3 gVector = pt-center;
    float gDistance = dot(gVector, gVector);    
    return (gDistance <= radius*radius);
} 

bool PointInSquare(vec4 SQUARE, vec3 pt) {
    return (SQUARE.x <=pt.x && pt.x <=SQUARE.z) && (SQUARE.y <=pt.y && pt.y <=SQUARE.w);  
} 

bool PointInTriangle(vec3 A, vec3 B, vec3 C, vec3 Pt) {

    vec3 v0 = C - A;
    vec3 v1 = B - A;
    vec3 v2 = Pt - A;

    // Compute dot products
    float dot00 = dot(v0, v0);
    float dot01 = dot(v0, v1);
    float dot02 = dot(v0, v2);
    float dot11 = dot(v1, v1);
    float dot12 = dot(v1, v2);

    // Compute barycentric coordinates
    float invDenom = 1 / (dot00 * dot11 - dot01 * dot01);
    float u = (dot11 * dot02 - dot01 * dot12) * invDenom;
    float v = (dot00 * dot12 - dot01 * dot02) * invDenom;

    // Check if point is in triangle
    return (u >= 0) && (v >= 0) && (u + v < 1);
} 


void MagneticAttraction(in vec3 gVector, inout vec3 Point_velocity, in MagneticController Magnet, in float dt) {   
    
    vec3 uVector = normalize(gVector);
    
    //   Acceleration =        COULOMB FORCE        /      Particle Mass
    vec3 Acceleration = uVector *(Ke*(-Magnet.charge*0.01)/(dot(gVector, gVector)+Magnet.epsilon))   /   1.0 ;
    
    Point_velocity+= Acceleration*dt;
 
}


bool PARTICLE_IS_ALIVE = true ;

void main()
{   
    vec3 gVector;
    vec3 OldPos;
    vec3  Pos = Particle[0].position;
    vec3  Vel = Particle[0].velocity;
    float Type= Particle[0].type;
    float Age = Particle[0].age;
    gl_Position = vec4(Pos,Vel); // HACK
    

    // Screen Collision
    if ( Pos.x>1440 ) { Vel.x = -Vel.x ; Pos.x=1440-(Pos.x-1440);}
    else if (Pos.x<0.0) { Vel.x = -0.7*Vel.x ; Pos.x=-Pos.x;}

    if ( Pos.y>900 ) { Vel.y = -Vel.y ; Pos.y=900-(Pos.y-900);}
    else if (Pos.y<0.0) { Vel.y = -0.7*Vel.y ; Pos.y=-Pos.y;}
    
    Age += dtime;
    
    if (Age < PARTICLE_LIFETIME)
    {

        OldPos = Pos;
        Vel += VISCOUS_DRAG*dtime + GRAVITY*dtime;
        
        if (PARTICLE_COLLECTORS == 1)
        {
            
            for (int i = 0 ; i < N_CIRCLE_COLLECTOR ; i++)
                if ( PointInCircle( uCircleDom[i].center, uCircleDom[i].radius, Pos) ) { PARTICLE_IS_ALIVE=false; break; }

            for (int i = 0 ; i < N_SQUARE_COLLECTOR ; i++)
                if ( PointInSquare( uSquareDom[i].square, Pos) ) { PARTICLE_IS_ALIVE=false; break; }
                
            for (int i = 0 ; i < N_TRIANGLE_COLLECTOR ; i++)
                if ( PointInTriangle( uTriangleDom[i].A, uTriangleDom[i].B, uTriangleDom[i].C, Pos) ) { PARTICLE_IS_ALIVE=false; break; }

        }
        
            
        if ( PARTICLE_IS_ALIVE)
        {
            Pos += Vel*dtime;
            
            for (int i = 0 ; i < N_MAGNETIC_CONTROLLER ; i++)
            {                        
                gVector = uMagneticCon[i].origin-Pos;
                if ( dot(gVector, gVector) < uMagneticCon[i].sqr_cutoff_distance)
                    MagneticAttraction(gVector, Vel, uMagneticCon[i], dtime);
            }
            
            if (PARTICLE_BOUNCERS == 1)
            {

                for (int i = I_CIRCLE_BOUNCER ; i < N_CIRCLE_BOUNCER ; i++)
                {
                    if ( PointInCircle( uCircleDom[i].center, uCircleDom[i].radius, Pos) )
                    {
                        BounceOffCircle(uCircleDom[i].center, uCircleDom[i].radius, OldPos, Pos, Vel);
                    }
                }
                
                for (int i = I_SQUARE_BOUNCER ; i < N_SQUARE_BOUNCER ; i++)
                {
                    if ( PointInSquare( uSquareDom[i].square, Pos) )
                    {
                        BounceOffSquare(uSquareDom[i].A, uSquareDom[i].B, uSquareDom[i].C, uSquareDom[i].D, OldPos, Pos, Vel);

                    }
                }
                    
                for (int i = I_TRIANGLE_BOUNCER ; i < N_TRIANGLE_BOUNCER ; i++)
                {
                    //BounceOffTriangle(uTriangleDom[i].A, uTriangleDom[i].B, uTriangleDom[i].C, OldPos, Pos, Vel);
                    
                    
                    if ( PointInTriangle( uTriangleDom[i].A, uTriangleDom[i].B, uTriangleDom[i].C, Pos) )
                    {
                        BounceOffTriangle(uTriangleDom[i].A, uTriangleDom[i].B, uTriangleDom[i].C, OldPos, Pos, Vel);
                        //Vel=vec3(0.0);
                    }
                }
            }
            
            Position_out = Pos;
            Velocity_out = Vel;
            Age_out = Age ;
            Type_out = Type;
            
            EmitVertex();
            EndPrimitive();
        }

    }

    
    

}
