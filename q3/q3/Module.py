
#from .Signal import Signal
from sys import api_version
import types
from .Object import Object
from .MainWindow import MainWindow

from . import moduletype
from . import consts
from . import direction
from .nodeiotype import NodeIoType
from .nodeiotype import NodeIoType as IoType
from .q3vector import Q3Vector
from .moduletype import ModuleType
from .valuetype import ValueType

from .EventSignal import EventProps

from . import strutils as su

from .ionodeflags import IoNodeFlags

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
        self._signalsAsNot = {}  
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Node] Parent has to be descendant of q3.Module')
              
        self._sigInternal = self._initHandleArg('sigInternal',
                kwargs = kwargs,
                required = False,
                defaultValue = False,
                desc ='Used to check if signal is contained in node, if yes - it will be deleted and disconnected together with parent node'               
            )
        self._driveSignal = None
        #self._driveSignalDelta = False
        #self._prevDriveSignal = None depr
        self._intSignal = None
        tsignal = self._initHandleArg('signal',
                kwargs = kwargs,
                desc = 'Internal or drive (for output node) signal contained in Node'
            )
        self.setIntSignalAsDrive()
        super(Node, self).__init__(*args, **kwargs)
        
        if tsignal != None:
            self.addSignal(tsignal)
            if self._sigInternal:
                self._intSignal = tsignal
            self._name = tsignal.name() if self._name == None else self._name
        if self._name == None:
            self.raiseExc(f'Name of Node required')             
                   
        
        #self._id = len(self.parent().graphModule().nodes())
        self._id = self.parent().rootModule().allNodes().push(self)
        self._no = len(self.parent().nodes())
        self.parent().intNodes().push(self)
        #self.parent()._nodes[self.id()]=self

        self.parent().rootModule().addNode(self)
        if not self.parent().graphModule() is self.parent():
            self.parent().addNode(self)
        if self.flags()==None: #some call do not put flags - create defaults
            tflags = IoNodeFlags()    
            self.setProp('ioNodeFlags',tflags)

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

    '''None - disconnected
    def resetValue(self):
        if self._driveSignal != None:
            self._driveSignal.resetValue()
    '''



    def driveSignal(self) -> 'Signal':
        return self._driveSignal

    def intSignal(self) -> 'Signal':
        return self._intSignal
    
    def value(self):
        result = None
        if self.intSignal() != None:
            result = self.intSignal().value()
        return result

    def setValue(self, nVal):
        assert self.intSignal() != None, '[node.setValue] intSignal is not set for the node'
        return self.intSignal().setValue(nVal)

    def signals(self):
        return self._signals

    def _checkSignalSize(self,signal):
        if self.size()!=None and signal!=None and ValueType.fromSize(self.size()).size()<signal.valueType().size():
            s1 = ValueType.fromSize(self.size()).size()
            s2 = signal.valueType().size()
            self.raiseExc(f'Signal size differs ({self.name()} {signal.name()}) s1:{s1} s2:{s2}')  

    def setIntSignalAsDrive(self):
        #go through none to propagate
        self.setDriveSignal(None)
        self.setDriveSignal(self.intSignal())


    def _propagateDynamicDriveSignalChange(self):
        if self.ioType() == IoType.DYNAMIC and self._driveSignal == self._intSignal:#propagate change if dynamic and (IMPORTANT) if set to self.intSignal
            nodesToCheck = self.module().graphModule().nodes() \
                .filterBy('ioType',IoType.DYNAMIC) \
                .filterBy('size',self.size())
            
            for n in nodesToCheck.values():
                if n!=self: #self already handled
                    ts = n.signals().byLid(self._driveSignal.id())
                    if ts!=None: #node has the signal - set as drive
                        n.setDriveSignal(ts) 

    def setDriveSignal(self, signal:'Signal'):
        if self._driveSignal == signal:#break recursion on dynamic dc propagate
            return
        if signal !=None:
            self._checkSignalSize(signal)
        propagateDynamicChange = False
        
        if self._driveSignal == None: #not set yet - just set it
            self._driveSignal = signal
            propagateDynamicChange = self._driveSignal == self._intSignal
            #self.parent()._hasDSChanged = True
            #if self._driveSignal!=None:
            #   self._driveSignal.dvOut(True)
        else: #ds alrady set - check variant
            if signal == None: #ds clear try - allow always ?
                self._driveSignal = signal
                #self.parent()._hasDSChanged = True
                #if self._driveSignal != self._intSignal: #cannot remove internal signal
                #    tid = self._driveSignal.id()                
                #    self.signals().removeByLid(tid)
                #self._driveSignal = self._intSignal
            else: #replacing with new ds #probably only for dynamic ?
                if self._driveSignal.size()!=signal.size():  #size differs - problem
                    self.raiseExc('Signal size differs')
                #msg = signal.canDrive() #don't think this logic is needed now
                #if msg == None:
                #self._prevDriveSignal = self._driveSignal
                #self.parent()._hasDSChanged = self._driveSignal.value() != signal.value()
                self._driveSignal = signal
                
                #self._driveSignal.dvOut(True)#deprecated
                propagateDynamicChange = self._driveSignal == self._intSignal

                #else: 
                #    self.raiseExc(f'[signal.canDrive]: {msg}')
        self.addSignal(signal)
        if propagateDynamicChange == True:
            self._propagateDynamicDriveSignalChange()

    def isSignalOn(self):
        return self.driveSignal().isOn() if self.driveSignal() != None else False

    def addSignal(self, signal:'Signal'):
        if signal == None: #none cannot be added
            return 
        self._checkSignalSize(signal)
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

    def dvOutSignal(self):
        for s in self.signals().values():
            if s.dvOut():
                return s
        return None



    def removeSignal(self, sig:'Signal'):
        if sig == None:
            return
        assert sig != self._intSignal, '[removeSignal] Cannot remove internal signal'
        self._signals.removeByLid(sig.id())
        if self.driveSignal()!=None and self.driveSignal().id() == sig.id():
            self.setDriveSignal(None)

    #@api
    def connect(self, targetNode:'Node', **kwargs):
        assert self.intSignal()!=None, '[node.connect] source internal signal is none' 
        assert targetNode!=None, '[node.connect] targetNode is none'
        #special case - connect to output from inside of graph 2nd level node - self.view == None
        isSC1 = self.view()==None and targetNode.ioType() == NodeIoType.OUTPUT and self.driveSignal()!=None
        #another special case connecting directly in and out of non root module
        isSC2 = not self.module().isRoot() and self.module() == targetNode.module()
        asNot = self._initHandleArg('asNot',
                kwargs = kwargs,
                required = False,
                defaultValue = False,
                desc ='Used to invert Node calculated value'               
            )
        if isSC1 or isSC2:
            #self.addSignal(targetNode.intSignal())
            #above won't work with new algo
            targetNode.setDriveSignal(self.intSignal())
            targetNode.setAsNot(self.intSignal().id(),asNot)
            return #we can return here as we're not making any visible change ?
        if (isinstance(targetNode,IoNode)):
            assert targetNode.ioType() in [NodeIoType.INPUT,NodeIoType.DYNAMIC], '[node.connect] targetNode.ioType has to be in [INPUT,DYNAMIC]'
        if self.view() == None or targetNode.view()==None: # standalone mode
            targetNode.setDriveSignal(self.intSignal())
            targetNode.setAsNot(self.intSignal().id(),asNot)            
            #dynamic (two way) nodes need feedback connection in case com direction change
            if self.ioType() == NodeIoType.DYNAMIC and targetNode.ioType() == NodeIoType.DYNAMIC:
                self.addSignal(targetNode.intSignal())

        #emit connection request
        self.events().emitNodeConnectionRequest({
            'sourceNode':self,
            'targetNode':targetNode
            })

    #@api
    def con(self, targetNode:'Node', **kwargs):
        return self.connect(targetNode,**kwargs)

    #@api - alias for connect 
    def c(self, targetNode:'Node', **kwargs):
        return self.connect(targetNode,**kwargs)

    def setAsNot(self,k,v:bool):
        self._signalsAsNot[k]=v
    
    def isSignalInverted(self, signal:'Signal'):
        return signal.id() in self._signalsAsNot and self._signalsAsNot[signal.id()] #invert

