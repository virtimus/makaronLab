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
       /*  read program on reset
       *
       *
       */

        std::vector<uint8_t>& c = content;

        /*
        //prg
        c[0]=0b00011110;// LDA 14
        c[1]=0b00101111;// ADD 15
        c[2]=0b00111000;// SUB 8
        c[3]=0b11110000;// HLT
        c[4]=0b00000000;// NOP
        // data
        c[8]= 0b00000010;
        c[14]=0b00011100;
        c[15]=0b00001110;
      */

        /*
       //prg
       c[0]=0b01010001;// ldi 1   //d81
       c[1]=0b00101110;// add $14 //d46
       c[2]=0b01001110;// sta $14 //d78
       c[3]=0b11100000;// out     //d224
       c[4]=0b01100000;// jmp 0   //d96
       c[5]=0b11110000;// hlt
       //data
       c[15]=0b00001110;
       */


       //https://youtu.be/Zg1NdPKoosU?t=1843
	   c[0]=0b00101111;// ADD $15
	   c[1]=0b11100000;// out
	   c[2]=0b01110100;// JC 4
	   c[3]=0b01100000;// JMP 0
	   c[4]=0b00111111;// SUB $15
	   c[5]=0b11100000;// OUT
	   c[6]=0b10000000;// JZ 0
	   c[7]=0b01100100;// JMP 4
       //data
       c[15]=0b0000001;

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
