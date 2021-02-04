import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

from .ModuleViewImpl import ModuleViewImpl, PropertiesBuilder
from ... import consts, prop, orientation, direction, colors

#node package
class PackageViewImpl(ModuleViewImpl):
        #self._moduleType = self.s().moduleType()
    def setInputsNode(self, node): #Node *const a_
        self.m_inputsNode = node
    def inputsNode(self):
        return self.m_inputsNode
    #nst *inputsNode() const { return m_inputsNode; }
    def setOutputsNode(self, node): #Node *const a_ 
        self.m_outputsNode = node
    def outputsNode(self):
        return self.m_outputsNode
    #outputsNode() const { return m_outputsNode; }
    # private:
    #def showProperties(self): override;
    #void handleEvent(Event const &a_event) override;
    #bool open() override;

    def __init__(self, parent, **kwargs):
        t_self = kwargs['_self'] if '_self' in kwargs else None
        assert t_self != None, '_self argument required'
        kwargs.pop('_self',None)
        super(PackageViewImpl, self).__init__(parent,**kwargs) #_self reset here
        self._self = t_self
        self.m_inputsNode = None #Node *
        self.m_outputsNode = None     #Node *
#--- HDR_END ---

    def showProperties(self):
        self.showCommonProperties()
        #package = static_cast<spaghetti::Package *>(m_element);
        package = self._element
        PATH = package.packagePath()
        ICON = package.packageIcon()
        self.propertiesInsertTitle("Package")
        #QTableWidgetItem *item{};

        def pathEditTextChanged(text):
            package.setPackagePath(text)

        #QLineEdit *pathEdit = new QLineEdit{ PATH };
        pathEdit = qtw.QLineEdit(PATH)
        pathEdit.setPlaceholderText('<path>')
        pathEdit.textChanged.connect(pathEditTextChanged)
        self._propertiesBuilder.addProperty(
            name='Path',
            widget = pathEdit        
        )

        def iconEditTextChanged(text):
            #(void)text;
            #qDebug() << "ICON:" << a_text;
            #/* !TODO! */
            pass

        #QLineEdit *iconEdit = new QLineEdit{ ICON };
        #iconEdit->setPlaceholderText("<icon>");
        iconEdit = qtw.QLineEdit(ICON)
        iconEdit.setPlaceholderText('<icon>')
        iconEdit.textChanged.connect(iconEditTextChanged)
        self._propertiesBuilder.addProperty(
            name='Icon',
            widget = iconEdit        
        )
        self.showIOProperties(direction.LEFT, self.m_inputsNode)
        self.showIOProperties(direction.RIGHT, self.m_outputsNode)


        '''
handleEvent(Event const &a_event)
{
  Node::handleEvent(a_event);

  if (!(m_inputsNode && m_outputsNode)) return;

  switch (a_event.type) {
    case EventType::eElementNameChanged: {
      auto const &EVENT = std::get<EventNameChanged>(a_event.payload);
      auto const IS_ROOT = m_element->package() == nullptr;
      if (!IS_ROOT) {
        auto const packageView = m_inputsNode->packageView();
        auto const editor = packageView->editor();
        auto const INDEX = editor->indexForPackageView(packageView);
        editor->setPackageViewTabName(INDEX, QString::fromStdString(EVENT.to));
      }
      break;
    }
    case EventType::eIONameChanged: {
      auto const &EVENT = std::get<EventIONameChanged>(a_event.payload);
      if (EVENT.input) {
        m_inputsNode->outputs()[EVENT.id]->setName(QString::fromStdString(EVENT.to));
        m_inputsNode->calculateBoundingRect();
      } else {
        m_outputsNode->inputs()[EVENT.id]->setName(QString::fromStdString(EVENT.to));
        m_outputsNode->calculateBoundingRect();
      }
      break;
    }
    case EventType::eIOTypeChanged: {
      auto const &EVENT = std::get<EventIOTypeChanged>(a_event.payload);
      if (EVENT.input)
        m_inputsNode->setSocketType(IOSocketsType::eInputs, EVENT.id, EVENT.to);
      else
        m_outputsNode->setSocketType(IOSocketsType::eOutputs, EVENT.id, EVENT.to);
      break;
    }
    case EventType::eInputAdded: {
      auto const &INPUTS = m_element->inputs();
      auto const INPUTS_SIZE = static_cast<int>(INPUTS.size());
      auto const &LAST_INPUT = INPUTS.back();
      auto const OUTPUTS_SIZE = m_inputsNode->outputs().size();
      auto const ADD_SOCKET_NEEDED = OUTPUTS_SIZE < INPUTS_SIZE;
      assert(ADD_SOCKET_NEEDED == true);
      m_inputsNode->addSocket(IOSocketsType::eOutputs, static_cast<uint8_t>(OUTPUTS_SIZE),
                              QString::fromStdString(LAST_INPUT.name), LAST_INPUT.type,SocketType::eOutput);
      m_inputsNode->calculateBoundingRect();
      break;
    }
    case EventType::eInputRemoved: {
      m_inputsNode->removeSocket(IOSocketsType::eOutputs);
      m_inputsNode->calculateBoundingRect();
      break;
    }
    case EventType::eOutputAdded: {
      auto const &OUTPUTS = m_element->outputs();
      auto const OUTPUTS_SIZE = static_cast<int>(OUTPUTS.size());
      auto const &LAST_OUTPUT = OUTPUTS.back();
      auto const INPUTS_SIZE = m_outputsNode->inputs().size();
      auto const ADD_SOCKET_NEEDED = INPUTS_SIZE < OUTPUTS_SIZE;
      assert(ADD_SOCKET_NEEDED == true);
      m_outputsNode->addSocket(IOSocketsType::eInputs, static_cast<uint8_t>(INPUTS_SIZE),
                               QString::fromStdString(LAST_OUTPUT.name), LAST_OUTPUT.type,SocketType::eInput);
      m_outputsNode->calculateBoundingRect();
      break;
    }
    case EventType::eOutputRemoved: {
      m_outputsNode->removeSocket(IOSocketsType::eInputs);
      m_outputsNode->calculateBoundingRect();
      break;
    }
  }
}        

        '''

    def open(self):
        editor = self.m_packageView.editor()
        editor.openOrCreatePackageView(self._element);
        return True