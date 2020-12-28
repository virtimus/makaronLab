#include "C65.h"
#include "C65C22.h"

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


namespace C65C22 {



C65C22::C65C22() : C65{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);
}




void C65C22::calculate()
  {
	// read inputs
	inpToPins(CPins::all);

  }

}//namespace C65C22
