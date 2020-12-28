#pragma once
#ifndef C65_W64_H
#define C65_W64_H

#include "C65.h"

namespace W64 {
	//using SiType = spaghetti::SocketItemType;
	//using IoType = spaghetti::IOSocketsType;
	//using VlType = spaghetti::ValueType;
	using IoValue = spaghetti::Element::Value;

	using Word64 = uint64_t;
	using Word32 = uint32_t;
	using Word16 = uint16_t;
	using Byte = uint8_t;
	using Bit = bool;

    namespace IoSide {
        static const auto Left =  spaghetti::IOSocketsType::eInputs;
        static const auto Right = spaghetti::IOSocketsType::eOutputs;
        static const auto Top = spaghetti::IOSocketsType::eTop;
        static const auto Down = spaghetti::IOSocketsType::eDown;
    }

    namespace IoType {
        static const auto Bool = spaghetti::ValueType::eBool;
        static const auto Word32 = spaghetti::ValueType::eInt;
        static const auto Float = spaghetti::ValueType::eFloat;
        static const auto Byte = spaghetti::ValueType::eByte;
        static const auto Word64 = spaghetti::ValueType::eFloat;
    }

    namespace SiType {// to be removed
        static const auto Input =  spaghetti::SocketItemType::eInput;
        static const auto Output =  spaghetti::SocketItemType::eOutput;
    	static const auto Dynamic =  spaghetti::SocketItemType::eDynamic;
    }

	class W64 : public C65 {
	public:
		W64();

		IoValue pinValue(const C65Pin pin);
		Word64 pinValueAsWord64(const C65Pin pin);
		void pinValueSet(const C65Pin pin, IoValue value);
	};

}



#endif // C65_W64_H
