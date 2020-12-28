#pragma once
#ifndef C65_CAT28C256_H
#define C65_CAT28C256_H

namespace CAT28C256 {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;
	static const C65Pin A14 {0,  "A14" ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A12 {1,  "A12" ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A7  {2,  "A7"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A6  {3,  "A6"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A5  {4,  "A5"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A4  {5,  "A4"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A3  {6,  "A3"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A2  {7,  "A2"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A1  {8,  "A1"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin A0  {9,  "A0"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin IO0 {10, "IO0" ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin IO1 {11, "IO1" ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin IO2 {12, "IO2" ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin GND {13, "GND" ,ioType::eInputs,  siType::eOutput};

	static const C65Pin VCC {14, "VCC" ,ioType::eOutputs, siType::eOutput};
	static const C65Pin WE  {15, "WE-" ,ioType::eOutputs, siType::eInput};//write enable - active low
	static const C65Pin A13 {16, "A13" ,ioType::eOutputs, siType::eOutput};
	static const C65Pin A8  {17, "A8"  ,ioType::eOutputs, siType::eOutput};
	static const C65Pin A9  {18, "A9"  ,ioType::eOutputs, siType::eOutput};
	static const C65Pin A11 {19, "A11" ,ioType::eOutputs, siType::eOutput};
	static const C65Pin OE  {20, "OE-" ,ioType::eOutputs, siType::eOutput};//output enable(when also ce) - active low
	static const C65Pin A10 {21, "A10" ,ioType::eOutputs, siType::eOutput};
	static const C65Pin CE  {22, "CE-" ,ioType::eOutputs, siType::eInput};//chip enable - active low
	static const C65Pin IO7 {23, "IO7" ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin IO6 {24, "IO6" ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin IO5 {25, "IO5" ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin IO4 {26, "IO4" ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin IO3 {27, "IO3" ,ioType::eOutputs, siType::eDynamic};

	static const C65Pin all[] = {
			A14, A12, A7,  A6,  A5,  A4,  A3,  A2,  A1,  A0,  IO0, IO1, IO2, GND,
			VCC, WE,  A13, A8,  A9,  A11, OE,  A10, CE,  IO7, IO6, IO5, IO4, IO3,
	};
	static const int allSize = 28;
}


class CAT28C256 final : public C65 {
protected:

public:
  static constexpr char const *const TYPE{ "chips/CAT28C256" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CAT28C256();

  void calculate();

};


} //namespace CAT28C256


#endif // C65_CAT28C256_H
