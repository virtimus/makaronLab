
import wx as wx 
import PyQt5.QtWidgets as qtw

#from .consts import consts
from . import consts
from . import Object as ob
from . import Element

#dir(consts)
#dir(wx)


class MainWindow(Element.Element):
    def __init__(self,*args, **kwargs):
        self._mainWindow=self._loadImpl(*args, **kwargs) 
        if (self._mainWindow==None):
            self._mainWindow=self.q3D().doMainWindow_Init()
            kwargs['impl']=self._mainWindow
        tParent = self._loadParent(*args, **kwargs)
        super(MainWindow, self).__init__(tParent, self._mainWindow) 

    def _show(self):        
        return self.q3D().doMainWindow_Show()

    def Show(self):
        self._show()
    
    def show(self):
        self._show()

    def setCentralWidget(self, widget):
        result = self._mainWindow.setCentralWidget(widget) if self.isQt() else self.raiseNoImpl('MainWindow','setCentralWidget')
        return result

    def setMenuBar(self, menuBar):
        #result = self._mainWindow.setMenuBar(menuBar) if self.isQt() else self._mainWindow.SetMenuBar(menuBar._wxObject)
        raiseNoImpl('MainWindow', 'setMenuBar -> use parent in menuBar creator')

    def SetMenuBar(self, menuBar):
        self.setMenuBar(menuBar)    

    def addDockWidget(self, area, dockwidget):               
        result = self._mainWindow.addDockWidget(area, dockwidget) if self.isQt() else self.raiseNoImpl('MainWindow','addDockWidget')
        return result 
 
    def Bind(self, a0, a1, a2):
        result = self.raiseNoImpl('MainWindow','Bind') if self.isQt() else self._mainWindow.Bind(a0,a1,a2)
        return result

    def buildStatusBar(self):
        result = self._mainWindow.statusBar() if self.isQt() else self._mainWindow.CreateStatusBar()
        return result

    def SetStatusText(self, a0):
        result = self._mainWindow.statusBar().showMessage(a0) if self.isQt() else self._mainWindow.SetStatusText(a0)
        return result

    def Close(self, a0):
        result = self.raiseNoImpl('MainWindow','Close') if self.isQt() else self._mainWindow.Close(a0) 
        return result       
