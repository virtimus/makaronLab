from abc import ABCMeta, abstractmethod
import logging
from typing import Callable

#from . import ModuleLibraryQ3c

from .nodeiotype import NodeIoType
from .moduletype import ModuleType
from . import direction, consts

from operator import xor

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
        libName = impla[0]
        moduleName = impla[1]
        moduleName = moduleName[1:] if moduleName != None and moduleName.startswith('/') else moduleName
        lib = ModuleFactory.loadLibrary(libName)
        assert lib != None, f'Problem with loading module library type:{libName}'
        result = lib.createModule(moduleName)
        assert result != None, f'Problem with loading module:{moduleName} from library type:{libName}'
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

from .EventSignal import SyncHandler, DoneItem
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
        moduleDoubleClicked = EventSignal(EventProps)
        detailWindowResized = EventSignal(EventProps)
        callDetailWindowCloseReq = SyncHandler()
        consoleWrite = EventSignal(EventProps)
        nodeConnectionRequest = EventSignal(EventProps)
        itemPositionHasChanged = EventSignal(EventProps)


        def emitOutputAdded(self,d:dict):
            d['eventName']='outputAdded'
            #doneItem = DoneItem()
            #DoneItem.emitAndWaitForDone(self.outputAdded,EventProps(d))
            #d['doneItem']=doneItem
            #self.outputAdded.emit(EventProps(d)) 
            #doneItem.waitForDone()
            self.outputAdded.emit(EventProps(d))

        def emitItemPositionHasChanged(self, d:dict):
            d['eventName']='itemPositionHasChanged' 
            self.itemPositionHasChanged.emit(EventProps(d))
        def emitNodeConnectionRequest(self, d:dict):
            #!TODO! validation, waiting for response?
            d['eventName']='nodeConnectionRequest' 
            self.nodeConnectionRequest.emit(EventProps(d))
   
    def __init__(self, **kwargs):
        """ Constructor """
        #self._isCollapsed = False todel 
        self._hideCWOnCollapse = True 
        self._self = None
        self._moduleType = None 
        self._events = ModuleImplBase.Events()  
        self._implStr = None #path in lib (if aplies) 
        self._defaultFlags = IoNodeFlags()
        self._dtwProps = None
        self._customProperties = {}
        self._centralWidget = None
        #self._defaultOutputFlags = IoNodeFlags(max=consts.MAX_OUTPUTS)
        #self._defaultDynamicFlags = IoNodeFlags(max=consts.MAX_DYNAMICS)    
        pass

    def customProperties(self):
        return self._customProperties

    def centralWidget(self):
        return self._centralWidget

    def showDetailWindow(self,**kwargs):
        pass

    def consoleWrite(self, text:str):
        self.events().consoleWrite.emit(EventProps({'text':text}))

    def cw(self, text:str):
        return self.consoleWrite(text)
        
    def setHideCWOnCollapse(self, hide):
        self._hideCWOnCollapse = hide
        
    def hideCWOnCollapse(self):
        return self._hideCWOnCollapse
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

    def mdlv(self):
        return self._self.view()

    def console(self):
        return self.mdlv().impl().console()

    def events(self):
        return self._events
        #return self.events

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
            #self.events().outputAdded.emit(EventProps({'outputId':result.id()}))
            self.events().emitOutputAdded({'outputId':result.id()}) # this can wait for async depending if doneItem used
        return result

    def removeIO(self, id): #todo event emmiter
        return self.s().removeIO(id)    

    def signals(self,by=None):
        return self.mdl().signals(by)
    
    def sigs(self,by=None):
        return self.mdl().sigs(by)

    def sig(self,by):
        return self.mdl().sig(by)
    
    def nodes(self,by=None):
        return self.mdl().nodes(by)

    def nods(self,by=None):
        return self.mdl().nods(by)

    def nod(self,by):
        return self.mdl().nod(by)

    def nodesByDir(self, dir:direction.Dir):
        return self.nodes().filterBy('dir',dir)

    def modules(self,by=None):
        return self.mdl().modules(by)

    def mods(self,by=None):
        return self.mdl().mods(by)

    def mod(self,by):
        return self.mdl().mod(by)

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

class And4GateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from AndGateModule")

    def init(self,**kwargs):
        return {
            'name':'AND4',
            'info':'AND4 logic gate'    
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
        d = self.newIO(
            name='D',
            ioType=IoType.INPUT
        )
        return {
            'Y':y,
            'A':a,
            'B':b,
            'C':c,
            'D':d
        }

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v2 = s.sig('B').value()
        v3 = s.sig('C').value()
        v4 = s.sig('D').value()
        vY = v1 and v2 and v3 and v4
        sY = s.sig('Y')
        sY.setValue( vY )
        #print(f'sY={sY.value()}')   
        # 


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

class NandGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from NandGateModule")

    def init(self,**kwargs):
        return {
            'name':'NAND',
            'info':'NAND logic gate'    
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
        v3 = not (v1 and v2)
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}')   
        # 

class Nand4GateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from NandGateModule")

    def init(self,**kwargs):
        return {
            'name':'NAND4',
            'info':'NAND4 logic gate'    
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
        d = self.newIO(
            name='D',
            ioType=IoType.INPUT
        )
        e = self.newIO(
            name='E',
            ioType=IoType.INPUT
        )
        return {
            'Y':y,
            'A':a,
            'B':b,
            'C':c,
            'D':d,
            'E':e
        }

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v2 = s.sig('B').value()
        v3 = s.sig('C').value()
        v4 = s.sig('D').value()
        v5 = s.sig('E').value()
        vY = not (v1 and v2 and v3 and v4 and v5)
        sY = s.sig('Y')
        sY.setValue( vY )
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
        
class Nor4GateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from NorGateModule")

    def init(self,**kwargs):
        return {
            'name':'NOR4',
            'info':'NOR4 logic gate'    
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
        d = self.newIO(
            name='D',
            ioType=IoType.INPUT
        )
        return {
            'Y':y,
            'A':a,
            'B':b,
            'C':c,
            'D':d
        }

    def calc(s, **kwargs):
        v1 = s.sig('A').value()
        v2 = s.sig('B').value()
        v3 = s.sig('C').value()
        v4 = s.sig('D').value()
        vY = True if not (v1 or v2 or v3 or v4) else False
        sY = s.sig('Y')
        sY.setValue( vY )
        #print(f'sY={sY.value()}')   
        # 

class OrGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from OrGateModule")

    def init(self,**kwargs):
        return {
            'name':'OR',
            'info':'OR logic gate'    
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
        v3 = True if (v1 or v2) else False
        sY = s.sig('Y')
        sY.setValue( v3 )
        #print(f'sY={sY.value()}')   
        # 
        # 
class XorGateModule(ModuleImplBaseLocal):
    def echo(self):
        print("Hello World from XorGateModule")

    def init(self,**kwargs):
        return {
            'name':'XOR',
            'info':'XOR logic gate'    
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
        vY = True if xor(v1,v2) else False
        sY = s.sig('Y')
        sY.setValue( vY )
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
        "AND4":And4GateModule,
        "NOT":NotGateModule,
        "NOR":NorGateModule,
        "NOR4":Nor4GateModule,
        "OR":OrGateModule,
        "XOR":XorGateModule,
        'NAND':NandGateModule,
        'NAND4':Nand4GateModule,
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