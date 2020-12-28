#include "C65.h"
#include "Word64ToBytes.h"
#include "spaghetti/element.h"

Word64ToBytes::Word64ToBytes()
{
  setMinInputs(1);
  setMaxInputs(1);
  setMinOutputs(8);
  setMaxOutputs(8);

  addInput(spaghetti::ValueType::eWord64, "W64", spaghetti::Element::IOSocket::eCanHoldWord64);

  addOutput(spaghetti::ValueType::eByte, "B0", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B1", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B2", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B3", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B4", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B5", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B6", spaghetti::Element::IOSocket::eCanHoldByte);
  addOutput(spaghetti::ValueType::eByte, "B7", spaghetti::Element::IOSocket::eCanHoldByte);

}

union U {
  uint64_t word64;
  //   vs.
  struct Byte {
	  uint8_t b0, b1, b2, b3, b4, b5, b6, b7;
  } bytes;
};

void Word64ToBytes::calculate()
{
  uint64_t const WORD64{ std::get<uint64_t>(m_inputs[0].value) };
  U u;
  u.word64 = WORD64;

  m_outputs[0].value = u.bytes.b0;
  m_outputs[1].value = u.bytes.b1;
  m_outputs[2].value = u.bytes.b2;
  m_outputs[3].value = u.bytes.b3;
  m_outputs[4].value = u.bytes.b4;
  m_outputs[5].value = u.bytes.b5;
  m_outputs[6].value = u.bytes.b6;
  m_outputs[7].value = u.bytes.b7;

}


