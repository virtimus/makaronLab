
# PYQT

import sys

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt, QPoint, QTimeLine
from PyQt5.QtGui import QBrush, QColor, QIcon, QPainter, QPalette
from PyQt5.QtWidgets import (QAction, QApplication, QGraphicsItem,
                             QGraphicsScene, QGraphicsView, qApp)

from ... import consts, prop
from ...moduletype import ModuleType


class WqGraphicsItem(qtw.QGraphicsItem):
    def __init__(self,parent):
        super(WqGraphicsItem,self).__init__(parent)

class WqDriver:
    def __init__(self,_self,parent,impl):
        #self._wqImpl = wqImpl
        self._object = impl
        self._impl = impl
        self._parent = parent
        self._self = _self

    def s(self):
        return self._self
    
    def impl(self):
        return self._impl

    def pimpl(self):
        return self._parent.impl()
    
    def p(self):
        return self._parent


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
            else:
                result = WqGraphicsItem(self.pimpl())
        return result; 

    def doModuleView_AfterInit(self):
        if self.s().isRoot():#@s:PackageView::PackageView
            self.s()._inputsView  = self.s().addModuleView('moduleInputs', type=ModuleType.INPUTS)
            self.s()._outputsView = self.s().addModuleView('moduleOutputs', type=ModuleType.OUTPUTS)
            #vec2d m_inputsPosition{ -400.0, 0.0 };
            self.s()._inputsView.setProp(prop.PositionX,-400.0)
            self.s()._inputsView.setProp(prop.PositionY,0.0)
            self.s()._outputsView.setProp(prop.PositionX,400.0)
            self.s()._outputsView.setProp(prop.PositionY,0.0)

            tImpl = self.impl()
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
        else:
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

    def doLayout_AddElement(self, element):
        result = self.impl().addWidget(element.impl())           
        
         