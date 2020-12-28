#include "C65.h"
#include "CRAM.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"



namespace CRAM {



CRAM::CRAM() : C65{}
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


void CRAM::calculate()
  {
	// read inputs
	inpToPins(CPins::all);


    bool rst = _pins.getPinS(CPins::RST);
    if (rst){
        //read program on reset
        //           LDA 14
        content[0]=0b00011110;
        //           ADD 15
        content[1]=0b00101111;
        //           SUB 8
        content[2]=0b00111000;
        //           HLT
        content[3]=0b01010000;
        //           NOP
        content[4]=0b00000000;
        // data
        content[8]=0b00000010;
       content[14]=0b00011100;
       content[15]=0b00001110;
    }

	short a0 = _pins.getPinS(CPins::A0);
	short a1 = _pins.getPinS(CPins::A1);
	short a2 = _pins.getPinS(CPins::A2);
	short a3 = _pins.getPinS(CPins::A3);

    size_t address = a0 + 2*a1 + 4*a2 + 8 *a3;
    bool we = !_pins.getPin(CPins::WE_);
    uint8_t value = content[address];
    if (we){
         value =  _pins.getPinS(CPins::D0)
                 + 2 *  _pins.getPinS(CPins::D1)
                 + 4 *  _pins.getPinS(CPins::D2)
                 + 8 *  _pins.getPinS(CPins::D3)
                 + 16*  _pins.getPinS(CPins::D4)
                 + 32*  _pins.getPinS(CPins::D5)
                 + 64*  _pins.getPinS(CPins::D6)
                 +128*  _pins.getPinS(CPins::D7)
                 ;
         content[address]=value;
    }


    bool cs = !_pins.getPin(CPins::CS_);


        short bv = getBit(value,0);
        _pins.setPin(CPins::O0,(cs)?bv>0:false);
        _pins.setPin(CPins::I0,bv>0);
        bv = getBit(value,1);
        _pins.setPin(CPins::O1,(cs)?bv>0:false);
        _pins.setPin(CPins::I1,bv>0);
        bv = getBit(value,2);
        _pins.setPin(CPins::O2,(cs)?bv>0:false);
        _pins.setPin(CPins::I2,bv>0);
        bv = getBit(value,3);
        _pins.setPin(CPins::O3,(cs)?bv>0:false);
        _pins.setPin(CPins::I3,bv>0);
        bv = getBit(value,4);
        _pins.setPin(CPins::O4,(cs)?bv>0:false);
        _pins.setPin(CPins::I4,bv>0);
        bv = getBit(value,5);
        _pins.setPin(CPins::O5,(cs)?bv>0:false);
        _pins.setPin(CPins::I5,bv>0);
        bv = getBit(value,6);
        _pins.setPin(CPins::O6,(cs)?bv>0:false);
        _pins.setPin(CPins::I6,bv>0);
        bv = getBit(value,7);
        _pins.setPin(CPins::O7,(cs)?bv>0:false);
        _pins.setPin(CPins::I7,bv>0);

    //_pins.setPin(CPins::D4,_pins.getPin(CPins::A0));
    ///std::string s = toBinary(_pins.tmpPinsG());
    //consoleAppendF("s:{}",s);
	pinsToOut(CPins::all);
  }

}//namespace C65C22
