
from .Object import Object
from .Pin import Pin
from .Module import Module

class Signal(Object):
    def __init__(self, *args, **kwargs):
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Signal] Parent has to be descendant of wq.Module')        
        self._size = None
        if len(args)>1:#//second param always size
            self._size = args[1]
            args = (args[0],None)
        self._size = kwargs['size'] if 'size' in kwargs else self._size
        if self._size == None:
            self.raiseExc('[Signal] size Unknown')
        self._drivePin = kwargs['drivePin'] if 'drivePin' in kwargs else None 
        if self._drivePin == None:
            self.raiseExc('[Signal] drivePin not given')
        self._slavePins = kwargs['slavePins'] if 'slavePins' in kwargs else [] 
        kwargs.pop('drivePin', None)
        kwargs.pop('slavePins', None)
        args = self._loadInitArgs(args)      
        super(Signal, self).__init__(*args, **kwargs)

    def addSlavePin(self,slP:Pin):
        self._slavePins.append(slP)
