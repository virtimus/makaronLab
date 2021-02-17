
#from .Signal import Signal
from .Object import Object
from .MainWindow import MainWindow

from . import moduletype
from . import consts
from . import direction
from .nodeiotype import NodeIoType
from .wqvector import WqVector
from .moduletype import ModuleType

from .EventSignal import EventProps

"""
CNode is a junction pint between different signals with same size
here should be decided which signal drives in
ie simulation tactic(impl) can get first signal attached to node as driverSignal
or first Signal with deltaVector.out 
"""
class Node(Object):
    def __init__(self, *args, **kwargs):
        #//self._deltaVector = DeltaVector.NONE 
        self._view = None
        self._signals = WqVector()    
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Node] Parent has to be descendant of wq.Module')
        self._name = kwargs['name'] if 'name' in kwargs else None
        self._info = kwargs['info'] if 'info' in kwargs else None
        self._desc = kwargs['desc'] if 'desc' in kwargs else None               
        self._sigInternal = self._initHandleArg('sigInternal',
                kwargs = kwargs,
                required = False,
                defaultValue = False,
                desc ='Used to check if signal is contained in node, if yes - it will be deleted and disconnected together with parent node'               
            )
        self._driveSignal = None
        self._intSignal = None
        tsignal = self._initHandleArg('signal',
                kwargs = kwargs,
                desc = 'Internal or drive (for output node) signal contained in Node'
            )
        if tsignal != None:
            self.addSignal(tsignal)
            if self._sigInternal:
                self._intSignal = tsignal
            self._name = tsignal.name() if self._name == None else self._name
        if self._name == None:
            self.raiseExc(f'Name of Node required')             
                   
        super(Node, self).__init__(*args, **kwargs)
        #self._id = len(self.parent().graphModule().nodes())
        self._id = self.parent().graphModule().nodes().nextId()
        self._no = len(self.parent().nodes())
        #self.parent()._nodes[self.id()]=self
        self.parent().graphModule().addNode(self)
        self.parent().addNode(self)

    def acceptVisitor(self, v):
        v.visitNode(self)

    def id(self):
        return self._id

    def no(self):
        return self._no

    def module(self):
        return self._parent
    
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

    def setSize(self, nsize:int):
        if self.size() == nsize:
            return
        if self.driveSignal() != None:
            self.driveSignal().setSize(nsize)

        for lid in self.signals(): #omit drive?
            s = self.signals().byLid(lid)
            s.setSize(nsize)

    def resetValue(self):
        if self._driveSignal != None:
            self._driveSignal.resetValue()

    def desc(self):
        return self._desc

    def info(self):
        return self._info

    def name(self):
        return self._name

    def driveSignal(self) -> 'Signal':
        return self._driveSignal

    def signals(self):
        return self._signals

    def setDriveSignal(self, signal:'Signal'):
        if self._driveSignal == None:
            self._driveSignal = signal
        else:
            if signal == None:
                tid = self._driveSignal.id()
                self.signals().removeByLid(tid)
                self._driveSignal = signal
            else:
                if self._driveSignal.size()!=signal.size():
                    self.raiseExc('Signal size differs')
                msg = signal.canDrive()
                if msg == None:
                    self._driveSignal = signal
                else: 
                    self.raiseExc(f'[signal.canDrive]: {msg}')
        self.addSignal(signal)

    def isSignalOn(self):
        return self.driveSignal().isOn() if self.driveSignal() != None else False

    def addSignal(self, signal:'Signal'):
        if signal == None:
            return 
        if self._driveSignal == None:
            self.setDriveSignal(signal)
        lid = signal.id()
        if lid in self._signals:
            #self.raiseExc(f'Signal with id {lid} already added')
            return
        if self._driveSignal.size()!=signal.size():
            self.raiseExc('Signal size differs')            
        self._signals.append(lid,signal)

    def removeSignal(self, sig:'Signal'):
        if sig == None:
            return
        self._signals.removeByLid(sig.id())
        if self.driveSignal()!=None and self.driveSignal().id() == sig.id():
            self.setDriveSignal(None)


    def connect(self, targetNodeId, **kwargs):
        pass

