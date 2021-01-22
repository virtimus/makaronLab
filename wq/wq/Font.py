
import wx
import PyQt5.QtWidgets as qtw

from . import Object
from . import consts


class FontPointSize(Object.Object):
    def __init__(self, parent, object, wqImpl):
        self._font = object
        #//self._fontPointSize = object.pointSize() if self.isQt(wqImpl) else object.PointSize()
        super(FontPointSize, self).__init__(parent,self._font, wqImpl=wqImpl)
    
    def __iadd__(self, other):
        if self.isQt():
            self._font.setPointSize(self._font.pointSize() + other)  
        else: 
            self._font.PointSize += other

class Font(Object.Object):
    def __init__(self, parent=None, impl=None, wqImpl=None):
        if wqImpl == None:
            wqImpl =  consts.WQ_IMPL if parent == None else parent._wqImpl
        if impl == None:
            self._font = qtw.QFont() if self.isQt(wqImpl) else wx.Font()
        else:
            self._font = impl
        self.PointSize  = FontPointSize(parent, self._font, wqImpl=wqImpl)    
        super(Font, self).__init__(parent, self._font,wqImpl=wqImpl)
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
    