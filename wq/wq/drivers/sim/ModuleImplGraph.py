import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

import threading

from ...ModuleFactory import IoType, ModuleFactory, ModuleImplBase, ModuleType

from .ModuleImplElement import ModuleImplElement

from .ionodeflags import IoNodeFlags

from ...wqvector import WqVector
#from ...Module import Module

#using Elements = std::vector<Element *>;
Elements = WqVector() #'Module' ModuleIMpl

"""
struct Connection {
    size_t from_id{};
    uint8_t from_socket{};
    uint8_t from_flags{};
    size_t to_id{};
    uint8_t to_socket{};
    uint8_t to_flags{};
};
"""
class Connection:
    def __init__(self, frModId, frId, toModId, toId):
        self._frModId = frModId
        self._frId = frId
        self._toModId = toModId
        self._toId = toId

    def sourceModuleId(self):
        return self._frModId

    def sourceId(self):
        return self._frId

    def targetModuleId(self):
        return self._toModId

    def targetId(self):
        return self._toId

    
Connections = WqVector(Connection)

from ...Timer import Timer

class AtomicBool():
    def __init__(self, value:bool=False):
        self._value = value

    def __nonzero__(self):
        return self._value

    def __assign__(self, other):
        self._value = other

    def on(self, val:bool=None):
        if val != None:
            self._value = val
        return self._value 




class AtomicInt(int):
    
    def inc(self):
        self = self+1

    def dec(self):
        self = self-1

#just package (not node)
class ModuleImplGraph(ModuleImplElement):
    #Package();
    #~Package() override;
    def __init__(self, **kwargs):
        #self._name = None (s)
        super(ModuleImplGraph, self).__init__(**kwargs)
        self.m_delta = None
        self.m_packageDescription = 'A package'
        self.m_inputsPosition = qtc.QPointF(-400.0, 0.0)
        self.m_outputsPosition = qtc.QPointF(400.0, 0.0)
        self.m_packagePath = ''
        self.m_packageIcon = ':/unknown.png'
        self.m_elements = Elements
        self.m_connections = Connections
        #std::vector<size_t> m_free{};
        self.m_dependencies = WqVector(WqVector)
        self.m_free = WqVector(int)
        self.m_dispatchThread = threading.Thread()
        self.m_dispatchThreadStarted = AtomicBool(False)
        self.m_quit = AtomicBool(False)
        self.m_pause = AtomicBool(False)
        self.m_paused = AtomicBool(False)
        self.m_pauseCount = AtomicInt(0)
        self.m_isExternal = False
        #self.m_elements.push_back(self._self)
        self.setDefaultNewInputFlags(IoNodeFlags.defaultFlags)
        self.setDefaultNewOutputFlags(IoNodeFlags.defaultFlags)

    def __del__(self):
        #SIZE = self.m_elements.size()
        for lid in self.m_elements:
            el = self.m_elements.removeByLid(lid,noIndexUpdate=True)
            del el

    #void consoleAppend(char *text);

    #void calculate() override;
    def update(self, delta): #duration_t const &a_
        self._delta = delta

    def packageDescription(self):
        return self.m_packageDescription

    def setPackageDescription(self, description):
        self.m_packageDescription = description


    def packagePath(self):
        return self.m_packagePath
    
    def setPackagePath(self, path):
        self.m_packagePath = path

    def packageIcon(self):
        return self.m_packageIcon

    def setPackageIcon(self, icon):
        self.m_packageIcon = icon
        
    #Element *add(char const *const a_name) { return add(string::hash(a_name)); }
    #Element *add(string::hash_t const a_hash);

    #void remove(Element *const a_element) { remove(a_element->id()); }
    #void remove(size_t const a_id);

    #Element *get(size_t const a_id) const;

    #bool connect(size_t const a_sourceId, uint8_t const a_sourceSocket, uint8_t const a_sourceFlags, size_t const a_targetId,
    #          uint8_t const a_targetSocket, uint8_t const a_targetFlags);
    #bool disconnect(size_t const a_sourceId, uint8_t const a_outputId,  uint8_t const a_outputFlags, size_t const a_targetId, uint8_t const a_inputId, uint8_t const a_inputFlags);

    #void dispatchThreadFunction();

    #void startDispatchThread();
    #void quitDispatchThread();
    #void pauseDispatchThread();
    #void resumeDispatchThread();

    #void setInputsPosition(double const a_x, double const a_y);
    def setInputsPosition(self, position):
        self.m_inputsPosition = position

    def inputsPosition(self):
        return self.m_inputsPosition

    #void setOutputsPosition(double const a_x, double const a_y);
    def setOutputsPosition(self, position):
        self.m_outputsPosition = position

    def outputsPosition(self):
        return self.m_outputsPosition

    def elements(self):
        return self.m_elements
    
    def connections(self):
        return self.m_connections

    #void open(std::string const &a_filename);
    #void save(std::string const &a_filename);
    #static Registry::PackageInfo getInfoFor(std::string const &a_filename);

    #if PACKAGE_MAP == PACKAGE_SPP_MAP
    #  using Callbacks = spp::sparse_hash_map<size_t, std::vector<size_t>>; !TODO!
    #elif PACKAGE_MAP == PACKAGE_STD_UNORDERED_MAP
    #  using Callbacks = std::unordered_map<size_t, std::vector<size_t>>;
    #endif
    #Callbacks m_dependencies{};

    def setInputsPosition(self,x, y):
        self.m_inputsPosition.x = x
        self.m_inputsPosition.y = y

    def setOutputsPosition(self, x, y):
        self.m_outputsPosition.x = x
        self.m_outputsPosition.y = y

