import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

from ...nodeiotype import NodeIoType

from ...wqvector import WqVector

from ... import consts, prop, orientation, direction, colors

from ...ModuleFactory import ModuleType

from .IoNodeView import IoNodeView

from ..sim.valuetype import ValueType

from . import stypes

from enum import Enum

class WqiShowMode(Enum):
    ICONIFIED = 1
    EXPANDED = 2


class PropertiesBuilder:
    def __init__(self, table):
        self._table = table
    

    def addProperty(self,**kwargs):

        propName = kwargs['name']
        cellWidget = kwargs['widget']
        lWidget = kwargs['lWidget'] if 'lWidget' in kwargs else None

        row = self._table.rowCount()
        self._table.insertRow(row)

        if (lWidget == None):
            itemL = qtw.QTableWidgetItem(propName) 
            itemL.setFlags(itemL.flags() & ~qtc.Qt.ItemIsEditable)
            self._table.setItem(row, 0, itemL)
        else:
            self._table.setItem(row, 0, lWidget)
        if isinstance(cellWidget,qtw.QTableWidgetItem):
            self._table.setItem(row, 0, cellWidget)
        else:
            self._table.setCellWidget(row, 1, cellWidget)    

SOCKET_SIZE = IoNodeView.SIZE
ROUNDED_SOCKET_SIZE = round((SOCKET_SIZE) / 10.0) * 10.0
ROUNDED_SOCKET_SIZE_2 = ROUNDED_SOCKET_SIZE / 2.0

NODE_TYPE = stypes.NODE_TYPE

