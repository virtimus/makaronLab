
from .Object import Object
from .MainWindow import MainWindow
from .Module import Module

from .moduletype import ModuleType

from enum import Enum

from . import direction


from q3.ui.engine import qtw,qtc,qtg

from .DetailWindow import DetailWindow

import threading


class ModuleView(Object):
    def __init__(self, *args, **kwargs):
        #self._gridDensity = None
        self._selectedModule = None
        self._parentTab = None 
        self._detailWindow = None
        self._avcThread = None
        self._hasTopsDowns = False
        self._tokenId = None
        #self._scheduledScalings = None;  
        args = self._loadInitArgs(args)
        d1 = isinstance(args[0],ModuleView)
        d2 = isinstance(args[0],MainWindow)
        self._isRoot = d2
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[ModuleView] Parent has to be descendant of q3.ModuleView or q3.MainWindow')
        self._module = kwargs['module'] if 'module' in kwargs else None
        if self._module == None:
            self.raiseExc('[ModuleView] keyword argument module required')
        if self._module._view != None:
            self.raiseExc(f'[ModuleView] Other view already assigned to module {self._module.name()}')
        self._module._view = self    
        d3 = isinstance(self._module,Module)
        if (not d3):
            self.raiseExc('[ModuleView] module given has to be descendant or class of Module')
        #args = (args[0], None) 
        #self._moduleViews = {0:self}
        #self._id = 0
        self._moduleView = self.q3D().doModuleView_Init()
        args = (args[0],self._moduleView) #impl
        kwargs.pop('module', None)      
        super(ModuleView, self).__init__(*args, **kwargs)
        if d2: #rootView - create additional inputs/outputs module
            self._inputsView = ModuleView(self,
                module=Module(self.module(),
                    direction.LEFT.graphModName(),
                    moduleType=ModuleType.IO,
                    props = {
                        'dir': direction.LEFT
                    }

                    )
                )
            self._outputsView = ModuleView(self,
                module=Module(self.module(),
                    direction.RIGHT.graphModName(),
                    moduleType=ModuleType.IO,
                    props = {
                        'dir':direction.RIGHT
                    }
                    )
                )
            if self._hasTopsDowns:
                self._topsView = ModuleView(self,
                    module=Module(self.module(),
                        direction.TOP.graphModName(),
                        moduleType=ModuleType.IO,
                        props = {
                            'dir':direction.TOP
                        }
                        )
                    ) 
                self._downsView = ModuleView(self,
                    module=Module(self.module(),
                        direction.DOWN.graphModName(),
                        moduleType=ModuleType.IO,
                        props = {
                            'dir':direction.DOWN
                        }
                        )
                    )


        self.q3D().doModuleView_AfterInit()
        if d1: #register in parent
            self.module().graphModule().addModuleView(self)
            #self._id = len(self.parent().moduleViews())
            #self.parent().addModuleView(self)
            #self.parent()._moduleViews[self._id]=self

        #recurse into submodules - moved to module.addModuleView
        #'''
        #self._moduleViews = {}
        #if len(self._module.modules())>1: #0 is self/root
        if self._isRoot:
            for tmoduleId in self._module.modules():                
                if tmoduleId>0: #not self
                    tmodule = self._module.modById(tmoduleId)
                    if (not tmodule.moduleType() in [ModuleType.IO]): # inputs/outputs don't need recursive init - view created
                        tModuleView = ModuleView(self,module=tmodule)
        #''
        if self.module().impl()!=None and hasattr(self.module().impl(),'__afterViewCreated__'):
            ac = getattr(self.module().impl(),'__afterViewCreated__')
            if (callable(ac)):
                ac(self.impl())
                #self.startInThread(ac)

    #def startInThread(self, tocall):
    #    self._avcThread = threading.Thread(target=tocall) #std::thread(&Package::dispatchThreadFunction, this);
    #    self._avcThread.start()

    #used to identify during async creation
    def tokenId(self):
        return self._tokenId
    
    def setTokenId(self, tokId):
        self._tokenId = tokId

    def events(self):
        return self.module().events()

    def parentTab(self):
        return self._parentTab

    def setParentTab(self, tab):
        self._parentTab = tab

    def hasTopsDowns(self):
        return self._hasTopsDowns

    #@api
    def prp(self,by):
        return self.impl().prp(by)

    #@api
    def tabIndex(self):       
        result = self._parentTab.parent().indexOf(self._parentTab) if self._parentTab != None and self._parentTab.parent()!=None else None
        return result

    #@api
    def expand(self):
        return self.impl().expand()

    #@api
    def collapse(self):
        return self.impl().collapse()

    def acceptVisitor(self, v):
        v.visitModuleView(self)  

    def id(self):
        #return self._id
        return self.module().id()

    def name(self):
        return self.module().name()


    def moduleViews(self):
        return self._moduleViews

    #@api
    def setRotate(self, rot:bool):
        self.impl().setRotate(rot)
        self.impl().updateRotation()

    #@api
    def setInvert(self,inv:bool):
        self.impl().setInvertH(inv)
        self.impl().updateInversion()

    #@api
    def modAdd(self, name:str, **kwargs):
        return self.newModule(name,**kwargs)

    def newModule(self,moduleName:str, **kwargs):
        nmodule = self._initHandleArg('module',kwargs = kwargs,
            desc = 'module to add view to'
            )
        if nmodule == None:
            nmodule = self.module().newModule(moduleName,**kwargs)
        if self.module().isRoot() and nmodule.view()==None: #if we are root and there is no view for module already
            tModuleView = ModuleView(self,module=nmodule)
        return nmodule



    #def addModuleView(self, moduleView:'ModuleView'): #commented no reg from outside ?
    #    tid = moduleView.id()
    #    if tid in self._moduleViews:
    #        self.raiseExc(f'ModuleView with id {tid} already in collection of subViews')
    #    self._moduleViews[tid]=moduleView


    # add-sumodule
    '''
    def addModuleView(self,name, type=ModuleType.ATOMIC, module=None):
        if (module == None):
            module = Module(self.module(),name,type=type)
        result = ModuleView(self,module=module)
        return result
    '''

    def module(self):
        return self._module

    def isRoot(self):
        #return self._module.isRoot()
        return self._isRoot

    def open(self):
        result = self.q3D().impl().open()
        return result
    
    #@s:PackageView::setSelectedNode
    #@api
    def setSelectedModule(self, module:Module):
        tmod = module if module != None else self.module()
        if tmod.view()!=None:
            self.impl().setSelected(tmod.view().impl())
            if tmod.view().detailWindow()!=None:
                if tmod.view().detailWindow().impl().isVisible():
                    tmod.view().detailWindow().show()
                    tmod.view().detailWindow().impl().activateWindow()
        self._selectedModule = tmod
        return self._selectedModule
    
    #@api
    def modsel(self,module:Module):
        return self.setSelectedModule(module)

    #@s:PackageView::showProperties()
    def showProperties(self):
        '''
        m_properties->clear();
        m_properties->setColumnCount(2);
        m_properties->setHorizontalHeaderLabels(QString("Name;Value").split(";"));

        m_selectedNode->showProperties();
        m_properties->horizontalHeader()->setStretchLastSection(true);
        '''
        pass



#    #@s:PackageView::wheelEvent(QWheelEvent *a_event)
#    def wheelEvent(self, event):
#        self.q3D().doModuleView_wheelEvent(event)

    def detailWindow(self):
        return self._detailWindow

    def showDetailWindow(self,**kwargs):
        tevent = self._initHandleArg('event',
            kwargs = kwargs,
            default = None,
            desc = 'Optional event param'
            )
        if self._detailWindow == None:
            self._detailWindow = DetailWindow(**kwargs) if self._detailWindow == None else self._detailWindow
        self._detailWindow.setEvent(tevent)
        self._detailWindow.show()
        self.module().graphModule().view().setSelectedModule(self.module())



            



