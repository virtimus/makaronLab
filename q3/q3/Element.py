
from q3.ui.engine import qtw,qtc,qtg

from . import consts
from . import Object
#, QWidget
class Element(Object.Object):
    def __init__(self,parent, impl=None, **kwargs): 
        super(Element, self).__init__(parent, impl, **kwargs)

    def resize(self, w:int, h:int):
        return self.q3D().doElement_Resize(w,h)

    def sizePolicy(self):
        return self.q3D().doElement_SizePolicy()

    def setSizePolicy(self, sizePolicy):
        return self.q3D().doElement_SetSizePolicy(sizePolicy)
                  