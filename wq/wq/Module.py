
#from .Signal import Signal
from .Object import Object
from .MainWindow import MainWindow

from . import moduletype
from . import consts
from . import direction
from .nodeiotype import NodeIoType

"""
CNode is a junction pint between different signals with same size
here should be decided which signal drives in
ie simulation tactic(impl) can get first signal attached to node as driverSignal
or first Signal with deltaVector.out 
"""
class Node(Object):
    def __init__(self, *args, **kwargs):
        #//self._deltaVector = DeltaVector.NONE 
        self._signals = {}    
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Node] Parent has to be descendant of wq.Module')
        self._name = kwargs['name'] if 'name' in kwargs else None

        self._info = kwargs['info'] if 'info' in kwargs else None
        self._desc = kwargs['desc'] if 'desc' in kwargs else None       
        self._driveSignal = None
        if 'signal' in kwargs:
            self.addSignal(kwargs['signal'])
            self._name = kwargs['signal'].name() if self._name == None else self._name
        if self._name == None:
            self.raiseExc(f'Name of Node required')                    
        super(Node, self).__init__(*args, **kwargs)
        self._id = len(self.parent().nodes())
        #self.parent()._nodes[self.id()]=self
        self.parent().addNode(self)
            
    def id(self):
        return self._id

    def module(self):
        return self._parent
    
    def driveSignal(self):
        return self._driveSignal

    def size(self):
        result = self.driveSignal().size() if self.driveSignal() != None else None
        if result == None and len(self.signals())>0:
            result = next(iter(self.signals())).size()
        return result
        '''
        if result == None and len(self._signals)>0:
            result = next(iter(self._signals.values())).size()
        return result; 
        '''
    
    def desc(self):
        return self._desc

    def info(self):
        return self._info

    def name(self):
        return self._name

    def setDriveSignal(self, signal:'Signal'):
        if self._driveSignal == None:
            self._driveSignal = signal
        else:
            if self._driveSignal.size()!=signal.size():
                self.raiseExc('Signal size differs')
            msg = signal.canDrive()
            if msg == None:
                self._driveSignal = signal
            else: 
                self.raiseExc(f'[signal.canDrive]: {msg}')


    def addSignal(self, signal:'Signal'):
        if self._driveSignal == None:
            self.setDriveSignal(signal)
        tid = signal.id()
        if tid in self._signals:
            self.raiseExc(f'Signal with id {tid} already added')
        if self._driveSignal.size()!=signal.size():
            self.raiseExc('Signal size differs')            
        self._signals[id]=signal

class IoNode(Node):
    def __init__(self, *args, **kwargs): 
        self._ioType = kwargs['ioType'] if 'ioType' in kwargs else None #nodeiotype
        if self._ioType == None:
            self.raiseExc('ioType required')
        self._extSignals = {}
        tsignal = kwargs['signal'] if 'signal' in kwargs else None
        if tsignal == None:
            self.raiseExc(f'Signal required fo ioNode')
        super(IoNode, self).__init__(*args, **kwargs)
        #for ioNode driveSignal is external or internal depending on type?
        #ioNode will be added always with internal signal
        #for inputs no driveSignal added for a start
        if self.ioType() == NodeIoType.INPUT:
            self._driveSignal = None


    def extSignals(self):
        return self._extSignals

    def ioType(self):
        return self._ioType


"""
Module represents logic processing element and handles also hierarchy (modules can contain other modules(as submodules))
rootModule (parent=MainWindow) handles model for main view of designed logic circuit
so - hierarchy can be:
rootModule (mainView) isRoot method
    ...
    elementModule (type=ModuleType.GRAPH)
        ...
        elementModule (type=ModuleType.GRAPH)
            ...
            atomicModule (type=native/WQC/simple etc - processing logic out of scope of local simulation)
Module contains:
    intSignals - set of internal signals
    signals - io signals (connected to io CNodes set - input/output "pins")


"""
class Module(Object):
    def __new__(cls, *args, **kwargs):
        kwargs['wqImpl']=consts.WQ_IMPL_SIM 
        return Object.__new__(cls,*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self._view = None 
        self._isIconified = False 
        self._iconifyingHidesCentralWidget = False 
        self._rotate = False
        self._invertH = False
        args = self._loadInitArgs(args)
        d1 = isinstance(args[0],Module)
        d2 = isinstance(args[0],MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[Module] Parent has to be descendant of wq.Module or wq.MainWindow')
        if args[1] == None:
            self.raiseExc('[Module] Name has to be given')
        self._name=args[1]
        #args = (args[0], None) 
        parent = args[0]
        impl = kwargs['impl'] if 'impl' in kwargs else None
        self._modules = {0:self}
        self._nodes = {}
        self._nodesByName = {}
        self._signals = {}
        self._signalsByName = {}
        self._id = 0
        kwargs.pop('type', None) 
        kwargs.pop('impl', None)        
        super(Module, self).__init__(parent, impl, **kwargs)
        if d1:
            self._id = len(self.parent().modules())
            self.parent().addModule(self)
    def id(self):
        return self._id

    def name(self):
        return self._name

    def path(self):
        result = "/"+self.name() if self.isRoot() else str(self.parent().path()) + "/" + self.name()

    def view(self):
        return self._view

    def nodes(self):
        return self._nodes
    
    def signals(self):
        return self._signals

    def sigByName(self, sigName:str):
        result = self._signalsByName[sigName] if sigName in self._signalsByName else None
        return result

    def nodByName(self, nodName:str):
        result = self._nodesByName[nodName] if nodName in self._nodesByName else None
        return result

    def modules(self):#submodules
        return self._modules

    def modById(self, id):
        return self._modules[id]

    def addSignal(self, signal:'Signal'):
        if signal.id() in self._signals:
            self.raiseExc(f'Signal with id {signal.id()} already in list')
        if signal.name() in self._signalsByName:
            self.raiseExc(f'Signal with name {signal.name()} already in list')
        self._signals[signal.id()]=signal
        self._signalsByName[signal.name()]=signal

    def addNode(self, node:'Node'):
        if node.id() in self._nodes:
            self.raiseExc(f'Node with id {node.id()} already in list')
        if node.name() in self._nodesByName:
            self.raiseExc(f'Node with name {node.name()} already in list')
        self._nodes[node.id()]=node
        self._nodesByName[node.name()]=node

    def addModule(self, module:'Module'):
        tid = module.id()
        if tid in self._modules:
            self.raiseExc(f'Module with id {tid} already in collection of submodules')
        self._modules[tid]=module
    
    def newSignal(self, **kwargs):
        from .Signal import Signal
        return Signal(self,**kwargs)

    def newNode(self, **kwargs):
        return Node(self,**kwargs) 

    def newIoNode(self, **kwargs):
        return IoNode(self,**kwargs)            
        
    def isRoot(self):
        return isinstance(self.parent(), MainWindow) #alt id == 0

    def iconify(self, iconify):
        self._isIconified = iconify

    def isIconified(self):
        return self._isIconified

    def setIconifyingHidesCentralWidget(self, hide):
        self._iconifyingHidesCentralWidget = hide
        
    def iconifyingHidesCentralWidget(self):
        return self._iconifyingHidesCentralWidget

    #EOrientation orientation
    def direction(self):
        dir = direction.RIGHT
        if (self._rotate):
            if (not self._invertH):
                dir = direction.UP
            else:
                dir = direction.DOWN
        else:
            if (self._invertH):
                dir = direction.LEFT
        return dir
