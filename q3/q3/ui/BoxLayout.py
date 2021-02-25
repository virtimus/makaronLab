from q3.ui.engine import qtw,qtc,qtg

from q3.q3vector import Q3Vector

from enum import Enum

class dir(Enum):
    H = 1
    V = 2

class Litem:
    def __init__(self,dir:dir,obj):
        self._dir = dir
        self._obj = obj

    def dir(self):
        return self._dir

    def obj(self):
        return self._obj

class BoxLayout(qtw.QGraphicsItem):
    def __init__(self,parent):
        super(BoxLayout, self).__init__(parent)
        self._boundingRect = qtc.QRectF(0, 0, 40, 40)

        self._widgets = Q3Vector(Litem)


        pass

    def addH(self, obj):
        lit = Litem(dir.H,obj)
        self._widgets.push(lit)

    def addV(self,obj):
        lit = Litem(dir.V,obj)
        self._widgets.push(lit)        


    def boundingRect(self) -> qtc.QRectF:
        h = 0
        v = 0
        d = dir.H
        maxv = 0
        for o in self._widgets.values():
            d = o.dir()
            o = o.obj()
            o.setPos(h,v)
            br = o.boundingRect()
            ow = br.width()
            oh = br.height()
            maxv = oh if oh > maxv else maxv
            h += ow if d == dir.H else 0
            v += oh if d == dir.V else 0


        self._boundingRect.setHeight(v+maxv)
        self._boundingRect.setWidth(h)

        return self._boundingRect

