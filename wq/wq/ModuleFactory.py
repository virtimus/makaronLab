from abc import ABCMeta, abstractmethod
import logging
from typing import Callable

#from . import ModuleLibraryWqc

from .nodeiotype import NodeIoType
from .moduletype import ModuleType

log = logging.getLogger(__name__)

class ModuleFactory:

    _registeredLibraries = {}

    _loadedLibraries = {}


    @classmethod
    def registerLibrary(cls, name: str) -> Callable:
        """ Class method to register Library class to the internal registry.
        Args:
            name (str): The name of the library
        Returns:
            The Library class itself.
        """

        def inner_wrapper(wrapped_class: ModuleLibraryBase) -> Callable:
            if name in cls._registeredLibraries:
                log.warn('Library %s already exists. Will replace it', name)
            cls._registeredLibraries[name] = wrapped_class
            return wrapped_class

        return inner_wrapper


    @classmethod
    def loadLibrary(cls, name: str, **kwargs) -> 'ModuleLibraryBase':
        """ Factory command to create the library.
        This method gets the appropriate Library class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the library to create.
        Returns:
            An instance of the library that is created.
        """

        if name not in cls._registeredLibraries:
            #log.warn('Library %s does not exist in the registry', name)
            return None

        if name in cls._loadedLibraries:
            return cls._loadedLibraries[name]
        else:
            exec_class = cls._registeredLibraries[name]
            library = exec_class(**kwargs)
            cls._loadedLibraries[name] = library
            return library  

    @classmethod
    def createModule(cls, modulePath:str):
        impla = modulePath.split('/')
        lib = ModuleFactory.loadLibrary(impla[0])
        result = lib.createModule(impla[1])
        return result


IoType = NodeIoType

class ModuleImplBase(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        """ Constructor """
        self._self = None
        self._moduleType = ModuleType.ATOMIC #default moduletype
        pass

    def s(self):
        return self._self

    def raiseExc(self, a0):
        raise Exception(a0)   

    def moduleType(self):
        return self._moduleType     

    @abstractmethod
    def echo(self):
        pass

    def newIO(self, **kwargs):
        tname = kwargs['name'] if 'name' in kwargs else None
        if tname == None:
            self.raiseExc('Name required')
        tsize = kwargs['size'] if 'size' in kwargs else 1
        tIoType = kwargs['ioType'] if 'ioType' in kwargs else None
        sig = self.s().newSignal(name=tname,size=tsize)
        result = self.s().newIoNode(signal=sig, ioType=tIoType)
        return result

    def sig(self, name:str):
        ts = self.s()
        return ts.sigByName(name)
    






class ModuleLibraryBase(metaclass=ABCMeta):
    """ Base class for an library """

    _modules = {}

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    @abstractmethod
    def createModule(self, moduleName: str, **kwargs) -> 'ModuleImplBase':
        """ Abstract method to create a module """
        pass

    @classmethod
    def listModules(cls):
        return cls._modules


class AndGateModule(ModuleImplBase):
    def echo(self):
        print("Hello World from AndGateModule")

    def init(self,**kwargs):
        return {
            'name':'AND',
            'info':'AND logic gate'    
        }

    def open(self):
        #result = AndGateModule()
        y = self.newIO(
            name='Y',
            ioType = IoType.OUTPUT
            )
        a = self.newIO(
            name='A',
            ioType=IoType.INPUT
        )   
        b = self.newIO(
            name='B',
            ioType=IoType.INPUT
        )
        return {
            'Y':y,
            'A':a,
            'B':b
        }

    def calc(s):
        s.sig('Y').setValue(s.sig('A').value() and s.sig('B').value())    

class Test2Module(ModuleImplBase):
    def echo(self):
        print("Hello World from test2")

@ModuleFactory.registerLibrary('local')
class LocalModuleLibrary(ModuleLibraryBase):

    _modules = {
        "AND":AndGateModule,
        "test2":Test2Module
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

    # Creates a local library
    local = ModuleFactory.loadLibrary('local')
    # ... then some modules ...
    test1 = local.createModule('test1')
    test2 = local.createModule('test2')
    # ... and finally access some methods ...
    test1.echo()
    test2.echo()