#pragma once
#ifndef C65_C65_H
#define C65_C65_H

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



/// some basic defines
#define C65_C65C02_CHIPS // 6502 chips implementation
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
  {}*/
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


};

class C65 : public spaghetti::Element {
protected:
	short pinsAllSize;
    std::vector<size_t> ioIndexes{};
    bool _prevInRise{false};
	C65Pins _pins;
	void setPinsAllSize(short size){ pinsAllSize = size;
	   unsigned short hsize = pinsAllSize/2;
       //setMinInputs(hsize);
       //setMaxInputs(hsize);
       //setMinOutputs(hsize);
       //setMaxOutputs(hsize);
	};
	short getPinsAllSize(){ return pinsAllSize; };
	void addAllIO(const C65Pin all[]);
	//void inpToPin(short pin);
	void inpToPin(const C65Pin pin);
	void inpToPins(const C65Pin all[]);
	void pinToOut(const C65Pin pin);
	void pinsToOut(const C65Pin all[]);
    bool isRise(bool currentSignal);
public:
	using SocketItemType = spaghetti::SocketItemType;
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;

	C65();

	template<typename ... Args>
	void consoleAppendF( const std::string& format, Args ... args )
	  {
	      char buff[300];
	      std::string sformat = format+"\n";
	      //sprintf(buff,format.c_str(), args ...);
	      //auto formatter = std::make_unique<spdlog::pattern_formatter>();
	      //std::stringstream sstr;
	      //std::streambuf sbuf;
	      //sstr << std::format(format,args ...);

	      //outbuf ob;
	      //std::streambuf *sb = std::cout.rdbuf(&sbuf);

	      // do some work here
	      //spaghetti::log::info(format.c_str(), args ...);
	      spdlog::level::level_enum lvl =  spdlog::level::info;
	      const std::string nme = "xx";
	      spdlog::details::log_msg log_msg(&nme, lvl);
	      log_msg.raw.write(sformat, args...);
	      //spdlog::pattern_time_type pattern_time = spdlog::pattern_time_type::local;
	      //auto formatter = std::make_shared<spdlog::pattern_formatter>(format, pattern_time);
	      //formatter->format(log_msg);
	      //std::ostringstream ss;
	      //std::ostream ss;
	      //fmt::print(ss,format,args ...);
	      //ss << log_msg.raw;
	      strcpy(buff, log_msg.raw.c_str());
	      consoleAppend(buff);
	      //consoleAppend(ss.str().c_str());

	      // make sure to restore the original so we don't get a crash on close!
	      //std::cout.rdbuf(sb);
	  }

};


class BoolsToByte final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/BoolsToByte" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  BoolsToByte();

  void calculate() override;
};

class ByteToBools final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/ByteToBools" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  ByteToBools();

  void calculate() override;
};



#endif // C65_C65_H
