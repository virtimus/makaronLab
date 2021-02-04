from ... import direction, consts

from ...ModuleFactory import IoType, ModuleFactory, ModuleImplBase, ModuleType

from .ionodeflags import IoNodeFlags

from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, pyqtSignal as EventSignal
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

from .valuetype import ValueType


from ...EventSignal import EventProps
   

#element
class ModuleImplElement(ModuleImplBase):


    def __init__(self, **kwargs):
        #self._name = None (s)
        super(ModuleImplElement, self).__init__(**kwargs)

        self.m_defaultNewInputFlags = IoNodeFlags()
        self.m_defaultNewOutputFlags = IoNodeFlags()
        self._moduleType = kwargs['moduleType'] if 'moduleType' in kwargs else ModuleType.ATOMIC
        
        self.m_package = None #initialisation on driver level
        self.m_node = None
        #self.m_id = None
        #self.m_name = None self.s()name
        pass

    #id() const noexcept { return m_id; }
    #def id(self):
    #    return self.m_id

    #bool isRoot() { return m_package == nullptr; }
    def isRoot(self):
        return self.m_package == None

    def name(self):
        return self.s().name()

    def description(self):
        return self.s().desc()



    #uint8_t defaultNewInputFlags() const { return m_defaultNewInputFlags; }
    def defaultNewInputFlags(self):
        return self.m_defaultNewInputFlags

    def setDefaultNewInputFlags(self, flags):
        self.m_defaultNewInputFlags = flags

    def defaultNewOutputFlags(self):
        return self.m_defaultNewOutputFlags

    def setDefaultNewOutputFlags(self, flags):
        self.m_defaultNewOutputFlags = flags


    #Package *package() const { return m_package; }  
    def package(self):
        return self.m_package


    # ---- HDR-END --------------------    

    
    def node(self):
        return self.m_node
        
    def setNode(self, node):
        self.m_node = node
    


    def registerEventHandler(self, handlerFunc): #EventCallback const &a_{ m_handler = a_handler; }
        self._events.elementNameChanged.connect(handlerFunc)
        self._events.inputAdded.connect(handlerFunc)
        self._events.outputAdded.connect(handlerFunc)
        self._events.ioNameChanged.connect(handlerFunc)
        self._events.inputRemoved.connect(handlerFunc)
        self._events.outputRemoved.connect(handlerFunc)
        self._events.ioTypeChanged.connect(handlerFunc)

    def s(self):
        return self._self



    def setName(self, name:str):
        OLD_NAME = self.s().name()
        #m_name = a_name;
        self.s().setName(name)
        self.elementNameChanged.emit(EventProps({'oldName':OLD_NAME, 'name':name}))
        #handleEvent(Event{ EventType::eElementNameChanged, EventNameChanged{ OLD_NAME, a_name } });
    
    def setInfo(self, info:str):
        self.s().setInfo(info)

    def setDesc(self, desc:str):
        self.s().setDesc(desc)

    def desc(self):
        return self.s().desc()

    #bool Element::addInput(ValueType const a_type, std::string const &a_name, uint8_t const a_flags){
	#return addInput(a_type,a_name,a_flags,SocketItemType::eInput);
    def addInput(self, valueType:ValueType, name:str, flags:IoNodeFlags) -> bool:
        return self.addInput(valueType,name,flags,IoType.INPUT)


    #bool Element::addInput(ValueType const a_type, std::string const &a_name, uint8_t const a_flags,SocketItemType sItemType)
    #return (addInputS(a_type,a_name,a_flags,sItemType)>=0);
    def addInput(self, valueType:ValueType, name:str, flags:IoNodeFlags,ioType:IoType) -> bool:
        return (self.addInputS(valueType, name, flags, ioType)>0)

    def _tsizeFromValueType(self, valueType:ValueType) -> int:
        return valueType.toSize()


    def _valueTypeFromSize(size:int):
        return ValueType.fromSize(size)

            


    def addInputS(self, valueType:ValueType, name:str, flags:IoNodeFlags, ioType:IoType) -> int:
        index = self.inputs().size()
        if (index + 1 > self._maxInputs):
            return -1

        #IOSocket input{};
        #input.name = a_name;
        #input.type = a_type;
        #input.flags = a_flags;
        #input.sItemType = sItemType;
        #input.inFlags = 1;

        tsize = self._tsizeFromValueType(valueType)

        input = self.newIO(
            name = name,
            direction = direction.LEFT,
            size = tsize,
            ioType = ioType,
            props = {
                'addInputFlags':flags,
                'ioNodeFlags':flags,
                'addInputValueType':valueType,
                'valueType':valueType
            }
        )
        
        self.resetIOSocketValue(input)

        #m_inputs.emplace_back(input); not needed - should be on list

        #handleEvent(Event{ EventType::eInputAdded, EventEmpty{} });
        #self.events().inputAdded.emit(EventProps({'inputId':input.id()}))

        #return index;
        return input.id()

    def resetIOSocketValue(self, io:'IoNode'):
        io.resetValue()

    #void Element::setInputName(uint8_t const a_input, std::string const &a_name)
    def setInputName(self, inputId:int, name:str):
        tinp = self.inputs().by('id',inputId)
        OLD_NAME = tinp.name()
        if (OLD_NAME == name):
            return
        #m_inputs[a_input].name = a_name;
        tinp.setName(name)
        #handleEvent(Event{ EventType::eIONameChanged, EventIONameChanged{ OLD_NAME, a_name, a_input, true } });
        self.events().ioNameChanged.emit(EventIONameChanged( OLD_NAME, name, inputId, True))

    def removeInput(self):
        tinp = self.inputs().last()
        #self.nodes().remove(tinp)
        #handleEvent(Event{ EventType::eInputRemoved, EventEmpty{} });
        inpId = tinp.id()
        self.removeIO(inpId)
        del tinp
        self.events().inputRemoved.emit(EventProps({'inputId':inpId}))

    def clearInputs(self):
        #m_inputs.clear();
        self.nodes().clearBy('ioType',IoType.INPUT)
  
    #bool Element::addOutput(ValueType const a_type, std::string const &a_name, uint8_t const a_flags){
	#return addOutput(a_type,a_name,a_flags,SocketItemType::eOutput);
    def addOutput(self, valueType:ValueType, name:str, flags:IoNodeFlags):
        return self.addOutput(valueType, name, flags, IoType.OUTPUT)

    #bool Element::addOutput(ValueType const a_type, std::string const &a_name, uint8_t const a_flags, SocketItemType sItemType)
    #return (addOutputS(a_type, a_name, a_flags, sItemType)>=0);
    def addOutput(self, valueType:ValueType, name:str, flags:IoNodeFlags, ioType:IoType):
        return self.addOutputS(valueType, name, flags, ioType) 

    #size_t Element::addOutputS(ValueType const a_type, std::string const &a_name, uint8_t const a_flags, SocketItemType sItemType){
	#  
    def addOutputS(self, valueType:ValueType, name:str, flags:IoNodeFlags, ioType:IoType):
        index = self.outputs().size()
        if (index + 1 > self._maxOutputs):
            return -1

        #IOSocket output{};
        #output.name = a_name;
        #output.type = a_type;
        #output.flags = a_flags;
        #output.sItemType = sItemType;
        #output.inFlags = 2;

        tsize = self._tsizeFromValueType(valueType)

        output = self.newIO(
            name = name,
            direction = direction.RIGHT,
            size = tsize,
            ioType = ioType,
            props = {
                'addOutputFlags':flags,
                'ioNodeFlags':flags,
                'addOutputValueType':valueType,
                'valueType':valueType
            }
        )

        self.resetIOSocketValue(output)

        #m_outputs.emplace_back(output); already done
        
        # handleEvent(Event{ EventType::eOutputAdded, EventEmpty{} });
        #self.outputAdded.emit(EventProps({'outputId':output.id()}))
        #self.events().outputAdded.emit(EventProps({'outputId':output.id()}))

        #return index;
        return output.id()  

    #void Element::setOutputName(uint8_t const a_output, std::string const &a_name)
    def setOutputName(self, outputId:int,name:str):
        tout = self.outputs().by('id',outputId)
        OLD_NAME = tout.name()
        if (OLD_NAME == name): 
            return
        
        #m_outputs[a_output].name = a_name;
        tout.setName(name)

        #handleEvent(Event{ EventType::eIONameChanged, EventIONameChanged{ OLD_NAME, a_name, a_output, false } });
        self.ioNameChanged.emit(EventIONameChanged(OLD_NAME, name, outputId, False))


    def removeOutput(self):
        #m_outputs.pop_back();
        #handleEvent(Event{ EventType::eOutputRemoved, EventEmpty{} });
        tout = self.outputs().last()
        self.nodes().remove(tout)
        #handleEvent(Event{ EventType::eInputRemoved, EventEmpty{} });
        self.events().outputRemoved.emit(EventProps({'outputId':tout.id()}))

    def clearOutputs(self):
        #m_inputs.clear();
        self.nodes().clearBy('ioType',IoType.OUTPUT)

    def setIOName(self, isInput:bool, id:int, name:str):
        if (isInput):
            self.setInputName(id, name)
        else:
            self.setOutputName(id, name)

    def setIOValueType(self, isInput:bool, id:int, valueType:ValueType):
        #io = a_input ? m_inputs[a_id] : m_outputs[a_id];
        io = self.nodes().by('id',id)
        #OLD_TYPE = io.prop('valueType')
        #if OLD_TYPE == None: # let's try deduct from size
        #    OLD_TYPE = self._valueTypeFromSize(io.size())

        #if (OLD_TYPE == valueType): 
        #    return
        tsize = self._tsizeFromValueType(valueType)
        osize = io.size()
        if (tsize == osize):
            return

        io.setSize(tsize)

        #io.type = a_type;
        self.resetIOSocketValue(io)

        #handleEvent(Event{ EventType::eIOTypeChanged, EventIOTypeChanged{ a_input, a_id, OLD_TYPE, a_type } });
        self.events().ioTypeChanged.emit(EventIOTypeChanged(isInput, id, osize, tsize ))


    #def connect(self, sourceId:int, outputId:int, outputFlags, inputId:int, inputFlags):
    def connect(self, fr, to):
        #sourceId = None
        #outputId = None
        #inputId = None
        #inputFlags = None
        #outputFlags = None
        #return self.m_package.connect(sourceId, outputId, outputFlags, self.m_id, inputId, inputFlags)
        return self.m_package.connect(self, fr, to)

 

    def init(self,**kwargs):    
        pass

    def open(self,**kwargs):    
        pass

    def calc(self,**kwargs):    
        pass



