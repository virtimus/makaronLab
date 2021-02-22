import wx
import PyQt5.QtWidgets as qtw

from .Object import Object
from .Menu import Menu

class MenuBar(Object):
    def __init__(self, parent, impl=None, **kwargs): 
        super(MenuBar, self).__init__(parent, impl, **kwargs)

    def Append(self, a0, a1):
        #return self._menuBar.Append(a0.implObject(),a1)
        pass 

    def addMenu(self, menuTitle):
        return Menu(self._parent, self.q3D().doMenuBar_AddMenu(menuTitle))
  

 
