import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

import sip

from ...nodeiotype import NodeIoType

from ...q3vector import Q3Vector

from ... import consts, prop, orientation, direction, colors

from ...ModuleFactory import ModuleType,ModuleImplBase

from .IoNodeView import IoNodeView

from ...valuetype import ValueType
from ...ionodeflags import IoNodeFlags

from ... import console

from . import stypes

from enum import Enum

from ...EventSignal import EventProps

class Q3iShowMode(Enum):
    COLLAPSED = 1
    EXPANDED = 2

class PropertiesBuilder:
    pass

class Property:
    def __init__(self, name, parent:PropertiesBuilder, propObj, lWidget, rWidget):
        self._parent = parent
        self._obj = None
        #self._obj._propRef = self
        self._name = name
        self._lWidget = None
        self._rWidget = None
        self.update(propObj, lWidget, rWidget)
    
    def name(self):
        return self._name

    def update(self, propObj, lWidget, rWidget):
        tPropRef = self if propObj !=None else None
        if propObj != None:
            self._obj = propObj
        self._obj._uiPropRef = tPropRef
        objView = getattr(self._obj,'view',None)
        if objView != None:
            if callable(objView):
                objView = objView()
            objView._uiPropRef = tPropRef
        self._lWidget = lWidget
        self._rWidget = rWidget
        
    '''
    def lWidget(self):
        return self._lWidget
    
    def rWidget(self):
        return self._rWidget
    '''

    def select(self):
        table = self._parent.table()
        if table != None and not sip.isdeleted(self._lWidget):
            ind = table.indexFromItem(self._lWidget)
            #itemL.setSelected(True)
            #self._lWidget.setText('selected')
            table.selectionModel().setCurrentIndex( ind, qtc.QItemSelectionModel.ClearAndSelect )

    def clear(self):
        self.update(None,None,None)



class PropertiesBuilder:
    def __init__(self, parent, table):
        self._table = table
        self._props = Q3Vector(Property)

    def props(self) -> Q3Vector(Property):
        return self._props

    def table(self):
        return self._table
    
    def clear(self):
        for p in self.props().values():
            p.clear()
        self.props().removeAll()

    def addProperty(self,**kwargs):

        propName = console.handleArg(self, 'name',kwargs=kwargs,
            desc = 'Name of property to add',
            required = True
            )

        propObj = console.handleArg(self, 'obj',kwargs=kwargs,
            desc = 'Owner of property to add',
            required = True
            )

        #propId = type(propObj).__name__+'.'+str(propObj.id())+'.'+propName

        cellWidget = console.handleArg(self, 'widget',kwargs=kwargs,
            desc = 'Property widget',
            default = None 
            )
        if cellWidget == None:
            propDesc = console.handleArg(self, 'propDesc',kwargs=kwargs,
                desc = 'Property meta-definition or property widget',
                required = True
                )
            cellWidget = self._buildWidgetFromPropertyDesc(propName, propDesc)

        assert cellWidget != None, f'CellWidget for property {propName} is None' 
        
        #lWidget = kwargs['lWidget'] if 'lWidget' in kwargs else None
        lWidget = console.handleArg(self, 'lWidget',kwargs=kwargs,
            desc = 'Additional widget'
            )

        isSelected = console.handleArg(self, 'selected',kwargs=kwargs,
            desc = 'Should be selected'
            )

        row = self._table.rowCount()
        self._table.insertRow(row)


            

        if (lWidget == None):
            lWidget = qtw.QTableWidgetItem(propName) 
            lWidget.setFlags(lWidget.flags() & ~qtc.Qt.ItemIsEditable)
            self._table.setItem(row, 0, lWidget)
            if cellWidget.toolTip()!=None: #share toolTip with widget
                lWidget.setToolTip(cellWidget.toolTip())
            if (isSelected or True):
                ind = self._table.indexFromItem(lWidget)
                #itemL.setSelected(True)
                self._table.selectionModel().setCurrentIndex( ind, qtc.QItemSelectionModel.ClearAndSelect )
        else:
            self._table.setItem(row, 0, lWidget)
        if isinstance(cellWidget,qtw.QTableWidgetItem):
            self._table.setItem(row, 0, cellWidget)
        else:
            self._table.setCellWidget(row, 1, cellWidget) 
        #if (isSelected or True):
        #    self._table.selectionModel().setCurrentIndex( row, qtc.QItemSelectionModel.ClearAndSelect )
        #prop = self.props().byLid(propId)
        #if prop == None:
        self.props().append(self.props().nextId(),Property(propName,self,propObj, lWidget,cellWidget))
        #else:
        #    prop.update(propObj, lWidget,cellWidget)

    def _buildWidgetFromPropertyDesc(self,propName,propDesc):
        class propType(Enum):
            LineEdit = 1
            ComboBox = 2

        result=None
        domainValues = console.handleArg(self,'domainValues',
            kwargs = propDesc,
            desc = 'A set of possible values (value domain)'
            )
        defaultValue = console.handleArg(self,'default',
            kwargs = propDesc,
            desc = 'Default/start value of property',
            domainValues = domainValues
            )
        onChangedHandler = console.handleArg(self,'onChange',
            kwargs = propDesc,
            desc = 'onChanged handler method'
            )
        desc = console.handleArg(self,'desc',
            kwargs = propDesc,
            desc = 'Description of property'
            )
        pType = propType.LineEdit
        if domainValues != None and len(domainValues)>0:
            pType = propType.ComboBox
        cProp = None
        if pType == propType.ComboBox:    
            cProp = qtw.QComboBox()
            for k in domainValues:
                label = domainValues[k]
                cProp.addItem(label, k)
            INDEX = cProp.findData(defaultValue)
            cProp.setCurrentIndex(INDEX)
            #self._properties.setCellWidget(row, 1, comboBox);
            def onActivated(index):
                currVal = cProp.itemData(index)
                if onChangedHandler!=None:
                    onChangedHandler(currVal)
            cProp.activated.connect(onActivated)
        else:
            cProp = qtw.QLineEdit(defaultValue)
            if desc != None:
                cProp.setToolTip(desc)
            #pathEdit.setPlaceholderText('<path>')
            if onChangedHandler!=None:
                cProp.textChanged.connect(onChangedHandler)
        return cProp
        #self.addProperty(
        #    name=name,
        #    widget = cProp        
        #    )  

