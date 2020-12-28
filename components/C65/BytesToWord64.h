#pragma once
#ifndef C65_BYTESTOWORD64_H
#define C65_BYTESTOWORD64_H

class BytesToWord64 final : public spaghetti::Element {
 public:
  static constexpr char const *const TYPE{ "chips/BytesToWord64" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  BytesToWord64();

  void calculate() override;
};

#endif // C65_BYTESTOWORD64_H
