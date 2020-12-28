#include "C65.h"
#include "CRIED.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"



namespace CRIED {



CRIED::CRIED() : C65{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
      //counterMax = 1;
}


void CRIED::calculate()
  {
	// read inputs
    inpToPins(CPins::all);

	// read pinIN
    bool pinIN = _pins.getPin(CPins::IN);
    //bool pinIN = std::get<bool>(m_inputs[0].value);//

	//detect signals
    bool INRise = isRise(pinIN);

    if (pinIN){
        //counterMax = 201;
    }


    if (INRise){
         counter = 0;
        _pins.setPin(CPins::OUT,true);
        // m_outputs[0].value = true;
	} else {
		if (counter>=counterMax){
            //_pins.setPin(CPins::OUT,false);
           // m_outputs[0].value = false;
			_pins.setPin(CPins::OUT,false);
            counter=counterMax+1;
		} else {
            counter++;
            _pins.setPin(CPins::OUT,true);
           // m_outputs[0].value = true;
		}
	}


    pinsToOut(CPins::all);
  }

}//namespace CRIED
