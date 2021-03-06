
from .ModuleFactory import *

from .Log import Log
import logging
import sys




from .Signal import Signal

from .Timer import Timer


log = Log(__name__)

#from bitstring import BitStream, BitArray

from .Q3Chips.ModuleImpl6502 import ModuleImpl6502
from .Q3Chips.ModuleImplClock import ModuleImplClock
from .Q3Chips.ModuleImplCPC import ModuleImplCPC
from .Q3Chips.ModuleImplAT28C256 import ModuleImplAT28C256
from .Q3Chips.ModuleImpl6522 import ModuleImpl6522
from .Q3Chips.ModuleImplRAM62256 import ModuleImplRAM62256

@ModuleFactory.registerLibrary('Q3Chips')
class ModuleLibraryQ3Chips(ModuleLibraryBase):

    _modules = {
        "c6502":ModuleImpl6502,
        "C6502":ModuleImpl6502,
        "CPC":ModuleImplCPC,
        "Clock":ModuleImplClock,
        'AT28C256':ModuleImplAT28C256,
        "C6522":ModuleImpl6522,
        "RAM62256":ModuleImplRAM62256,
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
    #print
    q3cLib = ModuleFactory.loadLibrary('q3c')
    # ... then some modules ...
    test1 = q3cLib.createModule('test1')
    test2 = q3cLib.createModule('test2')
    c6502 = q3cLib.createModule('c6502')
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