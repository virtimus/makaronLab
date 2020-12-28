

enum class ValueType { eBool, eInt, eFloat, eByte, eWord64 };//IoType
enum class SocketItemType { eInput, eOutput, eDynamic };//SiType
enum class IOSocketsType { eInputs, eOutputs, eTop, eDown};//IoSide
enum class EOrientation { eRight, eLeft, eUp, eDown };//TBD

Element -> GItem
Package -> Graph -> GView/GVItem
m_inputs/m_outputs -> pins
m_connections -> signal/edges

.package - > .mlg