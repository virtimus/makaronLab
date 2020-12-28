#include "C65.h"
#include "CAT28C256.h"
#include "C65C02.h"
#include "C65C22.h"
#include "C74LS189.h"
#include "CRPTR.h"
#include "CRPTRNode.h"
#include "CRAM.h"
#include "CDTButton.h"
#include "CDTButtonNode.h"
#include "CRIED.h"
#include "C74LS163A.h"
#include "CCLROM.h"
//#include "ByteToBools.h"
//#include "BoolsToByte.h"
#include "Byte27SD.h"
#include "Byte27SDNode.h"
#include "Word64ToBytes.h"
#include "BytesToWord64.h"
#include "ConstWord64Node.h"
#include "ConstWord64.h"
#include "InfoWord64Node.h"
#include "InfoWord64.h"
#include "InfoByte.h"
#include "InfoByteNode.h"
#include "ConstByte.h"
#include "ConstByteNode.h"
#include "spaghetti/element.h"
#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"

#include "W64RAM.h"

#ifdef C65_C65C02_CHIPS
#else//C65_C65C02_CHIPS
// ====================================================================
// required by current x16 merge -  from main.c
// from main.c
//#include "glue.h"

#include <vendor/x16/glue.h>

bool debugger_enabled = false;
char *paste_text = NULL;
char paste_text_data[65536];
bool pasting_bas = false;
uint16_t num_ram_banks = 64; // 512 KB default
bool log_video = false;
bool log_speed = false;
bool log_keyboard = false;
bool dump_cpu = false;
bool dump_ram = true;
bool dump_bank = true;
bool dump_vram = false;
bool warp_mode = false;
echo_mode_t echo_mode;
bool save_on_exit = true;
gif_recorder_state_t record_gif = RECORD_GIF_DISABLED;
char *gif_path = NULL;
uint8_t keymap = 0; // KERNAL's default

// fake debugger
/*/#include <SDL.h>
extern void DEBUGRenderDisplay(int width,int height){}
extern void DEBUGBreakToDebugger(void){}
extern int  DEBUGGetCurrentStatus(void){return 0;}
extern void DEBUGSetBreakPoint(int newBreakPoint){}
//void DEBUGInitUI(SDL_Renderer *pRenderer){}
extern void DEBUGFreeUI(){}
int showDebugOnRender = 0;*/										// Used to trigger rendering in video.c

//extern "C" void step6502();
//extern "C" void memory_init();

//extern void edConsoleAppend(char *text);
// required by current x16 merge - end ================================
// ====================================================================
#endif//C65_C65C02_CHIPS
extern C65C02::C65C02 * singleton_C65C02;


C65::C65() : spaghetti::Element{}
{

}



void C65::addAllIO(const C65Pin all[]){
	//int size = sizeof(&all);
	int size = getPinsAllSize();
	//spaghetti::log::info("addAllIO size:{}",size);
	for (int i=0;i<size;i++){
        C65Pin p = all[i];
        size_t ioIndex=0;
        if (p.ioSide == ioType::eInputs){
            if (W64::IoType::Word64 == p.ioType){
				ioIndex = addInputS(spaghetti::ValueType::eWord64, p.nameIO(), IOSocket::eCanHoldWord64, p.siType);
            } else if (W64::IoType::Byte == p.ioType){
				ioIndex = addInputS(spaghetti::ValueType::eByte, p.nameIO(), IOSocket::eCanHoldByte, p.siType);
			} else {
				ioIndex = addInputS(spaghetti::ValueType::eBool, p.nameIO(), IOSocket::eCanHoldBool, p.siType);
			}
		} else {
            if (W64::IoType::Word64 == p.ioType){
				ioIndex = addOutputS(spaghetti::ValueType::eWord64, p.nameIO(), IOSocket::eCanHoldWord64, p.siType);
            } else if (W64::IoType::Byte == p.ioType){
				ioIndex = addOutputS(spaghetti::ValueType::eByte, p.nameIO(), IOSocket::eCanHoldByte, p.siType);
			} else {
				ioIndex = addOutputS(spaghetti::ValueType::eBool, p.nameIO(), IOSocket::eCanHoldBool, p.siType);
			}
		}
        p.index = ioIndexes.size();
        ioIndexes.push_back(ioIndex);
        //consoleAppendF("p.ioIndex:{}",p.ioIndex);
	}

}

bool C65::isRise(bool pinIN){
    bool  INDelta =(pinIN != _prevInRise);
    bool INRise = (pinIN && !_prevInRise);
    _prevInRise = pinIN;
    return INRise;
}

