#pragma once
#ifndef CHIPS_CHIPS_H
#define CHIPS_CHIPS_H

#include <cstdlib>
#include <iostream>
#include <string>
#include <memory>
#include <string>
#include <stdexcept>

#include "spaghetti/element.h"
#include "spaghetti/logger.h"
#include <spaghetti/vendor/spdlog/spdlog.h>
#include <spaghetti/vendor/spdlog/fmt/fmt.h>

#include "makaron/api.h"

extern "C" {
	#define CHIPSCPC_IMPL
	#include "api.h"
}


/// some basic defines
/*#define C65_C65C02_CHIPS // 6502 chips implementation
#define CHECK_BIT(var,pos) ((var) & (1<<(pos)))

// some global funcs
short getBit(uint16_t value, short bitPos);
void clearBit(uint16_t &value, short bitPos);
void setBit(uint16_t &value, short bitPos);
void setBit(uint64_t &value, short bitPos);
std::string getBinStr(uint16_t value);
std::string getBinStr(uint8_t &value);
std::string getHexStr(uint16_t value);
std::string getHexStr(uint8_t value);

struct C65Pin {
  size_t index;// index on internal list
  std::string name;
  spaghetti::IOSocketsType ioSide;
  spaghetti::SocketItemType siType;
  spaghetti::ValueType ioType;
  std::string nameIO(){return name + ((siType == spaghetti::SocketItemType::eOutput)?"(o)":((siType == spaghetti::SocketItemType::eDynamic)?"(d)":"(i)"));}
 /* C65Pin(short a, std::string b,spaghetti::IOSocketsType c, spaghetti::SocketItemType d) :
	  index(a),
	  name(b),
	  ioType(c),
	  sItemType(d)
  {}* /
};





class C65Pins {
private:
	uint64_t newPins = 0;
	uint64_t oldPins = 0;
	uint64_t tmpPins = 0;



public:
    uint64_t tmpPinsG(){
        return tmpPins;
    }
    void tmpPinsS(uint64_t nVal){
    	tmpPins = nVal;
    }
	bool getPin(short bit){
        short v = getPinS(bit);
		return (v!=0);
	}

	short getPinS(short bit){
		return (tmpPins >> bit) & 1U;
	}

	void setPin(short bit, bool high){
		if (high){
			tmpPins |= 1UL << bit;
		} else {
			tmpPins &= ~(1UL << bit);
		}
	}

	void setPin(C65Pin pin, bool high){
		setPin(pin.index,high);
	}

	bool getPin(C65Pin pin){
		return getPin(pin.index);
	}

	short getPinS(C65Pin pin){
		return getPinS(pin.index);
	}

	void begin(){
		tmpPins = 0;
	}
	void commit(){
		oldPins = newPins;
		newPins = tmpPins;
		tmpPins = newPins;
	}
	void rollback(){
		tmpPins = newPins;
	}


};*/

namespace makaron::chips {

	template<typename ... Args>
	std::string formatS( const std::string& format, Args ... args ){
                fmt::MemoryWriter raw;

                raw.write(format, args ...);
		return raw.c_str();
	}

#define CHIPS_HASH_DEFS   static constexpr makaron::string::hash_t const HASH{ makaron::string::hash(TYPE) }; char const *type() const noexcept override { return TYPE; }; makaron::string::hash_t hash() const noexcept override { return HASH; }

class Chips : public makaron::GItem {
public:
	using SocketItemType = spaghetti::SocketItemType;
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;

	Chips();

};

} //namespace makaron::chips

#endif // CHIPS_CHIPS_H
