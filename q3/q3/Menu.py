
from q3.ui.engine import qtw,qtc,qtg 

from . import consts
from . import Object
from . import Label


class Menu(Object.Object):
    def __init__(self, parent, impl=None, **kwargs):   
        super(Menu, self).__init__(parent, impl, **kwargs) 

    def _addSeparator(self):
        return  self.q3D().doMenu_AddSeparator()

    def AppendSeparator(self):
        return self._addSeparator()

    def addSeparator(self):
        return self._addSeparator()

    def addAction(self,label:str, id=None, helpStr=None, onClick=None):
        return self.q3D().doMenu_addAction(label,id,helpStr,onClick)

        