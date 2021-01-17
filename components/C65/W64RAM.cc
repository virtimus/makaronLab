#include "C65.h"
#include "W64.h"
#include "W64RAM.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"



namespace W64 {



W64RAM::W64RAM() : W64{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
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


void W64RAM::calculate()
  {
	// read inputs
	inpToPins(CPins::all);


    bool rst = _pins.getPinS(CPins::RST);
    if (rst){
        //read program on reset
        //           LDA 14
        content[0]=0b00011110;//d 2+4+8+16=30
        //           ADD 15
        content[1]=0b00101111;//d 1+2+4+8+32=47
        //           SUB 8
        content[2]=0b00111000;//d
        //           HLT
        content[3]=0b01010000;
        //           NOP
        content[4]=0b00000000;
        // data
        content[8]=0b00000010;
       content[14]=0b00011100;//d 4+8+16=28
       content[15]=0b00001110;//2+4+8=14

       //28+15-8=35
    }

    uint64_t address = pinValueAsWord64(CPins::A);


    bool we = _pins.getPin(CPins::LD);
    uint64_t value = content[address];
    if (we){
         value = pinValueAsWord64(CPins::D);
         content[address]=value;
    }


    bool cs = _pins.getPin(CPins::EN);
    pinValueSet(CPins::I, value);
    if(cs){
        pinValueSet(CPins::O, value);
    } else {
        pinValueSet(CPins::O, (Word64)0);
    }

    //_pins.setPin(CPins::D4,_pins.getPin(CPins::A0));
    ///std::string s = toBinary(_pins.tmpPinsG());
    //consoleAppendF("s:{}",s);
	//pinsToOut(CPins::all);
  }

}//namespace W64
