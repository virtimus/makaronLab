
import wx
import PyQt5.QtWidgets as qtw

from .Object import Object
from . import Font

class Label(Object):
    def __init__(self, parent, impl=None,label=None, wqImpl=None):
        if wqImpl == None:
            wqImpl = parent._wqImpl
        if object == None:
            self._label = qtw.QLabel(parent.implObject()) if self.isQt(wqImpl) else wx.StaticText(parent.implObject())
        else:
            self._label = impl
        if self.isQt(wqImpl):
            self._label.setText(label)   
        super(Label, self).__init__(parent, self._label,wqImpl=wqImpl)
        #super(wx.StaticText, self).__init__(parent, label=label)

    def _getFont(self):
        t_font =  self._label.font() if self.isQt() else self._label.GetFont()
        return Font.Font(self,t_font)
    
    def _setFont(self, font):
        result = self._label.setFont(font) if self.isQt() else self._label.SetFont(font)
        return result

    def GetFont(self):
        result = self._getFont()
        return result        

    def font(self):
        result = self._getFont()
        return result

    def SetFont(self,font):
        return self._setFont(font)

    def setFont(self, font):
        return self._setFont(font)
