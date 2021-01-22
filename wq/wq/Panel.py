

import wx
import PyQt5.QtWidgets as qtw

from . import consts
from . import Object
from . import Element



class Panel(Element.Element):
    def __init__(self, parent, impl=None, **kwargs): 
        super(Panel, self).__init__(parent, impl, **kwargs)

    def SetSizer(self, sizer):
        #result = None if self.isQt() else self._panel.SetSizer(sizer.implObject())
        raiseNoImpl('Panel','SetSizer -> use parent in Layout creator')