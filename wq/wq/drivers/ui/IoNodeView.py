import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

import sip

from ...nodeiotype import NodeIoType
from ...wqvector import WqVector

from ... import consts, prop, orientation, direction, colors

#from ...Module import IoNode

from ... import colors
from ...valuetype import ValueType

from .IoLinkView import IoLinkView

from . import stypes

from ...ModuleFactory import ModuleType

#class IoLinkView:
#    pass 

class IoNodeView:
    pass 

IONODE_TYPE = stypes.IONODE_TYPE
#SocketItem
class IoNodeView(qtw.QGraphicsItem):
    SIZE = 16
    def __init__(self, parent:'ModuleViewImpl', ionode:'IoNode', dir:direction.Dir):
        super(IoNodeView, self).__init__(parent)
        self.m_node = parent
        self._parent = parent
        #self._ioType = ionode.ioType()
        #self.m_type = self._ioType #deprecated, redundant
        self._ionode = ionode
        self._self = ionode
        self._dir = dir
        self._font = qtg.QFont()
        self._font.setFamily("Consolas")
        self._font.setPointSize(10)
 
        self.setFlags(qtw.QGraphicsItem.ItemIsMovable | qtw.QGraphicsItem.ItemIsFocusable | qtw.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(qtc.Qt.LeftButton)
        self.setZValue(1)
        if (ionode.ioType() == NodeIoType.OUTPUT):
            self.setCursor(qtc.Qt.OpenHandCursor)
        else:
            self.setAcceptDrops(True)

        self._isHover = False
        self._inHover = False
        self._outHover = False
        self._isDrop = False
        self._used = False
        self._nameHidden = False
        self._multiuse = False

        self._colorSignalOn = None #!TODO!
        self._colorSignalOff = None
        #self._isSignalOn = False
        #self._isSignalOnPrev = None

        self._links = WqVector(IoLinkView)
        self.setValueType(ionode.valueType())

    #@api
    def mdl(self) -> 'IoNode':
        return self._ionode

    #@api
    def ioType(self):
        return self.mdl().ioType()

    def isSignalOn(self):
        return self.mdl().isSignalOn()

    def id(self):
        result = self._ionode.id()  if self._ionode != None else None
        return result  

    def showName(self):
        self._nameHidden = False

    def hideName(self):
        self._nameHidden = True

    def name(self):
        return self._ionode.name()

    def node(self):
        return self._ionode
    
    def dir(self):
        return self._dir

    def effectiveDir(self):
        result = self._dir 
        if (self.moduleView().isInvertH()):
            if (self._dir == direction.LEFT):
                result = direction.RIGHT
            elif (self._dir == direction.RIGHT):
                result = direction.LEFT
            elif (self._dir == direction.TOP):
                result = direction.DOWN
            elif (self._dir == direction.DOWN):
                result = direction.TOP                
            else:
                self.raiseExc('noImpl')
        if (self.moduleView().isRotate()):
            if result == direction.LEFT:
                result = direction.DOWN
            elif result == direction.RIGHT:
                result= direction.TOP
            elif result == direction.TOP:
                result= direction.LEFT
            elif result == direction.DOWN:
                result= direction.RIGHT
            else:
                self.raiseExc('noImpl')
        return result
        
       

    def setHover(self, hover):
        self._isHover = hover

    def setOutHover(self, hover):
        self._outHover = hover 

    def setInHover(self, hover):
        self._inHover = hover 

    def type(self):
        return IONODE_TYPE
    
    def setMultiuse(self, mu):
        self._multiuse = mu

    def boundingRect(self):
        result = qtc.QRectF( -(IoNodeView.SIZE / 2.), -(IoNodeView.SIZE / 2.), IoNodeView.SIZE,IoNodeView.SIZE )
        return result






    def paint(self, painter, option, widget=None):
        #Q_UNUSED(a_option);
        #Q_UNUSED(a_widget);
        rect = self.boundingRect()
        tiotype = self.ioType()
        tdir = self.dir()
        #effectivedir do not apply here because of rotation is handled by scene
        isInvert = self._parent.isInvertH()
        isInvertN = isInvert 
        if (tiotype == NodeIoType.OUTPUT and tdir==direction.LEFT) or (tiotype == NodeIoType.INPUT and tdir==direction.RIGHT):
            isInvertN = not isInvert
        startAngle = 90*16 if isInvertN else -90 * 16
        startAngleOutside = 90*16 if isInvertN else -90 * 16
        startAngleInside = -90 * 16  if isInvertN else 90*16
        if self.module().mType() == ModuleType.IO:
            if self.dir() in [direction.TOP,direction.DOWN]:
                startAngle = 0*16 if isInvert else -180 * 16
                startAngleOutside = 0*16 if isInvert else -180 * 16
                startAngleInside = -180 * 16  if isInvert else 0*16                 
        spanAngle = 180 * 16

        pen = qtg.QPen(colors.C.SOCKETBORDER.qColor())
        pens = None
        pen.setWidth(2)
        brush =  qtg.QBrush()
        if (self._isHover or self._inHover):
            brush.setColor(colors.C.SOCKETHOVER.qColor())
        elif (self._isDrop):
            brush.setColor(colors.C.SOCKETDROP.qColor())
        elif (self.isSignalOn()):
            brush.setColor(self._colorSignalOn)
        elif (not self.isSignalOn()):
            brush.setColor(self._colorSignalOff)
        #pens = qtg.QPen(brush.color())
        pens = self._colorSignalOn if self.isSignalOn() else self._colorSignalOff
        if (self._outHover and tiotype == NodeIoType.OUTPUT):
            pens = colors.C.SOCKETHOVER.qColor()
        #//  else if (tiotype == Type::eInput)
        #//    brush.setColor(config.getColor(Config::Color::eSocketInput));
        #//  else if (tiotype == Type::eOutput)
        #//    brush.setColor(config.getColor(Config::Color::eSocketOutput));
        if (tiotype == NodeIoType.DYNAMIC):
            brush.setStyle(qtc.Qt.Dense5Pattern)
        else:
            brush.setStyle(qtc.Qt.SolidPattern)

        painter.setPen(pen)
        painter.setBrush(brush)
        if (tiotype == NodeIoType.OUTPUT):
            painter.drawEllipse(rect)
            #painter.drawArc(rect.adjusted(-4, -4, +4, +4), startAngle, spanAngle)
            #painter.setPen(brush)
            if (self._used or self._links.itemCount()>0):
                painter.setPen(pens)
            painter.drawArc(rect.adjusted(-2, -2, +2, +2), startAngle, spanAngle)
        elif (tiotype == NodeIoType.DYNAMIC):
            painter.drawEllipse(rect)
            painter.drawArc(rect.adjusted(-2, -2, +2, +2), startAngleInside, spanAngle)
            painter.drawArc(rect.adjusted(-2, -2, +2, +2), startAngleOutside, spanAngle)
        else:
            painter.drawEllipse(rect)
            #painter.drawArc(rect.adjusted(-4, -4, +4, +4), startAngle, spanAngle)
            #painter.setPen(brush)
            painter.setPen(pens)
            painter.drawArc(rect.adjusted(-2, -2, +2, +2), startAngle, spanAngle)
            if (not self._used):
                #painter.save()
                painter.setPen(qtc.Qt.NoPen)
                painter.setBrush(pen.color())
                painter.drawEllipse(rect.adjusted(4, 4, -4, -4))
                #painter.restore()
            

        if ( not self._nameHidden):
            pen.setColor(colors.C.FONTNAME.qColor())
            painter.setPen(pen)
            painter.setFont(self._font)
            metrics = qtg.QFontMetrics(self._font)
            FONT_HEIGHT = metrics.height()
            if (direction.LEFT == self.dir()):
                painter.drawText((rect.width()) - 4, (FONT_HEIGHT / 2) - metrics.strikeOutPos(), self.name())
            else:
                painter.drawText(-metrics.width(self.name()) - IoNodeView.SIZE + IoNodeView.SIZE / 3, (FONT_HEIGHT / 2) - metrics.strikeOutPos(), self.name())


    def paint1(self, painter, option, widget=None):
        #Q_UNUSED(a_option);
        #Q_UNUSED(a_widget);
        rect = self.boundingRect()
        tiotype = self.ioType()

        pen = qtg.QPen(colors.C.SOCKETBORDER.qColor())
        pen.setWidth(2)
        brush =  qtg.QBrush()
        if (self._isHover):
            brush.setColor(colors.C.SOCKETHOVER.qColor())
        elif (self._isDrop):
            brush.setColor(colors.C.SOCKETDROP.qColor())
        elif (self.isSignalOn()):
            brush.setColor(self._colorSignalOn)
        elif (not self.isSignalOn()):
            brush.setColor(self._colorSignalOff)
        #//  else if (tiotype == Type::eInput)
        #//    brush.setColor(config.getColor(Config::Color::eSocketInput));
        #//  else if (tiotype == Type::eOutput)
        #//    brush.setColor(config.getColor(Config::Color::eSocketOutput));
        if (tiotype == NodeIoType.DYNAMIC):
            brush.setStyle(qtc.Qt.Dense5Pattern)
        else:
            brush.setStyle(qtc.Qt.SolidPattern)

        painter.setPen(pen)
        painter.setBrush(brush)
        if (tiotype == NodeIoType.OUTPUT):
            painter.drawEllipse(rect)
        elif (tiotype == NodeIoType.DYNAMIC):
            painter.drawRect(rect)
            painter.drawEllipse(rect)
        else:
            painter.drawRect(rect)
        
        if (not self._used):
            painter.save()
            painter.setPen(qtc.Qt.NoPen)
            painter.setBrush(pen.color())
            
            if (tiotype == NodeIoType.OUTPUT):
                painter.drawEllipse(rect.adjusted(4, 4, -4, -4))
            elif (tiotype == NodeIoType.DYNAMIC):
                painter.drawRect(rect.adjusted(4, 4, -4, -4))
                painter.drawEllipse(rect.adjusted(4, 4, -4, -4))
            else:
                painter.drawRect(rect.adjusted(4, 4, -4, -4))
            painter.restore()

        if ( not self._nameHidden):
            pen.setColor(colors.C.FONTNAME.qColor())
            painter.setPen(pen)
            painter.setFont(self._font)
            metrics = qtg.QFontMetrics(self._font)
            FONT_HEIGHT = metrics.height()
            if (direction.LEFT == self.dir()):
                painter.drawText((rect.width()) - 4, (FONT_HEIGHT / 2) - metrics.strikeOutPos(), self.name())
            else:
                painter.drawText(-metrics.width(self.name()) - IoNodeView.SIZE + IoNodeView.SIZE / 3, (FONT_HEIGHT / 2) - metrics.strikeOutPos(), self.name())


    def hoverEnterEvent(self, event): #QGraphicsSceneHoverEvent 
        #Q_UNUSED(event);
        self._isHover = True
        for l in self._links.values():
            if l.to() == self:
                l.setHover(self._isHover)

    def hoverLeaveEvent(self, event): #QGraphicsSceneHoverEvent
        #Q_UNUSED(event)
        self._isHover = False
        for l in self._links.values():
            if l.to() == self:
                l.setHover(self._isHover)

    def dragEnterEvent(self, event): #QGraphicsSceneDragDropEvent
        #Q_UNUSED(event)
        if (self._used and not self._multiuse):
            event.ignore()
            return
        view = self.scene().views()[0]#%PackageView
        linkItem = view.dragLink() #IoLinkView
        if ( linkItem == None or self._valueType != linkItem.valueType()):
            event.ignore()
            return
        linkItem.setTo(self)
        self._isDrop = True
     
    def dragLeaveEvent(self, event): #QGraphicsSceneDragDropEvent
        #Q_UNUSED(event)
        self._isDrop = False
        view = self.scene().views()[0]
        linkItem = view.dragLink()
        if (linkItem == None):
            return
        linkItem.setTo(None)

    def dragMoveEvent(self, event): #QGraphicsSceneDragDropEvent
        #Q_UNUSED(event)
        pass

    def dropEvent(self, event): #QGraphicsSceneDragDropEvent
        #Q_UNUSED(event);
        pv = self.scene().views()[0]
        linkItem = pv.dragLink()
        if (linkItem == None):
            return
        '''
        self._links.push_back(linkItem)
        linkItem.setTo(self)
        if linkItem.fr().node().driveSignal()!=None:
            self.node().setDriveSignal(linkItem.fr().node().driveSignal())
        self._used = True
        self._isDrop = False
        '''
        self.finishIoLinkView(linkItem)

        pv.acceptDragLink()

        #package = pv.package() #!TODO!
        package = pv.module().impl()
        f = linkItem.fr()
        package.connect(f, self) #elementId(), from.socketId(), from->ioFlags(), m_elementId, m_socketId, ioFlags());

        #self.setSignal(linkItem.isSignalOn())

    def mouseDoubleClickEvent(self, event):
        #print(f"Double Click{self.id()}")
        tdsig = self.mdl().driveSignal()
        tdsig.setValue(not tdsig.value())
 

    def mousePressEvent(self, event): #QGraphicsSceneMouseEvent
        #Q_UNUSED(event);
        if (self.ioType() == NodeIoType.INPUT):#input cannot be a start for link
            return
        self.setCursor(qtc.Qt.ClosedHandCursor)
        
        
    def newIoLinkView(self):
        linkItem = IoLinkView() #new LinkItem;
        linkItem.setColors(self._colorSignalOff, self._colorSignalOn)
        linkItem.setValueType(self._valueType)
        linkItem.setFr(self)
        #linkItem.setSignal(self._isSignalOn)
        self._links.push_back(linkItem)
        self.scene().addItem(linkItem)
        return linkItem

    def finishIoLinkView(self,linkItem:IoLinkView):
        if (linkItem == None):
            return
        self._links.push_back(linkItem)
        linkItem.setTo(self)
        if linkItem.fr().node().driveSignal()!=None:
            self.node().setDriveSignal(linkItem.fr().node().driveSignal())
        self._used = True
        self._isDrop = False
        pass
        

    def mouseMoveEvent(self, event): #QGraphicsSceneMouseEvent
        #Q_UNUSED(event);
        if (self.ioType() == NodeIoType.INPUT): #inputs not involved
            return

        if (qtc.QLineF(event.screenPos(), event.buttonDownScreenPos(qtc.Qt.LeftButton)).length() < qtw.QApplication.startDragDistance()):
            return
        
        mime = qtc.QMimeData()
        drag = qtg.QDrag(event.widget())
        drag.setMimeData(mime)
        

        '''
        linkItem = IoLinkView() #new LinkItem;
        linkItem.setColors(self._colorSignalOff, self._colorSignalOn)
        linkItem.setValueType(self._valueType)
        linkItem.setFr(self)
        #linkItem.setSignal(self._isSignalOn)
        
        self.scene().addItem(linkItem)
        self._links.push_back(linkItem)
        '''
        linkItem = self.newIoLinkView()
        
        view = self.scene().views()[0]
        view.setDragLink(linkItem)

        action = qtc.Qt.DropAction( drag.exec() )
        if (action == qtc.Qt.IgnoreAction):
            self.removeLink(linkItem)
            self.scene().removeItem(linkItem)
            view.cancelDragLink()
        else:
            self._used = True
        self.setCursor(qtc.Qt.OpenHandCursor)
        print(f'Used{self._used}')


    def mouseReleaseEvent(self, event): #QGraphicsSceneMouseEvent
        #Q_UNUSED(event);
        if (self.ioType() == NodeIoType.INPUT):
            return
        self.setCursor(qtc.Qt.OpenHandCursor)

    def itemChange(self, change, value): #qtw.QGraphicsItem.GraphicsItemChange,:qtc.QVariant
        if (change == qtw.QGraphicsItem.ItemScenePositionHasChanged):
            for l in self._links.values():
                l.trackNodes()
        return super().itemChange(change, value) #QGraphicsItem::

    def setName(self, name:str):
        self._ionode.setName(name)

    def module(self):
        return self._ionode.module()

    def moduleId(self):
        self.module().id()

    def moduleView(self):
        return self.module().view().impl()

    def graphModule(self):
        return self.module().graphModule()

    def nameWidth(self):
        metrics = qtg.QFontMetrics( self._font )
        return metrics.width(self.name())

    def setColors(self, signalOff, signalOn): #QColor const 
        self._colorSignalOff = signalOff
        self._colorSignalOn = signalOn

    def connect(self, other:IoNodeView): #SocketItem *const
        link = self.linkBetween(self, other)
        if (link != None): #already connected
            return
        '''
        linkItem = IoLinkView() #/LinkItem;
        linkItem.setColors(self._colorSignalOff, self._colorSignalOn)
        linkItem.setValueType(self._valueType)
        linkItem.setFr(self)
        self._links.push_back(linkItem)
        self.scene().addItem(linkItem)
        '''
        linkItem = self.newIoLinkView()

        self._used = True

        
        '''
        linkItem.setTo(other)
        other._links.push_back(linkItem)
        other._used = True
        other._isDrop = False
        '''
        other.finishIoLinkView(linkItem)
        

    def linkBetween(self, fr, to): #SocketItem *const
        for l in self._links.values():
            if l.fr() == fr and l.to() == to:
                return l
        return None

    def elementId(self):#!TODO!# deprecated
        return self._ionode.module().id()

    def socketId(self):#!TODO!# deprecated
        return self._ionode.id()

    def removeLink(self, linkItem): #LinkItem *const
        #it = std::remove(std::begin(m_links), std::end(m_links), a_linkItem);
        self._links.remove(linkItem)
        self._used = self._links.itemCount()>0

    def disconnect(self, other): #SocketItem *const
        link = self.linkBetween(self, other)
        if (link == None):
            return
        #FROM_ID = self.elementId()
        #FROM_SOCKET_ID = socketId();
        #ROM_IOFLAGS = ioFlags();
        ##auto const TO_ID = a_other->elementId();
        #auto const TO_SOCKET_ID = a_other->socketId();
        #auto const TO_IOFLAGS = a_other->ioFlags();

        #auto const packageView = m_node->packageView();
        graphModuleViewImpl = self.graphModule().impl()
        #auto const package = packageView->package();

        #package->disconnect(FROM_ID, FROM_SOCKET_ID, FROM_IOFLAGS, TO_ID, TO_SOCKET_ID, TO_IOFLAGS);
        graphModuleViewImpl.disconnect(self.id(),self.id(), other.id(),other.id())
        
        link.setHover(False)
        self.removeLink(link)
        other.removeLink(link)
        
        if (self._links.empty()):
            self._used = False
        
        self._isHover = False
        #//self.setOutHover(False)
        #//self.setInHover(False)
        other._used = False
        other._isHover = False
 
        #delete link;
        
        sip.delete(link)
        link = None


    def disconnectAll(self):
        if (self.ioType() == NodeIoType.INPUT):
            self.disconnectAllInputs()
        else:
            self.disconnectAllOutputs()
    
    def disconnectAllInputs(self):
        links = self._links
        for l in links:
            f = l.fr()
            f.disconnect(self)

    def disconnectAllOutputs(self):
        links = self._links
        for l in links:
            self.disconnect(l.to())

    def setValueType(self, type:ValueType): #ValueType const a_
        self._valueType = type
        self.setColors(self._valueType.colorSigOff(), self._valueType.colorSigOn())

    def valueType(self):
        return self._valueType

             
