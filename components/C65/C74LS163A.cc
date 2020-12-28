#include "C65.h"
#include "CRIED.h"
#include "C74LS163A.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"



namespace C74LS163A {



C74LS163A::C74LS163A() : C65/*CRIED::CRIED*/ {}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
      //counterMax = 1;
	  counter=0;
	  counterMax = 15; //(4 bits)
}

void C74LS163A::counterToPins(){
	_pins.setPin(P::Q0,getBit(counter,0));
	_pins.setPin(P::Q1,getBit(counter,1));
	_pins.setPin(P::Q2,getBit(counter,2));
	_pins.setPin(P::Q3,getBit(counter,3));
}

void C74LS163A::calculate()
  {
	// read inputs
    inpToPins(CPins::all);

    bool clock = _pins.getPin(P::CLK);
    bool enable = _pins.getPin(P::END);
    bool isRise = this->isRise(clock);


     bool cc = false;
   if (isRise){
	   if (enable){
		   counter++;
           cc=true;
           if (counter>counterMax) { counter = 0;  };          
	   }
	   bool reset = _pins.getPin(P::CL);
       if (reset) { counter = 0;}
   }


   bool load = _pins.getPin(P::LD);
   if (load){
       cc = true;
	   counter = _pins.getPinS(P::D0)+(_pins.getPinS(P::D1))*2+(_pins.getPinS(P::D2))*4+(_pins.getPinS(P::D3))*8;
       //if (enable && counter+1 > counterMax) {carryOut = true;}
   }
  bool carryOut = false;
  if (enable && counter+1 > counterMax) {carryOut = true;}
  _pins.setPin(P::RCO,carryOut);


    counterToPins();
    pinsToOut(CPins::all);
  }

}//namespace C74LS163A
