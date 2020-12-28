#include "C65.h"
//#include "ByteToBools.h"
#include "spaghetti/element.h"

//namespace C65BB {

ByteToBools::ByteToBools()
{
  setMinInputs(1);
  setMaxInputs(2);
  setMinOutputs(8);
  setMaxOutputs(30);

  addInput(spaghetti::ValueType::eByte, "Byte", spaghetti::Element::IOSocket::eCanHoldInt);
  addInput(spaghetti::ValueType::eBool, "LD-", spaghetti::Element::IOSocket::eCanHoldBool);

  addOutput(spaghetti::ValueType::eBool, "B0", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B1", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B2", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B3", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B4", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B5", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B6", spaghetti::Element::IOSocket::eCanHoldBool);
  addOutput(spaghetti::ValueType::eBool, "B7", spaghetti::Element::IOSocket::eCanHoldBool);

}

void ByteToBools::calculate()
{

    bool ld = true;
    if (m_inputs.size()>1){

        bool const LDBar{ std::get<bool>(m_inputs[1].value) };
        ld = !LDBar;
    }

  if (ld){
      uint8_t const BYTE{ std::get<uint8_t>(m_inputs[0].value) };
      for (int i=0;i<m_outputs.size();i++){
          m_outputs[i].value =  (bool)CHECK_BIT(BYTE,i);
      }
  } else {
      for (int i=0;i<m_outputs.size();i++){
          m_outputs[i].value =  false;
      }
  }
  /*m_outputs[0].value =  (bool)CHECK_BIT(BYTE,0);
  m_outputs[1].value =  (bool)CHECK_BIT(BYTE,1);
  m_outputs[2].value =  (bool)CHECK_BIT(BYTE,2);
  m_outputs[3].value =  (bool)CHECK_BIT(BYTE,3);
  m_outputs[4].value =  (bool)CHECK_BIT(BYTE,4);
  m_outputs[5].value =  (bool)CHECK_BIT(BYTE,5);
  m_outputs[6].value =  (bool)CHECK_BIT(BYTE,6);
  m_outputs[7].value =  (bool)CHECK_BIT(BYTE,7);*/

}

//} // namespace C65
