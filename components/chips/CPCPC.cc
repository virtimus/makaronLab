#include <Chips.h>
#include <CPCPC.h>
#include "disks/fdd-test.h"

extern "C" uint64_t readCpc();
//extern "C" uint64_t readCpc();
//extern "C" cpc_t cpc;
extern "C" cpc_t* readCpcPtr();

namespace makaron::chips {

CPCPC::CPCPC() : Chips{}
{
  setMinInputs(0);
  setMaxInputs(0);
  setMinOutputs(0);
  setMaxOutputs(0);
  _cpc = readCpcPtr();
  int o=0;
  fdd_init(&(_cpc->fdd));
  bool load_successful = fdd_cpc_insert_dsk(&(_cpc->fdd), dump_boulderdash_cpc_dsk, sizeof(dump_boulderdash_cpc_dsk));
  if (load_successful){
	  o=1;
  }

  //cpcRun();
  //addInput(spaghetti::ValueType::eWord64, "Word64", IOSocket::eCanHoldWord64 | IOSocket::eCanChangeName);
}

void CPCPC::calculate()
{
	//cpc_t &cpc = readCpc();
    //_currentValue = readCpc();
    if (!(_cpc->fdd.has_disc)){
        int o=0;
        fdd_init(&(_cpc->fdd));
        bool load_successful = fdd_cpc_insert_dsk(&(_cpc->fdd), dump_boulderdash_cpc_dsk, sizeof(dump_boulderdash_cpc_dsk));
        if (load_successful){
            o=1;
        }

    }

}


}//namespace makaron::chips

