
from .Object import Object
#from .Pin import Pin
from .Module import Module
from .Module import Node

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
        self._driveNode = None
        if 'driveNode' in kwargs:
            self.addNode(kwargs['driveNode'])       
        self._nodes = {} 
        if self._driveNode != None and self._driveNode.size() != None:
            self._size = self._driveNode.size()
        else: 
            self._size = kwargs['size'] if 'size' in kwargs else None
        if self._size == None:
            self.raiseExc('Size for signal not specified')
        self._value = False
        super(Signal, self).__init__(*args, **kwargs)
        self._id = len(self.parent().signals())
        #self.parent()._signals[self.id()]=self
        self.parent().addSignal(self)

    def id(self):
        return self._id

    def name(self):
        return self._name

    def size(self):
        return self._size

    def value(self):
        return self._value

    def setValue(self, newVal):
        self._value = newVal

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

    def addNode(self, node:Node):
        if self._driveNode == None:
            self.setDriveNode(node)
        tid = node.id()
        if tid in self._nodes:
            self.raiseExc(f'Node with id {tid} already added')        
        if self._driveNode.size()!=node.size():
            self.raiseExc('Node size differs')
        self._nodes[node.id()]=node 