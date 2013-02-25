from OpenGL.GL import *
from OpenGL.GL.ARB.framebuffer_object import *
import numpy as np
import zlib, cPickle
from decoders import optimized_image_load
from glObjects import TextureObject

class GLTexture2D(TextureObject):
    def __init__(self, imagefile, mipmap=True, nearest=False, anisotropic=False, repeat_texture=True):
        
        decoded_image = optimized_image_load(imagefile)

        self.width  = decoded_image.width
        self.height = decoded_image.height
        
        self.size=( float(self.width),float(self.height) )
        self.texcoords=(0.0,0.0,1.0,1.0)
        
        TextureObject.__init__(self, decoded_image.data, size=(self.width,self.height), format=decoded_image.format, internalformat='RGBA', mipmap=mipmap, nearest=nearest, anisotropic=anisotropic, repeat_texture=repeat_texture)
        
        

class Animation(GLTexture2D):
    def __init__(self, imagefile, H,V):

        i=imagefile.find('.')
        file_name=imagefile[:i]

        try: # Load Cached Animation
            cached_animation_file= open(file_name+'.cache', 'rb')
                                                    #n_frames
            self.format, self.width, self.height, self.last_frame = cPickle.load(cached_animation_file)
            restructured_image_data = cached_animation_file.read()            
            restructured_image_data = zlib.decompress(restructured_image_data)            
            self.restructured_image_data = cPickle.loads(restructured_image_data)
            
            cached_animation_file.close()
            
        except IOError: # Restructure Data from Original Image and Save Result
            
            decoded_image = optimized_image_load(imagefile, flipped=False)
            
            self.width  = decoded_image.width
            self.height = decoded_image.height
            self.format = decoded_image.format
            
            assert (decoded_image.format == 'RGBA'), "\nLe format du fichier image %s n'est pas pris en charge.\nLe fichier doit contenir un canal alpha !\n%s" %(imagefile, textureData.format)
                    
            dataR = decoded_image.data.reshape(self.height*H, self.width/H, len(self.format) )

            dx=self.width/H ; dy=self.height/V

            self.restructured_image_data=(dataR[ [ i*dy*H + j+ k*H for i in range(V) for j in range(H) for k in range(dy) ] ]).ravel()

            self.height=dx  ;  self.width=dy ; self.last_frame=H*V
            
            cached_animation_file= open(file_name+'.cache', 'wb')
                                                    #n_frames
            cPickle.dump((self.format, self.width, self.height, self.last_frame), cached_animation_file, cPickle.HIGHEST_PROTOCOL)
            restructured_image_data = cPickle.dumps(self.restructured_image_data, cPickle.HIGHEST_PROTOCOL)
            restructured_image_data = zlib.compress(restructured_image_data,4)
            cached_animation_file.write(restructured_image_data)
            
            cached_animation_file.close()
            ####################

        self.size=( float(self.width),float(self.height) )

        
        self.id = glGenTextures(1)
    
        glBindTexture(GL_TEXTURE_2D_ARRAY,self.id);
        
        glTexParameteri(GL_TEXTURE_2D_ARRAY,GL_TEXTURE_MIN_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D_ARRAY,GL_TEXTURE_MAG_FILTER,GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D_ARRAY,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D_ARRAY,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
        #glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_GENERATE_MIPMAP, GL_TRUE)      
        glTexImage3D(GL_TEXTURE_2D_ARRAY,0,GL_RGBA,self.width,self.height, self.last_frame, 0,GL_RGBA,GL_UNSIGNED_BYTE,self.restructured_image_data);        
        
