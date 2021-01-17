
from .Object import Object
from .MainWindow import MainWindow

from . import moduletype

class Module(Object):
    def __init__(self, *args, **kwargs):
        _view = None   
        args = self._loadInitArgs(args)
        d1 = isinstance(args[0],Module)
        d2 = isinstance(args[0],MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[Module] Parent has to be descendant of wq.Module or wq.MainWindow')
        if args[1] == None:
            self.raiseExc('[Module] Name has to be given')
        self._name=args[1]
        args = (args[0], None) 
        kwargs.pop('type', None)  
        super(Module, self).__init__(*args, **kwargs)
    
        
    def location(self):
        return self._name

    def name(self):
        return self._name

    def path(self):
        result = "/"+self.name() if self.isRoot() else str(self.parent().path()) + "/" + self.name()

    def view(self):
        return self._view
        
    '''
    def __hash__(self):
        return hash(self.path())

    def __eq__(self, other):
        #return (self.path()) == (other._path)
        #return (self.name, self.location) == (other.name, other.location)
        return (self.path() == other)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)        
    '''
    def isRoot(self):
        return isinstance(self.parent(), MainWindow)