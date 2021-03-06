
import pyqtgraph.console


from . import consts



def handleArg(obj, name, **kwargs):
        defD = kwargs
        tkwargs = defD['kwargs'] if 'kwargs' in defD else None
        if tkwargs == None: #single arg?
            if 'value' in kwargs: #single arg
                argVal = kwargs['value']
                tkwargs = kwargs
                tkwargs[name] =argVal

        assert tkwargs != None, f'kwargs is None !'
        trequired = defD['required'] if 'required' in defD else False       
        tdefault = defD['default'] if 'default' in defD else None
        tdomainValues = defD['domainValues'] if 'domainValues' in defD else None
        tdesc = defD['desc'] if 'desc' in defD else None
        result = tkwargs[name] if name in tkwargs else tdefault
        tclname = obj.__class__.__name__
        assert tdesc != None, f'[console.handleArg] Required description argument (desc) missing for {tclname}'
        assert result != None or not trequired, f'[console.handleArg] Required keyword argument "{name}" missing for {tclname}'
        assert tdomainValues == None or result == None or result in tdomainValues, f'Keyword argument {name} not in given domainValues:{tdomainValues}'
        return result

def isArgHelp(**kwargs):
    return 'help' in kwargs and kwargs['help']==True


from .EventSignal import EventBase, EventSignal, EventProps, SyncHandler


class ConsoleCtrl:
    class Events(EventBase):
        callConsoleWrite = SyncHandler()
        pass

    def __init__(self, parent, **kwargs):
        self._parent = parent
        self._registeredCommands = {'registerCommand':self.registerCommand,'registerProp':self.registerProp}
        self._registeredProps = {}
        self._globalNamespace = None
        self._events = ConsoleCtrl.Events()

        #self.events().callConsoleWrite.connect(self.consoleWrite)
    
    def parent(self):
        return self._parent

    def events(self):
        return self._events

    def __getattr__(self, name):
        result =  self._registeredCommands[name] if name in self._registeredCommands else None
        if name in self._registeredProps:
            result = result() # get the prop
        return result

    def setGlobalNamespace(self,ns):
        self._globalNamespace = ns

    def registerProp(self,name:str,handler):
        assert name not in self._registeredProps, f'Property with name {name} already registered'
        self._registeredProps[name]=handler
        result = self.registerCommand(name,handler,False)
        return result

    def registerCommand(self, name:str, handler, asGlobal=False):
        assert name not in self._registeredCommands, f'Method with name {name} already registered'
        #assert callable(handler), f'Handler not callable for command:{name} (registration problem)'
        if asGlobal and self._globalNamespace !=None:
            self._globalNamespace[name] = handler
        else:
            self._registeredCommands[name] = handler

    def command(self, commandName:str,asGlobal=False):
        result = None
        if asGlobal:
            result = self._globalNamespace[commandName] if commandName in self._globalNamespace else None
        else:
            result = self._registeredCommands[commandName] if commandName in self._registeredCommands else None
        return result
    #def registerAutoCorrection(self,)

namespace = {} #{'pg': pg, 'np': np}
text = 'makaronLab CLI'

globNS = globals()

def newConsoleWidget(parent,**kwargs):
    tconsctrl = ConsoleCtrl(parent,**kwargs)
    namespace['c']=tconsctrl
    namespace['gc']=globNS
    tconsctrl.setGlobalNamespace(namespace)
    cw = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)
    namespace['cw']=cw
    cw._namespace = namespace
    return cw
