from abc import ABCMeta, abstractmethod
import logging
from typing import Callable

#from . import ModuleLibraryWqc

from .nodeiotype import NodeIoType
from .moduletype import ModuleType
from . import direction, consts


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
        impla = modulePath.split(':')
        lib = ModuleFactory.loadLibrary(impla[0])
        assert lib != None, f'Problem with loading module library type:{impla[0]}'
        result = lib.createModule(impla[1])
        assert result != None, f'Problem with loading module:{impla[1]} from library type:{impla[0]}'
        result._implStr = modulePath
        return result


IoType = NodeIoType

from .EventSignal import EventSignal, EventBase, EventProps

from .ionodeflags import IoNodeFlags

class EventNameChanged:
    def __init__(self, oldName:str, newName:str):
        self._oldName = oldName
        self._newName = newName

class EventIONameChanged:
    def __init__(self,fromName,toName,lid,isInput):
        self._fromName = fromName
        self._toName = toName
        self._lid = lid
        self._isInput = isInput

class EventIOTypeChanged:
    def __init__(self, isInput, ioId, osize, tsize):
        self._isInput = isInput
        self._ioId = ioId
        self._oldSize = osize
        self._newSize = tsize

class ModuleImplBase(metaclass=ABCMeta):
    class Events(EventBase):
        elementNameChanged = EventSignal(EventNameChanged)
        inputAdded = EventSignal(EventProps)
        outputAdded = EventSignal(EventProps)
        ioNodeAdded = EventSignal(EventProps)
        ioNameChanged = EventSignal(EventIONameChanged)
        inputRemoved = EventSignal(EventProps)
        outputRemoved = EventSignal(EventProps)
        ioTypeChanged = EventSignal(EventIOTypeChanged)
        ioNodeRemoved = EventSignal(EventProps)
        pass    
    def __init__(self, **kwargs):
        """ Constructor """
        self._isIconified = False 
        self._iconifyingHidesCentralWidget = False 
        self._self = None
        self._moduleType = None 
        self._events = ModuleImplBase.Events()  
        self._implStr = None #path in lib (if aplies) 
        self._defaultFlags = IoNodeFlags()
        #self._defaultOutputFlags = IoNodeFlags(max=consts.MAX_OUTPUTS)
        #self._defaultDynamicFlags = IoNodeFlags(max=consts.MAX_DYNAMICS)    
        pass

    #@deprecated-start - replace with IoNodeFlags
    #uint8_t defaultNewInputFlags() const { return m_defaultNewInputFlags; }
    #def defaultNewInputFlags(self):
    #    return self.m_defaultNewInputFlags

    #def setDefaultNewInputFlags(self, flags):
    #    self.m_defaultNewInputFlags = flags

    #def defaultNewOutputFlags(self):
    #    return self.m_defaultNewOutputFlags

    #def setDefaultNewOutputFlags(self, flags):
    #    self.m_defaultNewOutputFlags = flags

    #@deprecated -> defaultFlags(dir).min()
    def minInputs(self):
        #return self._minInputs
        return self.defaultFlags(NodeIoType.INPUT).min()
    
    #@deprecated -> limitsIoNodes(dir).max()
    def maxInputs(self):
        #return self._maxInputs
        return self.defaultFlags(NodeIoType.INPUT).max()
    
    def minOutputs(self):
        #return self._minOutputs
        return self.defaultFlags(NodeIoType.OUTPUT).min()
        
    def maxOutputs(self):
        #return self._maxOutputs
        return self.defaultFlags(NodeIoType.OUTPUT).max()



    def setMinInputs(self, min):
        #if (min > self.maxInputs()):
        #    return
        #self._minInputs = min
        self.defaultFlags(NodeIoType.INPUT).setIfMin(min)
    
    def setMaxInputs(self, max):
        #if (max < self.minInputs()):
        #    return
        #self._maxInputs = max
        self.defaultFlags(NodeIoType.INPUT).setIfMax(max)

    def setMinOutputs(self, min):
        #if (min > self._maxOutputs):
        #    return
        #self._minOutputs = min
        self.defaultFlags(NodeIoType.OUTPUT).setIfMin(min)

    def setMaxOutputs(self, max):
        #if (max < self._minOutputs):
        #    return
        #self._maxOutputs = max 
        self.defaultFlags(NodeIoType.OUTPUT).setIfMax(max)
        
    def setIconifyingHidesCentralWidget(self, hide):
        self._iconifyingHidesCentralWidget = hide
        
    def iconifyingHidesCentralWidget(self):
        return self._iconifyingHidesCentralWidget
    #@deprecated-stop

    def defaultFlags(self,dir:direction.Dir):
        #if (NodeIoType.INPUT == ioType):
        #    return self._defaultInputFlags
        #elif NodeIoType.OUTPUT == ioType:
        #    return self._defaultOutputFlags
        #else:
        return self._defaultFlags

    def acceptVisitor(self, v):
        v.visitModuleImpl(self)

    def s(self):
        return self._self

    def mdl(self):
        return self._self

    def events(self):
        return self._events

    def id(self):
        return self._self.id()

    def name(self):
        return self._self.name()

    def setName(self, name):
        if self._self.name() != name:
            self._self.setName(name)

    def description(self):
        return self.desc()

    def desc(self):
        return self._self.desc()
    
    def info(self):
        return self._self.info()

    def raiseExc(self, a0):
        raise Exception(a0)   

    def moduleType(self):
        return self._moduleType


    @abstractmethod
    def init(self,**kwargs):    
        pass

    @abstractmethod
    def open(self,**kwargs):    
        pass

    @abstractmethod
    def calc(self,**kwargs):    
        pass

    def newIO(self, **kwargs):
        result=self.s().newIO(**kwargs)
        dir = result.dir()
        if dir in [direction.TOP,direction.DOWN]:
            self.events().ioNodeAdded.emit(EventProps({'nodeId':result.id()}))
        elif dir == direction.LEFT:
            self.events().inputAdded.emit(EventProps({'inputId':result.id()}))
        else:
            self.events().outputAdded.emit(EventProps({'outputId':result.id()}))
        return result

    def removeIO(self, id): #todo event emmiter
        return self.s().removeIO(id)    

    def sig(self, name:str):
        ts = self.s()
        return ts.sigByName(name) 

    def iconify(self, iconify):
        self._isIconified = iconify

    def isIconified(self):
        return self._isIconified


    
    def nodes(self):
        return self.s().nodes()

    def nodesByDir(self, dir:direction.Dir):
        return self.nodes().filterBy('dir',dir)

    #'inputs' is historical name deprecated in fact it is ionode on left !TODO! remimplement using nodes() vector
    #@deprecated
    def inputs(self):
        #return self.nodes().filterBy('direction',direction.LEFT)
        return self.nodesByDir(direction.LEFT)

    #@deprecated
    def outputs(self):
        #return self.s().nodes().filterBy('direction',direction.RIGHT)
        return self.nodesByDir(direction.RIGHT)

  

    def reset(self):
        pass 

    def updateTiming(self, delta):
        pass 



