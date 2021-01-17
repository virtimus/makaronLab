
from .Object import Object
from .Module import Module

class Pin(Object):
     def __init__(self, *args, **kwargs):    
        args = self._loadInitArgs(args)
        if not isinstance(args[0],Module):
            self.raiseExc('[Pin] Parent has to be descendant of wq.Module')
        if args[1] == None:
            self.raiseExc('[Pin] Name has to be given')
        self._name=args[1]
        self._desc = args[2] if len(args)>2 else None
        args = (args[0], None)
        super(Pin, self).__init__(*args, **kwargs)