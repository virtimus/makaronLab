import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

from ... import colors
from ..sim.valuetype import ValueType

from ... import consts, prop, orientation, direction, colors

from . import stypes

class IoNodeView:
    pass 

IOLINK_TYPE = stypes.IOLINK_TYPE

#LinkItem
class IoLinkView(qtw.QGraphicsPathItem):
    #LinkItem(QGraphicsItem *a_parent = nullptr);
    def __init__(self,parent=None): #parent:QGraphicsItem
        super(IoLinkView, self).__init__(parent)
        self._fr = None
        self._to = None
        self._toPoint = qtc.QPointF()
        self._boundingRect = qtc.QRectF()
        self._valueType = None
        self._isSnapped = False
        self._isHover = False
        self._isSignalOn = False
        self._shape =  qtg.QPainterPath() #QPainterPath m_shape{};
        self._path = qtg.QPainterPath() #QPainterPath m_path{};
        self._dashOffset = None #/0.0 #qreal
        self._tmp = {}
        '''
         QRectF m_boundingRect{};
  
  

  QColor m_colorSignalOn{};
  QColor m_colorSignalOff{};

  QPointF m_toPoint{};

  qreal m;

        '''
        self.setFlags(qtw.QGraphicsItem.ItemSendsGeometryChanges | qtw.QGraphicsItem.ItemIsFocusable | qtw.QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.setAcceptHoverEvents(True)



    def type(self):
        return IOLINK_TYPE

    def fr(self): #SocketItem/IoNodeView
        return self._fr

    def setFr(self, fr): # SocketItem *const 
        self._fr = fr
        position = qtc.QPointF( self.mapFromScene(self._fr.scenePos()) )
        self.setPos(position)
        self.trackNodes()        

    def to(self): #SocketItem/IoNodeView
        return self._to

    def setToIoNodeView(self, to:IoNodeView): # SocketItem *const 
        self._to = to
        self._isSnapped = to != None
        self.trackNodes()

    def setToPointF(self, to:qtc.QPointF):  #QPointF const
        self._toPoint = self.mapFromScene(to)
        self.trackNodes()

    def setTo(self, any):
        if any == None:
            self.setToIoNodeView(any)
        elif isinstance(any, qtc.QPointF): 
            self.setToPointF(any)
        else:
            self.setToIoNodeView(any)


    def setValueType(self, type:ValueType):
        self._valueType = type

    def valueType(self) -> ValueType:
        return self._valueType

    def isSnapped(self):
        return self._isSnapped
    
    def isSignalOn(self):
        return self._isSignalOn

    def boundingRect(self):
        return self._shape.boundingRect()

    def shape(self):
        return self._shape

    def paint(self, painter, option, widget=None): #QStyleOptionGraphicsItem, QWidget
        #(void)option;
        #(void)widget;

        signalColor = self._colorSignalOn if self._isSignalOn else self._colorSignalOff
        #QColor const notActive{ (isSelected() ? get_color(Color::eSelected) : signalColor) };
        notActive = colors.C.SELECTED.qColor() if self.isSelected() else signalColor
        #QColor const hover{ get_color(Color::eSocketHover) };
        hover = colors.C.SOCKETHOVER.qColor()
        #QPen pen{ (m_isHover ? hover : notActive) };
        pen = qtg.QPen(hover) if self._isHover else qtg.QPen(notActive)
        pstyle = qtc.Qt.SolidLine if (self._to != None) else qtc.Qt.DashDotLine
        pen.setStyle(pstyle)
        pen.setWidth(2)

        if (self._valueType != ValueType.BOOL):
            dash = pen
            hover2 = signalColor
            hover2.setAlpha(85)
            dash.setColor(hover2)
            dash.setStyle(qtc.Qt.DotLine)
            dash.setWidth(6)
            dash.setDashOffset(self._dashOffset)
            painter.setPen(dash)
            painter.drawPath(self._path)

        painter.setPen(pen)
        painter.drawPath(self._path)

        #if 'linkItemPos' in self._tmp:
        #    painter.drawLine(self._tmp['linkItemPos'],self._tmp['c1'])
        #    painter.drawLine(self._tmp['toPoint'],self._tmp['c2'])

    def hoverEnterEvent(self, event): #QGraphicsSceneHoverEvent
        #(void)event;
        self.setHover(True)

    def hoverLeaveEvent(self, event): #QGraphicsSceneHoverEvent
        #(void)event;
        self.setHover(False)

    def advance(self, phase): #int
        if (phase == None or not phase):
            return
        if (self._valueType != ValueType.BOOL):
            self._dashOffset -= 0.1
        self.update()

    def setHover(self, hover):
        self._isHover = hover
        if (self._fr != None):
            self._fr.setHover(self._isHover)
        if (self._to != None):
            self._to.setHover(self._isHover)

    def setColors(self, signalOff, signalOn): #QColor const a_
        self._colorSignalOff = signalOff
        self._colorSignalOn = signalOn

    def setSignal(self, signal):
        self._isSignalOn = signal
        if (self._to != None):
            self._to.setSignal(signal)

    def trackNodes(self):
        self.prepareGeometryChange()
        #QPointF const linkItemPos{ m_from->scenePos() };
        linkItemPos = qtc.QPointF(self._fr.scenePos())
        self.setPos(linkItemPos)
        self._path.clear()

        #QPointF const toPoint{ (m_to ?  : m_toPoint) };
        toPoint = self.mapFromScene(self._to.scenePos()) if (self._to != None) else self._toPoint
        self._toPoint = toPoint

        #double x = toPoint.x() < 0. ? toPoint.x() : 0.;
        #double y = toPoint.y() < 0. ? toPoint.y() : 0.;
        #double w = fabs(toPoint.x());
        #double h = fabs(toPoint.y());
        x = toPoint.x() if (toPoint.x() < 0) else 0.0
        y = toPoint.y() if (toPoint.y() < 0) else 0.0
        w = abs(toPoint.x())
        h = abs(toPoint.y())

        self._boundingRect.setX(x)
        self._boundingRect.setY(y)
        self._boundingRect.setWidth(w)
        self._boundingRect.setHeight(h)

        c1 = qtc.QPointF()
        c2 = qtc.QPointF()
        distWS = round(self._toPoint.x() * 0.5) 
        distW = abs(distWS) 
        distHS = round(self._toPoint.y() * 0.5)
        distH = abs(distHS) * 0.5 

        mindelta = 200

        deltaWR = 0
        deltaWL = 0
        if (distW<mindelta and (distW<10 or distWS<0)):
            deltaWR = mindelta-distW
        if (distW<mindelta and (distW<10 or distWS>0)):
            deltaWL = mindelta-distW

        deltaWD = 0
        deltaWU = 0
        if (distH<mindelta and (distH<5 or distHS<0)):
            deltaWD = mindelta-distH
        if (distH<mindelta and (distH<5 or distHS>0)):
            deltaWU = mindelta-distH

        c1x = None
        c2x = None
        c1y = None
        c2y = None 
        sourceDir = self._fr.effectiveDirection()
        targetDir = self._to.effectiveDirection() if self._to != None else None
        
        if sourceDir == direction.RIGHT:
            c1x = distW+deltaWR
            c1y = 0
        if targetDir == direction.RIGHT:
            c2x = self._toPoint.x() +distW+deltaWL 
            c2y = self._toPoint.y()
        if sourceDir == direction.LEFT:
            c1x = -distW-deltaWL
            c1y = 0            
        if targetDir == direction.LEFT:
            c2x = self._toPoint.x() -distW-deltaWR
            c2y = self._toPoint.y()

        if sourceDir == direction.DOWN:
            c1x = 0
            c1y = distH+deltaWD
        if targetDir == direction.DOWN:
            c2x = self._toPoint.x() 
            c2y = self._toPoint.y()+distH+deltaWU 
        if sourceDir == direction.TOP:
            c1x = 0
            c1y = -distH-deltaWU            
        if targetDir == direction.TOP:
            c2x = self._toPoint.x() 
            c2y = self._toPoint.y() -distH-deltaWD

        if targetDir == None: #dragging...
            c2x = self._toPoint.x() 
            c2y = self._toPoint.y() 
        

        c1.setX(c1x)
        c1.setY(c1y)
        c2.setX(c2x)
        c2.setY(c2y)

        self._path.cubicTo(c1, c2, self._toPoint)

        #self._tmp['linkItemPos'] = self.mapFromScene(linkItemPos)
        #self._tmp['toPoint']= self._toPoint
        #self._tmp['c1'] = c1
        #self._tmp['c2'] = c2
        
        


        #print(f'Elems:{self._path.elementCount()}')

	    #//m_from->node()->element()->
	    #//!TODO! memory acc problems (global ref invalid?)
	    #//consoleAppendF("{},{},{},{},c1.x{},c1.y{},c2.x{},c2.y{}",linkItemPos.x(),linkItemPos.y(),m_toPoint.x(),m_toPoint.y(),c1.x(),c1.y(),c2.x(),c2.y());

        stroker = qtg.QPainterPathStroker()
        stroker.setWidth(15)
        self._shape = stroker.createStroke(self._path)