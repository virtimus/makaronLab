
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
from .Pin import Pin
from .ModuleView import ModuleView
from .sidePanel.SidePanel import SidePanel

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

class EditorFrame(MainWindow):
    """
    A main frame of wqEditor
    """

    def __init__(self, parent, title=None,wqImpl=None):
        # ensure the parent's __init__ is called
        super(EditorFrame, self).__init__(parent)

        self._openModules = dict({})    

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

        layout=Layout(pnl, None, orientation.VERTICAL)
        layout.impl().setContentsMargins(6, 6, 6, 6)
        layout.impl().setSpacing(2)
        self._tabPanel = TabPanel(pnl)
        layout.addElement(self._tabPanel)
        tab = Tab(self._tabPanel)
        tab2 = Tab(self._tabPanel)
        tab3= Tab(self._tabPanel)
        tab4 = Tab(self._tabPanel)
        tab5 = Tab(self._tabPanel)
        hlayout=Layout(pnl, None, orientation.HORIZONTAL)
        hlayout.impl().setContentsMargins(6, 6, 6, 6)
        hlayout.impl().setSpacing(2)
        hlayout.impl().addLayout(layout.impl(),0)
        pnl.impl().setLayout(hlayout.impl())

        rootModule = Module(self,'rootModule')
        controlModule = Module(rootModule,'controlModule')
        infoModule = Module(rootModule,'infoModule')
        m6502Module = Module(rootModule,'m6502Module',type=ModuleType.WQC)
        drivePin = Pin(controlModule,'O1_64','Out Pin of controlModule')
        sl1 = Pin(infoModule,'I1_64','In Pin1 of InfoModule')
        inM6502 = Pin(m6502Module,'ICPU_64','In Pin of m6502')
        m6502DrivePin = Pin(m6502Module,'OCPU_64','Out Pin of m6502')
        sl2 = Pin(infoModule,'I2_64','In Pin2 of InfoModule')
        #pinRef = Pin()

        signal1 = Signal(rootModule, 64,drivePin=drivePin, slavePins = [sl1,inM6502])

        signal2 = Signal(rootModule, 64,drivePin=m6502DrivePin, slavePins = [sl2])

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
            
            panel_left.setWidgetResizable(True)
            panel_left.setWidget(label)
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

    #openOrCreatePackage
    def openModuleView(self,module:Module):
        found = self.openModules(module)
        if found != None:
            self._moduleViewIndex = found            
        else:
            moduleView = ModuleView(self,module=module)
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
        module = Module(self, "New")
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
        #super(EditorFrame, self).showEvent(event)