
from q3.ui.engine import qtw,qtc,qtg

EventSignalBase = qtc.Signal  



from .q3vector import Q3Vector
from .Timer import Timer

#@deprecated - wrong direction
class DoneItem: 
    def __init__(self):
        self._done = False

    def done(self):
        return self._done

    def setDone(self, n):
        self._done = n

    def waitForDone(self):
        tm = Timer()
        ms5k = tm.ms(5000)
        while(tm.now()-tm.startTime()<ms5k and not self._done):
            tm.sleepMs(0)
        assert self._done, '[DoneItem.waitForDone] Job not finished after 5 sek'

    def emit(self):
        self._event.emit(self._eventProps)

    @staticmethod
    def emitAndWaitForDone(event,ep:'EventProps'):
        di = DoneItem()
        di._event = event
        ep._props['doneItem']=di
        di._eventProps = ep
        th2 = threading.Thread(target=di.emit)
        th2.start()
        #Timer.sleepMs(500)
        #di.waitForDone()

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

import threading, queue
class QueueHandler:
    def __init__(self, *args,**kwargs):
        self._queue = queue.Queue()

    def connect(self):
        pass
             

EventSignal = EventSignalBase

class EventBase(qtw.QGraphicsObject):
    def __init__(self,*args,**kwargs):
        self._dynEvents = {}
        super(EventBase, self).__init__(*args,**kwargs)

    def dyn(self,name:str):
        #assert not name in self._dynEvents, f'DynEvent with name {name} already registered'
        if name not in self._dynEvents:
            self._dynEvents[name]=EventSignal(EventProps)
        return self._dynEvents[name]



class EventProps:
    def __init__(self, props={}):
        self._props = props
    
    def props(self, name:str=None):
        result = self._props[name] if name != None and name in self._props else self._props
        return result

    def setDone(self, d:bool):
        #doneItem = self.props('doneItem')
        #if doneItem!=None:
        #    doneItem.setDone(d)
        pass

CommandBase = EventBase

CommandSignal = EventSignal

class CommandProps(EventProps):
    def __init__(self, props={}):
        super(CommandProps, self).__init__(props)
