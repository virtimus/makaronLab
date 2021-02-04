import json
from collections import OrderedDict

#@refs:https://stackoverflow.com/questions/8651095/controlling-yaml-serialization-order-in-python

from ..Module import Module, Node, IoNode
from ..Signal import Signal
from ..ModuleView import ModuleView
from ..ModuleFactory import ModuleImplBase
from ..wqvector import WqVector

from ..dict import UnsortableOrderedDict as UODict

class Visitor:
    def __init__(self):
        self._jsD = OrderedDict()
        self._keyStack = WqVector()
        self._visitedModules = WqVector()
        self._visitedSignals = WqVector()
        self._visitedNodes = WqVector()
        self._visitedModViews = WqVector() 
        self._visitedModImpls = WqVector() 
        self._cstack = self._jsD
        self._ckey = None
        pass

    def pushState(self, id):
        name = self._ckey
        if name == None:
            return         
        self._keyStack.push(self._cstack)    
        c = OrderedDict()
        if self._cstack == None:
            print('[WARN] self._cstack == None')
        if not name in self._cstack:
            self._cstack[name] = OrderedDict()
        self._cstack[name][id] = c
        self._cstack = self._cstack[name][id]
        if self._cstack == None:
            print('[WARN] self._cstack == None')      
        return c

    def popState(self):
        self._cstack = self._keyStack.pop()
        if self._cstack == None:
            print('[WARN] self._cstack == None')        
        return self._cstack



    def visitModule(self, mod:Module):
        tid = mod.id()
        if tid in self._visitedModules:
            return
        self._visitedModules.append(tid, mod)
        tname = 'modules'  
        if (tid == 0):#root
            tname = 'rootModule' 
        self._ckey = tname
        c = self.pushState(tid) 
        
        c['name'] = mod.name()
        c['mType'] = mod.mType().name
        c['desc'] = mod.desc()
        c['rootModuleId'] = int(mod._rootModule.id())
        c['graphModuleId'] = int(mod._graphModule.id())
        c['class'] = str(mod.__class__)

        
        for m in mod.modules().values():
            self._ckey = 'modules'
            m.acceptVisitor(self)
        
        for n in mod.nodes().values():
            self._ckey = 'nodes'
            n.acceptVisitor(self)
        
        for s in mod.signals().values():
            self._ckey = 'signals'
            s.acceptVisitor(self)

        self._ckey = 'view'
        mod.view().acceptVisitor(self)
        self._ckey = 'impl'
        mod.impl().acceptVisitor(self)
        self.popState()
        
    def visitSignal(self, sig:Signal):
        tid = sig.id()
        if tid in self._visitedSignals:
            return
        self._visitedSignals.append(tid, sig)   
        c = self.pushState(tid) 

        c['name'] = sig.name()
        c['_no_'] = sig.no()
        c['size'] = int(sig.size())
        c['value'] = int(sig.value())
        c['class'] = str(sig.__class__)
#        c['driveNode'] = sig.driveNode().id() if sig.driveNode()!=None else None #'!!null'
#        self._ckey = 'nodes'
#        for n in sig.nodes().values():
#            self.pushState(s.id())
#            self.popState()
        self.popState()


    def visitNode(self, nod:Node):
        tid = nod.id()
        if tid in self._visitedNodes:
            return
        self._visitedNodes.append(tid, nod)   
        c = self.pushState(tid) 

        #c['class'] = str(nod.__class__)
        c['name'] = nod.name()
        c['_no_'] = nod.no()
        c['info'] = nod.info()
        c['desc'] = nod.desc()
        c['class'] = str(nod.__class__)
        c['driveSignal'] = nod.driveSignal().id() if nod.driveSignal()!=None else None #'!!null'
        self._ckey = 'signals'
        for s in nod.signals().values():
            self.pushState(s.id())
            self.popState()

        
        #c['value'] = sig.value()
        
        self.popState()
        return c

    def visitIoNode(self, nod:IoNode):
        c = self.visitNode(nod)
        if c != None: #not yet visited
            ioType = nod.ioType() 
            ioTypeName = ioType.name
            c['ioType'] = ioTypeName



    def visitModuleView(self, mv:ModuleView):
        tid = mv.id()
        if tid in self._visitedModViews:
            c = self.pushState(tid)
            self.popState()
            return
        self._visitedModViews.append(tid,mv)   
        c = self.pushState(tid) 

        c['class'] = str(mv.__class__)
        #c['value'] = sig.value()

        self.popState()


    def visitModuleImpl(self,mimpl:ModuleImplBase):
        tid = mimpl.id()
        if tid in self._visitedModImpls:
            return
        self._visitedModImpls.append(tid,mimpl)   
        c = self.pushState(tid) 
        c['name'] = mimpl.name()
        c['info'] = mimpl.info()
        c['desc'] = mimpl.desc()
        c['class'] = str(mimpl.__class__)
        c['implStr'] = mimpl._implStr
        #c['value'] = sig.value()

        self.popState()