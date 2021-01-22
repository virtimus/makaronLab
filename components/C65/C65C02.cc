#include "C65.h"
#include "C65C02.h"


#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"
//##include "cpu/fake6502.h"
//#include <vendor/x16/debugger.h>
#ifdef C65_C65C02_CHIPS

	#define CHIPS_IMPL
	#include <vendor/chips/chips/m6502.h>

	#define T(b) ASSERT_TRUE(b)
	#define R(r) cpu.r

	static m6502_t cpu;
	static uint64_t pins;
	static uint8_t RAM[1<<16] = { 0 };
	static m6502_desc_t cpu_desc{};

	static void w8(uint16_t addr, uint8_t data) {
	    RAM[addr] = data;
	}

	static void w16(uint16_t addr, uint16_t data) {
	    RAM[addr] = data & 0xFF;
	    RAM[(addr+1)&0xFFFF] = data>>8;
	}

	static uint16_t r16(uint16_t addr) {
	    uint8_t l = RAM[addr];
	    uint8_t h = RAM[(addr+1)&0xFFFF];
	    return (h<<8)|l;
	}

	static uint8_t r8(uint16_t addr) {
		return RAM[addr];
	}

	static void init(void) {
	    memset(RAM, 0, sizeof(RAM));
	    pins = m6502_init(&cpu, &cpu_desc/*&(m6502_desc_t){0}*/);
        //setBit(pins
	    cpu.S = 0xBD;   // perfect6502 starts with S at C0 for some reason
	    cpu.P = M6502_ZF|M6502_BF|M6502_IF;
	}

	static void prefetch(uint16_t pc) {
	    pins = M6502_SYNC;
	    M6502_SET_ADDR(pins, pc);
	    M6502_SET_DATA(pins, RAM[pc]);
	    cpu.PC = pc;
	}

	static void copy(uint16_t addr, uint8_t* bytes, size_t num) {
	    assert((addr + num) <= sizeof(RAM));
	    memcpy(&RAM[addr], bytes, num);
	}

	static void tick(void) {
	    pins = m6502_tick(&cpu, pins);
	    const uint16_t addr = M6502_GET_ADDR(pins);
	    if (pins & M6502_RW) {
	        /* memory read */
	        uint8_t val = RAM[addr];
	        M6502_SET_DATA(pins, val);
	    }
	    else {
	        /* memory write */
	        uint8_t val = M6502_GET_DATA(pins);
	        RAM[addr] = val;
	    }
	}

	static uint32_t step(void) {
	    uint32_t ticks = 0;
	    do {
	        tick();
	        ticks++;
	    } while (0 == (pins & M6502_SYNC));
	    return ticks;
	}

#else //C65_C65C02_CHIPS

	#include <vendor/x16/cpu/fake6502.h>
	//#include "fake6502.h"
	#include <vendor/x16/memory.h>
	#include <vendor/x16/glue.h>
	extern "C" uint8_t read6502(uint16_t address);
#endif //C65_C65C02_CHIPS

uint8_t ROM[32768];

C65C02::C65C02 * singleton_C65C02;

namespace C65C02 {

C65C02::C65C02() : C65{}
{
	  singleton_C65C02 = this;


	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
	  //singleton = this;
	  //singleton = this;
	  //setMinInputs(32);
	  //setMaxInputs(32);
	  //setMinOutputs(32);
	  //setMaxOutputs(32);
/*


	addInput(spaghetti::ValueType::eBool, "VPB(o)", IOSocket::eCanHoldBool,SocketItemType::eOutput);
	addInput(spaghetti::ValueType::eBool, "RDY(i)", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "PHI1O(o)", IOSocket::eCanHoldBool,SocketItemType::eOutput);
	addInput(spaghetti::ValueType::eBool, "IRQB(i)", IOSocket::eCanHoldBool); //low = interrupt request
	addInput(spaghetti::ValueType::eBool, "MLB(o)", IOSocket::eCanHoldBool,SocketItemType::eOutput);// memory lock
	addInput(spaghetti::ValueType::eBool, "NMIB(i)", IOSocket::eCanHoldBool);// non masked interrupt
	addInput(spaghetti::ValueType::eBool, "SYNC(o)", IOSocket::eCanHoldBool,SocketItemType::eOutput);
	addInput(spaghetti::ValueType::eBool, "VDD", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A0", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A1", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A2", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A3", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A4", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A5", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A6", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A7", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A8", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A9", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A10", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A11", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A12", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A13", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A14", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A15", IOSocket::eCanHoldBool,SocketItemType::eDynamic);
	addInput(spaghetti::ValueType::eBool, "A16", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A17", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A18", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A19", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A20", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A21", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A22", IOSocket::eCanHoldBool);
	addInput(spaghetti::ValueType::eBool, "A23", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "RESB(i)", IOSocket::eCanHoldBool,SocketItemType::eInput);// reset
	addOutput(spaghetti::ValueType::eBool, "PHI2O", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "SOB(i)", IOSocket::eCanHoldBool,SocketItemType::eInput);//high stack overflow
	addOutput(spaghetti::ValueType::eBool, "PHI2(i)", IOSocket::eCanHoldBool,SocketItemType::eInput);// clock input
	addOutput(spaghetti::ValueType::eBool, "BE(i)", IOSocket::eCanHoldBool,SocketItemType::eInput);//!!! high = bus (A/D) enable
	addOutput(spaghetti::ValueType::eBool, "NC", IOSocket::eCanHoldBool);// no connect
	addOutput(spaghetti::ValueType::eBool, "RWB(o)", IOSocket::eCanHoldBool);//read/write signal for ds (high - Dx is input)
	addOutput(spaghetti::ValueType::eBool, "D0", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D1", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D2", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D3", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D4", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D5", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D6", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D7", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D8", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D9", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D10", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "D11", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "D12", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "D13", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "D14", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "D15", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP0", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP1", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP2", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP3", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP4", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP5", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP6", IOSocket::eCanHoldBool);
    addOutput(spaghetti::ValueType::eBool, "NP7", IOSocket::eCanHoldBool);
	addOutput(spaghetti::ValueType::eBool, "VSS", IOSocket::eCanHoldBool);*/
#ifdef C65_C65C02_CHIPS
	init();
#else
	memory_init();
#endif

  }

