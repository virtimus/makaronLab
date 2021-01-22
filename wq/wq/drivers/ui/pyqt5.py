
# PYQT

import sys
import sip

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt, QPoint, QTimeLine
from PyQt5.QtGui import QBrush, QColor, QIcon, QPainter, QPalette
from PyQt5.QtWidgets import (QAction, QApplication, QGraphicsItem,
                             QGraphicsScene, QGraphicsView, qApp)

from ... import consts, prop, orientation, direction, colors
from ...moduletype import ModuleType

from ..driverBase import WqDriverBase


from enum import Enum

class GridDensity(Enum):
    LARGE = 1
    SMALL = 2

class WqiShowMode(Enum):
    ICONIFIED = 1
    EXPANDED = 2

class WqVector:
    def __iter__(self):
        return self._list.__iter__();

    def __next__(self):
        return self._list.__next__();

    def __init__(self):
        self._list = []
        pass

    def count(self):
        return len(self._list)


class SocketItem(qtw.QGraphicsItem):
    SIZE = 16
      
SOCKET_SIZE = SocketItem.SIZE
ROUNDED_SOCKET_SIZE = round((SOCKET_SIZE) / 10.0) * 10.0
ROUNDED_SOCKET_SIZE_2 = ROUNDED_SOCKET_SIZE / 2.0

