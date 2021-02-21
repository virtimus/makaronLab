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
        self.propertiesInsertTitle("Graph")
        #QTableWidgetItem *item{};

        def pathEditTextChanged(text):
            package.setPackagePath(text)

        #QLineEdit *pathEdit = new QLineEdit{ PATH };
        pathEdit = qtw.QLineEdit(PATH)
        pathEdit.setPlaceholderText('<path>')
        pathEdit.textChanged.connect(pathEditTextChanged)
        self._propertiesBuilder.addProperty(
            obj = self._element,
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
            obj = self._element,
            name='Icon',
            widget = iconEdit        
        )

        valueSR =  qtw.QCheckBox()
        valueSR.setChecked(self.isScriptRecordingOn())
        valueSR.stateChanged.connect(self.onPropScriptRecordingChanged)

        self._propertiesBuilder.addProperty(
            obj = self._element,
            name='scriptRecording',
            widget = valueSR        
        )


        self.showIOProperties(direction.LEFT, self.m_inputsNode)
        self.showIOProperties(direction.RIGHT, self.m_outputsNode)

        self.showCustomProperties()

    def onPropScriptRecordingChanged(self, event):
        state = event
        self.module().graphModule().setScriptRecording(state == 2)
        #self.updateScriptRecording()


    def open(self):
        editor = self.m_packageView.editor()
        editor.openOrCreatePackageView(self._element) #openModuleView
        return True