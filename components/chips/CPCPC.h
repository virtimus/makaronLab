#pragma once
#ifndef CHIPS_CPCPC_H
#define CHIPS_CPCPC_H

#include "Chips.h"

namespace makaron::chips {

class CPCPC final : public Chips {
 public:
  static constexpr char const *const TYPE{ "chips/CPCPC" };
  CHIPS_HASH_DEFS;

  CPCPC();
  cpc_t* currentCpc() { return _cpc;};
  uint64_t currentValue(){ return _currentValue; }
  void calculate() override;
 private:

  uint64_t _currentValue;
  cpc_t* _cpc;
};

}//namespace makaron::chips

#endif // CHIPS_CPCPC_H
