
from .Object import Object
from .Module import Module
from .deltavector import DeltaVector
#from .Signal import Signal
'''
class Pin(Object):
    def __init__(self, *args, **kwargs):
        #//self._deltaVector = DeltaVector.NONE     
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Pin] Parent has to be descendant of wq.Module')
        #if args[1] == None:
        #    self.raiseExc('[Pin] Name has to be given')  
        #self._name=args[1]
        
        #self._desc = kwargs['desc'] if 'desc' in kwargs else None
        #self._size = kwargs['size'] if 'size' in kwargs else 1
        self._intSignal = kwargs['intSignal'] if 'intSignal' in kwargs else None
        if self._intSignal == None:
            self.raiseExc(f'No intSignal given to pin {self.name()}')
        #self._info = args[2] if len(args)>2 else None
        self._extSignal = None
        args = (args[0], None)
        super(Pin, self).__init__(*args, **kwargs)


    def module(self):
        return self._parent
    
    def intSignal(self):
        return self._intSignal

    def size(self):
        return self.intSignal().size()
    
    def desc(self):
        return self.intSignal().desc()

    def info(self):
        return self.intSignal().info()

    def name(self):
        return self.intSignal().name()

    def signal(self):
        return self._intSsignal

    def addExtSignal(self, newSignal:Signal):
        if newSignal.size() != self.size():
            self.raiseExc(f'Cannot set signal {newSignal.name()} to pin {self.name()} - sizes differ')
        self._signal = newSignal
'''    