#implements nonroot mode of moduleView (spaghetti node)
class ModuleViewImpl(qtw.QGraphicsItem):
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
        self._rotate = False
        self._invertH = False
        #self._inputs = WqVector()
        #self._outputs = WqVector()
        self._nodeViews = WqVector()
        self._color = colors.MODULE_COLOR
        self._properties = None
        self._propertiesBuilder = None
        self._graphView = None
        self.m_packageView = None
        self._rotation = 0
        super(ModuleViewImpl,self).__init__(parent)

    def s(self):
        return self._self

    def moduleView(self): #for use by view elements
        return self._self

    def inputs(self):
        return self._nodeViews.filterBy('direction',direction.LEFT)
    
    def outputs(self):
        return self._nodeViews.filterBy('direction',direction.RIGHT)

    def nodeViews(self):
        return self._nodeViews

    def module(self):
        return self.moduleView().module()

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
            self.m_packageView.setSelectedNode(lastSelected)
            self.m_packageView.showProperties()
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
        elif change == qtw.QGraphicsItem.GraphicsItemChange.ItemRotationHasChanged:
            for ioNodeView in self._nodeViews.values():
                ioNodeView.itemChange(qtw.QGraphicsItem.ItemScenePositionHasChanged, None)
            
        return super().itemChange(change, value)






    '''!TODO!
void Node::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *a_event)
{
  auto const MODIFIERS = QApplication::keyboardModifiers();

  if (!((MODIFIERS & Qt::ControlModifier) && open())) (m_mode == Mode::eIconified) ? expand() : iconify();

  QGraphicsItem::mouseDoubleClickEvent(a_event);
}

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
            self._element.setPosition(self.x(), self.y())
            self._element.iconify(self._mode == WqiShowMode.ICONIFIED)
            self.setName(self._element.name())
            self.updateOutputs()
        elif mType == ModuleType.INPUTS:
            for inp in INPUTS.values():
                NAME = inp.name()
                self.addSocket(direction.RIGHT, inp.id(), NAME, inp.valueType(),inp.ioType())
        elif mType == ModuleType.OUTPUTS:
            for out in OUTPUTS.values():
                NAME = out.name()
                self.addSocket(direction.LEFT, out.id(), NAME, out.valueType(),out.ioType())
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
            self.setToolTip(f'{name}');


    def setIcon(self, icon):
        self._iconPath = icon
        self._icon.load(icon)

    def showName(self):
        self._showName = True
        self.calculateBoundingRect()
    

    def hideName(self):
        self._showName = False
        self.calculateBoundingRect()
        
    def iconify(self):
        if (self._element != None):
            self._element.iconify(True)
            if (self._element.iconifyingHidesCentralWidget() and self._centralWidget != None):
                self._centralWidget.hide()
        self._mode = WqiShowMode.ICONIFIED
        for inp in self.inputs().values():
            inp.hideName()
        for out in self.outputs().values():
            out.hideName()
        self.calculateBoundingRect()

    def expand(self):
        if (self._element != None):
            self._element.iconify(False)
        
            if (self._element.iconifyingHidesCentralWidget() and self._centralWidget != None):
                self._centralWidget.show()
            
        self._mode = WqiShowMode.EXPANDED

        for inp in self.inputs().values():
            inp.showName()
        
        for out in self.outputs().values():
            out.showName()

        self.calculateBoundingRect()






    def setPropertiesTable(self, properties): #QTableWidget *const a_properties
        self._properties = properties
        self._propertiesBuilder = PropertiesBuilder(self._properties)

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
    def direction(self):
        dir = direction.RIGHT
        if (self._rotate):
            if (not self._invertH):
                dir = direction.UP
            else:
                dir = direction.DOWN
        else:
            if (self._invertH):
                dir = direction.LEFT
        return dir

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
            self._rotate = False;
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
            name='Rotate',
            widget = valueRot        
        )

        currentInv = self.isInvertH()
        valueInv =  qtw.QCheckBox()
        valueInv.setChecked(currentInv)
        valueInv.stateChanged.connect(self.onPropCurrentInvChanged)

        self._propertiesBuilder.addProperty(
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
        elif mType == ModuleType.INPUTS:
            self.showIOProperties(direction.LEFT)
        elif mType == ModuleType.OUTPUTS:
            self.showIOProperties(direction.RIGHT)

    def _getInpDirection(self):
        dir = direction.LEFT # for input default dir is LEFT but ...       
        if self.mType() == ModuleType.INPUTS: #if it is INPUTS module - direction for input is right
            dir = direction.RIGHT
        return dir

    def heInputAdded(self, event):
        inpId = event.props('inputId')
        inp = self._element.inputs().byId(inpId)
        #INPUTS = self._element.inputs()
        #SIZE = inputs().size();
        #auto const &INPUT = INPUTS.back();
        #addSocket(IOSocketsType::eInputs, static_cast<uint8_t>(SIZE), QString::fromStdString(INPUT.name), INPUT.type,INPUT.sItemType);
        dir = self._getInpDirection()
        self.addSocket(dir, inp.id(), inp.name(), inp.valueType(), inp.ioType())
        self.calculateBoundingRect()
    
    def heInputRemoved(self,event):
        dir = self._getInpDirection()
        self.removeSocket(dir)
        self.calculateBoundingRect()

    def _getOutDirection(self):
        dir = direction.RIGHT # default for output socket
        if self.mType() == ModuleType.OUTPUTS:
            dir = direction.LEFT
        return dir

    def heOutputAdded(self, event):
        outId = event.props('outputId')
        out = self._element.outputs().byId(outId)
        #INPUTS = self._element.inputs()
        #SIZE = inputs().size();
        #auto const &INPUT = INPUTS.back();
        #addSocket(IOSocketsType::eInputs, static_cast<uint8_t>(SIZE), QString::fromStdString(INPUT.name), INPUT.type,INPUT.sItemType);
        dir = self._getOutDirection()
        self.addSocket(dir, out.id(), out.name(), out.valueType(), out.ioType())
        self.calculateBoundingRect()

    def heOutputRemoved(self, event):
        dir = self._getOutDirection()
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
        self._properties.setRowCount(0)
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
            name = 'ID',
            widget = item        

        )

        item = qtw.QTableWidgetItem(TYPE)
        item.setFlags(item.flags() & ~qtc.Qt.ItemIsEditable)
        #item.setData(qtc.Qt.DisplayRole, ID)
        self._propertiesBuilder.addProperty(
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
            name = 'Description',
            widget = descEdit
        )        

    def showIOProperties(self, dr):
        INPUTS = dr == direction.LEFT
        ios = self._element.inputs() if INPUTS else self._element.outputs()
        IOS_SIZE = ios.size()
        MIN_IOS_SIZE = self._element.minInputs() if INPUTS else self._element.minOutputs()
        MAX_IOS_SIZE = self._element.maxInputs() if INPUTS else self._element.maxOutputs()
        ADDING_DISABLED = MIN_IOS_SIZE == MAX_IOS_SIZE

        pTitle = 'Inputs' if INPUTS else 'Outputs'
        self.propertiesInsertTitle(pTitle)

        def countValueChanged(value):
            SIZE = self._element.inputs().size() if INPUTS else self._element.outputs().size()
            if (SIZE < value):
                if INPUTS:
                    self.addInput()
                else:
                    self.addOutput()
            else:
                if INPUTS:
                    self.removeInput()
                else:
                    self.removeOutput()

        count = qtw.QSpinBox()
        count.setRange(MIN_IOS_SIZE, MAX_IOS_SIZE)
        count.setValue(ios.size())
        count.valueChanged.connect(countValueChanged)
        self._propertiesBuilder.addProperty(
            name = 'Count',
            widget = count
        )   
        count.setDisabled(ADDING_DISABLED)
        
        #for (int i = 0; i < IOS_SIZE; ++i) {
        for io in ios.values():
            #auto const &IO = ios[static_cast<size_t>(i)];
            i = io.id()
            ioName = None
            if (io.flags().canChangeName()):
                ioName =  qtw.QLineEdit(io.name()) #QString::fromStdString(IO.name) } };
                def editingFinished(self):
                    self._element.setIOName(io,ioName.text())
                ioName.editingFinished.connect(editingFinished)
            else:
                ioName = qtw.QTableWidgetItem(io.name())
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
            
            self._propertiesBuilder.addProperty(
                name = 'Name',
                lWidget = ioName,
                widget = comboBox        
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
        item.background().setColor(qtc.Qt.darkGray)
        item.foreground().setColor(qtc.Qt.black)
        self._properties.setItem(ROW, 0, item)
        self._properties.setSpan(ROW, 0, 1, 2)


    #def changeIOName(IOSocketsType const a_type, int const a_id, QString const &a_name)
    def changeIOName(self, direction, vid, name):
        INPUTS = direction - direction.LEFT 

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
        INPUTS_COUNT = self.inputs().count()
        OUTPUTS_COUNT = self.outputs().count()
        SOCKETS_COUNT = max(INPUTS_COUNT, OUTPUTS_COUNT)
        CENTRAL_SIZE = self._centralWidget.boundingRect().size() if (self._centralWidget != None and  self._centralWidget.isVisible()) else self._icon.size() / 2
        SOCKETS_HEIGHT = SOCKETS_COUNT * ROUNDED_SOCKET_SIZE

        #maxNameWidth = [](auto &&a_a, auto &&a_b) { return a_a->nameWidth() < a_b->nameWidth(); };
        #auto const LONGEST_INPUT = max_element(m_inputs, maxNameWidth);
        #auto const LONGEST_OUTPUT = max_element(m_outputs, maxNameWidth);
        #int const LONGEST_INPUTS_NAME_WIDTH = LONGEST_INPUT != std::end(m_inputs) ? (*LONGEST_INPUT)->nameWidth() : 0;
        LONGEST_INPUTS_NAME_WIDTH = self.findMaxNameWidth(self.inputs())
        #int const LONGEST_OUTPUTS_NAME_WIDTH = LONGEST_OUTPUT != std::end(m_outputs) ? (*LONGEST_OUTPUT)->nameWidth() : 0;
        LONGEST_OUTPUTS_NAME_WIDTH = self.findMaxNameWidth(self.outputs())
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
        if (self._element != None and (direction.LEFT == self.direction() or direction.DOWN == self.direction())):
            sinp = width
            sout = 0.0
        for inp in self.inputs().values():
            inp.setPos(sinp, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        yOffset = ROUNDED_SOCKET_SIZE + NAME_OFFSET
        for out in self.outputs().values():
            out.setPos(sout, yOffset)
            yOffset += ROUNDED_SOCKET_SIZE
        self._boundingRect = qtc.QRectF(0.0, 0.0, width, height)

    def changeInputName(self, vid:int, name):
        self.changeIOName(direction.LEFT, vid, name)

    def changeOutputName(self, vid:int, name):
        self.changeIOName(direction.RIGHT, vid, name)

    def addInput(self):
        SIZE = self._element.inputs().size()
        INPUT_NAME = f'#{SIZE}'
        last = self._element.inputs().last()
        #first_available_type_for_flags(self._element.defaultNewInputFlags())
        TYPE = last.valueType() if last != None else self._element.defaultNewInputFlags().firstAvailableType()        
        tnt = NodeIoType.INPUT
        if self.mType() == ModuleType.INPUTS:
            tnt = NodeIoType.OUTPUT
        self._element.addInput(TYPE, INPUT_NAME, self._element.defaultNewInputFlags(), tnt)
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
        SIZE = self._element.outputs().size()
        OUTPUT_NAME = f'#{SIZE}'
        last=self._element.outputs().last()
        #{ first_available_type_for_flags(m_element->defaultNewOutputFlags()) };
        TYPE = last.valueType() if last != None else self._element.defaultNewOutputFlags().firstAvailableType() 
        tnt = NodeIoType.OUTPUT
        if self.mType() == ModuleType.OUTPUTS:
            tnt = NodeIoType.INPUT            
        self._element.addOutput(TYPE, OUTPUT_NAME, self._element.defaultNewOutputFlags(), tnt)
        self.m_packageView.showProperties()

    def removeOutput(self):
        self._element.removeOutput()
        self.m_packageView.showProperties()

    def setOutputName(self, socketId, name):
        self._element.setOutputName(socketId, name)
        self.outputs().byId(socketId).setName(name)
        self.calculateBoundingRect()
        self.m_packageView.showProperties()



    def addSocket(self, direction, vid, name, valueType:ValueType, mType:ModuleType):
        ioNode = self._element.nodes().byId(vid)
        #socket = new SocketItem{ this, ioType, a_type };
        #socket->setElementId(m_type == Type::eElement ? m_element->id() : 0);
        #socket->setSocketId(a_id);
        ioNodeView = IoNodeView(self, ioNode, direction)
        #ioNodeView.setName(a_name);
        ioNodeView.setToolTip(name)
        #ioNodeView.setValueType(valueType);

        if (self._mode == WqiShowMode.ICONIFIED):
            ioNodeView.hideName()
        else:
            ioNodeView.showName()

        self.nodeViews().push_back(ioNodeView)



    def removeSocket(self, dr):
        if dr == direction.LEFT:
            inpd = self.inputs().last()
            self.nodeViews().remove(inpd)
        else:
            outd = self.outputs().last()
            self.nodeViews().remove(outd)


    def setSocketType(self, direction, socketId, vType:ValueType):
        assert(self._element != None)
        
        INPUTS = direction == direction.LEFT
        #auto &io = INPUTS ? m_element->inputs()[a_socketId] : m_element->outputs()[a_socketId];
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
        if (self._element == None or self.mType() == ModuleType.OUTPUTS):
            return 
        '''
        IS_ELEMENT = self.mType() == ModuleType.ATOMIC
        ELEMENT_IOS = IS_ELEMENT ? m_element->outputs() : m_element->inputs();
  auto const &NODE_IOS = m_outputs;
  size_t const SIZE{ ELEMENT_IOS.size() };
  for (size_t i = 0; i < SIZE; ++i) {
    switch (ELEMENT_IOS[i].type) {
      case ValueType::eBool: {
        bool const SIGNAL{ std::get<bool>(ELEMENT_IOS[i].value) };
        NODE_IOS[static_cast<int>(i)]->setSignal(SIGNAL);
        break;
      }
      default: break;
    }
  }
}
    '''




    def setIcon(self, ico:str):
        self._iconPath = ico
        self._icon.load(ico)

       


    def findMaxNameWidth(self,coll):
        #!TODO!
        return 5









