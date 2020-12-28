#include <InfoByte.h>



InfoByte::InfoByte()
{
  setMinInputs(1);
  setMaxInputs(1);
  setMinOutputs(0);
  setMaxOutputs(0);

  addInput(spaghetti::ValueType::eByte, "Byte", IOSocket::eCanHoldByte | IOSocket::eCanChangeName);
}


