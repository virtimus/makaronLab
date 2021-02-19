

from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, pyqtSignal as EventSignalBase
import PyQt5.QtWidgets as qtw


from .q3vector import Q3Vector

#class EventSignalBaseImpl(EventSignalBase):
#    def __init__(self, *args, **kwargs):
#        super(EventSignalBaseImpl, self).__init__(*args, **kwargs)
#from . import Object
class SyncHandler:
    def __init__(self, *args,**kwargs):
        self._registeredHandlers = Q3Vector()
        #super(SyncHandler,self).__init__(*args,**kwargs)
    
    def registerHandler(self, handler):
        assert callable(handler), f'[registerHandler] recieived handler not callable!{handler}'
        hname = getattr(callable, '__name__', repr(callable))
        self._registeredHandlers.append(hname,handler)

    def connect(self, handler):
        return self.registerHandler(handler)

    def hasHandlers(self):
        return self._registeredHandlers.size()>0

    def emit(self,*args, **kwargs):
        return self.sync(*args, **kwargs)

    def sync(self, *args, **kwargs):
        for tcall in  self._registeredHandlers.values():
            thandled = tcall(*args,**kwargs)
            if thandled == True:
                return 



EventSignal = EventSignalBase

EventBase = qtw.QGraphicsObject

class EventProps:
    def __init__(self, props={}):
        self._props = props
    
    def props(self, name:str=None):
        result = self._props[name] if name != None and name in self._props else self._props
        return result

CommandBase = EventBase

CommandSignal = EventSignal

class CommandProps(EventProps):
    def __init__(self, props={}):
        super(CommandProps, self).__init__(props)
