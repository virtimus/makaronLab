

from q3.ui.engine import qtw,qtc,qtg

from . import Object
from . import Label
from . import consts 
from .ui import orientation


class Layout(Object.Object):
    def __init__(self, parent, impl=None, **kwargs):
        super(Layout, self).__init__(parent, impl, **kwargs)


    def Add(self, label:Label, sizerFlags):
        return self.q3D().doLayout_Add(label, sizerFlags)

    def addElement(self,element):
        return self.q3D().doLayout_AddElement(element)