#implements nonroot mode of moduleView (spaghetti node)
class WqGraphicsItem(qtw.QGraphicsItem):
    def __init__(self,parent):
        self._self = None # should finally point to ModuleView Object
        self._nameFont = qtg.QFont()
        self._element = None
        self._centralWidget = None #QGraphicsItem
        self._centralWidgetPosition = None  #QPointF
        self._mode = None #WqiShowMode
        self._icon = qtg.QPixmap()
        self._showName = True
        self._boundingRect = None
        self._inputs = WqVector()
        self._outputs = WqVector()
        self._color = qtg.QColor(105, 105, 105, 128)
        super(WqGraphicsItem,self).__init__(parent)

    def s(self):
        return self._self

    def setIcon(self, ico:str):
        self._iconPath = ico
        self._icon.load(ico)


    def setCentralWidget(self, w:QGraphicsItem):
        if (self._centralWidget != None):
            sip.delete(self._centralWidget)
            self._centralWidget = None
            self._centralWidget = w
            self._centralWidget.setParentItem(self)
            self._centralWidget.setPos(self._centralWidgetPosition)
        
    def iconify(self):
        if (self._element != None):
            self._element.iconify(True)
            if (self._element.iconifyingHidesCentralWidget() and self._centralWidget != None):
                self._centralWidget.hide()
        self._mode = WqiShowMode.ICONIFIED
        for inp in self._inputs:
            inp.hideName()
        for out in self._outputs:
            out.hideName()
        self.calculateBoundingRect()

    def findMaxNameWidth(self,coll):
        #TODO
        return 5

    def calculateBoundingRect(self):
        self.prepareGeometryChange()
        INPUTS_COUNT = self._inputs.count()
        OUTPUTS_COUNT = self._outputs.count()
        SOCKETS_COUNT = max(INPUTS_COUNT, OUTPUTS_COUNT)
        CENTRAL_SIZE = self._centralWidget.boundingRect().size() if (self._centralWidget != None and  self._centralWidget.isVisible()) else self._icon.size() / 2
        SOCKETS_HEIGHT = SOCKETS_COUNT * ROUNDED_SOCKET_SIZE

        #maxNameWidth = [](auto &&a_a, auto &&a_b) { return a_a->nameWidth() < a_b->nameWidth(); };
        #auto const LONGEST_INPUT = max_element(m_inputs, maxNameWidth);
        #auto const LONGEST_OUTPUT = max_element(m_outputs, maxNameWidth);
        #int const LONGEST_INPUTS_NAME_WIDTH = LONGEST_INPUT != std::end(m_inputs) ? (*LONGEST_INPUT)->nameWidth() : 0;
        LONGEST_INPUTS_NAME_WIDTH = self.findMaxNameWidth(self._inputs)
        #int const LONGEST_OUTPUTS_NAME_WIDTH = LONGEST_OUTPUT != std::end(m_outputs) ? (*LONGEST_OUTPUT)->nameWidth() : 0;
        LONGEST_OUTPUTS_NAME_WIDTH = self.findMaxNameWidth(self._outputs)
        INPUTS_NAME_WIDTH = LONGEST_INPUTS_NAME_WIDTH if self._mode == WqiShowMode.EXPANDED else 0
        OUTPUTS_NAME_WIDTH = LONGEST_OUTPUTS_NAME_WIDTH if self._mode == WqiShowMode.EXPANDED else 0
        NAME_OFFSET = ROUNDED_SOCKET_SIZE_2 if self._showName else 0
        width = CENTRAL_SIZE.width() 
        height = None
        if (SOCKETS_HEIGHT > CENTRAL_SIZE.height()):
            height = NAME_OFFSET + SOCKETS_HEIGHT + ROUNDED_SOCKET_SIZE
        else:
            height = NAME_OFFSET + CENTRAL_SIZE.height() + ROUNDED_SOCKET_SIZE_2
        if (SOCKETS_COUNT < 2):
            height += ROUNDED_SOCKET_SIZE_2
        width = ROUNDED_SOCKET_SIZE + INPUTS_NAME_WIDTH + CENTRAL_SIZE.width() + OUTPUTS_NAME_WIDTH + ROUNDED_SOCKET_SIZE
        width = round(width / 10.0) * 10.0
        height = round(height / 10.0) * 10.0
        CENTRAL_X = ROUNDED_SOCKET_SIZE + INPUTS_NAME_WIDTH
        CENTRAL_Y = NAME_OFFSET + (height / 2.0) - (CENTRAL_SIZE.height() / 2.0)
        self._centralWidgetPosition = qtc.QPointF(CENTRAL_X, CENTRAL_Y)
        if (self._centralWidget != None):
            self._centralWidget.setPos(self._centralWidgetPosition)
        yOffset = ROUNDED_SOCKET_SIZE + NAME_OFFSET
        sinp = 0.0
        sout = width
        if (self._element != None and (direction.LEFT == self._element.direction() or direction.DOWN == self._element.direction())):
            sinp = width
            sout = 0.0
        for inp in self._inputs:
            inp.setPos(sinp, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        yOffset = ROUNDED_SOCKET_SIZE + NAME_OFFSET
        for out in self._outputs:
            out.setPos(sout, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        self._boundingRect = qtc.QRectF(0.0, 0.0, width, height)

    #paint(QPainter *painter, QStyleOptionGraphicsItem const *option, QWidget *widget)
    def paint(self, painter,option,widget=None):
    #def paintEvent(self, event):
    #    qp = QPainter()
    #    qp.begin(self)
        #(void)a_option;
        #(void)a_widget;
        self.paintBorder(painter)
        if (self._centralWidget == None or not self._centralWidget.isVisible()):
            self.paintIcon(painter)
    #    qp.end()

    def paintIcon(self, painter):
        HALF_ICON_SIZE = self._icon.size() / 2
        Y = self._centralWidgetPosition.y()
        WIDTH = HALF_ICON_SIZE.width()
        HEIGHT = HALF_ICON_SIZE.height()
        painter.drawPixmap(self._centralWidgetPosition.x(), Y, WIDTH, HEIGHT, self._icon)


    def boundingRect(self):
        return self._boundingRect

    #void Node::paintBorder(QPainter *const a_painter)
    def paintBorder(self, painter):
        rect = self.boundingRect()

        pen = qtg.QPen() # pen{};
        pen.setColor(colors.C.SOCKETBORDER.qColor())
        pen.setWidth(2)
        #//QColor color{ 105, 105, 105, 128 };
        brush = qtg.QBrush( self._color)
        painter.setPen(qtc.Qt.NoPen)
        painter.setBrush(brush)
        painter.drawRect(rect)

        if (self._showName):
            nameRect =qtc.QRectF( 0.0, 0.0, self._boundingRect.width(), ROUNDED_SOCKET_SIZE )
            pen.setColor(colors.C.FONTNAME.qColor())
            nameBackground = QColor(colors.C.NAMEBACKGROUND.qColor())
            nameBackground.setAlpha(128)
            
            painter.setPen(qtc.Qt.NoPen)
            painter.setBrush(nameBackground)
            painter.drawRect(nameRect)
            
            pen.setColor(colors.C.FONTNAME.qColor())
            painter.setFont(self._nameFont)
            painter.setPen(pen)

            METRICS = qtg.QFontMetrics( self._nameFont )
            FONT_HEIGHT = METRICS.height()
            NAME_Y = (ROUNDED_SOCKET_SIZE / 2.0) + (FONT_HEIGHT - METRICS.strikeOutPos()) / 2.0 - 1.0
            painter.drawText(qtc.QPointF(5.0, NAME_Y), self.s().name())
        selColor = qtg.QColor(156, 156, 156, 255) if self.isSelected() else qtg.QColor(58, 66, 71, 255)
        pen.setColor( selColor )
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(qtc.Qt.NoBrush)
        painter.drawRect(rect)

class WqDriver(WqDriverBase):



    def doModuleView_Init(self):
        if self.s().isRoot():#@s:PackageView::PackageView
            sc = qtw.QGraphicsScene(self.pimpl())            
            result = qtw.QGraphicsView(sc,self.pimpl())
            result._scene = sc
            wheelEvent = getattr(self.s(), "wheelEvent", None)
            if callable(wheelEvent):
                result.wheelEvent = wheelEvent
            drawBackground = getattr(self.s(), "drawBackground", None)
            if callable(drawBackground):
                result.drawBackground = drawBackground                
        else:  
            if isinstance(self.pimpl(), QGraphicsView):
                result = WqGraphicsItem(None)
                self.pimpl()._scene.addItem(result)
            else:
                result = WqGraphicsItem(self.pimpl())
        return result; 

    def doModuleView_AfterInit(self):
        tImpl = self.impl()
        tImpl._self = self.s()
        tImpl._element = self.s().module()
        if self.s().isRoot():#@s:PackageView::PackageView
            #self.s()._inputsView  = self.s().addModuleView('moduleInputs', type=ModuleType.INPUTS)
            #self.s()._outputsView = self.s().addModuleView('moduleOutputs', type=ModuleType.OUTPUTS)
            #vec2d m_inputsPosition{ -400.0, 0.0 };
            self.s()._inputsView.setProp(prop.PositionX,-400.0)
            self.s()._inputsView.setProp(prop.PositionY,0.0)
            self.s()._outputsView.setProp(prop.PositionX,400.0)
            self.s()._outputsView.setProp(prop.PositionY,0.0)
            #tImpl.__class__ = MainWindow
            tImpl.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
            tImpl.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.HighQualityAntialiasing | QPainter.SmoothPixmapTransform)
            tImpl.setDragMode(QGraphicsView.ScrollHandDrag)
            tImpl.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            tImpl.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            tImpl.setResizeAnchor(QGraphicsView.NoAnchor)
            tImpl.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
            tImpl.setOptimizationFlags(QGraphicsView.DontSavePainterState | QGraphicsView.DontAdjustForAntialiasing)
            tImpl.setObjectName("PackageView")

            #m_nodesProxyModel->setSourceModel(m_nodesModel);

            tImpl._scene.setItemIndexMethod(QGraphicsScene.NoIndex)
            tImpl._scene.setSceneRect(-32000, -32000, 64000, 64000)
            tImpl._scene.setObjectName("PackageViewScene")

            brush = QBrush(QColor(169, 169, 169, 32))
            tImpl._scene.setBackgroundBrush(brush)

            #m_inputs->setPropertiesTable(m_properties);
            #m_outputs->setPropertiesTable(m_properties);

            #m_packageNode->setPropertiesTable(m_properties);

            tImpl.setAcceptDrops(True)
            '''
            using NodeType = Node::Type;
            m_inputs->setType(NodeType::eInputs);
            m_inputs->setPos(m_package->inputsPosition().x, m_package->inputsPosition().y);
            m_inputs->setElement(m_package);
            m_inputs->setIcon(":/logic/inputs.png");
            m_inputs->setPackageView(this);
            m_inputs->iconify();
            m_outputs->setType(NodeType::eOutputs);
            m_outputs->setPos(m_package->outputsPosition().x, m_package->outputsPosition().y);
            m_outputs->setElement(m_package);
            m_outputs->setIcon(":/logic/outputs.png");
            m_outputs->setPackageView(this);
            m_outputs->iconify();

            m_packageNode->setInputsNode(m_inputs);
            m_packageNode->setOutputsNode(m_outputs);
            m_packageNode->setElement(m_package);

            if (m_package->name().empty()) {
            auto &registry = /*Registry::get()*/m_editor->RegistryGet();
            m_package->setName(registry.elementName("logic/package"));
            }

            m_scene->addItem(m_inputs);
            m_scene->addItem(m_outputs);

            //m_timer.setInterval(1000 / 60);
            //m_timer.setInterval(5000);
            m_timer.setInterval(1);

            connect(&m_timer, &QTimer::timeout, [this]() { m_scene->advance(); });
            m_timer.start();

            if (m_standalone) m_package->startDispatchThread();
            '''
        else: #Node::Node
            tImpl._nameFont.setFamily("Consolas")
            tImpl._nameFont.setPointSize(8)

            tImpl.setFlags(qtw.QGraphicsItem.ItemIsMovable | qtw.QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

            tImpl.iconify()
            pass #nop

       

    def wheelEvent_onFactor(self):       
        factor = 1.0 + self.s()._scheduledScalings / 300.0
        temp = self.impl().transform()
        temp.scale(factor, factor)
        if (temp.m11() >= 0.2 and temp.m11() <= 4.0):
            self.impl().scale(factor, factor)

    def wheelEvent_onFinish(self):
        if (self.s()._scheduledScalings > 0):
            self.s()._scheduledScalings-=1
        else:
            self.s()._scheduledScalings+=1
        if (self.impl().sender()):
            self.impl().sender().deleteLater()
        REAL_SCALE = self.impl().transform().m11()
        self.s().updateGrid(REAL_SCALE)            

    def doModuleView_wheelEvent(self,event): 
        numDegrees = event.angleDelta().y()/8 #?pixelDelta
        numSteps = numDegrees/15

        if (self.s()._scheduledScalings == None):
            self.s()._scheduledScalings = 0

        self.s()._scheduledScalings += numSteps

        if (self.s()._scheduledScalings * numSteps < 0):
            self.s()._scheduledScalings = numSteps

        #QTimeLine *const animation{ new QTimeLine{ 350, this } };
        animation = QTimeLine(350, self.impl())
        animation.setUpdateInterval(20)

        #real = real()

        #self.impl().connect(animation, QTimeLine.valueChanged, self.wheelEvent_onFactor)
        animation.valueChanged.connect(self.wheelEvent_onFactor)
        #self.impl().connect(animation, QTimeLine.finished, self.wheelEvent_onFinish)
        animation.finished.connect(self.wheelEvent_onFinish)

        animation.start()       

    def doModuleView_Open(self):#@s:PAckageView::open
        tiv = self.s()._inputsView
        x = tiv.prop(prop.PositionX)
        y = tiv.prop(prop.PositionY)
        tii =  tiv.impl()
        tii.setPos(x,y)
        tov = self.s()._outputsView
        tov.impl().setPos(tov.prop(prop.PositionX),tov.prop(prop.PositionY))


        #Registry &registry{ /*Registry::get()*/m_editor->RegistryGet() };
        '''
        auto const &elements = m_package->elements();
        size_t const SIZE{ elements.size() };
        for (size_t i = 1; i < SIZE; ++i) {
        auto const element = elements[i];
        auto const node = registry.createNode(element->hash());
        auto const nodeName = QString::fromStdString(registry.elementName(element->hash()));
        auto const nodeIcon = QString::fromStdString(registry.elementIcon(element->hash()));
        auto const nodePath = QString::fromLocal8Bit(element->type());

        element->setNode(node);
        m_nodes[element->id()] = node;

        element->isIconified() ? node->iconify() : node->expand();
        node->setPackageView(this);
        node->setPropertiesTable(m_properties);
        node->setName(nodeName);
        node->setPath(nodePath);
        node->setIcon(nodeIcon);
        node->setPos(element->position().x, element->position().y);
        node->setElement(element);
        m_scene->addItem(node);

        m_nodesModel->add(node);
        m_nodesProxyModel->sort(0);
        }

        auto const &connections = m_package->connections();
        for (auto const &connection : connections) {
        auto const SOURCE_ID = connection.from_id;
        auto const SOURCE_SOCKET = connection.from_socket;
        auto const SOURCE_IOFLAGS = connection.from_flags;
        auto const TARGET_ID = connection.to_id;
        auto const TARGET_SOCKET = connection.to_socket;
        auto const TARGET_IOFLAGS = connection.to_flags;

        auto const source = SOURCE_ID != 0 ? getNode(SOURCE_ID) : m_packageNode->inputsNode();
        auto const target = TARGET_ID != 0 ? getNode(TARGET_ID) : m_packageNode->outputsNode();
        auto const sourceIos = SOURCE_IOFLAGS == 2 /*&& SOURCE_ID != 0*/ ? source->outputs():source->inputs();
        if (SOURCE_SOCKET>=sourceIos.size()){
            spaghetti::log::info("Przekroczenie dlugości wektora source dla: {}",source->name().toUtf8().constData());
        }
        auto const sourceSocket =  sourceIos[SOURCE_SOCKET];
        auto const targetIos = TARGET_IOFLAGS == 2 /*&& TARGET_ID != 0*/ ? target->outputs() : target->inputs();
        if (TARGET_SOCKET>=targetIos.size()){
            spaghetti::log::info("Przekroczenie dlugości wektora target dla:{} ",target->name().toUtf8().constData());
        }
        auto const targetSocket =  targetIos[TARGET_SOCKET];
        sourceSocket->connect(targetSocket);
        }
        '''

    def doModuleView_UpdateGrid(self, scale):
        newDensity = GridDensity.LARGE if scale >= 0.85 else GridDensity.SMALL 
        self.s()._gridDensity = newDensity

    def doModuleView_DrawBackground(self, painter, rect):
        penNormal = qtg.QPen(QColor(156, 156, 156, 32))
        penAxis = qtg.QPen(QColor(156, 156, 156, 128)) 

        #qreal const LEFT{ a_rect.left() };
        LEFT = rect.left()
        #qreal const RIGHT{ a_rect.right() };
        RIGHT = rect.right()
        #qreal const TOP{ a_rect.top() };
        TOP = rect.top()
        #qreal const BOTTOM{ a_rect.bottom() };
        BOTTOM = rect.bottom()

        #qreal const GRID_DENSITY{ (m_gridDensity == GridDensity::eSmall ? 100.0 : 10.0) };
        GRID_DENSITY = 100.0 if self.s()._gridDensity == GridDensity.SMALL else 10.0

        #qreal const START_X{ std::round(LEFT / GRID_DENSITY) * GRID_DENSITY };
        START_X = round(LEFT / GRID_DENSITY) * GRID_DENSITY
        #qreal const START_Y{ std::round(TOP / GRID_DENSITY) * GRID_DENSITY };
        START_Y = round(TOP / GRID_DENSITY) * GRID_DENSITY

        if self.s()._gridDensity == GridDensity.SMALL:
            penAxis.setWidth(2)
            penNormal.setWidth(2)
        
        
        #for x in range(START_X,RIGHT,GRID_DENSITY):
        x = START_X
        while x<RIGHT:
            PEN = penAxis if (x >= -0.1 and x <= 0.1) else penNormal
            painter.setPen(PEN)
            painter.drawLine(qtc.QPointF(x, TOP), qtc.QPointF(x, BOTTOM))
            x+=GRID_DENSITY

        #for y in range(START_Y,BOTTOM,GRID_DENSITY):
        y=START_Y
        while y<BOTTOM:
            PEN = penAxis if (y >= -0.1 and y <= 0.1) else penNormal 
            painter.setPen(PEN)
            painter.drawLine(qtc.QPointF(LEFT, y), qtc.QPointF(RIGHT, y))
            y+=GRID_DENSITY

    def doApp_Init(self):
        result = qtw.QApplication(sys.argv) 
        app = result
        app.setStyle(QtWidgets.QStyleFactory.create("Fusion"));

        darkPalette=QPalette()
        c1 = QColor(55, 55, 55);
        c2 = QColor(25, 25, 25);
        c3 = QColor(45, 130, 220);
        darkPalette.setColor(QPalette.Window, c1);
        darkPalette.setColor(QPalette.WindowText, Qt.white);
        darkPalette.setColor(QPalette.Base, c2);
        darkPalette.setColor(QPalette.AlternateBase, c1);
        darkPalette.setColor(QPalette.ToolTipBase, Qt.white);
        darkPalette.setColor(QPalette.ToolTipText, Qt.white);
        darkPalette.setColor(QPalette.Text, Qt.white);
        darkPalette.setColor(QPalette.Button, c1);
        darkPalette.setColor(QPalette.ButtonText, Qt.white);
        darkPalette.setColor(QPalette.BrightText, Qt.red);
        darkPalette.setColor(QPalette.Link, c3);
        darkPalette.setColor(QPalette.Highlight, c3);
        darkPalette.setColor(QPalette.HighlightedText, Qt.white);
        app.setPalette(darkPalette);
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2b8bdb; border: 1px solid white; }");

        '''
        palette = app.palette()
        palette.setColor(QPalette.Window, QColor(239, 240, 241))
        palette.setColor(QPalette.WindowText, QColor(49, 54, 59))
        palette.setColor(QPalette.Base, QColor(252, 252, 252))
        palette.setColor(QPalette.AlternateBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipText, QColor(49, 54, 59))
        palette.setColor(QPalette.Text, QColor(49, 54, 59))
        palette.setColor(QPalette.Button, QColor(239, 240, 241))
        palette.setColor(QPalette.ButtonText, QColor(49, 54, 59))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(41, 128, 185))
        # palette.setColor(QPalette.Highlight, QColor(126, 71, 130))
        # palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Light, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Shadow, QColor(234, 234, 234))
        app.setPalette(palette)
        '''


        return result

    def doMainWindow_Init(self):
        result = qtw.QMainWindow() 
        if 'title' in self._self._kwargs:
            result.setWindowTitle(self._self._kwargs['title'])

        #result = qtw.QFrame()
        result.resize(1600, 980)
        '''
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
        result.setSizePolicy(sizePolicy)
        '''
        showEvent = getattr(self._self, "showEvent", None)
        if callable(showEvent):
            result.showEvent = showEvent
        return result

    def doMainWindow_Show(self):
        result = self.impl().show()  
        return result 


    def doMenu_Init(self):        
        if self._impl == None:    
            self._self._qtMenu = qtw.QMenu(self._parent.implObject())
            self.s()._menu = self._self._qtMenu
            pass
        else:
            self.s()._menu = self._impl
        return self._self._menu         

    def doMenu_AddSeparator(self):
        result = self._self.implObject().addSeparator() 
        return result

    def doMenu_addAction(self, label,id,helpStr,onClick):
        if (label == None and consts.ID_EXIT == id):
            exitAct = QAction(QIcon('exit.png'), '&Exit', self._self.implObject())
            exitAct.setShortcut('Ctrl+Q')
            exitAct.setStatusTip('Exit application')
            exitAct.triggered.connect(qApp.quit)
            result = self._self.implObject().addAction(exitAct)
        else:
            result = self._self.implObject().addAction(label, onClick)
            if onClick != None:
                result.triggered.connect(onClick)
            #!TODO!result.onClick = onClick
        return result 

    def doMenuBar_Init(self):
        return self.pimpl().menuBar()


    def doMenuBar_AddMenu(self,menuTitle):
        return  self.impl().addMenu(menuTitle)
        '''
        else:           
            result = Menu(self._parent)
            self._wxMenuBar.Append(result.implObject(),menuTitle)
            return result  
            '''

    def doMdiPanel_Init(self):      
        result = qtw.QMdiArea(self._parent.impl())
        return result

    def doTabPanel_Init(self):      
        result = qtw.QTabWidget(self._parent.impl())
        '''
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
        result.setSizePolicy(sizePolicy)
        '''
        #result.setMinimumSize(QtCore.QSize(2080, 1630))
        return result

    def doTabPanel_AddTab(self, obj, title):
        return self.impl().addTab(obj.impl(),title)

    def doTabPanel_CurrentIndex(self):
        return self.impl().currentIndex()
    
    def doTab_Init(self):      
        result = qtw.QWidget()
        self._parent.impl().addTab(result,"test")
        return result

    def doLayout_Init(self):
        orient = self.s()._kwargs['orient'] if 'orient' in self.s()._kwargs else None
        result = qtw.QVBoxLayout() if orient == orientation.VERTICAL else qtw.QHBoxLayout()
        return result
        '''
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
        '''

    def doLayout_AddElement(self, element):
        result = self.impl().addWidget(element.impl()) 
        return result 

    def doLayout_Add(self,label, sizerFlags):
        result = self.impl().addWidget(label.inpl())  
        return result       
        
    def doElement_Init(self):
        result = qtw.QWidget(self.pimpl())
        return result

    def doElement_Resize(self,w,h):
        result = self.impl().resize(w,h)
        return result

    def doElement_SizePolicy(self):
        result = self.impl().sizePolicy()
        return result

    def doElement_SetSizePolicy(self, sizePolicy):
        result = self.impl().setSizePolicy(sizePolicy)
        return result
         
    def doPanel_Init(self):
        result = qtw.QFrame(self.pimpl())
        return result

    def doLabel_Init(self):
        result = qtw.QLabel(self.pimpl())
        if 'label' in self.s()._kwargs:
            result.setText(self.s()._kwargs['label'])
        return result

    def doLabel_GetFont(self):
        result = self.impl.font()
        return result

    def doLabel_SetFont(self, font):
        result = self.impl().setFont(font)
        return result 
        



