#pragma once
#ifndef C65_WORD64TOBYTES_H
#define C65_WORD64TOBYTES_H

#include "C65.h"
#include "spaghetti/element.h"

class Word64ToBytes final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/Word64ToBytes" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  Word64ToBytes();

  void calculate() override;
};

#endif // C65_WORD64TOBYTES_H
