#include "ConstWord64.h"



ConstWord64::ConstWord64()
{
  setMinInputs(0);
  setMaxInputs(0);
  setMinOutputs(1);
  setMaxOutputs(1);

  addOutput(spaghetti::ValueType::eWord64, "Value", spaghetti::Element::IOSocket::eCanHoldWord64 | spaghetti::Element::IOSocket::eCanChangeName);
  m_outputs[0].value = (uint64_t)1;
}

void ConstWord64::serialize(Json &a_json)
{
  Element::serialize(a_json);

  auto &properties = a_json["properties"];
  properties["value"] = m_currentValue;
}

void ConstWord64::deserialize(Json const &a_json)
{
  Element::deserialize(a_json);

  auto const &PROPERTIES = a_json["properties"];
  m_currentValue = PROPERTIES["value"].get<uint64_t>();

  m_outputs[0].value = m_currentValue;
}

void ConstWord64::set(uint64_t a_value)
{
  m_currentValue = a_value;
  m_outputs[0].value = m_currentValue;
}

