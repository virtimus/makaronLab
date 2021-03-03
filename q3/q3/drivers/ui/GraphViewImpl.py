import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

from enum import Enum

from ... import consts, prop, orientation, direction, colors, strutils
from ...q3vector import Q3Vector

from . import stypes

from ...Timer import Timer

from .ModuleViewImpl import ModuleViewImpl, PropertiesBuilder

from .PackageViewImpl import PackageViewImpl

class GridDensity(Enum):
    LARGE = 1
    SMALL = 2

#using Nodes = QHash<size_t, Node *>;
Nodes = Q3Vector(ModuleViewImpl)

#package_view
class GraphViewImpl(qtw.QGraphicsView):
    #explicit PackageView(Editor *const a_editor, Package *const a_package);
    # #// package created internally in constructor
    def __init__(self,scene,parent, editorFrame , package):
        super(GraphViewImpl,self).__init__(scene, parent)
        self._element = None
        self._gridDensity = None
        
        self._selectedModule = None 
        self._scheduledScalings = None
        self._properties = editorFrame._propertiesTable
        self.m_properties = editorFrame._propertiesTable

        self._editorFrame = editorFrame
        self.m_editor = editorFrame

        self.m_package = package
        self._inputsModImpl = None
        self.m_inputs = None 
        self._outputsModImpl = None
        self.m_outputs = None #initialised in open

        self.m_scene = scene
        self.m_timer = qtc.QTimer()
        self.m_nodes = Q3Vector(ModuleViewImpl)

        self.m_dragNode = None
        self.m_selectedNode = None
        self.m_dragLink = None
        self.m_packageNode = None

        self.m_snapToGrid = None
        self.m_standalone = None
        self._selectedNode = None

    def __afterInit__(self, q3d):

        self.m_standalone = self.m_package.package() == None
        if (self.m_standalone):
            self.m_packageNode = PackageViewImpl(None,_self=self._self) #static_cast<nodes::Package *>(/*Registry::get()*/m_editor->RegistryGet().createNode("logic/package"));
            self.m_package.setNode(self.m_packageNode)
        else:
            self.m_packageNode = self.m_package.node() #->node<nodes::Package>();
        #Q_ASSERT(m_package->node<Node*>());
        assert self.m_package.node() != None, 'Problem with package/node'

        self.setViewportUpdateMode(qtw.QGraphicsView.FullViewportUpdate)
        self.setRenderHints(qtg.QPainter.Antialiasing | qtg.QPainter.TextAntialiasing | qtg.QPainter.HighQualityAntialiasing |
                 qtg.QPainter.SmoothPixmapTransform)
        self.setDragMode(qtw.QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOn)
        self.setResizeAnchor(qtw.QGraphicsView.NoAnchor)
        self.setTransformationAnchor(qtw.QGraphicsView.AnchorViewCenter)
        self.setOptimizationFlags(qtw.QGraphicsView.DontSavePainterState | qtw.QGraphicsView.DontAdjustForAntialiasing)
        self.setObjectName("PackageView")

        #self.m_nodesProxyModel->setSourceModel(m_nodesModel);
        self.m_scene.setItemIndexMethod(qtw.QGraphicsScene.NoIndex)
        self.m_scene.setSceneRect(-32000, -32000, 64000, 64000)
        self.m_scene.setObjectName("PackageViewScene")
        brush = colors.C.GRAPH_BACKGROUND.qColor() 
        self.m_scene.setBackgroundBrush(brush)

        self.m_inputs = self.s()._inputsView.impl()
        self.m_outputs = self.s()._outputsView.impl()

        self.m_inputs.setPropertiesTable(self.m_properties)
        self.m_outputs.setPropertiesTable(self.m_properties)

        self.m_packageNode.setPropertiesTable(self.m_properties)

        self.setAcceptDrops(True)
        #using NodeType = Node::Type;
        #m_inputs->setType(NodeType::eInputs);
        self.m_inputs.setPos(self.m_package.inputsPosition().x(), self.m_package.inputsPosition().y())
        self.m_inputs.setElement(self.m_package)
        self.m_inputs.setIcon(":/logic/inputs.png")
        self.m_inputs.setPackageView(self)
        self.m_inputs.collapse()
        #self.m_outputs.setType(NodeType::eOutputs);
        self.m_outputs.setPos(self.m_package.outputsPosition().x(), self.m_package.outputsPosition().y())
        self.m_outputs.setElement(self.m_package)
        self.m_outputs.setIcon(":/logic/outputs.png")
        self.m_outputs.setPackageView(self)
        self.m_outputs.collapse()

        self.m_packageNode.setInputsNode(self.m_inputs)
        self.m_packageNode.setOutputsNode(self.m_outputs)
        self.m_packageNode.setElement(self.m_package)

        if (strutils.isBlank(self.m_package.name())):
            #auto &registry = /*Registry::get()*/m_editor->RegistryGet();
            #m_package->setName(registry.elementName("logic/package"));
            self.m_package.setName('!TODO!')
  
        self.m_scene.addItem(self.m_inputs)
        self.m_scene.addItem(self.m_outputs)
        #//m_timer.setInterval(1000 / 60);
        #//m_timer.setInterval(5000);
        self.m_timer.setInterval(1)

        def mTimerSceneAdvance():
            self.m_scene.advance()
        
        #connect(&m_timer, &QTimer::timeout, [this]() { m_scene->advance(); });
        self.m_timer.timeout.connect(mTimerSceneAdvance)
        self.m_timer.start()
        if (self.m_standalone):
            self.m_package.startDispatchThread()


    def __del__(self):
        super(GraphViewImpl, self).__del__()
        self.m_timer.stop()
        if (self.m_standalone):
            self.m_package.quitDispatchThread()
            del self.m_package


    def s(self):
        return self._self 

    #@deprecated - can be misleading mdlv/moduleView
    #def mdl(self):
    #    return self._self

    def mdlv(self):
        return self._self

    def module(self):
        return self._self.module() 

    def dragLink(self):
        return self.m_dragLink

    def setDragLink(self, link): #LinkItem *a_
        self.m_dragLink = link
        
    def acceptDragLink(self):
        self.m_dragLink = None 


    def editor(self):
        return self.m_editor

    def package(self):
        return self.m_package

    def snapToGrid(self):
        return self.m_snapToGrid

    def setFilename(self, filename):
        self.m_filename = filename
    
    def filename(self):
        return self.m_filename

    def nodes(self):
        return self.m_nodes

    def getNode(self, lid):
        return self.m_nodes.byLid(lid)

    #NodesListModel *model() const { return m_nodesModel; }
    #QSortFilterProxyModel *proxyModel() const { return m_nodesProxyModel; }

 
    # ------ HDR-END ------

    #def inputs(self):
    #    return self._inputsModImpl 
    
    #def outputs(self):
    #    return self._outputsModImpl 



    def setElement(self, el):
        if (self._element != None):
            return
        self._element = el       


    def open(self):#@s:PAckageView::open
        tiv = self.s()._inputsView
        x = tiv.prop(prop.PositionX)
        y = tiv.prop(prop.PositionY)
        tii =  tiv.impl()
        tii.setPos(x,y)
        tov = self.s()._outputsView
        tov.impl().setPos(tov.prop(prop.PositionX),tov.prop(prop.PositionY))

        self._inputsModImpl = tii 
        self.m_inputs = tii
        self._outputsModImpl = tov.impl()
        self.m_outputs = tov.impl() 

        self.m_inputs.setPropertiesTable(self._properties)
        self.m_outputs.setPropertiesTable(self._properties)

    def dragEnterEvent(self, event): #QDragEnterEvent *a_
        mimeData = event.mimeData()
        #//  mimeData->setData("metadata/is_package", IS_PACKAGE);
        #//  mimeData->setData("metadata/name", NAME);
        #//  mimeData->setData("metadata/icon", ICON);
        #//  mimeData->setData("metadata/filename", FILE);

        if (mimeData.hasFormat("metadata/name") and mimeData.hasFormat("metadata/icon")):
            isPackage = mimeData.data("metadata/is_package") == "true"
            pathString = 'logic/package' if isPackage else mimeData.text()
            name = mimeData.data("metadata/name")
            icon = mimeData.data("metadata/icon")
            file = mimeData.data("metadata/filename")
            stringData = pathString.toLatin1()
            path = stringData.data()
            DROP_POSITION = self.mapToScene(event.pos())
            
            #Registry &registry{ /*Registry::get()*/m_editor->RegistryGet() };

            assert(self.m_dragNode == None)
            
            #m_dragNode = registry.createNode(path);
            self.m_dragNode = self.module().newModule(name,impl=path).view().impl()

            self.m_dragNode.setPackageView(self)
            self.m_dragNode.setPropertiesTable(self.m_properties)
            self.m_dragNode.setName(name)
            self.m_dragNode.setPath(path)
            self.m_dragNode.setIcon(icon)
            self.m_dragNode.setPos(DROP_POSITION)
            self.m_scene.addItem(self.m_dragNode)
            self.m_dragNode.calculateBoundingRect()
            event.accept()
        else:
            #QGraphicsView::dragEnterEvent(a_event);
            super().dragEnterEvent(event)  

    def dragLeaveEvent(self, event): #QDragLeaveEvent *
        if (self.m_dragNode != None):
            self.m_scene.removeItem(self.m_dragNode)
            del self.m_dragNode
            self.m_dragNode = None

    def dragMoveEvent(self, event): #QDragMoveEvent *a_
        dropPosition = self.mapToScene(event.pos())
        if (self.m_dragNode != None):
            self.m_dragNode.setPos(dropPosition)
        elif (self.m_dragLink != None):
            #QGraphicsView::dragMoveEvent(a_event);
            super().dragMoveEvent(event)
            self.m_dragLink.setTo(self.mapToScene(event.pos()))


    def dropEvent(self, event): #QDropEvent *a_
        mimeData = event.mimeData()
        if (mimeData.hasFormat("text/uri-list")):
            #QString const FILENAME{ mimeData->text().trimmed() };
            FILENAME = strutils.trim(mimeData.text())
            #STRIPPED = FILENAME.right(FILENAME.size() - static_cast<int>(strlen("file://"))) };
            STRIPPED = strutils.replace(FILENAME,"file://",'')
            # emit requestOpenFile(STRIPPED);
            event.accept()
        elif (mimeData.hasFormat("metadata/name") and mimeData.hasFormat("metadata/icon")):
            self.m_package.pauseDispatchThread()
            isPackage = mimeData.data("metadata/is_package") == "true"
            file = mimeData.data("metadata/filename")
            pathString = event.mimeData().text()
            stringData = pathString.toLatin1()
            path = "logic/package" if isPackage else  stringData.data() 
            element = self.m_package.add(path)
            element.setNode(self.m_dragNode)
            if (strutils.isBlank(element.name())):
                element.setName(self.m_dragNode.name())
            if (isPackage):
                package = element #static_cast<Package *>(element);
                #//std:string strFile(QString{ file }.toStdString());
                package.open(file)
                package.setPackagePath(file)
                #//m_dragNode->setPackagePath(file);
            self.m_dragNode.setElement(element)
            self.m_dragNode.collapse()

            self.m_nodes.append(element.id(),self.m_dragNode)
            #self.m_nodesModel.add(self.m_dragNode);
            #self.m_nodesProxyModel->sort(0);
            self.m_dragNode = None
            self.m_package.resumeDispatchThread()
        
        #QGraphicsView::dropEvent(a_event);
        super().dropEvent(event)


    def keyPressEvent(self, event): #QKeyEvent *a_
        self.m_snapToGrid = event.modifiers() & qtc.Qt.ShiftModifier

    def keyReleaseEvent(self, event): #QKeyEvent *a_
        self.m_snapToGrid = event.modifiers() & qtc.Qt.ShiftModifier
        if event.key() == qtc.Qt.Key_R:
            self.centerOn(0.0, 0.0)
            self.resetMatrix()
            self.updateGrid(self.matrix().m11())
        #default: break;
        #selected = self.m_scene.selectedItems()
        #for item in selected:
        #    if (item.type() == NODE_TYPE):
        #        pass

    #@s:PackageView::wheelEvent(QWheelEvent *a_event)
    def wheelEvent(self, event):
        #self.q3D().doModuleView_wheelEvent(event)
    #def doModuleView_wheelEvent(self,event): 
        numDegrees = event.angleDelta().y()/8 #?pixelDelta
        numSteps = numDegrees/15

        if (self._scheduledScalings == None):
            self._scheduledScalings = 0

        self._scheduledScalings += numSteps

        if (self._scheduledScalings * numSteps < 0):
            self._scheduledScalings = numSteps

        #QTimeLine *const animation{ new QTimeLine{ 350, this } };
        animation = qtc.QTimeLine(350, self)
        animation.setUpdateInterval(20)

        #real = real()

        #self.impl().connect(animation, QTimeLine.valueChanged, self.wheelEvent_onFactor)
        animation.valueChanged.connect(self.wheelEvent_onFactor)
        #self.impl().connect(animation, QTimeLine.finished, self.wheelEvent_onFinish)
        animation.finished.connect(self.wheelEvent_onFinish)

        animation.start()

    def wheelEvent_onFactor(self):       
        factor = 1.0 + self._scheduledScalings / 300.0
        temp = self.transform()
        temp.scale(factor, factor)
        if (temp.m11() >= 0.2 and temp.m11() <= 4.0):
            self.scale(factor, factor)

    def wheelEvent_onFinish(self):
        if (self._scheduledScalings > 0):
            self._scheduledScalings-=1
        else:
            self._scheduledScalings+=1
        if (self.sender()):
            self.sender().deleteLater()
        REAL_SCALE = self.transform().m11()
        self.updateGrid(REAL_SCALE)  



    #@s:PackageView::drawBackground(QPainter *a_painter, QRectF const &a_rect)
    def drawBackground(self, painter, rect):

        penNormal = qtg.QPen(colors.PEN_NORMAL)
        penAxis = qtg.QPen(colors.PEN_AXIS) 

        #qreal const LEFT{ a_rect.left() };
        LEFT = rect.left()
        #qreal const RIGHT{ a_rect.right() };
        RIGHT = rect.right()
        #qreal const TOP{ a_rect.top() };
        TOP = rect.top()
        #qreal const BOTTOM{ a_rect.bottom() };
        BOTTOM = rect.bottom()

        #qreal const GRID_DENSITY{ (m_gridDensity == GridDensity::eSmall ? 100.0 : 10.0) };
        GRID_DENSITY = 100.0 if self._gridDensity == GridDensity.SMALL else 10.0

        #qreal const START_X{ std::round(LEFT / GRID_DENSITY) * GRID_DENSITY };
        START_X = round(LEFT / GRID_DENSITY) * GRID_DENSITY
        #qreal const START_Y{ std::round(TOP / GRID_DENSITY) * GRID_DENSITY };
        START_Y = round(TOP / GRID_DENSITY) * GRID_DENSITY

        if self._gridDensity == GridDensity.SMALL:
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

    def cancelDragLink(self):
        #delete self._dragLink;
        self.m_dragLink = None

    def canClose(self):
        return True

    def center(self):
        self.centerOn(0.0, 0.0)

    def showProperties(self):
        self._properties.clear()
        self._properties.setColumnCount(2)
        #self._properties.setSpan(0, 0, 1, 2)
        self._properties.setHorizontalHeaderLabels("Property;Value".split(";"))
        if self._selectedNode != None:
            self._selectedNode.showProperties()
        self._properties.horizontalHeader().setStretchLastSection(True)

    def deleteElement(self): #@todo should be changed to ed->model command and->event->remove->view/impl/model roundtrip
        selectedItems = self.m_scene.selectedItems()

        self.m_timer.stop()
        while (self.m_timer.isActive()):
            Timer.sleep(0)
        for item in selectedItems:
            if item.type() == stypes.NODE_TYPE:
                node = item #reinterpret_cast<Node *>(item);
                ID = node.element().id()
                self.m_nodes.removeByLid(ID)
                #self.m_nodesModel.remove(node)
                #m_nodesProxyModel->sort(0);
                if (node == self.m_selectedNode):
                    self.setSelectedNode(None)
                del node
            elif item.type() == stypes.LINK_TYPE:
                link = item #reinterpret_cast<LinkItem *>(item);
                link.disconnect()
                del link
                #model

        self.m_timer.start()
        self.showProperties()

    def updateName(self, node):
        #self.m_nodesModel.update(node);
        #self.m_nodesProxyModel.sort(0);
        self.m_nodes.rebuildIndexes()

    def selectItem(self, index): #QModelIndex const &a
        #INDEX = m_nodesProxyModel->mapToSource(a_index);
        #auto const node = m_nodesModel->nodeFor(INDEX);
        node = self.m_nodes.byLid(index)
        assert(node != None)
        
        self.scene().clearSelection()

        node.setSelected(True)
        self.setSelectedNode(node)
        self.showProperties()

        self.centerOn(node)


    def setSelectedNode(self, node): #Node *const 
        if (node == None):
            self._selectedNode = self.m_packageNode #._self.impl() #m_packageNode
        else:
            self._selectedNode = node
        if self._selectedNode != None:
            self._selectedNode.setPropertiesTable(self._properties)
        #self._selectedNode._properties = self._properties
        #self._selectedNode._propertiesBuilder = self._propertiesBuilder



    #@s:PackageView::updateGrid(qreal const a_scale)
    def updateGrid(self, scale):
        newDensity = GridDensity.LARGE if scale >= 0.85 else GridDensity.SMALL 
        self._gridDensity = newDensity

    def setSelected(self, item):
        pass