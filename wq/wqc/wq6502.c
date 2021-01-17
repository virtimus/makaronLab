

#include "wq6502.h"

	#define CHIPS_IMPL
	//##include <vendor/chips/chips/m6502.h>
	#include <m6502.h>
	#define T(b) ASSERT_TRUE(b)
	#define R(r) cpu.r

	static m6502_t cpu;
	static uint64_t pins;
	static uint8_t RAM[1<<16] = { 0 };
	static m6502_desc_t cpu_desc;
	bool prevClock = false;
	bool prevResb = false;

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

//namespace wq6502 {


	short C_pins_getPinS(uint64_t pv, short bit){
		return (pv >> bit) & 1U;
		}

	bool C_pins_getPin(uint64_t pv, short bit){
        short v = C_pins_getPinS(pv, bit);
		return (v!=0);
		}	

	short C_getBit(uint64_t value, short bitPos){
		short result = (value >> bitPos) & 1U;
		return result;
		}

	void C_setBit(uint64_t *value, short bitPos){
		(*value) |= ((uint64_t)1) << bitPos;
		}

	void C_clearBit(uint64_t *value, short bitPos){
		(*value) &= ~(1UL << bitPos);
		}

	void C_clearBit16(uint16_t *value, short bitPos){
		(*value) &= ~(1UL << bitPos);
		}

void wq6502_calculate(uint64_t pv){

	//C65Pins _pins;

	//_pins.tmpPinsS(pv);

bool pinPHI2 = C_pins_getPin(pv,CPins_PHI2);
bool clockDelta =(pinPHI2 != prevClock);
bool clockRise = (pinPHI2 && !prevClock);
prevClock = pinPHI2;
bool pinRDY = C_pins_getPin(pv,CPins_RDY);
bool pinRESB = C_pins_getPin(pv,CPins_RESB);
bool resetRise = (pinRESB && !prevResb);
if (resetRise){
	  //C65::consoleAppendF("C65C02: pin RESB rise - ===RESET=== ...",NULL);
	  // full reset sequence as shown for 6520C

	  //set reset PIN in m6502
    auto bp = M6502_PIN_RES;
    C_setBit(&pins,bp);

}
prevResb = pinRESB;
bool pinA23 = C_pins_getPin(pv,CPins_A23);
bool outRESB = C_pins_getPin(pv,CPins_RESB);
//spaghetti::log::info("pin PHI2 is:{}",pinPHI2);
//spaghetti::log::info("pin RDY is:{}",pinRDY);
//spaghetti::log::info("pin RESB is:{}",pinRESB);
//spaghetti::log::info("pin A23 is:{}",pinA23);
///spaghetti::log::info("RESBOut is:{}",outRESB);
if (pinRDY){
	  if (clockRise/*clockDelta*/){
		  //C65::consoleAppendF("C65C02: pin PHI2 is:{}",pinPHI2);
		  //spaghetti::log::info("C65C02: next processing step...");


			pins = m6502_tick(&cpu, pins);
			const uint16_t addr = M6502_GET_ADDR(pins);
			if (pins & M6502_RW) { /* memory read */

				uint8_t val = RAM[addr];

				if (C_getBit(addr,15)==1){// read ROM
					uint16_t taddr = addr;
					C_clearBit16(&taddr,15);
					val=ROM[taddr];
				}

				//spaghetti::log::info("{} {} {} {} {}",getBinStr(address),getBinStr(*value),getHexStr(address),"r",getHexStr(*value));
				//consoleAppendF("onRead6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"r",getHexStr(val).c_str());

				M6502_SET_DATA(pins, val);
			}
			else { /* memory write */

				uint8_t val = M6502_GET_DATA(pins);

				//consoleAppendF("onWrite6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"W",getHexStr(val).c_str());

				RAM[addr] = val;
			}


	  } else {
		  //spaghetti::log::info("C65C02: waiting clock tick...");
	  }
} else {
	  // halted state
	  //spaghetti::log::info("C65C02: in HALTED state.");
}

}// calculate

//} namespace wq6502
