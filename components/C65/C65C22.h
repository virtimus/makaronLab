#pragma once
#ifndef C65_C65C22_H
#define C65_C65C22_H

namespace C65C22 {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;
	static const C65Pin VSS  {0,  "VSS"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin PA0  {1,  "PA0"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA1  {2,  "PA1"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA2  {3,  "PA2"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA3  {4,  "PA3"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA4  {5,  "PA4"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA5  {6,  "PA5"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA6  {7,  "PA6"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PA7  {8,  "PA7"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB0  {9,  "PB0"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB1  {10, "PB1"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB2  {11, "PB2"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB3  {12, "PB3"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB4  {13, "PB4"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB5  {14, "PB5"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB6  {15, "PB6"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin PB7  {16, "PB7"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin CD1  {17, "CD1"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin CD2  {18, "CD2"  ,ioType::eInputs,  siType::eOutput};
	static const C65Pin VDD  {19, "CD2"  ,ioType::eInputs,  siType::eOutput};

	static const C65Pin CA1  {20, "CA1"  ,ioType::eOutputs, siType::eOutput};
	static const C65Pin CA2  {21, "CA2"  ,ioType::eOutputs, siType::eOutput};
	static const C65Pin RS0  {22, "RS0"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin RS1  {23, "RS1"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin RS2  {24, "RS2"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin RS3  {25, "RS3"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin RESB {26, "RESB" ,ioType::eOutputs, siType::eInput};
	static const C65Pin D0   {27, "D0"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D1   {28, "D1"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D2   {29, "D2"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D3   {30, "D3"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D4   {31, "D4"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D5   {32, "D5"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D6   {33, "D6"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D7   {34, "D7"   ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin PHI2 {35, "PHI2" ,ioType::eOutputs, siType::eInput};
	static const C65Pin CS1  {36, "CS1"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin CS2B {37, "CS2-"   ,ioType::eOutputs, siType::eInput};//active low
	static const C65Pin RWB  {38, "RWB"   ,ioType::eOutputs, siType::eInput};
	static const C65Pin IRQB {39, "IRQB"   ,ioType::eOutputs, siType::eOutput};

	static const C65Pin all[] = {
			VSS, PA0, PA1, PA2, PA3, PA4, PA5, PA6, PA7, PB0, PB1, PB2, PB3, PB4, PB5, PB6, PB7, CD1, CD2, VDD,
			CA1, CA2, RS0, RS1, RS2, RS3, RESB,D0,  D1,  D2,  D3,  D4,  D5,  D6,  D7,  PHI2,CS1, CS2B,RWB, IRQB
	};
	static const int allSize = 40;
}

class C65C22 final : public C65 {
protected:

public:
  static constexpr char const *const TYPE{ "chips/C65C22" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  C65C22();

  void calculate();
  void addAllIO(const C65Pin all[]);

};

}//namespace C65C22

#endif// C65_C65C22_H
