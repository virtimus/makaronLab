import wx
import PyQt5.QtWidgets as qtw

from .Object import Object
from .Menu import Menu

class MenuBar(Object):
    def __init__(self, parent, object=None, wqImpl=None):
        self._wxMenuBar:wx.MenuBar = None
        self._menuBar = self._wxMenuBar
        if (wqImpl == None):
            wqImpl = parent._wqImpl 
        if self.isQt(wqImpl):
            self._qtMenuBar = parent.implObject().menuBar() #qtw.QMenuBar(parent.implObject())
            self._menuBar = self._qtMenuBar
            pass
        else:
            self._wxMenuBar = wx.MenuBar()
            self._menuBar = self._wxMenuBar
            parent.implObject().SetMenuBar(self._wxMenuBar)
        super(MenuBar, self).__init__(parent, self._menuBar,wqImpl=wqImpl)
        #self._wxObject = wx.MenuBar()
        #super(MenuBar, self).__init__(None, self._menuBar)

    def Append(self, a0, a1):
        #return self._menuBar.Append(a0.implObject(),a1)
        pass 

    def addMenu(self, menuTitle):
        if self.isQt():
            return Menu(self._parent, self._qtMenuBar.addMenu(menuTitle))
        else:           
            result = Menu(self._parent)
            self._wxMenuBar.Append(result.implObject(),menuTitle)
            return result 
