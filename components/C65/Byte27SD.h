#pragma once
#ifndef C65_BYTE27SD_H
#define C65_BYTE27SD_H

#include <spaghetti/element.h>



class Byte27SD final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/Byte27SD" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }
  void serialize(Json &a_json) override;
  void deserialize(Json const &a_json) override;
  Byte27SD();

  void set(uint8_t a_value) { m_currentValue = a_value; };
  uint8_t currentValue() const { return m_currentValue; }

 private:
  uint8_t m_currentValue{0};
};


#endif // C65_BYTE27SD_H
