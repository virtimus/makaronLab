#include "C65.h"
#include "BoolsToByte.h"

//namespace C65BB {

BoolsToByte::BoolsToByte()
{
  setMinInputs(8);
  setMaxInputs(8);
  setMinOutputs(1);
  setMaxOutputs(1);

  addInput(spaghetti::ValueType::eBool, "B0", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B1", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B2", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B3", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B4", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B5", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B6", spaghetti::Element::IOSocket::eCanHoldBool);
  addInput(spaghetti::ValueType::eBool, "B7", spaghetti::Element::IOSocket::eCanHoldBool);



  addOutput(spaghetti::ValueType::eByte, "Byte", spaghetti::Element::IOSocket::eCanHoldByte);
}

void BoolsToByte::calculate()
{
   /*const bool B0{ std::get<bool>(m_inputs[0].value) };
   const bool B1{ std::get<bool>(m_inputs[1].value) };
   const bool B2{ std::get<bool>(m_inputs[2].value) };
   const bool B3{ std::get<bool>(m_inputs[3].value) };
   const bool B4{ std::get<bool>(m_inputs[4].value) };
   const bool B5{ std::get<bool>(m_inputs[5].value) };
   const bool B6{ std::get<bool>(m_inputs[6].value) };
   const bool B7{ std::get<bool>(m_inputs[7].value) };*/

  //m_outputs[0].value =  B0 + B1*2 + B2*4 + B3*8 + B4*16 + B5*32 + B6*64 + B7*128;
    uint8_t oval =0;
    uint8_t factor=1;
    for(int i=0;i<m_inputs.size();i++){
        const bool B1{ std::get<bool>(m_inputs[i].value) };
        oval+=factor*(B1?1:0);
        factor=factor*2;
    }
    m_outputs[0].value = oval;
}

//} // namespace C65