class IoNode(Node):
    def __init__(self, *args, **kwargs): 
        self._currMonType = None #used to save monType state in properties
        self._ioType = kwargs['ioType'] if 'ioType' in kwargs else None #nodeiotype
        if self._ioType == None:
            self.raiseExc('ioType required')
        self._extSignals = Q3Vector()
        tsignal = kwargs['signal'] if 'signal' in kwargs else None
        if tsignal == None:
            self.raiseExc(f'Signal required fo ioNode')
        self._name = kwargs['name'] if 'name' in kwargs else tsignal.name()
        self._dir = None
        if 'direction' in kwargs:
            self._dir = kwargs['direction']
        if self._dir == None:
            self._dir = direction.LEFT if self.ioType() == NodeIoType.INPUT else direction.RIGHT

        super(IoNode, self).__init__(*args, **kwargs)
        #for ioNode driveSignal is external or internal depending on type?
        #ioNode will be added always with internal signal
        #for inputs no driveSignal added for a start
        if self.ioType() == NodeIoType.INPUT:
            self._driveSignal = None
        else: # for dynamic and output 1st required signal attached as 'internal' - also a candidate for drive on clear
            self._intSignal = tsignal


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
        #P6-Big crash here ?
        result = self.prop('valueType')
        if result == None and self.intSignal()!=None and self.intSignal().valueType()!=None:
            result = self.intSignal().valueType()
        #else:
        return result


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
            self.raiseExc(f'[Module] "moduleType" required {self._name}')

        self._scriptRecording = False
        self._calculated = False
        self._modules = Q3Vector()
        self.modulesBy = self._modules.by #@api
        self.modsBy = self.modulesBy #@api
        self._modules.append(0,self)
        self._nodes = Q3Vector()
        self._allNodes = Q3Vector()
        self._intNodes = Q3Vector()
        self.nodesBy = self._nodes.by #@api
        self.nodsBy = self.nodesBy #@api
        #self._nodesByName = {} handled by Q3Vector
        self._tabIndex = None
        self._signals = Q3Vector()
        self._allSignals = Q3Vector()
        self._intSignals = Q3Vector()
        self.signalsBy = self._signals.by #@api
        self.sigsBy = self.signalsBy #@api
        self._sigFormulas = {} #additional calc formulas 
        self._moduleViews = Q3Vector()
        self.moduleViewsBy = self._moduleViews.by
        self.mViewsBy = self.moduleViewsBy 
        #self._info = None
        #self._desc = None
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

    def allSignals(self):
        return self._allSignals

    def allNodes(self):
        return self._allNodes 

    def intSignals(self):
        return self._intSignals

    def intNodes(self):
        return self._intNodes

    def consoleWrite(self, dta):
        self.impl().consoleWrite(dta+"\n")

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
            vimpl = self.view().impl() 
            vimpl.setPos(x,y)

    def recordScript(self, recData:dict):
        self.consoleWrite(f'[recordScript] {recData}')
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
                self.consoleWrite(f'[recordScript] c.rm.connect({sourceNodeId},{targetNodeId})')
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
    '''
    def name(self):
        return self._name
    '''
    def setName(self, n:str):
        self._name = n
    '''
    def info(self):
        return self._info

    def desc(self):
        return self._desc
    '''    

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
    def prp(self,by):
        result = self.view().prp(by) if self.view()!=None else None
        return result

    #@api
    def nodes(self, by=None):
        return self._nodes.defaultGetter('name',by)
    
    #@api
    def nods(self, by=None):
        return self.nodes(by)

    def _intNod(self):
        result = Q3Vector()
        if self.isRoot():
            tm = self.mod(direction.LEFT.graphModName())
            if tm!=None:
                result.appendAll(tm.nodes())
            tm = self.mod(direction.RIGHT.graphModName())
            if tm!=None:
                result.appendAll(tm.nodes()) #!TODO! reimplement optimal
        else:
            result = self.nodes().filterBy('parent',self)
        return result

    #@api
    def nod(self, by):
        assert by!=None, '[nod] "by" arg required not None'
        return self._intNod().defaultGetter('name',by) #nodes(by) !TODO! optimize filterBY 

    #@api
    def n(self, by):
        return self.nod(by)

    #@api
    def nodl(self,by):
        assert by!=None, '[nodl] "by" arg required not None'
        return self.nodes().filterBy('dir',direction.LEFT).defaultGetter('name',by)

    #@api
    def nodr(self,by):
        assert by!=None, '[nodr] "by" arg required not None'
        return self.nodes().filterBy('dir',direction.RIGHT).defaultGetter('name',by)

    #@api 
    def iAdd(self, name=None, **kwargs):
        kwargs['ioType']=NodeIoType.INPUT
        return self.ioAdd(name, **kwargs)

    #@api 
    def oAdd(self, name=None, **kwargs):
        kwargs['ioType'] = NodeIoType.OUTPUT
        return self.ioAdd(name,**kwargs)

    #@api
    def ioAdd(self, name=None, **kwargs):
        if name !=None:
            kwargs['name'] = name
        ioType = self._initHandleArg('ioType',kwargs=kwargs,
                #required = True,
                desc = 'ioType'
                )
        props = kwargs['props'] if 'props' in kwargs else {}        
        if self.isRoot(): # add to inp/out dep on dir          
            dir = kwargs['dir'] if 'dir' in kwargs else None
            assert dir != None or ioType!=None,'[mod.ioAdd] dir or ioType required'
            if dir == None:
                dir = direction.LEFT if ioType == NodeIoType.INPUT else direction.RIGHT
            mod = self.modules().by('name',dir.graphModName())
            #return mod.impl().newIO(**kwargs)
            nme = kwargs['name'] if 'name' in kwargs else None

            size = kwargs['size'] if 'size' in kwargs else 1

            #if ioType == NodeIoType.INPUT:
            #    return mod.view().impl().addInput(nme,size=size)
            #else:
            #    return mod.view().impl().addOutput(nme,size=size)
            #if mod.mType() == ModuleType.IO:
            isIO = mod.mType() == ModuleType.IO

            props['isRoot']= True

            result = mod.view().impl().addIoNode(
                dir = dir,
                name = nme,
                size = size,
                ioType = ioType,
                props = props
            )
            if isIO: #this may should go to constructor of ioNode?
                result.setDriveSignal(result.intSignal())
        else:
            result = self.impl().newIO(**kwargs)
        return result
    
    #@api
    def signals(self, by=None):
        return self._signals.defaultGetter('name',by)

    #@api
    def sigs(self,by=None):
        return self.signals(by)

    #signals onlu direct children of cur module
    def _intSig(self):
        result = Q3Vector()
        if self.isRoot():
            tm = self.mod(direction.LEFT.graphModName())
            if tm!=None:
                result.appendAll(tm.signals())
            tm = self.mod(direction.RIGHT.graphModName())
            if tm!=None:
                result.appendAll(tm.signals()) #!TODO! reimplement optimal
        else:
            result = self.signals().filterBy('parent',self) #signals(by) !TODO! optimize filterBY 
        return result

    #@api
    def sig(self,by):
        assert by!=None, '[sig] "by" arg required not None'
        return self._intSig().defaultGetter('name',by)

    #@api - shortest
    def s(self, by):
        return self.sig(by)

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
    
    #@api
    def m(self,by):
        return self.mod(by)
    
    #@api
    def modL(self): #lefts
        return self.mod(direction.LEFT.graphModName())
    

    #@api
    def modR(self): #rights
        return self.mod(direction.RIGHT.graphModName())

    #@api
    def modT(self): #tops
        return self.mod(direction.TOP.graphModName())

    #@api
    def modD(self): #downs
        return self.mod(direction.DOWN.graphModName())

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
        tIoType = kwargs['ioType'] if 'ioType' in kwargs else None
        assert tIoType!=None, '[mod.newIO] ioType required'
        tname = kwargs['name'] if 'name' in kwargs else None
        if tname == None:
            #self.raiseExc('Name required')
            tnodes = self.nodes().filterBy('ioType',tIoType)
            SIZE = tnodes.size() 
            tname = f'#{SIZE}'
        tsize = kwargs['size'] if 'size' in kwargs else 1
        tprops = kwargs['props'] if 'props' in kwargs else {}
        sig = self.newSignal(name=tname,size=tsize,props=tprops)
        kwargs.pop('ioType',None)
        if 'isRoot' in tprops and tprops['isRoot']==True: #added from api on root level 
            tIoType = tIoType.oposite()
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
    def modAdd(self, moduleName:str,**kwargs):
        result = self.newModule(moduleName,**kwargs)
        if self.view()!=None:
            self.view().modAdd(moduleName, module=result)
        return result

    def newModule(self, moduleName:str, **kwargs):
        #on api level i think it would be better to have default moduleType = GRAPH if impl not present
        if 'moduleType' not in kwargs and 'impl' not in kwargs:
            kwargs['moduleType'] = ModuleType.GRAPH
        result = Module(self,moduleName,**kwargs)
        self.impl().add(result)
        return result             
        
    def isRoot(self):
        return isinstance(self.parent(), MainWindow) #alt id == 0

    def calculate(self):
        #calc nodes on input

        calc = getattr(self.impl(),'calc')
        if callable(calc):
            calc()
        if len(self._sigFormulas)>0:
            for nodName in self._sigFormulas:
                nod = self.nod(nodName)
                if nod!=None and nod.driveSignal()!=None:
                    tformula = self._sigFormulas[nodName]
                    self._evalSigFormula(nod.driveSignal(),tformula)

    def setCalculate(self,ncalculate):
        md = self       
        nm = types.MethodType(ncalculate ,md)
        setattr(md,'calculate',nm)

    def setCalc(self,ncalc):
        md = self.impl()       
        nm = types.MethodType(ncalc ,md)
        setattr(md,'calc',nm) 

    def updateTiming(self, delta):
        uTime = getattr(self.impl(),'updateTiming')
        if callable(uTime):
            uTime(delta)  

    # additional formulas for output signals
    def _evalSigFormula(self, signal:'Signal', formula:str,globals:dict={}):
        tglobals = globals
        for s in self.signals().values():
            tglobals[s.name()]=s
        tformula = formula
        if formula.startswith('='):
            tformula = formula[1:] #omit = sign
        fresult = eval(tformula,tglobals)
        signal.setValue(fresult)

    def canHaveFormula(self, nodName):
        nod = self.nod(nodName)
        canHave = nod!=None and ((nod.ioType() == NodeIoType.OUTPUT and not self.isRoot()) or (nod.ioType() == NodeIoType.INPUT and self.isRoot())) #and nod.driveSignal()!=None
        if canHave:
            return nod 
        return None

    #@api - set additional signal formula
    def setSigFormula(self, nodName:str,formula:str):
        if su.trim(formula) == '=':
            if nodName in self._sigFormulas:
                del self._sigFormulas[nodName]
            return 
        nod = self.canHaveFormula(nodName)
        assert nod!=None, f'[setSigFormula] For setting formula node has to exist and be output ({nodName})'
        self._evalSigFormula(nod.intSignal(),formula)
        self._sigFormulas[nodName] = formula

    #@api - read additional signal formula
    def sigFormula(self, nodName:str):
        result = self._sigFormulas[nodName] if nodName in self._sigFormulas else None
        return result

           




