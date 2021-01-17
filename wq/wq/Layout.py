

import wx
import PyQt5.QtWidgets as qtw

from . import Object
from . import Label
from . import consts 
from . import orientation


class Layout(Object.Object):
    def __init__(self, parent, impl, l:int, object=None, wqImpl = None):
        #self._layout = wx.BoxSizer(l)
        if ( wqImpl == None ):
            wqImpl = parent._wqImpl
        if self.isQt(wqImpl):
            if (orientation.VERTICAL == l):
                self._layout = qtw.QVBoxLayout()
                pass
            else:
                self._layout = qtw.QHBoxLayout()
                pass
        else: 
            self._layout = wx.BoxSizer(l)
            parent.implObject().SetSizer(self._layout)
        super(Layout, self).__init__(parent, self._layout, wqImpl=wqImpl)
        #super(wx.Panel, self).__init__(parent)


    def Add(self, label:Label, sizerFlags):
        if self.isQt():
            self._layout.addWidget(label.implObject())
            pass
        else:
            #self._layout.Add(label.implObject(), sizerFlags)
            pass

    def addElement(self,element):
        return self.wqD().doLayout_AddElement(element)