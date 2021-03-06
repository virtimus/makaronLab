from . import consts
from .Object import Object
#from .Pin import Pin
from .Module import Module
from .Module import Node

from .q3vector import Q3Vector


from .valuetype import ValueType

from . import bitutils as bu

from .EventSignal import EventSignal, EventBase, EventProps

class Signal(Object):
    class Events(EventBase):
        signalValueChanged = EventSignal(EventProps)
        def emitSignalValueChanged(self, d:dict):
            d['eventName']='signalValueChanged' 
            self.signalValueChanged.emit(EventProps(d))

    def __init__(self, *args, **kwargs):
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Signal] Parent has to be descendant of q3.Module') 
        self._name = kwargs['name'] if 'name' in kwargs else None
        if self._name == None:
            self.raiseExc(f'Name of Signal required')   
        self._info = kwargs['info'] if 'info' in kwargs else None
        self._desc = kwargs['desc'] if 'desc' in kwargs else None
        self._dvOut = False 
        self._events = Signal.Events()
#        self._driveNode = None
#        if 'driveNode' in kwargs:
#            self.addNode(kwargs['driveNode'])       
#        self._nodes = Q3Vector(Node) 
#        if self._driveNode != None and self._driveNode.size() != None:
#            self._size = self._driveNode.size()
#        else: 
        tsize = kwargs['size'] if 'size' in kwargs else None
        if tsize == None:
            self.raiseExc('Size for signal not specified')
        assert tsize<=consts.MAX_SIGNAL_SIZE, f'Max signal size overflow({tsize})'
        svlType = ValueType.fromSize(tsize) 
        self._valueType = ValueType(0,tsize,svlType._colorSigOff,svlType._colorSigOn)
        self._valueType.setParentSignal(self)
        #self._size = self._valueType.size()
        #self._value = False if tsize == 1 else 0 moved to valueType
        super(Signal, self).__init__(*args, **kwargs)
        #self._id = len(self.parent().graphModule().signals())
        self._id = self.parent().rootModule().allSignals().push(self)
        self._no = len(self.parent().signals())
        #self.parent()._signals[self.id()]=self
        self.parent().graphModule().addSignal(self)
        if not self.parent().graphModule() is self.parent():
            self.parent().addSignal(self)

    def acceptVisitor(self, v):
        v.visitSignal(self)

    def module(self):
        return self.parent()

    def events(self):
        return self._events
    
    def consoleWrite(self, dta):
        self.module().consoleWrite(dta)

    def id(self):
        return self._id

    def no(self):
        return self._no

    def name(self):
        return self._name

    def size(self):
        #return self._size
        return self._valueType.size()
    '''
    def setSize(self, nsize:int):
        if self._size == nsize:
            return
        assert nsize<=consts.MAX_SIGNAL_SIZE, f'Max signal size overflow({nsize})'
        self._size = nsize
        self._valueType = ValueType.fromSize(self._size)
        #for node in self._nodes.values():!TODO! disconnect?
        #    node.setSize()
    '''

    def valueType(self):
        return self._valueType 
        
    def value(self):
        #return self._value
        return self._valueType.value()

    def valueAsUInt(self):
        return self._valueType.asUInt()

    def setValue(self, newVal):
        return self._valueType.setValue(newVal)

    #@api func to setup onValueChanged
    def setupValueChanged(self, onValueFunc):
        #self.onValueChanged = onValueFunc
        #first call to set value in monitor
        #onValueFunc(None,self.value())
        self.events().signalValueChanged.connect(onValueFunc)



    #@apiInternal - function to replace to monitor signal changes - called from valueType delta
    def onValueChanged(self, prevVal, newVal):
        self.events().emitSignalValueChanged({'prevVal':prevVal,'newVal':newVal})
        pass

    def isOn(self):
        result = self.value() if self.size()==1 else self.value()>0
        return result
    
    '''None - disconnected
    def resetValue(self):
        return self._valueType.resetValue()
    '''


    #some methods for slice calculation
    def __getitem__(self,i):
        ind = i
        size = 1
        if isinstance(i,slice):
            ind = i.start
            size = i.stop - i.start
        result = bu.readBits(self.valueAsUInt(),ind,size)
        return result

    def __len__(self):
        return self.size()

    def dvIn(self,n:bool=None):
        if n!=None:
            self._dvOut = not n
        return not self._dvOut

    def dvOut(self,n:bool=None):
        if n!=None:
            self._dvOut = n
        return self._dvOut



#        if self._value != prevValue and self._driveNode != None: #delta propagation ?
#            self._driveNode.resetValue()

##    def driveNode(self):
##        return self._driveNode
'''
    def setDriveNode(self, node:Node):
        if self._driveNode == None:
            self._driveNode = node
        else:
            if self._driveNode.size()!=node.size():
                self.raiseExc('Node size differs')
            msg = node.canDrive()
            if msg == None:
                self._driveNode = node
            else: 
                self.raiseExc(f'[node.canDrive]: {msg}')

    def nodes(self):
        return self._nodes

    def addNode(self, node:Node):
        if self._driveNode == None:
            self.setDriveNode(node)
        tid = node.id()
        if tid in self._nodes:
            self.raiseExc(f'Node with id {tid} already added')        
        if self._driveNode.size()!=node.size():
            self.raiseExc('Node size differs')
        self._nodes.append(node.id(),node) 

'''