class IoNode(Node):
    def __init__(self, *args, **kwargs): 
        self._ioType = kwargs['ioType'] if 'ioType' in kwargs else None #nodeiotype
        if self._ioType == None:
            self.raiseExc('ioType required')
        self._extSignals = WqVector()
        tsignal = kwargs['signal'] if 'signal' in kwargs else None
        if tsignal == None:
            self.raiseExc(f'Signal required fo ioNode')
        self._name = kwargs['name'] if 'name' in kwargs else tsignal.name()
        self._dir = kwargs['direction'] if 'direction' in kwargs else None
        if self._dir == None:
            self._dir = direction.LEFT if self.ioType() == NodeIoType.INPUT else direction.RIGHT

        super(IoNode, self).__init__(*args, **kwargs)
        #for ioNode driveSignal is external or internal depending on type?
        #ioNode will be added always with internal signal
        #for inputs no driveSignal added for a start
        if self.ioType() == NodeIoType.INPUT:
            self._driveSignal = None

    def acceptVisitor(self, v):
        v.visitIoNode(self)

    def name(self):
        return self._name

    def dir(self):
        return self._dir

    def extSignals(self):
        return self._extSignals

    def ioType(self):
        return self._ioType

    def flags(self):
        return self.prop('ioNodeFlags')

    def valueType(self):
        return self.prop('valueType')


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
        args = self._loadInitArgs(args)
        parent = args[0]
        d1 = isinstance(parent,Module)
        d2 = isinstance(parent,MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[Module] Parent has to be descendant of wq.Module or wq.MainWindow')
        if d1 and not ModuleType.GRAPH == parent.mType():
            self.raiseExc('[Module] module can be descendant only of graph module')
        self._graphModule = self if d2 else parent
        self._rootModule = self if d2 else parent.rootModule()
        

        if args[1] == None:
            self.raiseExc('[Module] Name has to be given')
        self._name=args[1]
        #args = (args[0], None) 


        impl = kwargs['impl'] if 'impl' in kwargs else None
        self._moduleType = kwargs['moduleType'] if 'moduleType' in kwargs else None
        self._isImplStr = isinstance(impl, str)
        if self._moduleType != None and self._isImplStr :
            self.raiseExc(f'[Module] moduleType cannot be given for module loaded from lib {self._name}')
        elif not self._isImplStr  and self._moduleType == None:
            self.raiseExc(f'[Module] ''moduleType'' required {self._name}')


        self._modules = WqVector()
        self._modules.append(0,self)
        self._nodes = WqVector()
        #self._nodesByName = {} handled by WqVector
        self._tabIndex = None
        self._signals = WqVector()
        self._moduleViews = WqVector()
        self._info = None
        self._desc = None
        #self._signalsByName = {}
        self._id = None
        kwargs.pop('type', None) 
        kwargs.pop('impl', None)        
        super(Module, self).__init__(parent, impl, **kwargs)
        #check type
        #if self._isImplStr:
        #    self._moduleType = self.impl().moduleType()
        if self.impl() == None:
            self.raiseExc(f'No impl loaded for module {self.name()}')
        if self.impl().moduleType() == None:
            self.raiseExc(f'Impl for module {self.name()} has not set moduleType')
        self._moduleType = self.impl().moduleType()
        
        if d1:
            self._id = self.parent().modules().nextId()
            self.parent().addModule(self)
        else:
            self._id = kwargs['id'] if 'id' in kwargs else 0


    def tabIndex(self):
        result = self.view().tabIndex() if self.view()!=None else None
        return result
    

    def acceptVisitor(self, visitor):
        visitor.visitModule(self)

    def moduleViews(self):
        return self._moduleViews

    def id(self):
        return self._id

    def name(self):
        return self._name

    def setName(self, n:str):
        self._name = n

    def info(self):
        return self._info

    def desc(self):
        return self._desc

    def graphModule(self):
        return self._graphModule

    def rootModule(self):
        return self._rootModule
    
    def setDesc(self, dsc:str):
        self._desc = dsc

    def path(self):
        result = "/"+self.name() if self.isRoot() else str(self.parent().path()) + "/" + self.name()

    def view(self):
        return self._view

    def events(self):
        return self.impl().events()

    #@api
    def nodes(self):
        return self._nodes
    #@api
    def nods(self):
        return self.nodes()
    
    #@api
    def signals(self):
        return self._signals

    #@api
    def sigs(self):
        return self.signals()

    def mType(self):
        return self.moduleType()

    def moduleType(self):
        return self._moduleType #impl().moduleType()

    def sigByName(self, sigName:str):
        result = self._signals.filterBy('name',sigName)
        result = result.first() if result.size()>0 else None
        return result

    def nodByName(self, nodName:str):
        result = self._nodes.filterBy('name',nodName)
        result = result.first() if result.size()>0 else None
        return result

    #@api
    def modules(self):#submodules
        return self._modules
        
    #@api
    def mods(self):
        return self.modules()

    def modById(self, id):
        return self._modules.byLid(id)

    def addSignal(self, signal:'Signal'):
        if signal.id() in self._signals:
            self.raiseExc(f'Signal with id {signal.id()} already in list')
        if self.mType() != ModuleType.GRAPH and signal.name() in self._signals.by('name'):
            self.raiseExc(f'Signal with name {signal.name()} already in list')
        #self._signals[signal.id()]=signal
        #self._signalsByName[signal.name()]=signal
        self._signals.append(signal.id(), signal)

    def addNode(self, node:'Node'):
        if node.id() in self._nodes:
            self.raiseExc(f'Node with id {node.id()} already in list')
        if self.mType() != ModuleType.GRAPH and node.name() in self._nodes.by('name'):
            self.raiseExc(f'Node with name {node.name()} already in list')
        #self._nodes[node.id()]=node
        #self._nodesByName[node.name()]=node
        self._nodes.append(node.id(),node)

    def addModule(self, module:'Module'):
        tid = module.id()
        if tid in self._modules:
            self.raiseExc(f'Module with id {tid} already in collection of submodules')
        self._modules.append(tid, module)

    def addModuleView(self,mv:'ModuleView'):
        tid = mv.id()
        if tid in self._moduleViews:
            self.raiseExc(f'ModuleView with id {tid} already in collection of views')
        self._moduleViews.append(tid, mv)
    
    def newSignal(self, **kwargs):
        from .Signal import Signal
        return Signal(self,**kwargs)

    def newNode(self, **kwargs):
        return Node(self,**kwargs) 

    def newIoNode(self, **kwargs):
        return IoNode(self,**kwargs) 

    def newIO(self, **kwargs):
        tname = kwargs['name'] if 'name' in kwargs else None
        if tname == None:
            self.raiseExc('Name required')
        tsize = kwargs['size'] if 'size' in kwargs else 1
        tIoType = kwargs['ioType'] if 'ioType' in kwargs else None
        tSigProps = kwargs['props'] if 'props' in kwargs else None
        sig = self.newSignal(name=tname,size=tsize,props=tSigProps)
        kwargs.pop('ioType',None)
        result = self.newIoNode(signal=sig, sigInternal=True, ioType=tIoType,**kwargs)
        return result 

    def removeIO(self,id):
        ioNode = self.nodes().byLid(id)
        dsignal = ioNode.driveSignal()
        if dsignal != None:
            self.signals().removeByLid(dsignal.id())
            del dsignal
        if ioNode != None:
            self.nodes().removeByLid(ioNode.id())
            del ioNode



    def newModule(self, moduleName, **kwargs):
        result = Module(self,moduleName,**kwargs)
        self.impl().add(result)
        return result             
        
    def isRoot(self):
        return isinstance(self.parent(), MainWindow) #alt id == 0

    def calculate(self):
        calc = getattr(self.impl(),'calc')
        if callable(calc):
            calc()

    def updateTiming(self, delta):
        uTime = getattr(self.impl(),'updateTiming')
        if callable(uTime):
            uTime(delta)        




