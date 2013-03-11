#! /usr/bin/env python
# *-* coding: UTF-8 *-*

import weakref

class cVars:
    id=-1    
    __objects_by_Name__=weakref.WeakValueDictionary()
    __objects_by_Id__= weakref.WeakValueDictionary()
    
    isCygnusInitialized = False
