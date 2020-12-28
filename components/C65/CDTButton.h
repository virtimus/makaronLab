#pragma once
#ifndef C65_CDTBUTTON_H
#define C65_CDTBUTTON_H

namespace CDTButton {

class CDTButton final : public spaghetti::Element {
public:
  static constexpr char const *const TYPE{ "chips/CDTButton" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CDTButton();

  void toggle();

  //void calculate();
  //private uint64_t content;
  //std::vector<uint8_t> content{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

  void set(bool a_state);

  void updState();

  bool currentValue() const { return m_currentValue; }

 private:
  bool m_currentValue{};
};


} //namespace CDTBUTTON


#endif // C65_CDTBUTTON_H
