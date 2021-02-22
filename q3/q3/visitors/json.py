import json
from collections import OrderedDict

#@refs:https://stackoverflow.com/questions/8651095/controlling-yaml-serialization-order-in-python

from ..Module import Module, Node, IoNode
from ..Signal import Signal
from ..ModuleView import ModuleView
from ..ModuleFactory import ModuleImplBase
from ..EditorFrame import EditorFrame
from ..q3vector import Q3Vector

from ..dict import UnsortableOrderedDict as UODict

class Visitor:
    apiMethods = 'apiMethods'
    def __init__(self):
        self._jsD = OrderedDict()
        self._keyStack = Q3Vector()
        self._visitedModules = Q3Vector()
        self._visitedSignals = Q3Vector()
        self._visitedNodes = Q3Vector()
        self._visitedModViews = Q3Vector() 
        self._visitedModImpls = Q3Vector() 
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
        if (id != None):
            self._cstack[name][id] = c
            self._cstack = self._cstack[name][id]
        else:#none as id means 'only one object'
            self._cstack[name] = c
            self._cstack = self._cstack[name]            
        if self._cstack == None:
            print('[WARN] self._cstack == None')      
        return c

    def popState(self):
        self._cstack = self._keyStack.pop()
        if self._cstack == None:
            print('[WARN] self._cstack == None')        
        return self._cstack

    def visitEditor(self,ed:EditorFrame):
        self._ckey = 'editorFrame'
        c = self.pushState(None)
        appClass = str(ed.app().__class__) if ed.app() != None else None
        conClass = str(ed.consoleWidget().__class__) if ed.consoleWidget() != None else None
        
        c['app']=OrderedDict({
            'class':appClass    
        })
        c['consoleWidget']=OrderedDict({
            'class':conClass
        })
        
        self._ckey ='rootModuleByInd' 
        i = 0
        tc = ed.rootModuleCount()
        for ti in range(i,tc, 1):
            c = self.pushState(ti)
            module = ed.rootModuleByInd(ti)
            module.acceptVisitor(self) 
            self.popState()

        #ed._rootModule.acceptVisitor(self)
        self.popState()


    def visitModule(self, mod:Module):
        tid = mod.id()
        if tid in self._visitedModules:
            return
        self._visitedModules.append(tid, mod)
        tname = 'modules'
        tids = tid  
        if (tid == 0):#root
            tname = 'rootModule'
            tids = None

        self._ckey = tname
        c = self.pushState(tids) 
        
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
# nodes collection reduced from signal - to be verified if needed there
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
        #apiMetods
        c[self.apiMethods] = {}
        am = c[self.apiMethods]
        am['connect']={
            'desc':'s.connect(t) - connect from s to t node'
        }
        
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