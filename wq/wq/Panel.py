

import wx
import PyQt5.QtWidgets as qtw

from . import consts
from . import Object
from . import Element



class Panel(Element.Element):
    def __init__(self, parent, impl=None,  wqImpl=None):        
        if (wqImpl == None):
            wqImpl = parent._wqImpl 
        
        if (impl==None): 
            #self._panel = qtw.QMdiArea(parent.impl()) if self.isQt(wqImpl) else wx.Panel(parent.implObject()) 
            self._panel = qtw.QFrame(parent._object) if self.isQt(wqImpl) else wx.Panel(parent.implObject())
            #if self.isQt(wqImpl):
            #    parent._object.setCentralWidget(self._panel)
        else:
            self._panel = impl

        super(Panel, self).__init__(parent, self._panel, wqImpl=wqImpl)
        #super(wx.Panel, self).__init__(parent)

    def SetSizer(self, sizer):
        #result = None if self.isQt() else self._panel.SetSizer(sizer.implObject())
        raiseNoImpl('Panel','SetSizer -> use parent in Layout creator')