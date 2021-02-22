
from . import consts, console
from . import orientation
from . import direction
from .moduletype import ModuleType
from .Panel import Panel

from .MainWindow import MainWindow
from .MenuBar import MenuBar
from .Layout import Layout
from .Tab import Tab
from .TabPanel import TabPanel
#from .MessageBox import MessageBox


from .Signal import Signal
from .Module import Module
from .Module import Node
#from .Pin import Pin
from .ModuleView import ModuleView
from .sidePanel.SidePanel import SidePanel
from .ModuleFactory import ModuleFactory

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
#from .ModuleLibraryQ3Chips import ModuleLibraryQ3Chips

from .q3vector import Q3Vector

from .console import ConsoleCtrl

class EditorFrame(MainWindow):
    """
    A main frame of q3Editor
    """

    def __init__(self, parent, title=None,q3Impl=None):
        # ensure the parent's __init__ is called
        super(EditorFrame, self).__init__(parent)
        self._app = parent
        #self._consoleWidget = None
        self._consoleWidget = console.newConsoleWidget(self)
        ss=2
        self.cw().write(f'testWritefrom editorFrame constructor:{ss}')
        #@deprecated
        #self._openModules = dict({})
        self._rootModules = Q3Vector(Module)
        #self._rootModuleSelected = None
        self._moduleViewIndex = None

        #@deprecated
        self._libModules = dict({})  #module dict for dragging/creating views/opening(if package)   

        self.buildLayout()
        
        # create a menu bar
        self.buildMenuBar()

        # and a status bar
        self.buildStatusBar()

        self.buildLibraries()

        self.buildSampleRoot()

        #network ready (init/open phase) - now simulation (calculate/inspect)...

        self.buildSidePanels(self._tabPanel)
        #signal.addSlavePin(pinRef)

    def buildLayout(self):
        # create a panel in the frame
        pnl = Panel(self)
        #tb = q3.MainWindowTB(self.impl())
        #pnl = q3.Panel(self,self.impl()._content)
        self.impl().setCentralWidget(pnl.impl())
        layout=Layout(pnl, orient=orientation.VERTICAL)
        layout.impl().setContentsMargins(6, 6, 6, 6)
        layout.impl().setSpacing(2)
        self._tabPanel = TabPanel(pnl)
        layout.addElement(self._tabPanel)
        self._tabPanel.impl().currentChanged.connect(self.onTabChanged)
        self._tabPanel.impl().tabCloseRequested.connect(self.onTabCloseRequested)
        #tab = Tab(self._tabPanel)
        #tab2 = Tab(self._tabPanel)
        #tab3= Tab(self._tabPanel)
        #tab4 = Tab(self._tabPanel)
        #tab5 = Tab(self._tabPanel)
        hlayout=Layout(pnl, orient=orientation.HORIZONTAL)
        hlayout.impl().setContentsMargins(6, 6, 6, 6)
        hlayout.impl().setSpacing(2)
        hlayout.impl().addLayout(layout.impl(),0)
        pnl.impl().setLayout(hlayout.impl())

    def onTabChanged(self, event=None):
        self._moduleViewIndex = event
        self.c().write(f'\nonTabChanged:{self._moduleViewIndex}\n')

    def onTabCloseRequested(self, event=None):
        index = event
        lmodule = self.rootModules().filterBy('tabIndex',index)
        module =lmodule.first()
        module = self.rootModules().remove(module) 
        moduleView = module.view()
        self._tabPanel.impl().removeTab(index)
        del moduleView


    def buildLibraries(self):
        #load libraries
        #q3cLib = ModuleFactory.loadLibrary('q3c')
        #q3lLib = ModuleFactory.loadLibrary('local')

        #moduleList = q3cLib.listModules()
        #for k in moduleList:
        #    print(k)

        #    self._libModules['q3c.'+k] = { "moduleDef":moduleList[k]

        #c6502=q3cLib.createModule('c6502')
        #res = c6502.init({})
        #print(res)
        #resp = c6502.open()
        #'''
        pass

    def newSidePanel(self, **kwargs):
        tparent = console.handleArg(self,'parent',kwargs = kwargs,
            required = True,
            desc = 'Parent object for SidePanel',)

        tside = console.handleArg(self,'side',kwargs = kwargs,
            required = True,
            desc = 'Side of Panel(direction enum)')

        tsize = console.handleArg(self,'size',kwargs = kwargs,
            default = 200,
            desc = 'Size of panel')
        
        twidget = console.handleArg(self,'widget',kwargs = kwargs,
            required = True,
            desc = 'Panel widget')
        if (console.isArgHelp(**kwargs)):
            return ['newSidePanel',tparent,tside,tsize,twidget]

        tpanel = SidePanel(tparent, 
            side=tside
            )
        tpanel.setOpenEasingCurve(qtc.QEasingCurve.Type.OutElastic);
        tpanel.setCloseEasingCurve(qtc.QEasingCurve.Type.InElastic);
        tpanel.setPanelSize(tsize)
        tpanel.init()
        tpanel.setWidgetResizable(True)
        tpanel.setWidget(twidget)
        return tpanel

        
    def buildSidePanels(self, parent):
        def rightPanel():
        
            tpanel = SidePanel(parent.impl(), 
                side=direction.RIGHT
                )
            tpanel.setOpenEasingCurve(qtc.QEasingCurve.Type.OutElastic);
            tpanel.setCloseEasingCurve(qtc.QEasingCurve.Type.InElastic);
            tpanel.setPanelSize(300)
            tpanel.init()

            label = qtw.QLabel("Left")
            label.setAlignment(qtc.Qt.AlignCenter)

            tw = qtw.QTableWidget()
            tw.setRowCount(10)
            tw.setColumnCount(2)
            self._propertiesTable = tw
            
            tpanel.setWidgetResizable(True)
            #panel_left.setWidget(label)
            tpanel.setWidget(tw)
            self._panelRight = tpanel
        rightPanel()

        
        self._panelBottom = self.newSidePanel(
            parent = parent.impl(),
            side = direction.DOWN,
            widget = self._consoleWidget
        )


    def buildMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        menuBar = MenuBar(self)
        fileMenu = menuBar.addMenu("&File")
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")


        # Make a file menu with Hello and Exit items
        #fileMenu = q3.Menu(self)
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        newItem = fileMenu.addAction("&New...\tCtrl+N", 
            helpStr="Help string shown in status bar for this menu item",
            onClick=self.OnNew)
        #newItem.setShortcut(qtc.Qt.CTRL+qtc.Qt.Key_W)
        newItem.setShortcut('Ctrl+N')

        saveItem = fileMenu.addAction("&Save...\tCtrl+S", 
            helpStr="Help string shown in status bar for this menu item",
            onClick=self.OnSave)
        saveItem.setShortcut('Ctrl+S')

        deleteItem = editMenu.addAction("&Delete...\tDel", 
            helpStr="Help string shown in status bar for this menu item",
            onClick=self.OnDeleteItem)
        deleteItem.setShortcut('Del')

        fileMenu.addSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.addAction(None, consts.ID_EXIT,
            onClick=self.OnExit)

        # Now a help menu for the about item
        #helpMenu = q3.Menu(self)
        aboutItem = helpMenu.addAction(None, consts.ID_ABOUT,
            onClick=self.OnAbout)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.


        # Give the menu bar to the frame
        #self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        #//s//elf.Bind(q3.EVT_MENU, self.OnHello, helloItem)
        #//self.Bind(q3.EVT_MENU, self.OnExit,  exitItem)
        #//self.Bind(q3.EVT_MENU, self.OnAbout, aboutItem)

    #@api
    def consoleWidget(self):
        return self._consoleWidget

    #@api
    def cw(self):
        return self.consoleWidget()

    
    #@api
    def console(self) -> ConsoleCtrl:
        result = self._consoleWidget._namespace['c'] if self._consoleWidget!=None else None
        return result

    #@api
    def c(self):
        return self.console()
        
    #@api
    def consoleNamespace(self):
        result = self._consoleWidget._namespace if self._consoleWidget != None else None
        return result

    #@api
    def app(self):
        return self._app

    def OnExit(self, event=None):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnNew(self, event=None):
        if event!=None: #double call?
            self.newModuleView()

    def OnHello(self, event=None):
        """Say hello to the user."""
        #MessageBox("Hello again from wxPython")

        import json

        print('Hellop')
        s = json.dumps(self._rootModule.__dict__)

        print(s)

    def OnSave(self, event=None):
        from .visitors.json import Visitor as JsonVisitor
        v = JsonVisitor()
        self.acceptVisitor(v)

        print(v._jsD)

        from . import yaml

        with open('/tmp/save.yaml', 'w+') as handle:
            yaml.dump(v._jsD, handle,default_flow_style=False)

    def OnDeleteItem(self, event=None):
        print('DEletteeee')
        tab = self._tabPanel
        index = tab.currentIndex()
        graphViewImpl = tab.impl().widget(index)
        graphViewImpl.deleteElement()
        pass


    def OnAbout(self, event=None):
        """Display an About Dialog"""
        qtg.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      q3.OK|q3.ICON_INFORMATION)

    #openOrCreatePackageView
    def openModuleView(self,module:Module):
        found = module.tabIndex()
        if found != None:
            self._moduleViewIndex = found            
        else:
            moduleView = ModuleView(self,module=module) #recurive by nested modules
            moduleView.open()
            moduleView.setSelectedModule(None)
            moduleView.showProperties()
            title = module.name()
            self._moduleViewIndex = self._tabPanel.addTab(moduleView, title)
            tabWidget = self._tabPanel.impl().widget(self._moduleViewIndex)
            moduleView.setParentTab(tabWidget)
            self.rootModules().append(self.rootModules().nextId(),module)
        self._tabPanel.impl().setCurrentIndex(self._moduleViewIndex)
        self._moduleView = module.view()
        return self._moduleViewIndex
                      

    def newModuleView(self):
        tnextId = self.rootModules().nextId()
        module = Module(self, f"New-{tnextId}", moduleType=ModuleType.GRAPH, id=tnextId)
        self.openModuleView(module)

    _firstTime = True 
    #: QShowEvent #@s:editor::showEvent
    def showEvent(self, event):
        if (EditorFrame._firstTime):
            EditorFrame._firstTime = False
            tab = self._tabPanel
            '''
            self.newModuleView()
            #//  openPackage();
            
            index = tab.currentIndex()
            moduleViewImpl = tab.impl().widget(index)
            moduleViewImpl.centerOn(0.0, 0.0)
            '''
            self.openModuleView(self._rootModule)
            index = tab.currentIndex()
            graphViewImpl = tab.impl().widget(index)
            graphViewImpl.centerOn(0.0, 0.0)

            from .visitors.json import Visitor as JsonVisitor
            v = JsonVisitor()
            self._rootModule.acceptVisitor(v)

            #print(v._jsD)

            from . import yaml

            with open('/tmp/bootDump.yaml', 'w+') as handle:
                yaml.dump(v._jsD, handle,default_flow_style=False)

            '''
            self._nestedModule._nestedView = self._nestedModule._view 
            self._nestedModule._view = None
            #!TMP!
            self.openModuleView(self._nestedModule)
            index = tab.currentIndex()
            moduleViewImpl = tab.impl().widget(index)
            moduleViewImpl.centerOn(0.0, 0.0)
            '''
            self.cw().write(f'afterShowEd:{index}')


        #super(EditorFrame, self).showEvent(event)

    def acceptVisitor(self, v):
        v.visitEditor(self)

    #@deprecated
    def rootModuleCount(self):
        tabPanelWidget = self._tabPanel.impl() #QTabWidget
        assert tabPanelWidget != None, '[editorFrame.rootModuleByInd] tabPanel impl not found'
        tc = tabPanelWidget.count()
        return tc

    #@deprecated
    def rootModuleByInd(self, ind:int):
        tabPanelWidget = self._tabPanel.impl() #QTabWidget
        assert tabPanelWidget != None, '[editorFrame.rootModuleByInd] tabPanel impl not found'
        tabWidget = tabPanelWidget.widget(ind)
        assert tabWidget != None, f'[editoFrame.rootModuleByInd] tabWidget[{ind}] not found'
        module = tabWidget._self.module()
        assert module != None, f'[editoFrame.rootModuleByInd] in tabWidget[{ind}] module not found'
        return module

    #@deprecated
    def rootModuleSelectedIndex(self):
        return self._tabPanel.currentIndex()
    
    #@deprecated
    def rootModuleSelected(self):
        return self.rootModuleByInd(self.rootModuleSelectedIndex())

    #@api
    def rootModules(self,by=None) -> Q3Vector(Module):
        return self._rootModules.defaultGetter('name',by)

    #@api
    def rms(self,by=None):
        return self.rootModules(by)

    #@api
    def rootModuleSelect(self, index:int):
        rm = self.rootModules().byLid(index)
        assert rm != None, f'Module with tabIndex:{index} not found'
        self.openModuleView(rm)
    
    #@api
    def rmsel(self, index:int):
        return self.rootModuleSelect(self, index)

    #@api
    def rootModule(self) -> Module:
        rm = self.rootModules().byLid(self._moduleViewIndex)
        assert rm != None, f'Current module with tabIndex:{self._moduleViewIndex} not found'
        return rm
    
    #@api
    def rm(self):
        return self.rootModule()

    #@api
    def rootModuleSignals(self,by=None):
        return self.rootModule().signals().defaultGetter('name',by)

    #@api
    def rootModuleNodes(self,by=None):
        return self.rootModule().nodes().defaultGetter('name',by) 

    #@api
    def rootModuleModules(self,by=None):
        return self.rootModule().modules().defaultGetter('name',by)

    def buildSampleRoot(self):
        rootModule = Module(self,'rootModule',
            moduleType = ModuleType.GRAPH
        )
        self._rootModule = rootModule

        #andModuleImpl = q3lLib.createModule('AND')       
        #andModule = Module(rootModule,'andModule',
        #    impl = 'local/AND'
        #    )
        andModule1 = rootModule.newModule('andModule1',
            impl = 'local:/AND'
            )

        andModule2 = rootModule.newModule('andModule2',
            impl = 'local:/AND'
            )

        notModule = rootModule.newModule('notModule',
            impl = 'local:/NOT'
            )

        norModule1 = rootModule.newModule('norModule1',
            impl = 'local:/NOR'
            ) 

        norModule2 = rootModule.newModule('norModule2',
            impl = 'local:/NOR'
            )  

        graphModule1 = rootModule.newModule('graphModule1',
            #impl = 'file:/tmp/test'
            moduleType = ModuleType.GRAPH
            )
        
        from .ModuleLibraryQ3Chips import ModuleLibraryQ3Chips
        
        m6502Module = rootModule.newModule('m6502Module',
            #type=ModuleType.ATOMIC,
            impl='Q3Chips:/c6502'
            )
        
        #'''
        cpcModule = rootModule.newModule('cpcModule',
            #type=ModuleType.ATOMIC,
            impl='Q3Chips:/CPC'
            )
        #'''
        
        #ff = graphModule1.name()
        #self._nestedModule = graphModule1
        #'''
        '''
        controlModule = Module(rootModule,'controlModule')
        infoModule = Module(rootModule,'infoModule')
        m6502Module = Module(rootModule,'m6502Module',
            type=ModuleType.Q3C,
            impl=c6502
            )
        driveSig = Signal(controlModule,size=1, name='O1_64',info='Out Signal of controlModule')
        slave1Sig = Signal(infoModule,size=1, name='I1_64',info='In Signal of InfoModule')
        C6502InSig = Signal(m6502Module,size=1, name='ICPU_64',info='In Signal of m6502')
        C6502OutSig = Signal(m6502Module,size=1, name='OCPU_64',info='Out Signal of m6502')
        slave2Sig = Signal(infoModule,size=1, name='I2_64',info='In Signal of InfoModule')
        #pinRef = Pin()

        #signal1 = Signal(rootModule, 64,drivePin=drivePin, slavePins = [sl1,inM6502])

        #signal2 = Signal(rootModule, 64,drivePin=m6502DrivePin, slavePins = [sl2])
        #//rootModule.connect(driveSig, slave1Sig) #conn from control to info
        #//rootModule.connect(driveSig, C6502InSig)
        #//rootModule.connect(C6502OutSig, slave2Sig)
        #//rootModule.connect(m6502Module, slave2Sig)
        coNodOut = Node(controlModule, size=1, driveSignal=driveSig, name='coOut')
        coNodOut.addSignal(slave1Sig)
        '''
