from ... import direction, consts

from ...ModuleFactory import IoType, ModuleFactory, ModuleImplBase, ModuleType
from ..driverBase import Q3DriverBase

from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, pyqtSignal as EventSignal

#import PyQt5.QtWidgets as qtw
#import PyQt5.QtCore as qtc
#import PyQt5.QtGui  as qtg

from ...valuetype import ValueType

from .ModuleImplElement import ModuleImplElement    
from .ModuleImplGraph import ModuleImplGraph
from .ModuleImplIO import ModuleImplIO

class Q3Driver(Q3DriverBase):

    def doModule_Init(self):
        result = None
        name = self.s().name()
        print(f'Hello from doModule_Init! name:{name}')
        impl = self.s()._kwargs['impl'] if 'impl' in self.s()._kwargs else None
        if isinstance(impl,str): #// we have path to module impl
            result = ModuleFactory.createModule(impl)
            result._self = self.s()
            self._modImplInit = result.init()
            if 'info' in self._modImplInit:
                result._self._info = self._modImplInit['info']
            self._modImplOpen = result.open() 
        elif self.s().isRoot(): #impl for root module (package?)
            result = ModuleImplGraph(moduleType=self.s().moduleType())
            result._self = self.s()
            pass
        elif self.s().moduleType() == ModuleType.GRAPH:
            result = ModuleImplGraph(moduleType=self.s().moduleType())
            result._self = self.s()
            #result.newIO(name="T",ioType=IoType.INPUT)
        elif self.s().moduleType() in [ModuleType.IO]:
            result = ModuleImplIO(moduleType=self.s().moduleType())
            result._self = self.s()    
            result.m_package = self.s().parent().impl()          
        else: #!TODO! impl for non root module (element) or maybe chace if atomic and exception unhandled?
            result = ModuleImplElement(moduleType=self.s().moduleType())
            result._self = self.s()
            result.m_package = self.s().parent().impl()
            pass
        result._self = self.s()
        self.callAfterInit(result)
        return result