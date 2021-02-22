
import wx
import PyQt5.QtWidgets as qtw

from . import Object
from . import consts


class FontPointSize(Object.Object):
    def __init__(self, parent, object, q3Impl):
        self._font = object
        super(FontPointSize, self).__init__(parent,self._font, q3Impl=q3Impl)
    
    def __iadd__(self, other):
        if self.isQt():
            self._font.setPointSize(self._font.pointSize() + other)  
        else: 
            self._font.PointSize += other

class Font(Object.Object):
    def __init__(self, parent=None, impl=None, q3Impl=None):
        if q3Impl == None:
            q3Impl =  consts.Q3_IMPL if parent == None else parent._q3Impl
        if impl == None:
            self._font = qtw.QFont() if self.isQt(q3Impl) else wx.Font()
        else:
            self._font = impl
        self.PointSize  = FontPointSize(parent, self._font, q3Impl=q3Impl)    
        super(Font, self).__init__(parent, self._font,q3Impl=q3Impl)
        #super(wx.StaticText, self).__init__(parent, label=label)

    #def PointSize(Self):
    #    return _font.PointSize

    def _bold(self, retObject=False):
        if retObject:
            if self.isQt():
                self._font.setBold(True)
                result = self._font
            else:
                result = self._font.Bold()
        else:
            result = self._font.getBold() if self.isQt() else self._font.GetBold()
        return result

    def _setBold(self, nb):
        result = self._font.setBold(nb) if self.isQt() else self._font.SetBold(nb)
        return result

    def Bold(self):
        return self._bold(True)

    def bold(self):
        return self._bold()    

    def SetBold(self, nb):
        return self._setBold() 

    def setBold(self, nb):
        return self._setBold()                   
    