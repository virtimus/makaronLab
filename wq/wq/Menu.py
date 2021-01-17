
import wx
import PyQt5.QtWidgets as qtw

from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtGui import QIcon 

from . import consts
from . import Object
from . import Label


class Menu(Object.Object):
    def __init__(self, parent, impl=None, wqImpl=None):
        #//wqD = self.loadWqDriver(parent,object,wqImpl)
        self._menu = self.wqD().doMenu_Init()
        wqD = None
        '''
        if (wqImpl == None):
            wqImpl = parent._wqImpl 
        if object == None:    
            if self.isQt(wqImpl):
                self._qtMenu = qtw.QMenu(parent.implObject())
                self._menu = self._qtMenu
                pass
            else:
                self._wxMenu = wx.Menu()
                self._menu = self._wxMenu
                #parent.implObject().Append(self._wxMenu)
        else:
            self._menu = object
        '''    
        super(Menu, self).__init__(parent, self._menu, wqImpl = wqImpl, wqD = wqD)

    '''
    def Append(self, a0, a1=None, a2=None):
        if self.isQt():
            pass
        else:
            if (a1 == None):
                return self._menu.Append(a0)
                pass
            else:
                return self._menu.Append(a0, a1, a2)
                pass
                '''

    def _addSeparator(self):
        result = self.wqD().doMenu_AddSeparator()
        return result

    def AppendSeparator(self):
        return self._addSeparator()

    def addSeparator(self):
        return self._addSeparator()

    def addAction(self,label:str, id=None, helpStr=None, onClick=None):
        return self.wqD().doMenu_addAction(label,id,helpStr,onClick)

        