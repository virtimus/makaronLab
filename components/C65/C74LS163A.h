#pragma once
#ifndef C65_C74LS163A_H
#define C65_C74LS163A_H

#include "C65.h"
#include "CRIED.h"
/**
 * 4bit Program counter
 */
namespace C74LS163A {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;

	static const C65Pin CL  {0,  "CL"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin CLK {1,  "CLK" ,ioType::eInputs,  siType::eInput};
	static const C65Pin D0  {2,  "D0"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin D1  {3,  "D1"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin D2  {4,  "D2"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin D3  {5,  "D3"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin END {6,  "END" ,ioType::eInputs,  siType::eInput};
	static const C65Pin GND {7,  "GND" ,ioType::eInputs,  siType::eOutput};

	static const C65Pin VCC {8,  "VCC" ,ioType::eOutputs,  siType::eInput};
	static const C65Pin RCO {9,  "RCO" ,ioType::eOutputs,  siType::eOutput};
	static const C65Pin Q0  {10, "Q0"  ,ioType::eOutputs,  siType::eOutput};
	static const C65Pin Q1  {11, "Q1"  ,ioType::eOutputs,  siType::eOutput};
	static const C65Pin Q2  {12, "Q2"  ,ioType::eOutputs,  siType::eOutput};
	static const C65Pin Q3  {13, "Q3"  ,ioType::eOutputs,  siType::eOutput};
	static const C65Pin ENQ {14, "ENQ" ,ioType::eOutputs,  siType::eInput};
	static const C65Pin LD  {15, "LD"  ,ioType::eOutputs,  siType::eInput};

	static const C65Pin all[] = {
            CL, CLK, D0, D1, D2, D3, END, GND,
            VCC,RCO, Q0, Q1, Q2, Q3, ENQ, LD
	};

    static const int allSize = 16;
}

namespace P = CPins;

class C74LS163A final : public C65/*CRIED::CRIED*/ {

public:
  static constexpr char const *const TYPE{ "chips/C74LS163A" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  C74LS163A();

  void calculate();

private:
  void counterToPins();
 // bool prevIN{false};
  //uint16_t counter{0};
  //uint16_t counterMax{1};
  uint16_t counter{0};
  uint16_t counterMax{15};
};


} //namespace C74LS163A


#endif // C65_C74LS163A_H
