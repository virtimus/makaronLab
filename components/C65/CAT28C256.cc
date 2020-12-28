#include "C65.h"
#include "CAT28C256.h"
#include "C65C02.h"
//#include <vendor/x16/glue.h>

namespace CAT28C256 {

void romPart2_11(){
	  for (int i=0;i<32768;i++){
		  ROM[i]=0xea;
	  }
}

void romPart2_14(){
	romPart2_11();
	ROM[0x7ffc]=0x00;
	ROM[0x7ffd]=0x80;
}

void romPart2_16(){
	romPart2_14();

	ROM[0]=0xa9;// load a register with value
	ROM[1]=0x42;

	ROM[2]=0x8d;// store a register at 0x6000
	ROM[3]=0x00;
	ROM[4]=0x60;
}

CAT28C256::CAT28C256() : C65{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);

	  //initROM
	  //romPart2_11();
	  //romPart2_14();
	  romPart2_16();



}




void CAT28C256::calculate()
  {
	// read inputs
	inpToPins(CPins::all);



  }

}//namespace CAT28C256
