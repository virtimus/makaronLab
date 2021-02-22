
eorientation -> direction
package -> graph not! -> Module(ModuleType=GRAPH)
Package -> Graph -> GView/GVItem

Element -> Module(ModuleType=ATOMIC),ModuleBaseIMpl

m_inputs/m_outputs -> IONode,IoNodeIMPL (ioType INPUT/OUTPUT)
m_connections -> signal/nodes
IONodeView
editor -> editor,EditorFrame
package_view -> ModuleView,GraphModuleViewImpl

IOSocket { enum Flags ->IoNodeFlags

ported:
- link_item -> IoLinkView
- socket_item -> IoNodeView
- node -> ModuleViewImpl
toimpl:
- package_view -> GraphViewImpl showproperties itp
- package -> Module(root or GRAPH) -> sim/ModuleImplGraph
- element -> Module(atomic) ModuleImplElement

node/package?






.package - > .mlg

In This simulation framework SIGNAL is the first class citizen ...

Skeleton elements:
- Signal, Module, ModuleFactory
- Simulator, SimulatorEngine

Presentation:
- Editor, ModuleView(expanded mode),

registry -> 
- ModuleFactory
    impl() = spaghetti registry ?, nmigen? kicad?
    _moduleLibraries = {} // by name
    openModule('modulePath',args)
    registerLibrary
- ModuleLibrary

    methods:
        init - initialize library - response - library of module descriptions identified by names/id's
        open - create module by name/id
        insp - inspect
        exit - close library




editor -> 
- Editor
    methods:
        registerFactory - register new factory



packageView(tab) -> 
- ModuleView

element/node/package -> 
- Module(type, n pins(connected with ref to ext signal or disconnected), &m statements/submodules, i internal signals)

    Module.type (native/python/graph, q3c, statement, verilog, kicad etc)
    Module.impl() - low level api access
    methods:
        init
        open
        calc
        insp
        exit


connections (input/output) -> 
- Signal(n pin refs, drivePin, slavePins - only one pin is "drivePin" at a time - rest is slave) 

- SignalValue - long sequence of bits (lib? - bitstream?) 
    SignalValue.impl() = bitstream

simulation processing engine/driver
api:
    init - init factory
        open - open module
            inspect - module current state
            calculate - propagate/calculate signals
        close - close module
    quit - close factory






enum class ValueType { eBool, eInt, eFloat, eByte, eWord64 };//IoType
enum class SocketItemType { eInput, eOutput, eDynamic };//SiType
enum class IOSocketsType { eInputs, eOutputs, eTop, eDown};//IoSide
enum class EOrientation { eRight, eLeft, eUp, eDown };//TBD

