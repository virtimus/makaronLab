import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg

import threading

from ...ModuleFactory import IoType, ModuleFactory, ModuleImplBase, ModuleType

from .ModuleImplElement import ModuleImplElement

from ...ionodeflags import IoNodeFlags

from ...q3vector import Q3Vector
#from ...Module import Module

#using Elements = std::vector<Element *>;
#Elements = Q3Vector() #'Module' ModuleIMpl

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
'''
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

    
Connections = Q3Vector(Connection)
'''
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
        self.m_elements = Q3Vector()
        #self.m_connections = Connections
        #std::vector<size_t> m_free{};
        #self.m_dependencies = Q3Vector(Q3Vector)
        self.m_free = Q3Vector(int)
        self.m_dispatchThread = threading.Thread()
        self.m_dispatchThreadStarted = AtomicBool(False)
        self.m_quit = AtomicBool(False)
        self.m_pause = AtomicBool(False)
        self.m_paused = AtomicBool(False)
        self.m_pauseCount = AtomicInt(0)
        self.m_isExternal = False
        #self.m_elements.push_back(self._self)
        #self.setDefaultNewInputFlags(IoNodeFlags.defaultFlags)
        #self.setDefaultNewOutputFlags(IoNodeFlags.defaultFlags)

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
    
    #def connections(self):
    #    return self.m_connections

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

    def calc(self):
        els = self.m_elements.values()
        if self.m_elements.size()>0:
            el = self.m_elements.first()
            if el.view() == None: #3d level and down - calculate recursive
                self.calculate()
        #print(f'{els}')

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

    def connect(self, fr, to): #IoNodeView to IoNodeView
        #self.connectById(fr.id(),to.id()) 
        #def connectById(self, sourceId, targetId):
        self.pauseDispatchThread()
        sourceId = fr.id()
        targetId = to.id()
        sourceModuleId = fr.moduleId()
        targetModuleId = to.moduleId()
        self.resumeDispatchThread()
        return True

    def disconnect(self, sourceModuleId, sourceId, targetModuleId, targetId):
        self.pauseDispatchThread()
        targetIoNode = self.mdl().graphModule().nodes().byLid(targetId)
        targetIoNode.setDriveSignal(None)
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
        

