
#from .Signal import Signal
from .Object import Object
from .MainWindow import MainWindow

from . import moduletype
from . import consts
from . import direction
from .nodeiotype import NodeIoType
from .q3vector import Q3Vector
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
        self._signals = Q3Vector()    
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Node] Parent has to be descendant of q3.Module')
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

    def module(self) -> 'Module':
        return self._parent

    def events(self):
        return self.module().events()

    def view(self):
        return self._view
    
    def size(self):
        result = self.driveSignal().size() if self.driveSignal() != None else None
        if result == None and self.signals().size()>0:
            result = self.signals().first().size()
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
        if self._driveSignal == None: #not set yet - just set it
            self._driveSignal = signal
        else: #ds alrady set - check variant
            if signal == None: #ds clear try - allow always ?
                tid = self._driveSignal.id()
                self.signals().removeByLid(tid)
                self._driveSignal = signal
            else: #setting new ds
                if self._driveSignal.size()!=signal.size():  #size differs - problem
                    self.raiseExc('Signal size differs')
                #msg = signal.canDrive() #don't think this logic is needed now
                #if msg == None:
                self._driveSignal = signal
                #else: 
                #    self.raiseExc(f'[signal.canDrive]: {msg}')
        self.addSignal(signal)

    def isSignalOn(self):
        return self.driveSignal().isOn() if self.driveSignal() != None else False

    def addSignal(self, signal:'Signal'):
        if signal == None: #none cannot be added
            return 
        if self._driveSignal != None:
            if self._driveSignal.size()!=signal.size(): # size differs - problem
                self.raiseExc('Signal size differs')  
        else: #first added signal as Drive
            self.setDriveSignal(signal)
        lid = signal.id()
        if lid in self._signals: #silently ignore
            #self.raiseExc(f'Signal with id {lid} already added')
            return          
        self._signals.append(lid,signal)

    def removeSignal(self, sig:'Signal'):
        if sig == None:
            return
        self._signals.removeByLid(sig.id())
        if self.driveSignal()!=None and self.driveSignal().id() == sig.id():
            self.setDriveSignal(None)

    #@api
    def connect(self, targetNode:'Node', **kwargs):
        assert self.driveSignal()!=None, '[node.connect] Drive signal is none'
        assert targetNode!=None, '[node.connect] targetNode is none'
        if (isinstance(targetNode,IoNode)):
            assert targetNode.ioType() in [NodeIoType.INPUT,NodeIoType.DYNAMIC], '[node.connect] targetNode.ioType has to be in [INPUT,DYNAMIC]'
        if self.view() == None or targetNode.view()==None: # standalone mode
            targetNode.setDriveSignal(self.driveSignal())
        #emit connection request
        self.events().emitNodeConnectionRequest({
            'sourceNode':self,
            'targetNode':targetNode
            })

    #@api - alias for connect 
    def con(self, targetNode:'Node', **kwargs):
        return self.connect(targetNode,**kwargs)

class IoNode(Node):
    def __init__(self, *args, **kwargs): 
        self._ioType = kwargs['ioType'] if 'ioType' in kwargs else None #nodeiotype
        if self._ioType == None:
            self.raiseExc('ioType required')
        self._extSignals = Q3Vector()
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
            atomicModule (type=native/Q3C/simple etc - processing logic out of scope of local simulation)
Module contains:
    intSignals - set of internal signals
    signals - io signals (connected to io CNodes set - input/output "pins")


