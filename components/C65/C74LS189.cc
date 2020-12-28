#include "C65.h"
#include "C74LS189.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"
//##include "cpu/fake6502.h"
//#include <vendor/x16/debugger.h>
//#include <vendor/x16/cpu/fake6502.h>
//#include "fake6502.h"
//#include <vendor/x16/memory.h>
//#include <vendor/x16/glue.h>


namespace C74LS189 {



C74LS189::C74LS189() : C65{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
      for(int i=0;i<16;i++){
        content[i]=0;
      }
}

std::string  toBinary(uint64_t n)
{
    std::string s = "";
    while (n > 0)
    {
        s =  ( (n % 2 ) == 0 ? "0" : "1") +s;
        n = n / 2;
    }
    return s;
}


void C74LS189::calculate()
  {
	// read inputs
	inpToPins(CPins::all);

	short a0 = _pins.getPinS(CPins::A0);
	short a1 = _pins.getPinS(CPins::A1);
	short a2 = _pins.getPinS(CPins::A2);
	short a3 = _pins.getPinS(CPins::A3);

	size_t address = a0 + 2* a1 + 4* a2 + 8 * a3;
	uint16_t value = content[address];
    short bv = getBit(value,0);
    _pins.setPin(CPins::O1_,bv==0);
    bv = getBit(value,1);
    _pins.setPin(CPins::O2_,bv==0);
    bv = getBit(value,2);
    _pins.setPin(CPins::O3_,bv==0);
    bv = getBit(value,3);
    _pins.setPin(CPins::O4_,bv==0);
    //_pins.setPin(CPins::D4,_pins.getPin(CPins::A0));
    ///std::string s = toBinary(_pins.tmpPinsG());
    //consoleAppendF("s:{}",s);
	pinsToOut(CPins::all);
  }

}//namespace C65C22