void C65::inpToPin(const C65Pin pin){
	//inpToPin(pin.index);
	//int size = getPinsAllSize();
	//int hsize = (int)(size/2);

	//spaghetti::log::info("inpToPin:{}:{}:{}",pin.index,size,hsize);
    size_t ioIndex = ioIndexes[pin.index];
    if (pin.ioSide == W64::IoSide::Left){
        if (W64::IoType::Word64 == pin.ioType){
    		//!TODO!
        } else if (W64::IoType::Byte == pin.ioType){
    		//!TODO!
    	} else {
    		_pins.setPin(pin.index, std::get<bool>(m_inputs[ioIndex].value));
    	}

	} else {
		//int ind = pin.index-hsize;
		//spaghetti::log::info("ind:{}",ind);
        if (W64::IoType::Word64 == pin.ioType){
    		//!TODO!
        } else if (W64::IoType::Byte == pin.ioType){
    		//!TODO!
    	} else {
    		_pins.setPin(pin.index, std::get<bool>(m_outputs[ioIndex].value));
    	}

	}
}

void C65::pinToOut(const C65Pin pin){
	//inpToPin(pin.index);
	///int size = getPinsAllSize();
	//int hsize = (int)(size/2);
    size_t ioIndex = ioIndexes[pin.index];
    short c;
	//spaghetti::log::info("inpToPin:{}:{}:{}",pin.index,size,hsize);
    c = _pins.getPin(pin.index);
    bool val = (c == 0) ? false : true;
    if (pin.ioSide == W64::IoSide::Left){
        if (W64::IoType::Word64 == pin.ioType){
    		//!TODO!
        } else if (W64::IoType::Byte == pin.ioType){
    		//!TODO!
    	} else {
    		m_inputs[ioIndex].value = val;
    	}
	} else {
        if (W64::IoType::Word64 == pin.ioType){
    		//!TODO!
        } else if (W64::IoType::Byte == pin.ioType){
    		//!TODO!
    	} else {
    		m_outputs[ioIndex].value = val;
    	}
	}
}

/*todelete!
void C65::inpToPin(short pin){
	  if (pin<32){
		  pins.setPin(pin, std::get<bool>(m_inputs[pin].value));
	  } else {
		  short pini = pin-32;
		  pins.setPin(pin, std::get<bool>(m_outputs[pini].value));
	  }
  }*/

void C65::inpToPins(const C65Pin all[]){
	int size = getPinsAllSize();
	for (int i=0;i<size;i++){
		C65Pin p = all[i];
		inpToPin(p);
	}
}

void C65::pinsToOut(const C65Pin all[]){
	int size = getPinsAllSize();
	for (int i=0;i<size;i++){
		C65Pin p = all[i];
		pinToOut(p);
	}
}

/*template<typename ... Args>
void C65::consoleAppendF( const std::string& format, Args ... args )
  {
	  //spaghetti::log::info(format, args ...);
  / *    size_t size = snprintf( nullptr, 0, format.c_str(), args ... ) + 1; // Extra space for '\0'
      if( size <= 0 ){ throw std::runtime_error( "Error during formatting." ); }
      std::unique_ptr<char[]> buf( new char[ size ] );
      snprintf( buf.get(), size, format.c_str(), args ... );
      std::string str = std::string( buf.get(), buf.get() + size - 1 ); // We don't want the '\0' inside
	  //std::string str = string_format(format, args ...);
      char *cstr = new char[str.length() + 1];
      strcpy(cstr, str.c_str());* /

      char buff[300];
      sprintf(buff,format.c_str(), args ...);

      consoleAppend(buff);
  }*/

// =============================================================
// ============  GLOBAL SCOPE ==================================
// =============================================================


short getBit(uint16_t value, short bitPos){
	short result = (value >> bitPos) & 1U;
	return result;
}

void clearBit(uint16_t &value, short bitPos){
	value &= ~(1UL << bitPos);
}

void setBit(uint16_t &value, short bitPos){
	value |= ((uint16_t)1) << bitPos;
}

void setBit(uint64_t &value, short bitPos){
	value |= ((uint64_t)1) << bitPos;
}

std::string getBinStr(uint16_t value){
	  char buff[17];
	  short v;
	  for (int i=0;i<16;i++){
		  v = getBit(value,i);
		  buff[15-i]=(v>0)?'1':'0';
	  }
	  buff[16]='\x0';
	  return buff;
}

std::string getBinStr(uint8_t &value){
	  char buff[9];
	  short v;
	  for (int i=0;i<8;i++){
		  v = getBit(value,i);
		  buff[7-i]=(v>0)?'1':'0';
	  }
	  buff[8]='\x0';
	  return buff;
}

std::string getHexStr(uint16_t value){
	//std::stringstream sstream;
	//sstream << std::setfill('0') << std::setw(4) << std::hex << value;
	char output[6];
	sprintf(output,"%04x",value);
	std::string result = output;
	return result;
	}

std::string getHexStr(uint8_t value){
	//std::stringstream sstream;
	//sstream << std::setfill('0') << std::setw(2) << std::hex << value;
	//std::string result = sstream.str();
	char output[4];
	sprintf(output,"%02x",value);
	std::string result = output;
	return result;
	}