# --- HDR-END -------------------------------------

    def calculate(self):
        '''
        for connection in self.m_connections.values():
            #Element *const source{ get(connection.from_id) };
            sourceIoNode = self.get(connection.frId) 
            #Element *const target{ get(connection.to_id) };
            targetIoNode = self.get(connection.toId)
            #auto const IS_SOURCE_SELF = connection.from_id == 0;
            IS_SOURCE_SELF = sourceIoNode.parent().mType() in [ModuleType.INPUTS, ModuleType.OUTPUTS]
            #auto const IS_TARGET_SELF = connection.to_id == 0;
            IS_TARGET_SELF = targetIoNode.parent().mType() in [ModuleType.INPUTS, ModuleType.OUTPUTS]
            #auto const &SOURCE_IO =  IS_SOURCE_SELF || connection.from_flags != 2  ? source->inputs() : source->outputs();
            #auto &targetIO =  IS_TARGET_SELF || connection.to_flags == 2 ? target->outputs() : target->inputs();
            #targetIO[connection.to_socket].value = SOURCE_IO[connection.from_socket].value;
            if (sourceIoNode.driveSignal()!=None):
                targetIoNode.driveSignal().setValue(sourceIoNode.driveSignal().value())
        '''

        for node in self.mdl().nodes().values():
            ds = node.driveSignal()
            if ds != None and node.signals().size()>0:
                dv = ds.value()
                for ss in node.signals().values():
                    ss.setValue(dv)
            elif ds == None and node.signals().size()>0: #this means disconnected == False
                dv = False
                for ss in node.signals().values():
                    ss.setValue(dv)

        for element in self.m_elements.values():
            if (element == None or element == self._self):
                continue
            element.updateTiming(self.m_delta)
            element.calculate()

    def add(self, el:'Module'):
        self.pauseDispatchThread()
        if el == None:
            self.raiseExc('Cannot add None element')
        self.m_elements.append(el.id(),el)
        el.impl().m_package = self
        el.impl().m_id = el.id() #element->m_id = index;
        el.impl().reset()
        #element->reset();

        self.resumeDispatchThread()
        return el

    def remove(self, lid):
        self.pauseDispatchThread()
        el = self.m_elements.removeByLid(lid)
        del el
        self.resumeDispatchThread()

    def get(self, lid):
        result = self.m_elements.byLid(lid)
        assert result != None,  f'Element with lid:{lid} not found'
        return result

    def findConnections(self, sourceModuleId, sourceId, targetModuleId, targetId) -> WqVector:
        result = self.m_connections.filterBy('targetModuleId',targetModuleId)
        if result.size()==0:
            return result
        result = result.filterBy('targetId',targetId)
        if result.size() == 0:
            return result
        result = result.filterBy('sourceModuleId',sourceModuleId)
        if result.size() == 0:
            return result
        result = result.filterBy('sourceId',sourceId)    
        return result

    #bool Package::connect(size_t const a_sourceId, uint8_t const a_sourceSocket, uint8_t const a_sourceFlags, size_t const a_targetId,
    #                  uint8_t const a_targetSocket, uint8_t const a_targetFlags)

    def connect(self, fr, to): #IoNodeView to IoNodeView
        #self.connectById(fr.id(),to.id()) 
        #def connectById(self, sourceId, targetId):
        self.pauseDispatchThread()
        sourceId = fr.id()
        targetId = to.id()
        sourceModuleId = fr.moduleId()
        targetModuleId = to.moduleId()
        #sourceIoNode = self.get(sourceId)
        #targetIoNode = self.get(targetId)
        #log.info("Connecting source: {}@{}@{} to target: {}@{}@{}", a_sourceId, static_cast<int>(a_sourceSocket),static_cast<int>(a_sourceFlags),
        #                a_targetId, static_cast<int>(a_targetSocket),static_cast<int>(a_targetFlags));


        #bool isSourcePackage = (str1.compare(source->type())==0) && !source->isRoot();

        #//auto const &SOURCE =  sourceFlags == 2 && a_sourceId != 0 ? source->m_outputs : source->m_inputs;
        #//auto const &SOURCE = (isSourcePackage && a_sourceId != 0) || (sourceFlags != 2 && a_sourceId != 0) ? source->m_outputs : source->m_inputs;
        #auto const &SOURCE =  a_sourceId == 0  ?  source->m_inputs : source->m_outputs;
        #//a_targetId != 0 &&
        #uint8_t  targetFlags = a_targetFlags;
        #/*if (str1.compare(target->type())==0) {
        #targetFlags = ( a_targetFlags == 2 )?1:2;
        #}*/

        #//bool isTargetPackage = (str1.compare(target->type())==0) && !target->isRoot();

        #//auto &TARGET = (isTargetPackage && a_targetId != 0) || (targetFlags != 2 && a_targetId != 0) ? target->m_inputs : target->m_outputs;
        #auto &TARGET = a_targetId == 0 ? target->m_outputs : target->m_inputs ;
        #auto const SOURCE_SIZE = SOURCE.size();
        #auto const TARGET_SIZE = TARGET.size();
        #assert(a_sourceSocket < SOURCE_SIZE && "Socket ID don't exist");
        #assert(a_targetSocket < TARGET_SIZE && "Socket ID don't exist");

        #TARGET[a_targetSocket].id = a_sourceId;
        #TARGET[a_targetSocket].slot = a_sourceSocket;
        #TARGET[a_targetSocket].inFlags = sourceFlags;

        #spaghetti::log::info("Notifying {}({})@{} when {}({})@{} changes..", a_targetId, target->name(),
        #                static_cast<int32_t>(a_targetSocket), a_sourceId, source->name(),
        #                static_cast<int32_t>(a_sourceSocket));
        cons = self.findConnections(sourceModuleId, sourceId, targetModuleId, targetId)
        assert cons.size() == 0,'Already connected ({sourceId},{targetId})'
        nConnection = Connection(sourceModuleId, sourceId, targetModuleId, targetId)
        self.m_connections.push_back(nConnection)
        #auto &dependencies = m_dependencies[a_sourceId];
        #auto const IT = std::find(std::begin(dependencies), std::end(dependencies), a_targetId);
        #if (IT == std::end(dependencies)) dependencies.push_back(a_targetId);
        dependencies = self.m_dependencies.byLid(sourceId)
        if (dependencies == None):
            dependencies = WqVector(int)
        dependencies.push_back(targetId)
        self.resumeDispatchThread()
        return True

    #bool Package::disconnect(size_t const a_sourceId, uint8_t const a_outputId, uint8_t const a_outputFlags,size_t const a_targetId,
    #                     uint8_t const a_inputId, uint8_t const a_inputFlags)
    def disconnect(self, sourceModuleId, sourceId, targetModuleId, targetId):
        self.pauseDispatchThread()
        #Element *const target{ get(a_targetId) };
        #targetIoNode = self.get(targetId)
        targetIoNode = self.mdl().graphModule().nodes().byLid(targetId)
        #spaghetti::log::debug("Disconnecting source: {}@{} from target: {}@{}", a_sourceId, static_cast<int>(a_outputId),
        #                a_targetId, static_cast<int>(a_inputId));
        #auto &targetInput = a_inputFlags != 2 ? target->m_inputs[a_inputId] : target->m_outputs[a_inputId];
        #targetInput.id = 0;
        #targetInput.slot = 0;
        #targetInput.inFlags = 0;
        #self.resetIOSocketValue(targetIoNode)
        targetIoNode.setDriveSignal(None)

        #auto it = std::remove_if(std::begin(m_connections), std::end(m_connections), [=](Connection &a_connection) {
        #return a_connection.from_id == a_sourceId && a_connection.from_socket == a_outputId && a_connection.from_flags == a_outputFlags
    	#	&& a_connection.to_id == a_targetId && a_connection.to_socket == a_inputId && a_connection.to_flags == a_inputFlags;
        #m_connections.erase(it, std::end(m_connections));
        cons = self.findConnections(sourceModuleId, sourceId, targetModuleId, targetId)
        for conLid in cons:
            self.m_connections.removeByLid(conLid)

        #auto &dependencies = m_dependencies[a_sourceId];
        #dependencies.erase(std::find(std::begin(dependencies), std::end(dependencies), a_targetId), std::end(dependencies));
        deps = self.m_dependencies.byLid(sourceId)
        if deps != None:
            self.m_dependencies.remove(deps)

        self.resumeDispatchThread()
        return True


    def dispatchThreadFunction(self):
        #using clock_t = std::chrono::high_resolution_clock;
        #auto const ONE_MILLISECOND = std::chrono::milliseconds(1);
        #auto last = clock_t::now() - ONE_MILLISECOND;
        clock_t = Timer()
        last = clock_t.now() - clock_t.ms(1)
        while not self.m_quit.on():
            NOW = clock_t.now()
            DELTA = NOW - last
            self.update(DELTA)
            self.calculate()

            last = NOW

            WAIT_START = clock_t.now()
            while ((clock_t.now() - WAIT_START) < clock_t.ms(1)):
                #std::this_thread::sleep_for(ONE_MILLISECOND);
                clock_t.sleepMs(1)

            if (self.m_pause.on()):
                self.m_paused.on(True)
                while (self.m_pause.on()):
                    clock_t.sleepMs(0) #std::this_thread::yield();
                self.m_paused.on(False)
                #("Pause stopped..");

    def startDispatchThread(self):
        if (self.m_dispatchThreadStarted.on()):
            return
        #("Starting dispatch thread..");
        self.m_dispatchThread = threading.Thread(target=self.dispatchThreadFunction) #std::thread(&Package::dispatchThreadFunction, this);
        self.m_dispatchThread.start()
        self.m_dispatchThreadStarted.on(True)

    def quitDispatchThread(self):
        if (not self.m_dispatchThreadStarted.on()):
            return
        #("Quitting dispatch thread..");

        if (self.m_pause.on()):
            #("Dispatch thread paused, waiting..");
            while (self.m_pause.on()):
                Timer.sleep(0) #c std::this_thread::yield();

        self.m_quit.on(True)
        if (self.m_dispatchThread.is_alive()):
            #("Waiting for dispatch thread join..");
            self.m_dispatchThread.join(10)
            assert not self.m_dispatchThread.is_alive(), "Problem with stopping dispatchThread"
            #("After dispatch thread join..");
        self.m_dispatchThreadStarted.on(False)

    def pauseDispatchThread(self):
        if (self.m_package != None):
            self.m_package.pauseDispatchThread()
            return
        if (not self.m_dispatchThreadStarted.on()):
            return
        self.m_pauseCount.inc() # self++
        #("Trying to pause dispatch thread ({})..", m_pauseCount.load());
        if (self.m_pauseCount > 1):
            return
        self.m_pause.on(True)
        #("Pausing dispatch thread ({})..", m_pauseCount.load());
        while (not self.m_paused.on()):
            Timer.sleepMs(0) # std::this_thread::yield();


    def resumeDispatchThread(self):
        if (self.m_package != None):
            self.m_package.resumeDispatchThread()
            return
        if (not self.m_dispatchThreadStarted.on()):
            return
        
        self.m_pauseCount.dec(); ###--;
        #("Trying to resume dispatch thread ({})..", m_pauseCount.load());
        if (self.m_pauseCount > 0):
            return
        #("Resuming dispatch thread ({})..", m_pauseCount.load());
        self.m_pause.on(False)

    #def open(std::string const &a_filename)
    def open(self, filename):
        #("Opening package {}", a_filename);
        #std::ifstream file{ a_filename };
        #if (!file.is_open()) return;
        self.pauseDispatchThread()
        #Json json{};
        #file >> json;
        #deserialize(json);
        self.m_isExternal = self.m_package != None
        #("{} Is external: {}", a_filename, m_isExternal);
        self.resumeDispatchThread()

    def save(self, filename):
        #("Saving package {}", a_filename);
        self.pauseDispatchThread()
        #Json json{};
        #serialize(json);
        #std::ofstream file{ a_filename };
        #file << json.dump(2);
        self.resumeDispatchThread()

    #Registry::PackageInfo Package::getInfoFor(std::string const &a_filename)
    def getInfoFor(filename):
        #Registry::PackageInfo type{};
        #std::ifstream file{ a_filename };
        #if (!file.is_open()) return type;
        #Json json{};
        #file >> json;
        #type.filename = a_filename;
        #type.icon = json["package"]["icon"];
        #type.path = json["package"]["path"];
        #return type;
        return None
        

