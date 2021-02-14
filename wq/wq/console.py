
import pyqtgraph.console


from . import consts



def handleArg(obj, name, **kwargs):
        defD = kwargs
        kwargs = defD['kwargs'] if 'kwargs' in defD else None
        assert kwargs != None, f'kwargs is None !'
        trequired = defD['required'] if 'required' in defD else False       
        tdefault = defD['default'] if 'default' in defD else None
        tdesc = defD['desc'] if 'desc' in defD else None
        result = kwargs[name] if name in kwargs else tdefault
        tclname = obj.__class__.__name__
        assert tdesc != None, f'[console.handleArg] Required description argument (desc) missing for {tclname}'
        assert result != None or not trequired, f'[console.handleArg] Required keyword argument {name} missing for {tclname}'
        return result

def isArgHelp(**kwargs):
    return 'help' in kwargs and kwargs['help']==True





class ConsoleCtrl:
    def __init__(self, parent, **kwargs):
        self._parent = parent
        self._registeredCommands = {'registerCommand':self.registerCommand}
        self._globalNamespace = None
    
    def parent(self):
        return self._parent

    def __getattr__(self, name):
        result =  self._registeredCommands[name] if name in self._registeredCommands else None
        return result

    def setGlobalNamespace(self,ns):
        self._globalNamespace = ns

    def registerCommand(self, name:str, handler, asGlobal=False):
        assert name not in self._registeredCommands, f'Method with name {name} already registered'
        #assert callable(handler), f'Handler not callable for command:{name} (registration problem)'
        if asGlobal and self._globalNamespace !=None:
            self._globalNamespace[name] = handler
        else:
            self._registeredCommands[name] = handler

    #def registerAutoCorrection(self,)

namespace = {} #{'pg': pg, 'np': np}
text = 'makaronLab CLI'

globNS = globals()

def newConsoleWidget(parent,**kwargs):
    tconsctrl = ConsoleCtrl(parent,**kwargs)
    namespace['g']=tconsctrl
    namespace['gc']=globNS
    tconsctrl.setGlobalNamespace(namespace)
    c = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)
    c._namespace = namespace
    return c