  //char const *type() const noexcept override { return TYPE; }
  //spaghetti::string::hash_t hash() const noexcept override { return HASH; }





void C65C02::calculate()
  {
	  bool pinPHI2prev = _pins.getPin(CPins::PHI2);//.index
	  //package()->consoleAppend("Hello from C65C02");

	  inpToPins(CPins::all);

	  //m_inputs[CPins::RDY].value = !std::get<bool>(m_inputs[CPins::RDY].value);
	  //inpToPin(CPins::RDY);
	  //inpToPin(CPins::A23);
	  //inpToPin(CPins::RESB);
	  //inpToPin(CPins::PHI2);

	  bool pinPHI2 = _pins.getPin(CPins::PHI2);
	  bool clockDelta =(pinPHI2 != prevClock);
	  bool clockRise = (pinPHI2 && !prevClock);
	  prevClock = pinPHI2;
	  bool pinRDY = _pins.getPin(CPins::RDY);
	  bool pinRESB = _pins.getPin(CPins::RESB);
	  bool resetRise = (pinRESB && !prevResb);
	  if (resetRise){
		  //C65::consoleAppendF("C65C02: pin RESB rise - ===RESET=== ...",NULL);
		  // full reset sequence as shown for 6520C
#ifdef C65_C65C02_CHIPS
		  //set reset PIN in m6502
          auto bp = M6502_PIN_RES;
          setBit(pins,bp);
#else //C65_C65C02_CHIPS
		  read6502(0xec3f);
		  read6502(0xec3f);
		  read6502(0xffff);
		  read6502(0xec3f);
		  read6502(0x0145);
		  read6502(0x0144);
		  read6502(0x0143);
		  reset6502();
#endif//C65_C65C02_CHIPS
	  }
	  prevResb = pinRESB;
	  bool pinA23 = _pins.getPin(CPins::A23);
	  bool outRESB = std::get<bool>(m_outputs[0].value);
	  //spaghetti::log::info("pin PHI2 is:{}",pinPHI2);
	  //spaghetti::log::info("pin RDY is:{}",pinRDY);
	  //spaghetti::log::info("pin RESB is:{}",pinRESB);
	  //spaghetti::log::info("pin A23 is:{}",pinA23);
	  ///spaghetti::log::info("RESBOut is:{}",outRESB);
	  if (pinRDY){
		  if (clockRise/*clockDelta*/){
			  C65::consoleAppendF("C65C02: pin PHI2 is:{}",pinPHI2);
			  spaghetti::log::info("C65C02: next processing step...");
#ifdef C65_C65C02_CHIPS

		pins = m6502_tick(&cpu, pins);
		const uint16_t addr = M6502_GET_ADDR(pins);
        uint8_t val;

		if (pins & M6502_RW) { /* memory read */

            val = RAM[addr];

			if (getBit(addr,15)==1){// read ROM
				uint16_t taddr = addr;
				clearBit(taddr,15);
				val=ROM[taddr];
			}

			//spaghetti::log::info("{} {} {} {} {}",getBinStr(address),getBinStr(*value),getHexStr(address),"r",getHexStr(*value));
			consoleAppendF("onRead6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"r",getHexStr(val).c_str());

			M6502_SET_DATA(pins, val);
		}
		else { /* memory write */

            val = M6502_GET_DATA(pins);

			consoleAppendF("onWrite6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"W",getHexStr(val).c_str());

			RAM[addr] = val;
		}
        int ind = CPins::A0.index;
        for (int i=0;i<16;i++){
            bool bit = (getBit(addr,i)==1);
            _pins.setPin(ind+i,bit);
        }
        ind = CPins::D0.index;
        for (int i=0;i<16;i++){
             bool bit = (getBit(val,i)==1);
             _pins.setPin(ind+i,bit);
         }

        //std::transform(str.begin(), str.end(),str.begin(), ::toupper);

#else //C65_C65C02_CHIPS
			  step6502();
#endif //C65_C65C02_CHIPS
		  } else {
			  //spaghetti::log::info("C65C02: waiting clock tick...");
		  }
	  } else {
		  // halted state
		  spaghetti::log::info("C65C02: in HALTED state.");
	  }
	  /*bool allSets{ true };
	  int i=0;
	  for (auto &input : m_inputs) {
	    bool const VALUE{ std::get<bool>(input.value) };
	    if (!VALUE) {
	        //allSets = false;
	    	m_outputs[i].value=false;
	      //break;
	    } else {
	    	//allSets = true;
	    	m_outputs[i].value=true;
	    }
	    i++;
	  }*/

	  //m_outputs[0].value = allSets;

	  pinsToOut(CPins::all);

  }



} //namespace C65C02






