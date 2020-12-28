#pragma once
#ifndef C65_CONSTWORD64_H
#define C65_CONSTWORD64_H

#include <spaghetti/element.h>



class ConstWord64 final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/ConstWord64" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };

  ConstWord64();

  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  void serialize(Json &a_json) override;
  void deserialize(Json const &a_json) override;

  void set(uint64_t a_value);

  uint64_t currentValue() const { return m_currentValue; }

 private:
  uint64_t m_currentValue{};
};



#endif // C65_CONSTWORD64_H
