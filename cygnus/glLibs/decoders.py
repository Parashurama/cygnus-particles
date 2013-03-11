import Image
import numpy as np
import pyglet
from pyglet.image.codecs.gdkpixbuf2 import GdkPixbuf2ImageDecoder as PygletDecoder, gdkpixbuf, gdk
from pyglet.image.codecs.pil import PILImageDecoder as PILDecoder
from pyglet.image.codecs.dds import DDSImageDecoder as DDSDecoder

from ctypes import *

class CustomPILDecoder(PILDecoder):
    def decode(self, file, filename):
        try:
            image = Image.open(file)
        except Exception, e:
            raise IOError(
                'PIL cannot read %r: %s' % (filename or file, e))
        #print "FallBackMode for ", filename
        self.width, self.height = image.size        
        self.format= image.mode
        self.data = np.asarray(image, 'B')

        return self

#class DDS_Decoder(DDSDecoder):
    


class PNG_Decoder(PygletDecoder):    
    def _pixbuf_to_image(self, pixbuf):
        
        # Get format and dimensions
        self.width = gdkpixbuf.gdk_pixbuf_get_width(pixbuf)
        self.height = gdkpixbuf.gdk_pixbuf_get_height(pixbuf)
        channels = gdkpixbuf.gdk_pixbuf_get_n_channels(pixbuf)
        rowstride = gdkpixbuf.gdk_pixbuf_get_rowstride(pixbuf)
        pixels = gdkpixbuf.gdk_pixbuf_get_pixels(pixbuf)
        
        # Copy pixel data.        
        buffer = (c_ubyte * (rowstride * self.height))()
        memmove(buffer, pixels, rowstride * (self.height - 1) + self.width * channels)
        
        # Release pixbuf
        gdk.g_object_unref(pixbuf)

        # Determine appropriate GL type
        if channels == 3:
            self.format = 'RGB'
        else:
            self.format = 'RGBA'
        
        self.data = np.frombuffer( buffer, 'B').reshape(self.height,self.width,channels)
        
        return self

def optimized_image_load(filename, flipped=True):
    
    file = open(filename, 'rb')
    
    if not hasattr(file, 'seek'):
        print "CAREFUL: COPY in StringIO"
        file = StringIO(file.read())
    
    try:
        decoder= PNG_Decoder()
        decoded_image = decoder.decode(file, filename)
        
    except:
        file.seek(0)
        decoder= CustomPILDecoder()
        decoded_image = decoder.decode(file, filename)
        
    if flipped:
        decoded_image.data=decoded_image.data[::-1]
        
    return decoded_image

