#include "C65.h"
#include "BytesToWord64.h"

//namespace C65BB {

BytesToWord64::BytesToWord64()
{
  setMinInputs(8);
  setMaxInputs(8);
  setMinOutputs(1);
  setMaxOutputs(1);

  addInput(spaghetti::ValueType::eByte, "B0", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B1", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B2", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B3", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B4", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B5", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B6", spaghetti::Element::IOSocket::eCanHoldByte);
  addInput(spaghetti::ValueType::eByte, "B7", spaghetti::Element::IOSocket::eCanHoldByte);



  addOutput(spaghetti::ValueType::eWord64, "Word64", spaghetti::Element::IOSocket::eCanHoldWord64);
}

union U {
  uint64_t word64;
  //   vs.
  struct Byte {
	  uint8_t b0, b1, b2, b3, b4, b5, b6, b7;
  } bytes;
};

void BytesToWord64::calculate()
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
   // uint64_t oval =0;
    //uint64_t factor=1;
    //for(int i=0;i<m_inputs.size();i++){
	 U u;
        const uint8_t B0{ std::get<uint8_t>(m_inputs[0].value) };
        const uint8_t B1{ std::get<uint8_t>(m_inputs[1].value) };
        const uint8_t B2{ std::get<uint8_t>(m_inputs[2].value) };
        const uint8_t B3{ std::get<uint8_t>(m_inputs[3].value) };
        const uint8_t B4{ std::get<uint8_t>(m_inputs[4].value) };
        const uint8_t B5{ std::get<uint8_t>(m_inputs[5].value) };
        const uint8_t B6{ std::get<uint8_t>(m_inputs[6].value) };
        const uint8_t B7{ std::get<uint8_t>(m_inputs[7].value) };



        u.bytes.b0 = B0;
        u.bytes.b1 = B1;
        u.bytes.b2 = B2;
        u.bytes.b3 = B3;
        u.bytes.b4 = B4;
        u.bytes.b5 = B5;
        u.bytes.b6 = B6;
        u.bytes.b7 = B7;

         //oval+=factor*(B1?1:0);
        //factor=factor*2;
    //}
    m_outputs[0].value = u.word64;
}

//} // namespace C65
