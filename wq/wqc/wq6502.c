


	#define CHIPS_IMPL
	//##include <vendor/chips/chips/m6502.h>
	#include <m6502.h>

#include "wq6502.h"
//#include <vector>


	#define T(b) ASSERT_TRUE(b)
	//#define R(r) cpu.r

	//m6502_t cpu
	//static std::vector<m6502_t> v_cpu;

	//uint64_t pins
	//static std::vector<uint64_t> v_pins;

	//typedef struct S_RAM { uint8_t RAM[1<<16]; } S_RAM;
	//typedef struct S_ROM { uint8_t ROM[32768]; } S_ROM;

	//static uint8_t RAM[1<<16] = { 0 };
	//static std::vector<S_RAM> V_RAM;

	//static uint8_t ROM[1<<16] = { 0 };
	//static std::vector<S_ROM> V_ROM;
	
	//static m6502_desc_t cpu_desc;
	//static std::vector<m6502_desc_t> v_cpu_desc;

	//bool prevClock = false;
	//static std::vector<bool> v_prevClock;

	//bool prevResb = false;
	//static std::vector<bool> v_prevResb;

	DECLARE_DYN_ARRAY(wq6502Info_t);
	DYN_ARRAY(wq6502Info_t) wq6502a = {0};

	 
	static void w8(size_t iv,uint16_t addr, uint8_t data) {
	    //RAM[addr] = data;
		wq6502a.buf[iv].RAM[addr] = data;
	}

	static void w16(size_t iv,uint16_t addr, uint16_t data) {
	    wq6502a.buf[iv].RAM[addr] = data & 0xFF;
	    wq6502a.buf[iv].RAM[(addr+1)&0xFFFF] = data>>8;
	}

	static uint16_t r16(size_t iv,uint16_t addr) {
	    uint8_t l = wq6502a.buf[iv].RAM[addr];
	    uint8_t h = wq6502a.buf[iv].RAM[(addr+1)&0xFFFF];
	    return (h<<8)|l;
	}

	static uint8_t r8(size_t iv,uint16_t addr) {
		return wq6502a.buf[iv].RAM[addr];
	}

	static size_t init(void) {

		size_t iv = wq6502a.n;//sizeof(wq6502a.buf);

		wq6502Info_t wq6502Info;

		DYN_ADD(wq6502a, wq6502Info, errorAlloc);

		wq6502Info_t* pb= &wq6502a.buf[iv];

		pb->iv = iv;

		//m6502_t cpu = wq6502a.buf[iv].cpu;
		//wq6502a.buf[iv].cpu = cpu;//.emplace_back(cpu);

		//S_RAM RAM{};
		memset(pb->RAM, 0, sizeof(pb->RAM));
		//V_RAM.emplace_back(RAM);

		//S_ROM ROM{};
		//V_ROM.emplace_back(ROM);

		//m6502_desc_t& cpu_desc = pb->cpu_desc;
		//v_cpu_desc.emplace_back(cpu_desc)

		pb->prevClock = false;
		//v_prevClock.emplace_back(prevClock);

		pb->prevResb = false;
		//v_prevResb.emplace_back(prevResb);
	    
	    pb->pins = m6502_init(&pb->cpu, &pb->cpu_desc/*&(m6502_desc_t){0}*/);
		//v_pins.emplace_back(pins);

        //setBit(pins
	    pb->cpu.S = 0xBD;   // perfect6502 starts with S at C0 for some reason
	    pb->cpu.P = M6502_ZF|M6502_BF|M6502_IF;

		return iv;
		errorAlloc: printf( "Allocation error i = %d\n", iv );
	}

	static void prefetch(size_t iv, uint16_t pc) {

	    wq6502a.buf[iv].pins = M6502_SYNC;
	    M6502_SET_ADDR(wq6502a.buf[iv].pins, pc);
	    M6502_SET_DATA(wq6502a.buf[iv].pins, wq6502a.buf[iv].RAM[pc]);
	    wq6502a.buf[iv].cpu.PC = pc;
	}

	static void copy(size_t iv,uint16_t addr, uint8_t* bytes, size_t num) {
	    assert((addr + num) <= sizeof(wq6502a.buf[iv].RAM));
	    memcpy(&wq6502a.buf[iv].RAM[addr], bytes, num);
	}

	static void tick(size_t iv) {
	    wq6502a.buf[iv].pins = m6502_tick(&wq6502a.buf[iv].cpu, wq6502a.buf[iv].pins);
	    const uint16_t addr = M6502_GET_ADDR(wq6502a.buf[iv].pins);
	    if (wq6502a.buf[iv].pins & M6502_RW) {
	        /* memory read */
	        uint8_t val = wq6502a.buf[iv].RAM[addr];
	        M6502_SET_DATA(wq6502a.buf[iv].pins, val);
	    }
	    else {
	        /* memory write */
	        uint8_t val = M6502_GET_DATA(wq6502a.buf[iv].pins);
	        wq6502a.buf[iv].RAM[addr] = val;
	    }
	}

	static uint32_t step(size_t iv) {
	    uint32_t ticks = 0;
	    do {
	        tick(iv);
	        ticks++;
	    } while (0 == (wq6502a.buf[iv].pins & M6502_SYNC));
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

	void C_pins_setPin(uint64_t* pv, short bit, bool high){
		if (high){
			(*pv) |= 1UL << bit;
		} else {
			(*pv) &= ~(1UL << bit);
		}
	}	

	short C_getBit(uint64_t value, short bitPos){
		short result = (value >> bitPos) & 1U;
		return result;
		}

	short C_getBit16(uint16_t value, short bitPos){
		short result = (value >> bitPos) & 1U;
		return result;
		}

	short C_getBit8(uint8_t value, short bitPos){
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

void C_getBinStr16(uint16_t value, char* buff){
	  short v;
	  for (int i=0;i<16;i++){
		  v = C_getBit16(value,i);
		  buff[15-i]=(v>0)?'1':'0';
	  }
	  buff[16]='\x0';
}

void C_getBinStr8(uint8_t value, char* buff){
	  //char buff[9];
	  short v;
	  for (int i=0;i<8;i++){
		  v = C_getBit8(value,i);
		  buff[7-i]=(v>0)?'1':'0';
	  }
	  buff[8]='\x0';
	  //return &buff;
}

char* C_getHexStr16(uint16_t value){
	//std::stringstream sstream;
	//sstream << std::setfill('0') << std::setw(4) << std::hex << value;
	char output[6];
	sprintf(output,"%04x",value);
	//std::string result = output;
	return &output;
	}

char* C_getHexStr8(uint8_t value){
	//std::stringstream sstream;
	//sstream << std::setfill('0') << std::setw(2) << std::hex << value;
	//std::string result = sstream.str();
	char output[4];
	sprintf(output,"%02x",value);
	//std::string result = output;
	return &output;
	}

 void wq6502_init(wq6502Info_t* info){
	size_t iv = init();
	//wq6502Info_t info;
	info->iv = iv;
	info->pins = wq6502a.buf[iv].pins;
	return info;
}



uint64_t wq6502_calc(size_t iv, uint64_t pv){
	char buff[20];
	wq6502Info_t* pb= &wq6502a.buf[iv];

#ifdef Q3C_CLASSIC_6502
	return m6502_tick(&pb->cpu, pv);
#else

	//C65Pins _pins;

	//_pins.tmpPinsS(pv);

const bool pinPHI2 = C_pins_getPin(pv,CPINS_PHI2);
const bool clockDelta =(pinPHI2 != pb->prevClock);

const bool clockRise = (pinPHI2 && !wq6502a.buf[iv].prevClock);//true;//
wq6502a.buf[iv].prevClock = pinPHI2;
const bool pinRDY = C_pins_getPin(pv,CPINS_RDY);//true; //

const bool pinRESB = C_pins_getPin(pv,CPINS_RESB);
const bool resetRise = (pinRESB && !wq6502a.buf[iv].prevResb);

if (resetRise){
	  //C65::consoleAppendF("C65C02: pin RESB rise - ===RESET=== ...",NULL);
	  // full reset sequence as shown for 6520C

	  //set reset PIN in m6502
    short bp = M6502_PIN_RES;
    C_setBit(&wq6502a.buf[iv].pins,bp);

}

pb->prevResb = pinRESB;
//bool pinA23 = C_pins_getPin(pv,CPINS_A23);
//const bool outRESB = C_pins_getPin(pv,CPINS_RESB);
//spaghetti::log::info("pin PHI2 is:{}",pinPHI2);
//spaghetti::log::info("pin RDY is:{}",pinRDY);
//spaghetti::log::info("pin RESB is:{}",pinRESB);
//spaghetti::log::info("pin A23 is:{}",pinA23);
///spaghetti::log::info("RESBOut is:{}",outRESB);
if (pinRDY){
	  if (clockRise/*clockDelta*/){
		  //C65::consoleAppendF("C65C02: pin PHI2 is:{}",pinPHI2);
		  //spaghetti::log::info("C65C02: next processing step...");

			uint8_t val;
			//uint64_t pinsIn = pins;

			pb->pins = m6502_tick(&pb->cpu, pb->pins);
			//uint64_t pinsOut = pins;
			const uint16_t addr = M6502_GET_ADDR(wq6502a.buf[iv].pins);
			if (wq6502a.buf[iv].pins & M6502_RW) { /* memory read */

				C_pins_setPin(&pv, CPINS_RWB,true);

				val = wq6502a.buf[iv].RAM[addr];

				if (C_getBit(addr,15)==1){// read ROM
					uint16_t taddr = addr;
					C_clearBit16(&taddr,15);
					val=wq6502a.buf[iv].ROM[taddr];
				}

				printf("R ");

				//spaghetti::log::info("{} {} {} {} {}",getBinStr(address),getBinStr(*value),getHexStr(address),"r",getHexStr(*value));
				//consoleAppendF("onRead6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"r",getHexStr(val).c_str());

				M6502_SET_DATA(wq6502a.buf[iv].pins, val);

			}
			else { /* memory write */

				C_pins_setPin(&pv, CPINS_RWB,false);

				val = M6502_GET_DATA(wq6502a.buf[iv].pins);

				//consoleAppendF("onWrite6502: {} {} {} {} {}",getBinStr(addr).c_str(),getBinStr(val).c_str(),getHexStr(addr).c_str(),"W",getHexStr(val).c_str());

				wq6502a.buf[iv].RAM[addr] = val;

				printf("W ");
			}
			C_getBinStr16(addr,buff);
			printf(" ADR:%s",buff);
			C_getBinStr8(val,buff);
			printf(" DTA:%s\n",buff);

        for (int i=0;i<16;i++){
            const bool bit = (C_getBit16(addr,i)==1);
            C_pins_setPin(&pv, CPINS_A0+i,bit);
        }

        for (int i=0;i<16;i++){
            const bool bit = (C_getBit8(val,i)==1);
            C_pins_setPin(&pv,CPINS_D0+i,bit);
        }


	  } else {
		  //spaghetti::log::info("C65C02: waiting clock tick...");
	  }
} else {
	  // halted state
	  //spaghetti::log::info("C65C02: in HALTED state.");
}

	return pv;
#endif
}// calculate

//} namespace wq6502