"""
class Module(Object):
    def __new__(cls, *args, **kwargs):
        kwargs['q3Impl']=consts.Q3_IMPL_SIM 
        return Object.__new__(cls,*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self._view = None 
        args = self._loadInitArgs(args)
        parent = args[0]
        d1 = isinstance(parent,Module)
        d2 = isinstance(parent,MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[Module] Parent has to be descendant of q3.Module or q3.MainWindow')
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

        self._scriptRecording = False
        self._modules = Q3Vector()
        self.modulesBy = self._modules.by #@api
        self.modsBy = self.modulesBy #@api
        self._modules.append(0,self)
        self._nodes = Q3Vector()
        self.nodesBy = self._nodes.by #@api
        self.nodsBy = self.nodesBy #@api
        #self._nodesByName = {} handled by Q3Vector
        self._tabIndex = None
        self._signals = Q3Vector()
        self.signalsBy = self._signals.by #@api
        self.sigsBy = self.signalsBy #@api
        self._moduleViews = Q3Vector()
        self.moduleViewsBy = self._moduleViews.by
        self.mViewsBy = self.moduleViewsBy 
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
        

    def consoleWrite(self, dta):
        self.impl().consoleWrite(dta)

    def isScriptRecordingOn(self):
        return self._scriptRecording

    def setScriptRecording(self, n:bool):
        self._scriptRecording = n

    #@api
    def connect(self, sourceNodeId:int,targetNodeId:int):
        sourceNode = self.nodes(sourceNodeId)
        targetNode = self.nodes(targetNodeId)
        assert sourceNode != None, f'[Module.connect] sourceNodeId:{sourceNodeId} not found'
        assert targetNode != None, f'[Module.connect] targetNodeId:{targetNodeId} not found'
        return sourceNode.connect(targetNode)

    def setPos(self, x, y):
        if self.view()!=None:
            self.view().impl().setPos(x,y)

    def recordScript(self, recData:dict):
        self.consoleWrite(f'[recordScript] {recData}\n')
        recordType = recData['recordType']
        if recordType == 'event':
            eventName = recData['eventName']
            event = recData['event']
            if eventName == 'itemPositionHasChanged':
                x = event.props('x')
                y = event.props('y')
                id = event.props('elementId')
                self.consoleWrite(f'[recordScript] c.rm.modulesBy(\'id\',{id}).setPos({x},{y})')
            elif eventName == 'nodeConnectionRequest':
                self.consoleWrite(f'[recordScript] Unhandled eventName:{eventName} {event.props()}')
            else:
                self.consoleWrite(f'[recordScript] Unhandled eventName:{eventName}')
        elif recordType == 'methodCall':
            methodName = recData['methodName']
            if methodName == 'IoNodeView.finishIoLinkView':
                sourceNodeId = recData['sourceNodeId']
                targetNodeId = recData['targetNodeId']
                self.consoleWrite(f'[recordScript] c.rm.connect({sourceNodeId},{targetNodeId})\n')
            else:
                self.consoleWrite(f'[recordScript] Unhandled methodName:{methodName}')
        else:
            self.consoleWrite(f'[recordScript] Unhandled recordType:{recordType}')


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
    def nodes(self, by=None):
        return self._nodes.defaultGetter('name',by)
    
    #@api
    def nods(self, by=None):
        return self.nodes(by)

    #@api
    def nod(self, by):
        assert by!=None, '[nod] "by" arg required not None'
        return self.nodes(by)

    #@api
    def nodl(self,by):
        assert by!=None, '[nodl] "by" arg required not None'
        return self.nodes().filterBy('dir',direction.LEFT).defaultGetter('name',by)

    #@api
    def nodr(self,by):
        assert by!=None, '[nodr] "by" arg required not None'
        return self.nodes().filterBy('dir',direction.RIGHT).defaultGetter('name',by)
    
    #@api
    def signals(self, by=None):
        return self._signals.defaultGetter('name',by)

    #@api
    def sigs(self,by=None):
        return self.signals(by)

    #@api
    def sig(self,by):
        assert by!=None, '[sig] "by" arg required not None'
        return self.signals(by)

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
    def modules(self,by=None):#submodules
        return self._modules.defaultGetter('name',by)
        
    #@api
    def mods(self,by=None):
        return self.modules(by)

    #@api
    def mod(self,by):
        assert by!=None, '[mod] "by" arg required not None'
        return self.modules(by)

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
        ioType = ioNode.ioType()
        if dsignal != None:
            self.signals().removeByLid(dsignal.id())
            ioNode.removeSignal(dsignal)
            #del dsignal !TODO! maybe by type ?
        if ioNode != None:
            self.nodes().removeByLid(ioNode.id())
            v = ioNode.view()
            v.onNodeRemoval()
            del v
            del ioNode

    #@api
    def modAdd(self, moduleName,**kwargs):
        return self.newModule(moduleName,**kwargs)

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




