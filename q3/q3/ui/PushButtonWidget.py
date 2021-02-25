

from enum import Enum

from q3.ui.engine import qtw,qtc,qtg

class PBType(Enum):
    ePush = 1
    eToggle = 2

HBUTTON = 15
HBUTTON_SPACE = 5
HBUTTON_GLOBAL = 25

class PushButtonWidget(qtw.QGraphicsItem):
    def __init__(self,parent):
        super(PushButtonWidget, self).__init__(parent)
        self._boundingRect = qtc.QRectF( 0, 0, 40, HBUTTON+HBUTTON_SPACE)
        self._type = PBType.eToggle
        self._state = False
        pass


    def boundingRect(self) -> qtc.QRectF:
        return self._boundingRect

    #void mousePressEvent(QGraphicsSceneMouseEvent *a_event) override
    def mousePressEvent(self, event):
        #   (void)a_event;
        if (self._type == PBType.ePush):
            self._state = True
        else: #toggle
            self._state = not self._state
        self.onChangeState(self._state)
        
        
    def onChangeState(self, state):
        pass

    def mouseReleaseEvent(self, event):
        if (self._type == PBType.ePush):
            self._state = False
            self.onChangeState(self._state)
        else:#nop
            pass 
    
    def state(self):
        return self._state 

    def paint(self, painter, option, widget=None):

        #self.updRec();
        
        tcolor = qtg.QColor(203, 217, 81,255) if self.state() else qtg.QColor(244, 53, 64,255)
        tbrush = qtg.QBrush(tcolor)
        tbrush.setColor(tcolor)
        tbrush.setStyle(qtc.Qt.SolidPattern)

        tpen = qtg.QPen(qtc.Qt.black)

        painter.setPen(tpen)
        painter.setBrush(tbrush)

        painter.drawRect(self.boundingRect())
  


