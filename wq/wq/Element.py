

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget, QStyle
import wx

from . import consts
from . import Object
#, QWidget
class Element(Object.Object):
    def __init__(self,parent, impl=None, other=None, wqImpl=consts.WQ_IMPL):
        if impl==None:
            impl = QWidget(parent.impl())
        self._element = impl;        
        super(Element, self).__init__(parent, self._element, wqImpl=wqImpl)
        if self.isQt():
            #super(QWidget, self).__init__(self._widget)
            pass
        else:
            pass #!TODO!

    def resize(self, w:int, h:int):
        result = self._element.resize(w,h) if self.isQt() else self.raiseNoimpl('Widget','resize')

    def sizePolicy(self):
        result = self._element.sizePolicy() if self.isQt() else self.raiseNoImpl('Widget','sizePolicy')

    def setSizePolicy(self, sizePolicy):
        result = self._element.setSizePolicy(sizePolicy) if self.isQt() else raiseNoImpl('Widget','sizePolicy')
                  