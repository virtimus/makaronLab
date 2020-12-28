#include "W64.h"

namespace W64 {

W64::W64() :C65::C65{}
{

}


IoValue W64::pinValue(const C65Pin pin){
    size_t ioIndex = ioIndexes[pin.index];
    if (pin.ioSide == IoSide::Left){
    	return m_inputs[ioIndex].value;
    } else {
    	return m_outputs[ioIndex].value;
    }
}

Word64 W64::pinValueAsWord64(const C65Pin pin){
	IoValue value = pinValue(pin);

	return std::get<Word64>(value);
}

void W64::pinValueSet(const C65Pin pin, IoValue value){
    size_t ioIndex = ioIndexes[pin.index];
    if (pin.ioSide == IoSide::Left){
    	m_inputs[ioIndex].value = value;
    } else {
    	m_outputs[ioIndex].value = value;
    }
}

} //namespace W64
