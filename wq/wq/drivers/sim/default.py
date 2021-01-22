
from ...ModuleFactory import ModuleFactory
from ..driverBase import WqDriverBase

class WqDriver(WqDriverBase):


    def doModule_Init(self):
        result = None
        name = self.s().name()
        print(f'hello from doModule_Init! name:{name}')
        impl = self.s()._kwargs['impl'] if 'impl' in self.s()._kwargs else None
        if isinstance(impl,str): #// we have path to module impl
            impla = impl.split('/')
            lib = ModuleFactory.loadLibrary(impla[0])
            result = lib.createModule(impla[1])
            result._self = self.s()
            self._modImplInit = result.init()
            self._modImplOpen = result.open()            
        return result