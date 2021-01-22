
from .ModuleFactory import *

from .Log import Log
import logging
import sys

import wqc

log = Log(__name__)

class ModuleImpl6502(ModuleImplBase):
    def __init__(self, **kwargs):
        #log.warn("Hello from log")
        #self._6502desc = wqc.c6502_init()
        self._opened = None
        super(ModuleImpl6502,self).__init__(**kwargs)

    def __del__(self):
        log.warn("Hello from del")
        super(ModuleImpl6502,self).__init__()
    '''
    def __getattr__(self, name):
        return name

    def __setattr__(self, name:str, value):
        print("setting atrrr:"+str(name)+str(value))   
    '''   

    def echo(self):
        print("Hello World from 6502")

    def init(self,initParms:dict) -> dict:
        self._init = wqc.c6502_init(initParms)
        return self._init
    
    def open(self):
        if self._opened == None:
            self._opened = wqc.c6502_open()
        return self._opened

    def calc(self):
        self._opened['pins'] = wqc.c6502_calc(self._opened['iv'],self._opened['pins']); 
        return self._opened['pins']

@ModuleFactory.registerLibrary('wqc')
class ModuleLibraryWqc(ModuleLibraryBase):

    _modules = {
        "c6502":ModuleImpl6502
    }

    @classmethod
    def createModule(cls, moduleName: str, **kwargs) -> 'ModuleImplBase':
        """ Runs the given command using subprocess """

        if moduleName not in cls._modules:
            #log.warn('Module %s does not exist in the library', name)
            return None


        module_class = cls._modules[moduleName]
        moduleImpl = module_class(**kwargs)
        return moduleImpl

if __name__ == '__main__':
    #for handler in logger.handlers:
    #    filename = handler.baseFilename
    #    print(filename)
    # Creates a local library
    print
    wqcLib = ModuleFactory.loadLibrary('wqc')
    # ... then some modules ...
    test1 = wqcLib.createModule('test1')
    test2 = wqcLib.createModule('test2')
    c6502 = wqcLib.createModule('c6502')
    # ... and finally access some methods ...
    test1.echo()
    test2.echo()
    c6502.echo() 

    #res = c6502.testAttr

    print(res)

    res = c6502.init({
        'empty':"dupa"
        })

    print(res) 

    cpu = c6502.open() 

    import time

    def set_bit(value, bit):
        return value | (1<<bit)

    def clear_bit(value, bit):
        return value & ~(1<<bit)

    def hex64(n):
        return hex (n & 0xffffffffffffffff) #[:-1]    

    print(cpu) 
    start = time.time()
    for i in range(0,40,1):
        cpu = c6502.calc()
        print(f'hex64:{hex64(cpu)}')  
        cpu = set_bit(cpu,63)
    stop = time.time()
    print(f'Calculated in {stop-start}s')   