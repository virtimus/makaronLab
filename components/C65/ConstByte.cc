#include "ConstByte.h"



ConstByte::ConstByte()
{
  setMinInputs(0);
  setMaxInputs(0);
  setMinOutputs(1);
  setMaxOutputs(1);

  addOutput(spaghetti::ValueType::eByte, "Value", spaghetti::Element::IOSocket::eCanHoldByte | spaghetti::Element::IOSocket::eCanChangeName);
  m_outputs[0].value = (uint8_t)1;
}

void ConstByte::serialize(Json &a_json)
{
  Element::serialize(a_json);

  auto &properties = a_json["properties"];
  properties["value"] = m_currentValue;
}

void ConstByte::deserialize(Json const &a_json)
{
  Element::deserialize(a_json);

  auto const &PROPERTIES = a_json["properties"];
  m_currentValue = PROPERTIES["value"].get<uint64_t>();

  m_outputs[0].value = m_currentValue;
}

void ConstByte::set(uint8_t a_value)
{
  m_currentValue = a_value;
  m_outputs[0].value = m_currentValue;
}

