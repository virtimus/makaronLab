
from .Object import Object
from .MainWindow import MainWindow
from .Module import Module

from .moduletype import ModuleType

from enum import Enum


from PyQt5.QtGui import QBrush, QColor, QPen

from PyQt5.QtCore import QPointF




class ModuleView(Object):
    def __init__(self, *args, **kwargs):
        #self._gridDensity = None
        self._selectedModule = None 
        #self._scheduledScalings = None;  
        args = self._loadInitArgs(args)
        d1 = isinstance(args[0],ModuleView)
        d2 = isinstance(args[0],MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[ModuleView] Parent has to be descendant of wq.ModuleView or wq.MainWindow')
        self._module = kwargs['module'] if 'module' in kwargs else None
        if self._module == None:
            self.raiseExc('[ModuleView] keyword argument module required')
        self._module._view = self    
        d3 = isinstance(self._module,Module)
        if (not d3):
            self.raiseExc('[ModuleView] module given has to be descendant or class of Module')
        #args = (args[0], None) 
        self._moduleViews = {0:self}
        self._id = 0
        self._moduleView = self.wqD().doModuleView_Init()
        args = (args[0],self._moduleView) #impl
        kwargs.pop('module', None)         
        super(ModuleView, self).__init__(*args, **kwargs)

        if d2: #rootView - create additional inputs/outputs module
            self._inputsView = ModuleView(self,
                module=Module(self.module(),
                    'moduleInputs',
                    type=ModuleType.INPUTS
                    )
                )
            self._outputsView = ModuleView(self,
                module=Module(self.module(),
                    'moduleOutputs',
                    type=ModuleType.OUTPUTS
                    )
                )
        self.wqD().doModuleView_AfterInit()
        if d1: #register in parent
            self._id = len(self.parent().moduleViews())
            #self.parent().addModuleView(self)
            self.parent()._moduleViews[self._id]=self

        #recurse into submodules
        self._moduleViews = {}
        if len(self._module.modules())>1: #0 is self/root
            for tmoduleId in self._module.modules():                
                if tmoduleId>0: #not self
                    tmodule = self._module.modById(tmoduleId)
                    if (not tmodule.type() in [ModuleType.INPUTS, ModuleType.OUTPUTS]): # inputs/outputs don't need recursive init - view created
                        tModuleView = ModuleView(self,module=tmodule)
            
    def id(self):
        return self._id

    def name(self):
        return self.module().name();


    def moduleViews(self):
        return self._moduleViews


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
        return self._module.isRoot()

    def open(self):
        result = self.wqD().impl().open()
        return result
    
    #@s:PackageView::setSelectedNode
    def setSelectedModule(self, module):
        self._selectedModule = module if module != None else self.module()
        return self._selectedModule

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
#        self.wqD().doModuleView_wheelEvent(event)



  

