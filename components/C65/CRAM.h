#pragma once
#ifndef C65_CRAM_H
#define C65_CRAM_H


namespace CRAM {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;









static const C65Pin A0  {0, "A0"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin A1  {1, "A1"  ,ioType::eInputs, siType::eInput};
    static const C65Pin A2  {2 ,"A2"  ,ioType::eInputs, siType::eInput};
    static const C65Pin A3  {3 ,"A3"  ,ioType::eInputs, siType::eInput};
	static const C65Pin D0  {4, "D0" ,ioType::eInputs,  siType::eInput};
	static const C65Pin D1  {5, "D1" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D2  {6, "D2"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin D3  {7, "D3" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D4  {8, "D4"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin D5  {9, "D5" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D6  {10, "D6" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D7  {11, "D7" ,ioType::eInputs, siType::eInput};
    static const C65Pin CS_  {12,"CS-"  ,ioType::eInputs, siType::eInput};
    static const C65Pin WE_ {13,"WE-" ,ioType::eInputs, siType::eInput};
    static const C65Pin RST {14,"RST" ,ioType::eInputs, siType::eInput};

    static const C65Pin O0 {15,"O0" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O1 {16,"O1" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O2 {17,"O2" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O3 {18,"O3" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O4 {19,"O4" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O5 {20,"O5" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O6 {21,"O6" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O7 {22,"O7" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I0 {23,"I0" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I1 {24,"I1" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I2 {25,"I2" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I3 {26,"I3" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I4 {27,"I4" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I5 {28,"I5" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I6 {29,"I6" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin I7 {30,"I7" ,ioType::eOutputs, siType::eOutput};


	static const C65Pin all[] = {
            A0, A1, A2, A3,  D0,  D1, D2, D3, D4, D5, D6, D7,  CS_, WE_, RST,
            O0, O1, O2, O3,  O4,  O5, O6, O7, I0, I1, I2, I3,  I4,  I5, I6, I7,
	};
    static const int allSize = 31;
}


class CRAM final : public C65 {
public:
  static constexpr char const *const TYPE{ "chips/CRAM" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CRAM();

  void calculate();
  //private uint64_t content;
  std::vector<uint8_t> content{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
};


} //namespace C74LS189


#endif // C65_CRAM_H
