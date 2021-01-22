#pragma once
#ifndef C65_INFOBYTE_H
#define C65_INFOBYTE_H

#include <spaghetti/element.h>



class InfoByte final : public spaghetti::Element {
private:
	bool _hexValue = false;
 public:
  static constexpr char const *const TYPE{ "chips/InfoByte" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };

  InfoByte();

  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  bool hexValue() const { return _hexValue; }
  void setHexValue(bool n) { _hexValue = n; }

};



#endif // C65_INFOBYTE_H
