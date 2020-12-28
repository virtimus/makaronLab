#pragma once
#ifndef C65_CRIED_H
#define C65_CRIED_H

//#include "C65.h"
//#include "spaghetti/element.h"
/**
 * Raising edge detector
 */
namespace CRIED {

namespace CPins {
	using siType = spaghetti::SocketItemType;
	using ioType = spaghetti::IOSocketsType;

	static const C65Pin IN  {0, "IN"  ,ioType::eInputs,  siType::eInput};
	static const C65Pin OUT {1, "OUT" ,ioType::eOutputs,  siType::eOutput};

    static const C65Pin all[] = {
            IN,
            OUT
	};

    static const int allSize = 2;
}

class CRIED final : public C65 {
public:
  static constexpr char const *const TYPE{ "chips/CRIED" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CRIED();

  void calculate();
protected:
  uint16_t counter{0};
  uint16_t counterMax{1};
private:

};


} //namespace CRIED


#endif // C65_CRIED_H
