from . import consts
from .drivers.ui import pyqt5 as drvQt
from .drivers.ui import wxWidgets as drvWx
from .drivers import loader as wqLoader

class Object():
    def __new__(cls, *args, **kwargs):
        result = object.__new__(cls)
        result._args = args
        result._kwargs = kwargs
        tParent = result._loadParent(*args, **kwargs)
        tImpl = result._loadImpl(*args, **kwargs)
        tWqImpl = kwargs['wqImpl'] if 'wqImpl' in kwargs else consts.WQ_IMPL
        result._wqD = result.__loadWqDriver(tParent,tImpl,tWqImpl)        
        return result

    def __init__(self, parent, impl, **kwargs):
        self._props = {}
        wqD = kwargs['wqD'] if 'wqD' in kwargs else None
        wqImpl = kwargs['wqImpl'] if 'wqImpl' in kwargs else None
        if wqD != None:
            self._wqD = wqD
        else:
            if wqImpl == None and self._wqD == None:
                self.raiseNoImpl('Object','init -> wqImpl required')
            
        if (self._wqD != None and (impl == None or isinstance(impl, str))):#load implementation from string if given
            tClName = self.__class__.__name__ #if impl == None else impl
            tMethod = getattr(self._wqD, "do"+tClName+"_Init",None)
            if tMethod == None and isinstance(impl, str):
                self.raiseNoImpl('Object',f'init - no driver implementation found for {tClName}')
            if tMethod!=None:
                impl = tMethod()                    
        self._object = impl
        self._impl = self._object
        #if  self._impl != None:
        #    self._impl._wqob = self
        if (self._wqD._impl==None):
            self._wqD._impl=self._impl
        self._parent = parent
        if (self._wqD._parent==None):
            self._wqD._parent=self._parent
        #if wqImpl==None:
        #    wqImpl = self._wqD._wqImpl
        #self._wqImpl = wqImpl

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

    def __loadWqDriver(self,parent,impl,wqImpl):
        if wqImpl == None:
            wqImpl = parent._wqImpl if parent != None and hasattr(parent,'_wqImpl') else consts.WQ_IMPL
        self._wqImpl = wqImpl
        WqDriver = wqLoader.loadWqDriver(self._wqImpl)
        '''
        if self.isQt(wqImpl):
            result = drvQt.WqDriver(self,parent,impl)
        else:
            result = drvWx.WqDriver(self,parent,impl)
        '''
        result = WqDriver(self,parent,impl)
        return result

    def wqD(self):
        return self._wqD

    def implObject(self):
        return self.impl()

    def impl(self):
        return  self._impl 

    def parent(self):
        return self._parent  

    def isQt(self, wqImpl=None):
        result = (consts.WQ_IMPL_QT == self._wqImpl) if (wqImpl == None) else (consts.WQ_IMPL_QT == wqImpl)
        return result

    def isWx(self, wqImpl=None):
        result = (consts.WQ_IMPL_WX == self._wqImpl) if (wqImpl == None) else (consts.WQ_IMPL_WX == wqImpl)
        return result

    def prop(self,propName):
        result = self._props[propName] if propName in self._props else None
        return result
    
    def setProp(self, propName, propValue):
        self._props[propName] = propValue
        return self

    def setObjectName(self,name:str):
        result = self.impl().setObjectName(name) if self.isQt() else self.raiseNoImpl('Object','setObjectName')
        #result = self.wqD().doObject_SetObjectName(name)

    def raiseNoImpl(self, a0, a1):
        raise Exception(a0, a1 + ' -> noImpl')

    def raiseExc(self, a0):
        raise Exception(a0)