SOCKET_SIZE = IoNodeView.SIZE
ROUNDED_SOCKET_SIZE = round((SOCKET_SIZE) / 10.0) * 10.0
ROUNDED_SOCKET_SIZE_2 = ROUNDED_SOCKET_SIZE / 2.0

NODE_TYPE = stypes.NODE_TYPE

#implements nonroot mode of moduleView (spaghetti node)
class ModuleViewImpl(qtw.QGraphicsItem):
    def __init__(self,parent):
        self._self = None # should finally point to ModuleView Object
        self._nameFont = qtg.QFont()
        self._element:ModuleImplBase = None
        self._centralWidget = None #QGraphicsItem
        self._centralWidgetPosition = None  #QPointF
        self._mode = None #Q3iShowMode
        self._icon = qtg.QPixmap()
        self._showName = True
        self._boundingRect = None
        self._rotate = False
        self._invertH = False
        #self._inputs = Q3Vector()
        #self._outputs = Q3Vector()
        self._nodeViews = Q3Vector()
        self._color = colors.MODULE_COLOR
        self._properties = None
        self._propertiesBuilder = None
        self._graphView = None
        self.m_packageView = None
        self._rotation = 0
        super(ModuleViewImpl,self).__init__(parent)
        #self.setContextMenuPolicy(qtc.Qt.ActionsContextMenu)

    def s(self):
        return self._self

    def moduleView(self): #for use by view elements
        return self._self

    #@api
    def mdlv(self) -> 'ModuleView':
        return self._self
    
    #@api
    def mdl(self) -> 'Module':
        return self._self.module()

    #@api
    def events(self):
        return self.mdlv().events()

    #@deprecated->nodeViewsByDir
    def inputs(self):
        #return self._nodeViews.filterBy('direction',direction.LEFT)
        return self.nodeViewsByDir(direction.LEFT)
    
    #@deprecated->nodeViewsByDir
    def outputs(self):
        #return self._nodeViews.filterBy('direction',direction.RIGHT)
        return self.nodeViewsByDir(direction.RIGHT)

    #@api-method
    def nodeViewsByDir(self, dir:direction.Dir):
        return self._nodeViews.filterBy('dir',dir)


    def nodeViews(self):
        return self._nodeViews

    def module(self):
        return self.moduleView().module()

    def ed(self):
        m = self.module()
        gm = m.graphModule()
        return gm.parent()
    
    def console(self):
        return self.ed().console()

    def type(self):
        return NODE_TYPE

    def packageView(self):
        return self.m_packageView

    def setPackageView(self, pv):
        self.m_packageView = pv
        self._graphView = self.m_packageView 

    def setGraphView(self, pv):
        self.m_packageView = pv
        self._graphView = self.m_packageView 
    #----------------------
    def boundingRect(self):
        return self._boundingRect

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

    def pvShowProperties(self):
        self.m_packageView.showProperties()

    def mType(self):
        return self.module().moduleType()

    def setSelected(self, item):
        if (self.m_packageView != None):
            self.m_packageView.setSelectedNode(item)
            self.m_packageView.showProperties()
        

    #QVariant Node::itemChange(QGraphicsItem::GraphicsItemChange a_change, QVariant const &a_value)
    def itemChange(self, change, value):
        #(void)change;
        #(void)value;
        if (change == qtw.QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged):
            lastSelected = None
            selectedItems = self.scene().selectedItems()
            for item in selectedItems:
                if (item.type() == NODE_TYPE):
                    lastSelected = item
            if isinstance(lastSelected,ModuleViewImpl) and lastSelected.mdlv()!=None:
                self.mdlv().setSelectedModule(lastSelected.mdlv().module())
            else:
                self.setSelected(lastSelected)
        elif change == qtw.QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            POSITION = value #.toPointF()
            X = round(POSITION.x() / 10.0) * 10.0 
            Y = round(POSITION.y() / 10.0) * 10.0 
            return qtc.QPointF( X, Y )
        elif change == qtw.QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if (self._element != None):
                POSITION =  value #.toPointF()
                '''
                moduleType = self.module().moduleType()
                if moduleType == ModuleType.INPUTS:
                    package = self._element
                    package.setInputsPosition(POSITION.x(), POSITION.y())
                elif moduleType == ModuleType.OUTPUTS:
                    package = self._element
                    package.setOutputsPosition(POSITION.x(), POSITION.y())
                else: #if moduleType == ModuleType.ATOMIC:#case Type::eElement:
                '''
                #self._element.setPosition(POSITION.x(), POSITION.y())
                self.events().emitItemPositionHasChanged({
                    'position':POSITION,
                    'x':POSITION.x(),
                    'y':POSITION.y(),
                    'elemClassName':type(self._element).__name__,
                    'elementId':self._element.id()
                })
        elif change == qtw.QGraphicsItem.GraphicsItemChange.ItemRotationHasChanged:
            for ioNodeView in self._nodeViews.values():
                ioNodeView.itemChange(qtw.QGraphicsItem.ItemScenePositionHasChanged, None)
            
        return super().itemChange(change, value)






    '''!TODO!

void Node::advance(int a_phase)
{
  if (!a_phase) return;

  updateOutputs();

  refreshCentralWidget();

  update();
}
'''
    def updateRotation(self):
        if (self.isRotate()):
            self._rotation = -90
            self.setRotation(self._rotation)
        else:
            self._rotation = 0
            self.setRotation(self._rotation)
        

    def updateInversion(self):
        self.calculateBoundingRect()

    def elementSet(self): #virtual
        pass

    #void Node::setElement(Element *const a_element)
    def setElement(self, el):
        if (self._element != None):
            return
        

        self._element = el

        self.updateRotation()

        mType = self.mType() 

        #if (mType == ModuleType.ATOMIC):
        #self._element.registerEventHandler(self.handleEvent)
        self._element.events().inputAdded.connect(self.heInputAdded)
        self._element.events().inputRemoved.connect(self.heInputRemoved)
        self._element.events().outputAdded.connect(self.heOutputAdded)
        self._element.events().outputRemoved.connect(self.heOutputRemoved)
        self._element.events().ioNodeAdded.connect(self.heIoNodeAdded)
        self._element.events().ioNodeRemoved.connect(self.heIoNodeRemoved)
        self._element.events().moduleDoubleClicked.connect(self.heModuleDoubleClicked)
        self._element.events().consoleWrite.connect(self.heConsoleWrite)
        self._element.events().nodeConnectionRequest.connect(self.heNodeConnectionRequest)
        self._element.events().itemPositionHasChanged.connect(self.heItemPositionHasChanged)


        INPUTS = self._element.inputs()
        OUTPUTS = self._element.outputs()

        if mType == ModuleType.ATOMIC:
            for inp in INPUTS.values():
                NAME = inp.name()
                #addSocket(direction.LEFT, inp.id(), NAME, INPUTS[i].type, INPUTS[i].sItemType);
                self.addSocket(direction.LEFT, inp.id(), NAME, inp.valueType(), inp.ioType())
            for out in OUTPUTS.values():
                NAME = out.name()
                #addSocket(IOSocketsType::eOutputs, static_cast<uint8_t>(i), NAME, OUTPUTS[i].type,OUTPUTS[i].sItemType);
                self.addSocket(direction.RIGHT,out.id(), NAME, out.valueType(), out.ioType())
            #self._element.setPosition(self.x(), self.y())
            #self._element.collapse(self._mode == Q3iShowMode.COLLAPSED)
            self.setName(self._element.name())
            self.updateOutputs()
        elif mType == ModuleType.IO:
            dir = self.module().prop('dir')
            ios = INPUTS if dir == direction.RIGHT else OUTPUTS
            for inp in ios.values():
                NAME = inp.name()
                self.addSocket(dir, inp.id(), NAME, inp.valueType(),inp.ioType())
        #elif mType == ModuleType.OUTPUTS:
        #    for out in OUTPUTS.values():
        #        NAME = out.name()
        #        self.addSocket(direction.LEFT, out.id(), NAME, out.valueType(),out.ioType())
        self.elementSet()
        self.calculateBoundingRect()

    def setDesc(self, desc):
        self._desc =  desc
        if (self._element != None):
            self._element.setDesc(desc)
        
    def setName(self, name):
        self._name = name
        if (self.m_packageView != None):
            self.m_packageView.updateName(self)

        if (self._element != None):
            self._element.setName(name)
            self.setToolTip(f'{name}{self._element.id()}')
        else:
            self.setToolTip(f'{name}')


    def setIcon(self, icon):
        self._iconPath = icon
        self._icon.load(icon)

    def showName(self):
        self._showName = True
        self.calculateBoundingRect()
    

    def hideName(self):
        self._showName = False
        self.calculateBoundingRect()
        
    def collapse(self):
        if (self._element != None):
            #self._element.collapse(True)
            self._collapsed = True
            if (self._element.hideCWOnCollapse() and self._centralWidget != None):
                self._centralWidget.hide()
        self._mode = Q3iShowMode.COLLAPSED
        for inp in self.inputs().values():
            inp.hideName()
        for out in self.outputs().values():
            out.hideName()
        self.calculateBoundingRect()

    def expand(self):
        if (self._element != None):
            #self._element.collapse(False)
            self._collapsed = False
        
            if (self._element.hideCWOnCollapse() and self._centralWidget != None):
                self._centralWidget.show()
            
        self._mode = Q3iShowMode.EXPANDED

        for inp in self.inputs().values():
            inp.showName()
        
        for out in self.outputs().values():
            out.showName()

        self.calculateBoundingRect()

    #@api
    def switchView(self):
        if self._mode == Q3iShowMode.EXPANDED:
            self.collapse()
        else:
            self.expand()

    def contextMenuEvent(self, event):
        menu = qtw.QMenu()
        quitAction = menu.addAction("Quit")
        quitAction.triggered.connect(self.test)
        selectedAction = menu.exec(event.screenPos())
        #action = menu.exec_(self.mapToGlobal(event.pos()))
        #if action == quitAction:
        #    qApp.quit()

    def test(self):
        print('testttyy')

    def mouseDoubleClickEvent(self, event):
        if event.button() == qtc.Qt.RightButton:
            return
        evProps = EventProps({
            'event': event,
            'moduleId':self.mdl().id()
        })
        self.mdl().events().moduleDoubleClicked.emit(evProps)



    def setPropertiesTable(self, properties): #QTableWidget *const a_properties
        self._properties = properties
        self._propertiesBuilder = PropertiesBuilder(self, self._properties)

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
            nameBackground = colors.C.NAMEBACKGROUND.qColor()
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

    def paintIcon(self, painter):
        HALF_ICON_SIZE = self._icon.size() / 2
        Y = self._centralWidgetPosition.y()
        WIDTH = HALF_ICON_SIZE.width()
        HEIGHT = HALF_ICON_SIZE.height()
        painter.drawPixmap(self._centralWidgetPosition.x(), Y, WIDTH, HEIGHT, self._icon)


    #EOrientation orientation
    '''
    def dir(self):
        dir = direction.RIGHT
        if (self._rotate):
            if (not self._invertH):
                dir = direction.TOP
            else:
                dir = direction.DOWN
        else:
            if (self._invertH):
                dir = direction.LEFT
        return dir
    '''

    def isInvertH(self):
        return self._invertH
    
    def setInvertH(self, invertH:bool):
        if (invertH):
            self._invertH = True
        else:
            self._invertH = False


    def isRotate(self) -> bool:
        return self._rotate;#//EOrientation::eUp == orientation();

    def setRotate(self, rotate):
        #//m_orient = (n)?EOrientation::eUp:EOrientation::eRight;
        if (rotate):
            self._rotate = True
        else:
            self._rotate = False
		#//m_invertH = false;

	#//updateRotation();


    def onPropCurrentRotChanged(self, event):
        state = event
        self.setRotate(state == 2)
        self.updateRotation()

    def onPropCurrentInvChanged(self, event):
        state = event
        self.setInvertH(state == 2)
        self.updateInversion()


    def showOrientationProperties(self):
        self.propertiesInsertTitle('Orientation')
        currentRot = self.isRotate()
        valueRot =  qtw.QCheckBox()
        valueRot.setChecked(currentRot)
        valueRot.stateChanged.connect(self.onPropCurrentRotChanged)

        self._propertiesBuilder.addProperty(
            obj = self._element,
            name='Rotate',
            widget = valueRot        
        )

        currentInv = self.isInvertH()
        valueInv =  qtw.QCheckBox()
        valueInv.setChecked(currentInv)
        valueInv.stateChanged.connect(self.onPropCurrentInvChanged)

        self._propertiesBuilder.addProperty(
            obj = self._element,
            name='InvertH',
            widget = valueInv        
        )

    def showProperties(self):
        self.showCommonProperties()
        self.showOrientationProperties()

        mType = self.mType()
        if mType == ModuleType.ATOMIC:
            self.showIOProperties(direction.LEFT)
            self.showIOProperties(direction.RIGHT)
        elif mType == ModuleType.IO:
            dir = self.module().prop('dir')
            self.showIOProperties(dir)
        #    #self.showIOProperties(direction.LEFT)
        #elif mType == ModuleType.OUTPUTS:
        #    self.showIOProperties(direction.RIGHT)
        self.showCustomProperties()

    def _getInpDir(self):
        dir = direction.LEFT # for input default dir is LEFT but ...       
        if self.mType() == ModuleType.IO: #if it is INPUTS module - direction for input is right
            dir = direction.RIGHT
        return dir

    def heInputAdded(self, event):
        inpId = event.props('inputId')
        inp = self._element.inputs().byId(inpId)
        dir = self._getInpDir()
        self.addSocket(dir, inp.id(), inp.name(), inp.valueType(), inp.ioType())
        self.calculateBoundingRect()

    def heIoNodeAdded(self, event):
        inpId = event.props('nodeId')
        inp = self._element.nodes().byId(inpId)
        #dir = self._getInpDir()
        dir = self._getIoDir(inp.dir())
        self.addSocket(dir, inp.id(), inp.name(), inp.valueType(), inp.ioType())
        self.calculateBoundingRect()
    
    def heInputRemoved(self,event):
        dir = self._getInpDir()
        self.removeSocket(dir)
        self.calculateBoundingRect()

    def heIoNodeRemoved(self,event):
        inpId = event.props('nodeId')
        #inp = self._element.nodes().byId(inpId)
        #dir = self._getInpDir()
        dir = self._getIoDir(event.props('dir'))
        self.removeSocket(dir)
        self.calculateBoundingRect()

    def heModuleDoubleClicked(self,event):
        MODIFIERS = qtw.QApplication.keyboardModifiers()
        if MODIFIERS & qtc.Qt.ControlModifier:
            self.mdlv().showDetailWindow(event=event)
        else:
            self.switchView()

    def heConsoleWrite(self,event):
        text = event.props('text')
        self.console().write(text)

    def isScriptRecordingOn(self):
        return self.module().graphModule().isScriptRecordingOn()

    def recordScript(self, d:dict):
        return self.module().graphModule().recordScript(d)


    def heNodeConnectionRequest(self, event):
        sourceNode = event.props('sourceNode')
        targetNode = event.props('targetNode')
        sourceNode.view().connect(targetNode.view())
        if self.isScriptRecordingOn():
            self.recordScript({
                'recordType':'event',
                'eventName':'nodeConnectionRequest',
                'event':event
            })

    def heItemPositionHasChanged(self, event):
        if self.isScriptRecordingOn():
            self.recordScript({
                'recordType':'event',
                'eventName':'itemPositionHasChanged',
                'event':event
            })



    #def heModuleDoubleClicked2(self,event):
    #    print('dupa')

    def _getIoDir(self,dir:direction.Dir):
        result = dir
        if self.mType() == ModuleType.IO:
            result = dir.oposite()
        return result

    def _getOutDir(self):
        dir = direction.RIGHT # default for output socket
        if self.mType() == ModuleType.IO:
            dir = direction.LEFT
        return dir

    def heOutputAdded(self, event):
        outId = event.props('outputId')
        out = self._element.outputs().byId(outId)
        dir = self._getOutDir()
        self.addSocket(dir, out.id(), out.name(), out.valueType(), out.ioType())
        self.calculateBoundingRect()

    def heOutputRemoved(self, event):
        dir = self._getOutDir()
        self.removeSocket(dir)
        self.calculateBoundingRect()

    def handleEvent(self, event): #Event const &a_
        pass
        '''
        if event.typeS() == 'elementNameChanged':
            pass
        elif event.typeS() == 'ioNameChanged':
            #EVENT = std::get<EventIONameChanged>(a_event.payload);
            #changeIOName(EVENT.input ? IOSocketsType::eInputs : IOSocketsType::eOutputs, EVENT.id,
            #       QString::fromStdString(EVENT.to));
            direct = direction.LEFT if event._isInput else direction.RIGHT
            self.changeIOName(direct, event._lid, event._toName)
            self.calculateBoundingRect()
        elif event.typeS() == 'consoleTrig':
            #auto const &EVENT = std::get<EventConsoleTrig>(a_event.payload);
            #char *cstr = new char[EVENT.text.length() + 1];
            #strcpy(cstr, EVENT.text.c_str());
            #m_packageView->consoleAppend(cstr);
            #break;
            pass
        elif event.typeS() == 'ioTypeChanged':
            pass
        elif event.typeS() == 'inputAdded': 
            
        elif event.typeS() == 'outputAdded': 

        elif event.typeS() == 'inputRemoved':

        elif event.typeS() == 'outputRemoved':
  
        '''          
 

    def showCommonProperties(self):
        #self._properties.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
        self._properties.setRowCount(0)
        self._propertiesBuilder.clear()
        self.propertiesInsertTitle("Element")


        #QTableWidgetItem *item{};
        ID = self._element.id()
        TYPE = '' #{ QString::fromLocal8Bit(m_element->type()) };
        NAME = self._element.name()
        DESCRIPTION = self._element.description()

        item = qtw.QTableWidgetItem(ID)
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        item.setData(qtc.Qt.DisplayRole, ID)
        self._propertiesBuilder.addProperty(
            obj = self._element,
            name = 'ID',
            widget = item        

        )

        item = qtw.QTableWidgetItem(TYPE)
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        #item.setData(qtc.Qt.DisplayRole, ID)
        self._propertiesBuilder.addProperty(
            obj = self._element,
            name = 'TYPE',
            widget = item        
        )

        def onNameChanged(text):
            self.setName(text)

        #item = qtw.QTableWidgetItem(NAME)
        nameEdit = qtw.QLineEdit(NAME)
        #nameEdit.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        #item.setData(qtc.Qt.DisplayRole, ID)
        nameEdit.textChanged.connect(onNameChanged)
        self._propertiesBuilder.addProperty(
            obj = self._element,
            name = 'Name',
            widget = nameEdit
                   
        )

        def onDescChanged(text):
            self.setDesc(text)

        #item = qtw.QTableWidgetItem(NAME)
        descEdit = qtw.QLineEdit(DESCRIPTION)
        #nameEdit.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        #item.setData(qtc.Qt.DisplayRole, ID)
        descEdit.textChanged.connect(onDescChanged)
        self._propertiesBuilder.addProperty(
            obj = self._element,
            name = 'Description',
            widget = descEdit
        ) 

    def showCustomProperties(self):
        tel = self._element
        tcProps = tel.customProperties()
        if tcProps!=None and len(tcProps)>0:
            self.propertiesInsertTitle('Custom properties')
            for propName in tcProps:
                propDesc = tcProps[propName] 
                self._propertiesBuilder.addProperty(
                    obj = self._element,
                    name = propName,
                    propDesc = propDesc
                    )
        pass


    def showIOProperties(self, dir:direction.Dir, modImpl=None):
        INPUTS = dir == direction.LEFT
        tel = self._element if modImpl==None else modImpl._element
        ioEventTarget = self if modImpl==None else modImpl
        ios = tel.nodesByDir(dir)
        IOS_SIZE = ios.size()
        MIN_IOS_SIZE = tel.defaultFlags(dir).min()
        MAX_IOS_SIZE = tel.defaultFlags(dir).max()
        ADDING_DISABLED = MIN_IOS_SIZE == MAX_IOS_SIZE

        pTitle = dir.label()
        self.propertiesInsertTitle(pTitle)

        def countValueChanged(value):
            SIZE = ios.size()
            if (SIZE < value):
                if dir in [direction.TOP,direction.DOWN]:
                    ioEventTarget.addIoNode(dir)
                elif INPUTS:
                    ioEventTarget.addInput()
                else:
                    ioEventTarget.addOutput()
            else:
                if dir in [direction.TOP,direction.DOWN]:
                    ioEventTarget.removeIoNode(dir)
                elif INPUTS:
                    ioEventTarget.removeInput()
                else:
                    ioEventTarget.removeOutput()

        count = qtw.QSpinBox()
        count.setRange(MIN_IOS_SIZE, MAX_IOS_SIZE)
        count.setValue(ios.size())
        count.valueChanged.connect(countValueChanged)
        self._propertiesBuilder.addProperty(
            obj = self._element,
            name = ' Count',#dir.label()+
            widget = count
        )   
        count.setDisabled(ADDING_DISABLED)
        
        #for (int i = 0; i < IOS_SIZE; ++i) {
        for io in ios.values():
            #auto const &IO = ios[static_cast<size_t>(i)];
            ioView = io.view()
            isAnyHover = ioView.isAnyHover()# or ioView.isInHover
            if (isAnyHover):
                self.console().write(f'isAnyHoverOn for {io.name()}\n')
            i = io.id()
            ioName = None
            ioNameStr = io.name()+'('+str(io.size())+')'
            if (io.flags().canChangeName()):
                ioName =  qtw.QLineEdit(ioNameStr) #QString::fromStdString(IO.name) } };
                def editingFinished(self):
                    tel.setIOName(io,ioName.text())
                ioName.editingFinished.connect(editingFinished)
            else:
                ioName = qtw.QTableWidgetItem(ioNameStr)
                ioName.setFlags(ioName.flags() & ~qtc.Qt.ItemIsEditable)
                #self._properties->setItem(row, 0, item);
    


            comboBox = qtw.QComboBox()
            for vt in io.flags().canHoldValues():
                comboBox.addItem(vt.toString(), vt.toInt())

            INDEX = comboBox.findData(io.valueType().toInt())
            comboBox.setCurrentIndex(INDEX)
            #self._properties.setCellWidget(row, 1, comboBox);

            def onActivated(index):
                VALUE_TYPE = ValueType.fromInt(comboBox.itemData(index))
                self.setSocketType(direction, i, VALUE_TYPE)

            comboBox.activated.connect(onActivated)

            comboBox2 = qtw.QComboBox()
            for ioType in NodeIoType:
                comboBox2.addItem(ioType.name, ioType.value)

            tw = qtw.QTableWidget()
            #tw.width=100
            tw.horizontalHeader().hide()
            tw.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
            tw.verticalHeader().hide()
            tw.verticalScrollBar().setDisabled(True)
            tw.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
            tw.horizontalScrollBar().setDisabled(True)
            tw.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
            tw.setRowCount(1)
            tw.setColumnCount(2)
            #ROW = tw.rowCount()
            #tw.insertRow(ROW)
            
            tw.setCellWidget(0,0,comboBox)
            tw.setCellWidget(0,1,comboBox2)
            self._propertiesBuilder.addProperty(
                obj = io,
                name = 'Name',
                lWidget = ioName,
                widget = tw,
                selected = isAnyHover        
                )          



 

    def setCentralWidget(self, w:qtw.QGraphicsItem):
        if (self._centralWidget != None):
            sip.delete(self._centralWidget)
            self._centralWidget = None
            self._centralWidget = w
            self._centralWidget.setParentItem(self)
            self._centralWidget.setPos(self._centralWidgetPosition)

    def propertiesInsertTitle(self, title):
        ROW = self._properties.rowCount()
        self._properties.insertRow(ROW)
        item = qtw.QTableWidgetItem(title)
        item.setTextAlignment(qtc.Qt.AlignHCenter | qtc.Qt.AlignVCenter)
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        #//item.background().setColor(qtc.Qt.lightGray)
        item.setBackground(qtc.Qt.darkGray)
        #item.foreground().setColor(qtc.Qt.black)
        item.setForeground(qtc.Qt.black)
        self._properties.setItem(ROW, 0, item)
        self._properties.setSpan(ROW, 0, 1, 2)


    #def changeIOName(IOSocketsType const a_type, int const a_id, QString const &a_name)
    def changeIOName(self, direction, vid, name):
        #INPUTS = direction - direction.LEFT 

        #SocketItem *socket{};
        #if (self.mType() == ModuleType.ATOMIC):
        #    socket = INPUTS ? m_inputs[a_id] : m_outputs[a_id];
        #else
        #    socket = m_type == Type::eInputs ? m_outputs[a_id] : m_inputs[a_id];
        socket = self.nodes().byId(vid)

        socket.setName(name)
        self.calculateBoundingRect()

    '''
template<typename Container, class Comparator>
auto max_element(Container &a_container, Comparator a_comparator)
{
  return std::max_element(std::begin(a_container), std::end(a_container), a_comparator);
}
    '''

    def calculateBoundingRect(self):
        self.prepareGeometryChange()
        INPUTS_COUNT = self.nodeViewsByDir(direction.LEFT).itemCount() #self.inputs().count()
        OUTPUTS_COUNT = self.nodeViewsByDir(direction.RIGHT).itemCount() #self.outputs().count()
        TOPS_COUNT = self.nodeViewsByDir(direction.TOP).itemCount()
        DOWNS_COUNT = self.nodeViewsByDir(direction.DOWN).itemCount()
        SOCKETS_COUNT = max(INPUTS_COUNT, OUTPUTS_COUNT)
        HSOCKETS_COUNT = max(TOPS_COUNT,DOWNS_COUNT)
        CENTRAL_SIZE = self._centralWidget.boundingRect().size() if (self._centralWidget != None and  self._centralWidget.isVisible()) else self._icon.size() / 2
        SOCKETS_HEIGHT = SOCKETS_COUNT * ROUNDED_SOCKET_SIZE
        SOCKETS_WIDTH = HSOCKETS_COUNT * ROUNDED_SOCKET_SIZE

        #maxNameWidth = [](auto &&a_a, auto &&a_b) { return a_a->nameWidth() < a_b->nameWidth(); };
        #auto const LONGEST_INPUT = max_element(m_inputs, maxNameWidth);
        #auto const LONGEST_OUTPUT = max_element(m_outputs, maxNameWidth);
        #int const LONGEST_INPUTS_NAME_WIDTH = LONGEST_INPUT != std::end(m_inputs) ? (*LONGEST_INPUT)->nameWidth() : 0;
        LONGEST_INPUTS_NAME_WIDTH = self.findMaxNameWidth(self.inputs())
        #int const LONGEST_OUTPUTS_NAME_WIDTH = LONGEST_OUTPUT != std::end(m_outputs) ? (*LONGEST_OUTPUT)->nameWidth() : 0;
        LONGEST_OUTPUTS_NAME_WIDTH = self.findMaxNameWidth(self.outputs())
        INPUTS_NAME_WIDTH = LONGEST_INPUTS_NAME_WIDTH if self._mode == Q3iShowMode.EXPANDED else 0
        OUTPUTS_NAME_WIDTH = LONGEST_OUTPUTS_NAME_WIDTH if self._mode == Q3iShowMode.EXPANDED else 0
        NAME_OFFSET = ROUNDED_SOCKET_SIZE_2 if self._showName else 0
        width = CENTRAL_SIZE.width() 
        height = None
        if (SOCKETS_HEIGHT > CENTRAL_SIZE.height()):
            height = NAME_OFFSET + SOCKETS_HEIGHT + ROUNDED_SOCKET_SIZE
        else:
            height = NAME_OFFSET + CENTRAL_SIZE.height() + ROUNDED_SOCKET_SIZE_2
        if (SOCKETS_COUNT < 2):
            height += ROUNDED_SOCKET_SIZE_2
        width = max(SOCKETS_WIDTH+ ROUNDED_SOCKET_SIZE,ROUNDED_SOCKET_SIZE + INPUTS_NAME_WIDTH + CENTRAL_SIZE.width() + OUTPUTS_NAME_WIDTH + ROUNDED_SOCKET_SIZE)

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
        sydown = ROUNDED_SOCKET_SIZE + NAME_OFFSET
        sytop = 0
        if (self._element != None and (self.isInvertH())):
            sinp = width
            sout = 0.0
            sytop = ROUNDED_SOCKET_SIZE + NAME_OFFSET
            sydown = 0
        #for inp in self.inputs().values():
        for inp in self.nodeViewsByDir(direction.LEFT).values():
            inp.setPos(sinp, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        yOffset = ROUNDED_SOCKET_SIZE + NAME_OFFSET
        #for out in self.outputs().values():
        for out in self.nodeViewsByDir(direction.RIGHT).values():
            out.setPos(sout, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        xoffset = ROUNDED_SOCKET_SIZE
        yOffset = sydown
        for io in self.nodeViewsByDir(direction.DOWN).values():
            io.setPos(xoffset,yOffset)
            xoffset += ROUNDED_SOCKET_SIZE
        xoffset = ROUNDED_SOCKET_SIZE
        yOffset = sytop
        for io in self.nodeViewsByDir(direction.TOP).values():
            io.setPos(xoffset,yOffset)
            xoffset += ROUNDED_SOCKET_SIZE

        self._boundingRect = qtc.QRectF(0.0, 0.0, width, height)

    def changeInputName(self, vid:int, name):
        self.changeIOName(direction.LEFT, vid, name)

    def changeOutputName(self, vid:int, name):
        self.changeIOName(direction.RIGHT, vid, name)

    #@deprecated
    def addInput(self):
        dir = direction.LEFT
        ioNodes = self._element.nodesByDir(dir)
        SIZE = ioNodes.size() #self._element.inputs().size()
        INPUT_NAME = f'#{SIZE}'
        last = ioNodes.last() #self._element.inputs().last()
        #first_available_type_for_flags(self._element.defaultNewInputFlags())
        TYPE = last.valueType() if last != None else self._element.defaultFlags(dir).firstAvailableType()        
        tnt = NodeIoType.INPUT
        if self.mType() == ModuleType.IO:
            tnt = NodeIoType.OUTPUT
        result = self._element.addInput(TYPE, INPUT_NAME, self._element.defaultFlags(dir), tnt)
        self.m_packageView.showProperties()
        result = self._element.nodes().byLid(result) if result >-1 else None
        return result

    def addIoNode(self, dir:direction.Dir):
        tnt = NodeIoType.INPUT if dir in [direction.TOP,direction.LEFT] else NodeIoType.OUTPUT
        if self.mType() == ModuleType.IO:
            tnt = NodeIoType.OUTPUT if dir in [direction.TOP,direction.LEFT] else NodeIoType.INPUT
            #dir = dir.oposite()
        ioNodes = self._element.nodesByDir(dir)
        SIZE = ioNodes.size() #self._element.inputs().size()
        NAME = f'#{SIZE}'
        last = ioNodes.last() #self._element.inputs().last()
        #first_available_type_for_flags(self._element.defaultNewInputFlags())
        TYPE = last.valueType() if last != None else self._element.defaultFlags(dir).firstAvailableType()        
        result = self._element.addIoNode(dir,TYPE, NAME, self._element.defaultFlags(dir), tnt)
        self.m_packageView.showProperties()
        result = self._element.nodes().byLid(result) if result >-1 else None
        return result

    def removeIoNode(self, dir:direction.Dir):
        self._element.removeIoNode(dir)
        self.m_packageView.showProperties()

    def removeInput(self):
        self._element.removeInput()
        self.m_packageView.showProperties()
    
    def setInputName(self, socketId, name):
        self._element.setInputName(socketId, name)
        self.inputs().byId(socketId).setName(name)
        self.calculateBoundingRect()
        self.m_packageView.showProperties()


    def addOutput(self):
        dir = direction.RIGHT        
        ioNodes = self._element.nodesByDir(dir)
        SIZE = ioNodes.size() #self._element.outputs().size()
        NAME = f'#{SIZE}'
        last= ioNodes.last() #self._element.outputs().last()
        #{ first_available_type_for_flags(m_element->defaultNewOutputFlags()) };
        TYPE = last.valueType() if last != None else self._element.defaultFlags(dir).firstAvailableType() 
        tnt = NodeIoType.OUTPUT
        #dirp = dir
        if self.mType() == ModuleType.IO:
            tnt = NodeIoType.INPUT                 
        self._element.addOutput(TYPE, NAME, self._element.defaultFlags(dir), tnt)
        self.m_packageView.showProperties()

    def removeOutput(self):
        self._element.removeOutput()
        self.m_packageView.showProperties()

    def setOutputName(self, socketId, name):
        self._element.setOutputName(socketId, name)
        self.outputs().byId(socketId).setName(name)
        self.calculateBoundingRect()
        self.m_packageView.showProperties()



    def addSocket(self, dir, vid, name, valueType:ValueType, mType:ModuleType):
        ioNode = self._element.nodes().byId(vid)
        if ioNode.valueType() == None:
            if ioNode.signals().size()>0:
                sig = ioNode.signals().first()
                valueType = ValueType.fromSize(sig.size())
                ioNode.setProp('valueType',valueType)

        if ioNode.flags() == None:
            tflags = IoNodeFlags()
            '''
            if (dir == direction.LEFT):
                tflags = ioNode.module().impl().defaultNewInputFlags()
            else:
                tflags = ioNode.module().impl().defaultNewOutputFlags()
            '''    
            ioNode.setProp('ioNodeFlags',tflags)

        ioNodeView = IoNodeView(self, ioNode, dir)
        #ioNodeView.setName(a_name);
        ioNodeView.setToolTip(name)
        #ioNodeView.setValueType(valueType);

        if (self._mode == Q3iShowMode.COLLAPSED):
            ioNodeView.hideName()
        else:
            ioNodeView.showName()

        #self.nodeViews().push_back(ioNodeView)
        self.nodeViews().append(ioNodeView.id(),ioNodeView)



    def removeSocket(self, dir):
        #if dir == direction.LEFT:
            #inpd = self.inputs().last()
        inpd = self.nodeViewsByDir(dir).last()
        self.nodeViews().removeByLid(inpd.id())
        sip.delete(inpd)
        del inpd           
        #else:
        #    outd = self.outputs().last()
        #    self.nodeViews().removeByLid(outd.id())
        #    sip.delete(outd)
        #    del outd
            


    def setSocketType(self, direction, socketId, vType:ValueType):
        assert(self._element != None)
        
        INPUTS = direction == direction.LEFT

        io = self._element.nodes().byId(socketId)

        if (not io.flags().valueTypeAllowed(vType)):
            self.raiseExc(f'Changing io''s {self._element.id()}@{io.id()} type to {vType.toString()} is not allowed.')


        socket = self.nodeViews().byId(socketId)

        if (socket.valueType() == vType):
            return

        socket.disconnectAll()

        self._element.setIOValueType(INPUTS, socketId, vType)

        socket.setValueType(vType)


    def updateOutputs(self):
        #if (self._element == None or self.mType() == ModuleType.OUTPUTS):
        #    return 
        pass

    def setIcon(self, ico:str):
        self._iconPath = ico
        self._icon.load(ico)

    def findMaxNameWidth(self,coll:Q3Vector):
        result = None
        if (coll!=None and coll.size()>0):
            result = coll.by('nameWidth',coll.byModifier.MAX)
        result = result.nameWidth() if result!=None else 5
        return result









