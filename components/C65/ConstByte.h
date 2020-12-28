#pragma once
#ifndef C65_CONSTBYTE_H
#define C65_CONSTBYTE_H

#include <spaghetti/element.h>



class ConstByte final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/ConstByte" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };

  ConstByte();

  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  void serialize(Json &a_json) override;
  void deserialize(Json const &a_json) override;

  void set(uint8_t a_value);

  uint8_t currentValue() const { return m_currentValue; }

 private:
  uint8_t m_currentValue{};
};



#endif // C65_CONSTBYTE_H
