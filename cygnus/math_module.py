import numbers, math

class Vec2(object):
    __slots__=('x','y')
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def __iadd__(self, value):
        if isinstance(value, numbers.Number):
            self.x+=value
            self.y+=value
            
        elif isinstance(value, Vec2):
            self.x+=value.x
            self.y+=value.y
        else:
            raise TypeError("unsupported operand type(s) for +=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __add__(self, value):
        if isinstance(value, numbers.Number):
            return Vec2(self.x+value, self.y+value)
        elif isinstance(value, Vec2):
            return  Vec2(self.x+value.x, self.y+value.y)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __radd__(self, value):
        self.__add__(value)

            
    def __isub__(self, value):
        if isinstance(value, numbers.Number):
            self.x-=value
            self.y-=value
            
        elif isinstance(value, Vec2):
            self.x-=value.x
            self.y-=value.y
        else:
            raise TypeError("unsupported operand type(s) for -=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __sub__(self, value):
        if isinstance(value, numbers.Number):
            return Vec2(self.x-value, self.y-value)
        elif isinstance(value, Vec2):
            return  Vec2(self.x-value.x, self.y-value.y)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __rsub__(self, value):
        self.__sub__(value)
    
        
    def __imul__(self, value):
        if isinstance(value, numbers.Number):
            self.x*=value
            self.y*=value
            
        elif isinstance(value, Vec2):
            self.x*=value.x
            self.y*=value.y
        else:
            raise TypeError("unsupported operand type(s) for *=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            return Vec2(self.x*value, self.y*value)
        elif isinstance(value, Vec2):
            return  Vec2(self.x*value.x, self.y*value.y)
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
    
    def __rmul__(self, value):
        self.__mul__(value)
    
    def copy(self):
        return Vec2(self.x, self.y)
        
    def magnitude(self):
        return math.sqrt(dot2(self, self))
        
    def normalize(self):
        inv_mag = self.magnitude()
        self.x*=inv_mag
        self.y*=inv_mag
    
    def normalized(self):
        new_vec = self.copy()
        new_vec.normalize()
        return new_vec
        
    def __iter__(self):
        return iter((self.x, self.y))
        
    def __repr__(self):
        return 'Vec2({}, {})'.format(self.x, self.y)

class Vec3(object):
    __slots__=('x','y','z')
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(y)
        
    def __iadd__(self, value):
        if isinstance(value, numbers.Number):
            self.x+=value
            self.y+=value
            self.z+=value
            
        elif isinstance(value, Vec3):
            self.x+=value.x
            self.y+=value.y
            self.z+=value.z
        else:
            raise TypeError("unsupported operand type(s) for +=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __add__(self, value):
        if isinstance(value, numbers.Number):
            return Vec3(self.x+value, self.y+value, self.z+value)
        elif isinstance(value, Vec3):
            return Vec3(self.x+value.x, self.y+value.y, self.z+value.z)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __radd__(self, value):
        self.__add__(value)

            
    def __isub__(self, value):
        if isinstance(value, numbers.Number):
            self.x-=value
            self.y-=value
            self.z-=value
            
        elif isinstance(value, Vec3):
            self.x-=value.x
            self.y-=value.y
            self.z-=value.z
        else:
            raise TypeError("unsupported operand type(s) for -=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __sub__(self, value):
        if isinstance(value, numbers.Number):
            return Vec3(self.x-value, self.y-value, self.z-value)
        elif isinstance(value, Vec3):
            return Vec3(self.x-value.x, self.y-value.y, self.z-value.z)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
            
    def __rsub__(self, value):
        return self.__sub__(value)
        
    def __imul__(self, value):
        if isinstance(value, numbers.Number):
            self.x*=value
            self.y*=value
            self.z*=value
            
        elif isinstance(value, Vec3):
            self.x*=value.x
            self.y*=value.y
            self.z*=value.z
        else:
            raise TypeError("unsupported operand type(s) for *=: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            return Vec3(self.x*value, self.y*value, self.z*value)
        elif isinstance(value, Vec3):
            return Vec3(self.x*value.x, self.y*value.y, self.z*value.z)
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(self.__class__.__name__, value.__class__.__name__))
            
    def __rmul__(self, value):
        return self.__mul__(value)
    
    def copy(self):
        return Vec3(self.x, self.y, self.z)
        
    def magnitude(self):
        return math.sqrt(dot3(self, self))
        
    def normalize(self):
        inv_mag = self.magnitude()
        self.x*=inv_mag
        self.y*=inv_mag
        self.z*=inv_mag
    
    def normalized(self):
        new_vec = self.copy()
        new_vec.normalize()
        return new_vec
        
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    
    def __repr__(self):
        return 'Vec3({}, {}, {})'.format(self.x, self.y, self.z)
        
def lerp(edge0, edge1):
    return edge0 + x * (edge1 -edge0)

def lerp2(vec0, vec1, value):
    return Vec2( vec0.x + value * (vec1.x -vec0.x),
                 vec0.y + value * (vec1.y -vec0.y) )

def lerp3(vec0, vec1, value):
    return Vec3( vec0.x + value * (vec1.x -vec0.x),
                 vec0.y + value * (vec1.y -vec0.y),
                 vec0.z + value * (vec1.z -vec0.z) )

def dot2(vec0, vec1):
    return vec0.x*vec1.x + vec0.y*vec1.y

def dot3(vec0, vec1):
    return vec0.x*vec1.x + vec0.y*vec1.y + vec0.z*vec1.z

def cross2(vec0, vec1):    
    return (vec0.x*vec1.y - vec0.y*vec1.x)

def cross3(vec0, vec1):    
    return Vec3( vec0.y*vec1.z - vec0.z*vec1.y,
                 vec0.z*vec1.x - vec0.x*vec1.z,
                 vec0.x*vec1.y - vec0.y*vec1.x )
