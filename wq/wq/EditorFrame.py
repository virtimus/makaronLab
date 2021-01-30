
from . import consts
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
from .ModuleLibraryWqc import ModuleLibraryWqc

class EditorFrame(MainWindow):
    """
    A main frame of wqEditor
    """

    def __init__(self, parent, title=None,wqImpl=None):
        # ensure the parent's __init__ is called
        super(EditorFrame, self).__init__(parent)

        self._openModules = dict({})

        self._libModules = dict({})  #module dict for dragging/creating views/opening(if package)   

        #self.impl().setWindowFlags(Qt.FramelessWindowHint)

        # create a panel in the frame
        pnl = Panel(self)
        #tb = wq.MainWindowTB(self.impl())
        #pnl = wq.Panel(self,self.impl()._content)
        self.impl().setCentralWidget(pnl.impl())

        # put some text with a larger bold font on it
        #st = wq.StaticText(pnl, label="Hello World!")
        #font = st.GetFont()
        #font.PointSize += 10
        #font = font.Bold()
        #st.SetFont(font)

        # and create a sizer to manage the layout of child widgets
        #sizer = wq.BoxSizer(pnl, None, wq.VERTICAL)
        #sizer.Add(st, wq.SizerFlags().Border(wq.TOP|wq.LEFT, 25))
        #pnl.SetSizer(sizer)
        
        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()

        
        '''
        statusLabel = QLabel(self.impl());
        statusProgressBar = QProgressBar(self.impl());

        #// set text for the label
        statusLabel.setText("Status Label");
        self.SetStatusText("Welcome to wxPython!")

        #// make progress bar text invisible
        #statusProgressBar.setTextVisible(False);

        #// add the two controls to the status bar
        self.impl().statusBar().addPermanentWidget(statusLabel);
        self.impl().statusBar().addPermanentWidget(statusProgressBar,1)
        '''

        layout=Layout(pnl, orient=orientation.VERTICAL)
        layout.impl().setContentsMargins(6, 6, 6, 6)
        layout.impl().setSpacing(2)
        self._tabPanel = TabPanel(pnl)
        layout.addElement(self._tabPanel)
        tab = Tab(self._tabPanel)
        tab2 = Tab(self._tabPanel)
        tab3= Tab(self._tabPanel)
        tab4 = Tab(self._tabPanel)
        tab5 = Tab(self._tabPanel)
        hlayout=Layout(pnl, orient=orientation.HORIZONTAL)
        hlayout.impl().setContentsMargins(6, 6, 6, 6)
        hlayout.impl().setSpacing(2)
        hlayout.impl().addLayout(layout.impl(),0)
        pnl.impl().setLayout(hlayout.impl())

        

        #load libraries
        wqcLib = ModuleFactory.loadLibrary('wqc')
        #wqlLib = ModuleFactory.loadLibrary('local')

        moduleList = wqcLib.listModules()
        for k in moduleList:
            print(k)

        #    self._libModules['wqc.'+k] = { "moduleDef":moduleList[k]

        c6502=wqcLib.createModule('c6502')
        res = c6502.init({})
        #print(res)
        resp = c6502.open()
        #'''
        rootModule = Module(self,'rootModule',
            moduleType = ModuleType.GRAPH
        )
        self._rootModule = rootModule

        #andModuleImpl = wqlLib.createModule('AND')       
        #andModule = Module(rootModule,'andModule',
        #    impl = 'local/AND'
        #    )
        andModule = rootModule.newModule('andModule',
            impl = 'local/AND'
            )


        #'''
        '''
        controlModule = Module(rootModule,'controlModule')
        infoModule = Module(rootModule,'infoModule')
        m6502Module = Module(rootModule,'m6502Module',
            type=ModuleType.WQC,
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



        #network ready (init/open phase) - now simulation (calculate/inspect)...

        self.createSidePanels(self._tabPanel)


        #signal.addSlavePin(pinRef)


        
    def createSidePanels(self, parent):
        def leftPanel():
        
            panel_left = SidePanel(parent.impl(), 
                side=direction.LEFT
                )
            panel_left.setOpenEasingCurve(qtc.QEasingCurve.Type.OutElastic);
            panel_left.setCloseEasingCurve(qtc.QEasingCurve.Type.InElastic);
            panel_left.setPanelSize(400)
            panel_left.init()

            label = qtw.QLabel("Left")
            label.setAlignment(qtc.Qt.AlignCenter)

            tw = qtw.QTableWidget()
            tw.setRowCount(10)
            tw.setColumnCount(2)
            self._propertiesTable = tw
            
            panel_left.setWidgetResizable(True)
            #panel_left.setWidget(label)
            panel_left.setWidget(tw)
            self._panelLeft = panel_left
        leftPanel()


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        menuBar = MenuBar(self)
        fileMenu = menuBar.addMenu("&File")
        helpMenu = menuBar.addMenu("&Help")


        # Make a file menu with Hello and Exit items
        #fileMenu = wq.Menu(self)
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.addAction("&Hello...\tCtrl-H", 
            helpStr="Help string shown in status bar for this menu item",
            onClick=self.OnHello)
        fileMenu.addSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.addAction(None, consts.ID_EXIT,
            onClick=self.OnExit)

        # Now a help menu for the about item
        #helpMenu = wq.Menu(self)
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
        #//s//elf.Bind(wq.EVT_MENU, self.OnHello, helloItem)
        #//self.Bind(wq.EVT_MENU, self.OnExit,  exitItem)
        #//self.Bind(wq.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event=None):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event=None):
        """Say hello to the user."""
        MessageBox("Hello again from wxPython")


    def OnAbout(self, event=None):
        """Display an About Dialog"""
        MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wq.OK|wq.ICON_INFORMATION)

    def openModules(self, module:Module=None):
        if (module!= None):
            result = self._openModules[module.name()] if module.name() in self._openModules else None
        else:
            result = self._openModules
        return result

    #openOrCreatePackageView
    def openModuleView(self,module:Module):
        found = self.openModules(module)
        if found != None:
            self._moduleViewIndex = found            
        else:
            moduleView = ModuleView(self,module=module) #recurive by nested modules
            moduleView.open()
            moduleView.setSelectedModule(None)
            moduleView.showProperties()
            #connect(packageView, &PackageView::requestOpenFile,
            #[this](QString const a_filename) { openPackageFile(a_filename); });

            #auto const IS_ROOT_PACKAGE = a_package->package() == nullptr;
            #$QString const TITLE{ (IS_ROOT_PACKAGE ? "New package" : QString::fromStdString(a_package->name())) };
            title = module.name()
            self._moduleViewIndex = self._tabPanel.addTab(moduleView, title)
            self._openModules[module.name()] = self._moduleViewIndex
            #self._moduleView = moduleView
        self._tabPanel.impl().setCurrentIndex(self._moduleViewIndex)
        self._moduleView = module.view()
        return self._moduleViewIndex
                      

    def newModuleView(self):
        module = Module(self, "New", moduleType=ModuleType.GRAPH)
        self.openModuleView(module)

    _firstTime = True 
    #: QShowEvent #@s:editor::showEvent
    def showEvent(self, event):
        if (EditorFrame._firstTime):
            EditorFrame._firstTime = False
            self.newModuleView()
            #//  openPackage();
            tab = self._tabPanel
            index = tab.currentIndex()
            moduleViewImpl = tab.impl().widget(index)
            moduleViewImpl.centerOn(0.0, 0.0)

            self.openModuleView(self._rootModule)
            index = tab.currentIndex()
            moduleViewImpl = tab.impl().widget(index)
            moduleViewImpl.centerOn(0.0, 0.0)


        #super(EditorFrame, self).showEvent(event)