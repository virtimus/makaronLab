#pragma once
#ifndef C65_W64RAM_H
#define C65_W64RAM_H

#include "C65.h"
#include "W64.h"

namespace W64 {


namespace CPins {
        //using siType = SiType;
       // using ioType = IoType;
        //using vlType = VlType;


static const C65Pin A   {0,"A",   IoSide::Left,  SiType::Input, IoType::Word64 };
static const C65Pin D   {1,"D",   IoSide::Left,  SiType::Input, IoType::Word64 };
static const C65Pin LD  {2,"LD",  IoSide::Left,  SiType::Input};
static const C65Pin EN  {3,"EN",  IoSide::Left,  SiType::Input};
static const C65Pin RST {4,"RST", IoSide::Left,  SiType::Input};
static const C65Pin O   {5,"O",   IoSide::Right, SiType::Output, IoType::Word64};
static const C65Pin I   {6,"I",   IoSide::Right, SiType::Output, IoType::Word64};
static const C65Pin IA   {7,"IA",   IoSide::Right, SiType::Output, IoType::Word64};


	static const C65Pin all[] = {
            A,D,LD,EN,RST,
            O,I, IA
	};
    static const int allSize = 8;
}


class W64RAM final : public W64::W64 {
public:
  static constexpr char const *const TYPE{ "chipsW64/W64RAM" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  W64RAM();

  void calculate();
  std::vector<uint64_t> content{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
};


} //namespace W64


#endif // C65_W64RAM_H
