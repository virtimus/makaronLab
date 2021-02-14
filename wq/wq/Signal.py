
from .Object import Object
#from .Pin import Pin
from .Module import Module
from .Module import Node

from .wqvector import WqVector

class Signal(Object):
    def __init__(self, *args, **kwargs):
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Signal] Parent has to be descendant of wq.Module') 
        self._name = kwargs['name'] if 'name' in kwargs else None
        if self._name == None:
            self.raiseExc(f'Name of Signal required')   
        self._info = kwargs['info'] if 'info' in kwargs else None
        self._desc = kwargs['desc'] if 'desc' in kwargs else None
#        self._driveNode = None
#        if 'driveNode' in kwargs:
#            self.addNode(kwargs['driveNode'])       
#        self._nodes = WqVector(Node) 
#        if self._driveNode != None and self._driveNode.size() != None:
#            self._size = self._driveNode.size()
#        else: 
        self._size = kwargs['size'] if 'size' in kwargs else None
        if self._size == None:
            self.raiseExc('Size for signal not specified')
        self._value = False if self._size == 1 else 0
        super(Signal, self).__init__(*args, **kwargs)
        #self._id = len(self.parent().graphModule().signals())
        self._id = self.parent().graphModule().signals().nextId()
        self._no = len(self.parent().signals())
        #self.parent()._signals[self.id()]=self
        self.parent().graphModule().addSignal(self)
        self.parent().addSignal(self)

    def acceptVisitor(self, v):
        v.visitSignal(self)

    def id(self):
        return self._id

    def no(self):
        return self._no

    def name(self):
        return self._name

    def size(self):
        return self._size

    def setSize(self, nsize:int):
        if self._size == nsize:
            return
        self._size = nsize
        #for node in self._nodes.values():!TODO! disconnect?
        #    node.setSize()

    def value(self):
        return self._value

    def setValue(self, newVal):
        if newVal != self._value:
            self._value = newVal

    def isOn(self):
        result = self._value if self.size()==1 else self._value>0
        return result
    
    def resetValue(self):
        prevValue = self._value
        if isinstance(self._value, bool):
            self._value = False
        else:
            self._value = 0
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