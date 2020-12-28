#pragma once
#ifndef C65_C74LS189_H
#define C65_C74LS189_H

namespace C74LS189 {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;
	static const C65Pin A0  {0, "A0"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin CS_ {1, "CS-" ,ioType::eInputs,  siType::eInput};
	static const C65Pin WE_ {2, "WE-" ,ioType::eInputs,  siType::eInput};
	static const C65Pin D1  {3, "D1"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin O1_ {4, "O1-" ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin D2  {5, "D2"  ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin O2_ {6, "O2-" ,ioType::eInputs,  siType::eDynamic};
	static const C65Pin GND {7, "GND" ,ioType::eInputs,  siType::eOutput};

	static const C65Pin VCC {8, "VCC" ,ioType::eOutputs, siType::eInput};
	static const C65Pin A1  {9, "A1"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin A2  {10,"A2"  ,ioType::eOutputs, siType::eInput};
	static const C65Pin A3  {11,"A3"  ,ioType::eOutputs, siType::eInput};
    static const C65Pin D4  {12,"D4"  ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin O4_ {13,"O4-" ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin D3  {14,"D3"  ,ioType::eOutputs, siType::eDynamic};
	static const C65Pin O3_ {15,"O3-" ,ioType::eOutputs, siType::eDynamic};


	static const C65Pin all[] = {
            A0, CS_, WE_,  D1,  O1_,  D2,  O2_,  GND,
            VCC, A1,  A2, A3,  D4,  O4_, D3,  O3_,
	};
	static const int allSize = 16;
}


class C74LS189 final : public C65 {
public:
  static constexpr char const *const TYPE{ "chips/C74LS189" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  C74LS189();

  void calculate();
  //private uint64_t content;
  std::vector<uint16_t> content{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
};


} //namespace C74LS189


#endif // C65_C74LS189_H