class ModuleImplBaseLocal(ModuleImplBase):
    def __init__(self, **kwargs):
        super(ModuleImplBaseLocal, self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC #default moduletype


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


class AndGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from AndGateModule")

    def init(self,**kwargs):
        return {
            'name':'AND',
            'info':'AND logic gate'    
        }

    def open(self,**kwargs):
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

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v2 = s.sig('B').value()
        v3 = v1 and v2
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}')   
        # 


class NorGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from NorGateModule")

    def init(self,**kwargs):
        return {
            'name':'NOR',
            'info':'NOR logic gate'    
        }

    def open(self,**kwargs):
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

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v2 = s.sig('B').value()
        v3 = True if not (v1 or v2) else False
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}')   
        # 
        
class NotGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from NotGateModule")

    def init(self,**kwargs):
        return {
            'name':'NOT',
            'info':'NOT logic gate'    
        }

    def open(self,**kwargs):
        #result = AndGateModule()
        y = self.newIO(
            name='Y',
            ioType = IoType.OUTPUT
            )
        a = self.newIO(
            name='A',
            ioType=IoType.INPUT
        )   
        return {
            'Y':y,
            'A':a
        }

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v3 = not v1 
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}') 
        # 
        # 

class TestGModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from TestGraphModule")

    def init(self,**kwargs):
        return {
            'name':'TESTG',
            'info':'TESTG Graph module'    
        }

    def open(self,**kwargs):
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
        c = self.newIO(
            name='C',
            ioType=IoType.INPUT
        )         


        return {
            'Y':y,
            'A':a,
            'B':b,
            'C':c
        }

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v3 = not v1 
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}')   

class Test2Module(ModuleImplBase):
    def echo(self):
        print("Hello World from test2")

@ModuleFactory.registerLibrary('local')
class LocalModuleLibrary(ModuleLibraryBase):

    _modules = {
        "AND":AndGateModule,
        "NOT":NotGateModule,
        "NOR":NorGateModule,
        "TESTG":TestGModule,
        "test2":Test2Module
    }

    @classmethod
    def createModule(cls, moduleName: str, **kwargs) -> 'ModuleImplBase':
        """ Runs the given command using subprocess """

        #strip slash
        moduleName = moduleName[1:] if moduleName != None and moduleName.startswith('/') else moduleName

        if moduleName not in cls._modules:
            #log.warn('Module %s does not exist in the library', name)
            return None


        module_class = cls._modules[moduleName]
        moduleImpl = module_class(**kwargs)
        return moduleImpl


@ModuleFactory.registerLibrary('file')
class FileModuleLibrary(ModuleLibraryBase):


    @classmethod
    def createModule(cls, moduleName: str, **kwargs) -> 'ModuleImplBase':

        assert False, f'Problem loading module:{moduleName} - currently no implementation of module library type ''file'''



if __name__ == '__main__':

    # Creates a local library
    #https://www.geeksforgeeks.org/logic-gates-in-python/
    local = ModuleFactory.loadLibrary('local')
    # ... then some modules ...
    test1 = local.createModule('test1')
    test2 = local.createModule('test2')
    # ... and finally access some methods ...
    test1.echo()
    test2.echo()