
#include "Byte27SD.h"



Byte27SD::Byte27SD()
{
  setMinInputs(2);
  setMaxInputs(2);
  setMinOutputs(0);
  setMaxOutputs(0);

  addInput(spaghetti::ValueType::eInt, "Byte", spaghetti::Element::IOSocket::eCanHoldInt);
  addInput(spaghetti::ValueType::eBool, "Dot", spaghetti::Element::IOSocket::eCanHoldBool);
}


void Byte27SD::serialize(Json &a_json) {
	 Element::serialize(a_json);
	  auto &jsonElement = a_json["element"];
	  jsonElement["Byte27SD_DigitPos"] = currentValue();
}


void Byte27SD::deserialize(Json const &a_json){
	Element::deserialize(a_json);
	auto const &ELEMENT = a_json["element"];
	if ((ELEMENT.find("Byte27SD_DigitPos")!=ELEMENT.end())){
			auto const &dp = ELEMENT["Byte27SD_DigitPos"];
			set(dp);
	}
}
