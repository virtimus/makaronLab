#pragma once
#ifndef C65_INFOWORD64_H
#define C65_INFOWORD64_H

#include <spaghetti/element.h>



class InfoWord64 final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/InfoWord64" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };

  InfoWord64();

  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }
};



#endif // C65_INFOWORD64_H
