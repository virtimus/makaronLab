#pragma once
#ifndef C65_CCLROM_H
#define C65_CCLROM_H


namespace CCLROM {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;

    static const C65Pin A0  {0, "A0"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin A1  {1, "A1"  ,ioType::eInputs, siType::eInput};
    static const C65Pin A2  {2 ,"A2"  ,ioType::eInputs, siType::eInput};
    static const C65Pin A3  {3 ,"A3"  ,ioType::eInputs, siType::eInput};
	static const C65Pin A4  {4, "A4" ,ioType::eInputs,  siType::eInput};
	static const C65Pin A5  {5, "A5" ,ioType::eInputs,  siType::eInput};
    static const C65Pin A6  {6, "A6"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin A7  {7, "A7" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D4  {8, "D4"  ,ioType::eInputs,  siType::eInput};
    static const C65Pin D5  {9, "D5" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D6  {10, "D6" ,ioType::eInputs,  siType::eInput};
    static const C65Pin D7  {11, "D7" ,ioType::eInputs, siType::eInput};
    static const C65Pin CS_  {12,"CS-"  ,ioType::eInputs, siType::eInput};
    static const C65Pin RST {13,"RST" ,ioType::eInputs, siType::eInput};

    static const C65Pin O0 {14,"O0" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O1 {15,"O1" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O2 {16,"O2" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O3 {17,"O3" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O4 {18,"O4" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O5 {19,"O5" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O6 {20,"O6" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O7 {21,"O7" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O8 {22,"O8" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin O9 {23,"O9" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OA {24,"OA" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OB {25,"OB" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OC {26,"OC" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OD {27,"OD" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OE {28,"OE" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OF {29,"OF" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OG {30,"OG" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OH {31,"OH" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OI {32,"OI" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OJ {33,"OJ" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OK {34,"OK" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OL {35,"OL" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin OM {36,"OM" ,ioType::eOutputs, siType::eOutput};
    static const C65Pin NNXS {37,"NNXS" ,ioType::eOutputs, siType::eOutput};

    static const C65Pin NXS {38,"NXS" ,ioType::eOutputs, siType::eOutput};


	static const C65Pin all[] = {
            A0, A1, A2, A3,  A4,  A5, A6, A7, D4, D5, D6, D7,  CS_, RST,
            O0, O1, O2, O3,  O4,  O5, O6, O7, O8, O9, OA, OB,  OC,  OD, OE, OF, OG, OH, OI, OJ, OK, OL, OM, NNXS, NXS
	};
    static const int allSize = 39;

    static const uint32_t clearMask = 0b11111111111111;//x14 inputs

    static const short outIndex = 14;
}


class CCLROM final : public C65 {
public:
  static constexpr char const *const TYPE{ "chips/CCLROM" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CCLROM();

  void calculate();

private:
  void putRom(size_t addr,uint32_t value);
	  void compileBatch();
	  std::vector<std::string> _pcodesVec{};
	  uint32_t compileOMap(std::vector<std::string> const oMap, std::string stepDef);
  //private uint64_t content;
  std::vector<std::string> romContentBatch{
	  "oMap:HOLD",
	  "oMap:RAM-IN",
	  "oMap:MR-IN",
	  "oMap:RAM-OUT",
	  "oMap:IR-IN",
	  "oMap:IR-OUT",
	  "oMap:AR-IN",
	  "oMap:AR-OUT",
	  "oMap:AL-OUT",
	  "oMap:AL-SUB",
	  "oMap:BR-IN",
	  "oMap:BR-OUT",
	  "oMap:OUT-IN",
	  "oMap:CN-ENC",
	  "oMap:CN-JUMP",
	  "oMap:CN-OUT",
	  "oMap:RST",
	  "oMap:FLR-IN",
	  "oMap:PRMODE",
	  "oInit:CN-OUT MR-IN",
	  "oInit:RAM-OUT IR-IN CN-ENC",
      "oPCod:LDA",//0001
	  "oStep: IR-OUT  MR-IN",
	  "oStep: RAM-OUT AR-IN",
      "oPCod:ADD",//0010
	  "oStep: IR-OUT  MR-IN",
	  "oStep: RAM-OUT BR-IN",
	  "oStep: AL-OUT AR-IN FLR-IN",
      "oPCod:SUB",//0011
      "oStep: IR-OUT MR-IN",
      "oStep: AL-SUB RAM-OUT BR-IN ",
      "oStep: AL-OUT AR-IN FLR-IN",
      "oPCod:STA",//0100
      "oStep: IR-OUT MR-IN",//put adress part of instruction into MR (to point given ram address)
	  "oStep: AR-OUT RAM-IN",//store reg A into RAM
      "oPCod:LDI",//0101:load immidiate - load value given into register A
      "oStep: IR-OUT AR-IN",
	  "oPCod:JMP",//0110:jump - jump unconditional to address given
	  "oStep: IR-OUT CN-JUMP",
	  "oPCod:JC",//0111:jump on carry - behavior (conditional reset of step counter) harcoded in simulated hardware
	  "oStep: IR-OUT CN-JUMP",
	  "oPCod:JZ",//1000:jump on zero - behavior (conditional reset of step counter) harcoded in simulated hardware
	  "oStep: IR-OUT CN-JUMP",
	  "oPCod:9",//1001
	  "oPCod:10",//1010
	  "oPCod:11",//1011
	  "oPCod:12",//1100
	  "oPCod:13",//1101
	  "oPCod:OUT",//1110
	  "oStep: AR-OUT OUT-IN",
      "oPCod:HLT",//1111
      "oStep: HOLD",

  };

  std::vector<uint32_t> romContent{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
  std::vector<std::string> opCodes{"NOP"};
};


} //namespace C74LS189


#endif // C65_CCLROM_H