template<typename ... Args>
void cAppF(const std::string& format, Args...args){
	//((spaghetti::elements::logic::C65C02*)c65C02)->test();
	((C65C02::C65C02*)singleton_C65C02)->consoleAppendF(format,args...);
}

extern "C" {

#ifdef C65_C65C02_CHIPS

#else //C65_C65C02_CHIPS

void onRead6502(uint16_t address, uint8_t *value){
	//const char EVENT[] = "onRead6502";
	/*spaghetti::log::info("{}------------",EVENT);
	spaghetti::log::info("{}-adr-dec: {}",EVENT,address);
	spaghetti::log::info("{}-adr-bin: {}",EVENT,getBinStr(address));
	spaghetti::log::info("{}-adr-hex: {}",EVENT,getHexStr(address));
	spaghetti::log::info("{}-val-dec: {}",EVENT,*result);
	spaghetti::log::info("{}-val-bin: {}",EVENT,getBinStr(*result));
	spaghetti::log::info("{}-val-hex: {}",EVENT,getHexStr(*result));*/
	if (getBit(address,15)==1){// read ROM
		uint16_t taddr = address;
		clearBit(taddr,15);
		(*value)=ROM[taddr];
	}

	//spaghetti::log::info("{} {} {} {} {}",getBinStr(address),getBinStr(*value),getHexStr(address),"r",getHexStr(*value));
	cAppF("onRead6502: {} {} {} {} {}",getBinStr(address).c_str(),getBinStr(*value).c_str(),getHexStr(address).c_str(),"r",getHexStr(*value).c_str());


}

void onWrite6502(uint16_t address, uint8_t *value){
	/*const char EVENT[] = "onWrite6502";
	spaghetti::log::info("{}------------",EVENT);
	spaghetti::log::info("{}-adr-dec: {}",EVENT,address);
	spaghetti::log::info("{}-adr-bin: {}",EVENT,getBinStr(address));
	spaghetti::log::info("{}-adr-hex: {}",EVENT,getHexStr(address));
	spaghetti::log::info("{}-val-dec: {}",EVENT,*value);
	spaghetti::log::info("{}-val-bin: {}",EVENT,getBinStr(*value));
	spaghetti::log::info("{}-val-hex: {}",EVENT,getHexStr(*value));*/
	cAppF("onWrite6502: {} {} {} {} {}",getBinStr(address).c_str(),getBinStr(*value).c_str(),getHexStr(address).c_str(),"W",getHexStr(*value).c_str());
}

#endif //C65_C65C02_CHIPS

}

extern "C" SPAGHETTI_API void register_plugin(spaghetti::Registry &a_registry)
{
  //spaghetti::log::init_from_plugin();

  a_registry.registerElement<C65C02::C65C02>("C65C02 (Bool[])", ":/unknown.png");
  a_registry.registerElement<C65C22::C65C22>("C65C22 (Bool[])", ":/unknown.png");
  a_registry.registerElement<C74LS189::C74LS189>("C74LS189 (Bool[])", ":/unknown.png");
  a_registry.registerElement<CRAM::CRAM>("CRAM (Bool[])", ":/unknown.png");
  a_registry.registerElement<CRIED::CRIED>("CRIED (Bool[])", ":/unknown.png");
  a_registry.registerElement<C74LS163A::C74LS163A>("C74LS163A (Bool[])", ":/unknown.png");
  a_registry.registerElement<CAT28C256::CAT28C256>("CAT28C256 (Bool[])", ":/unknown.png");
  a_registry.registerElement<CRPTR::CRPTR,CRPTR::CRPTRNode>("CRPTR - repeater(Bool[])", ":/unknown.png");
  a_registry.registerElement<CDTButton::CDTButton, CDTButton::CDTButtonNode>("Double Toggle Button (Bool)", ":/ui/toggle_button.png");
  a_registry.registerElement<BoolsToByte>("BoolsToByte", ":/unknown.png");
  a_registry.registerElement<ByteToBools>("ByteToBools", ":/unknown.png");
  a_registry.registerElement<CCLROM::CCLROM>("CCLROM", ":/unknown.png");
  a_registry.registerElement<Byte27SD,Byte27SDNode>("Byte27SD", ":/unknown.png");
  a_registry.registerElement<Word64ToBytes>("Word64ToBytes", ":/unknown.png");
  a_registry.registerElement<ConstWord64,ConstWord64Node>("ConstWord64", ":/unknown.png");
  a_registry.registerElement<BytesToWord64>("BytesToWord64", ":/unknown.png");
  a_registry.registerElement<InfoWord64,InfoWord64Node>("InfoWord64", ":/unknown.png");
  a_registry.registerElement<InfoByte,InfoByteNode>("InfoByte", ":/unknown.png");
  a_registry.registerElement<ConstByte,ConstByteNode>("ConstByte", ":/unknown.png");

  a_registry.registerElement<W64::W64RAM>("W64RAM", ":/unknown.png");


}
