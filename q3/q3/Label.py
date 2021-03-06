
from q3.ui.engine import qtw,qtc,qtg

from .Object import Object
from . import Font

class Label(Object):
    def __init__(self, parent, impl=None, **kwargs):
        super(Label, self).__init__(parent,impl,**kwargs)

    def _getFont(self):
        t_font = self.q3D().doLabel_GetFont()
        #//t_font =  self._label.font() if self.isQt() else self._label.GetFont()
        return Font.Font(self,t_font)
    
    def _setFont(self, font):
        return self.q3D().doLabel_SetFont(font)
        #result = self._label.setFont(font) if self.isQt() else self._label.SetFont(font)
        #return result

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
