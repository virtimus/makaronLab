#include <InfoWord64.h>



InfoWord64::InfoWord64()
{
  setMinInputs(1);
  setMaxInputs(1);
  setMinOutputs(0);
  setMaxOutputs(0);

  addInput(spaghetti::ValueType::eWord64, "Word64", IOSocket::eCanHoldWord64 | IOSocket::eCanChangeName);
}


