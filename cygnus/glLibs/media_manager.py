
class ImageLoader(dict):
    def __init__(self, name=None, isCollection=False):
        dict.__setattr__(self, 'cache', {})
        dict.__setattr__(self, 'name', name)
        dict.__setattr__(self, 'isCollection', isCollection)
        
    def __setattr__(self, name, value):
        
        instancetype, filename, args = value[0], value[1], value[2:]
        
        if (args and isinstance(args[-1], dict) ):
            kwargs = args[-1]
            args = args[:-1]
        else :
            kwargs = {}
            
        self.cache[name]=(instancetype, filename, args, kwargs)
        
    def Register(self, name, instancetype, file, *args, **kwargs):
        assert isinstance(name, basestring), "Name sould be string instance not {0}".format(type(name))
        self.cache[name]=(instancetype, file, args, kwargs)
        
    def RegisterCollections(self, name, collection):
        assert isinstance(name, basestring), "Name sould be string instance not {0}".format(type(name))
        
        self[name]=ImageLoader(name=name, isCollection=True)
        for image in collection:
            self[name].Register(*image)
        
    def __getitem__(self, name):
        if isinstance(name, basestring):
            try:
                return dict.__getitem__(self, name)         
            except KeyError:
                try:
                    instancetype, file, args, kwargs = self.cache[name]
                except KeyError:
                    raise KeyError("Name {0} not referenced in Database named '{2}' {1} ".format(name, self, self.name) )
                
                self[name]=instancetype(file, *args, **kwargs)
                
                return dict.__getitem__(self, name) 
        else:
            collection, name =  name
            
            try:
                COLLECTION =  dict.__getitem__(self, collection)         
            except KeyError:
                raise KeyError("Collection Name {0} not referenced in Database {1} ".format(collection, self) )
            
            return COLLECTION.__getitem__(name)

class ImagesManager(ImageLoader):
    def __init__(self):
        ImageLoader.__init__(self)
        
    def GetTexture(self, filename, instancetype, *args, **kwargs):
        if not filename in self:
            self.Register(filename, instancetype, filename, *args, **kwargs)
        
        return self[filename]

