from . import consts, console
from .drivers.ui import pyqt5 as drvQt
from .drivers.ui import wxWidgets as drvWx
from .drivers import loader as q3Loader

from .Log import Log
log = Log(__name__)

class Object():
    def __new__(cls, *args, **kwargs):
        result = object.__new__(cls)
        result._args = args
        result._kwargs = kwargs
        tParent = result._loadParent(*args, **kwargs)
        tImpl = result._loadImpl(*args, **kwargs)
        tQ3Impl = kwargs['q3Impl'] if 'q3Impl' in kwargs else consts.Q3_IMPL
        result._q3D = result.__loadQ3Driver(tParent,tImpl,tQ3Impl)        
        return result

    def __init__(self, parent, impl, **kwargs):
        self._parent = parent
        #kwargs['props'] if 'props' in kwargs else {}
        self._props = self._initHandleArg('props',
            kwargs = kwargs,
            default = {},
            desc = 'Additional dynamic properties not defined in model'
            )
        #kwargs['q3D'] if 'q3D' in kwargs else None
        q3D = self._initHandleArg('q3D',
            kwargs = kwargs,
            desc = 'Indstance of implementation driver/factory for model elements'
        )
        q3Impl = self._initHandleArg('q3Impl',
            kwargs = kwargs,
            desc = 'Implementation driver/factory path/class'
        )
        if q3D != None:
            self._q3D = q3D
        else:
            if q3Impl == None and self._q3D == None:
                self.raiseNoImpl('Object','init -> q3Impl required')
            
        if (self._q3D != None and (impl == None or isinstance(impl, str))):#load implementation from string if given
            tClName = self.__class__.__name__ #if impl == None else impl
            tMethod = getattr(self._q3D, "do"+tClName+"_Init",None)
            if tMethod == None and isinstance(impl, str):
                self.raiseNoImpl('Object',f'init - no driver implementation found for {tClName}')
            if tMethod!=None:
                impl = tMethod() 
            else:
                #dclass = self._q3D.__class__
                #log.warn(f'[init] No implementation found for class:{tClName} driver class:{dclass}') 
                pass                  
        self._object = impl
        self._impl = self._object
        if (self._q3D._impl==None):
            self._q3D._impl=self._impl
        
        if (self._q3D._parent==None):
            self._q3D._parent=self._parent


    def _initHandleArg(self, name:str, **kwargs):
        return console.handleArg(self, name,**kwargs)


    def _loadParent(self,*args, **kwargs): 
        tParent = args[0] if  len(args)>0 else None
        if tParent == None:
            tParent = kwargs['parent'] if 'parent' in kwargs else None
        return tParent

    def _loadImpl(self,*args, **kwargs):
        tImpl = args[1] if len(args)>1 else None
        if tImpl == None:
            tImpl = kwargs['impl'] if 'impl' in kwargs else None  
        return tImpl


    def _loadInitArgs(self, args):
        if len(args)<1:
            args = (None, None)
        if len(args)<2:
            args = (args[0],None)  
        return args    

    def __loadQ3Driver(self,parent,impl,q3Impl):
        if q3Impl == None:
            q3Impl = parent._q3Impl if parent != None and hasattr(parent,'_q3Impl') else consts.Q3_IMPL
        self._q3Impl = q3Impl
        Q3Driver = q3Loader.loadQ3Driver(self._q3Impl)
        '''
        if self.isQt(q3Impl):
            result = drvQt.Q3Driver(self,parent,impl)
        else:
            result = drvWx.Q3Driver(self,parent,impl)
        '''
        result = Q3Driver(self,parent,impl)
        return result

    def q3D(self):
        return self._q3D

    def implObject(self):
        return self.impl()

    def impl(self):
        return  self._impl 

    def parent(self):
        return self._parent  

    def isQt(self, q3Impl=None):
        result = (consts.Q3_IMPL_QT == self._q3Impl) if (q3Impl == None) else (consts.Q3_IMPL_QT == q3Impl)
        return result

    def isWx(self, q3Impl=None):
        result = (consts.Q3_IMPL_WX == self._q3Impl) if (q3Impl == None) else (consts.Q3_IMPL_WX == q3Impl)
        return result

    def prop(self,propName):
        result = self._props[propName] if propName in self._props else None
        return result
    
    def props(self,propName):
        return self.prop(propName);
    
    def setProp(self, propName, propValue):
        self._props[propName] = propValue
        return self

    def setObjectName(self,name:str):
        result = self.impl().setObjectName(name) if self.isQt() else self.raiseNoImpl('Object','setObjectName')
        #result = self.q3D().doObject_SetObjectName(name)

    def raiseNoImpl(self, a0, a1):
        raise Exception(a0, a1 + ' -> noImpl')

    def raiseExc(self, a0):
        raise Exception(a0)