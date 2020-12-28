#pragma once
#ifndef C65_CRPTR_H
#define C65_CRPTR_H




namespace CRPTR {

using PBStates = std::vector<bool>;


class CRPTR final : public spaghetti::Element {
protected:
	PBStates m_pbstates{};
public:
  static constexpr char const *const TYPE{ "chips/CRPTR" };
  static constexpr spaghetti::string::hash_t const HASH{ spaghetti::string::hash(TYPE) };
  char const *type() const noexcept override { return TYPE; }
  spaghetti::string::hash_t hash() const noexcept override { return HASH; }

  CRPTR();

  //overrides
  size_t addInputS(spaghetti::ValueType const a_type, std::string const &a_name, uint8_t const a_flags, spaghetti::SocketItemType sItemType) override;
  size_t addOutputS(spaghetti::ValueType const a_type, std::string const &a_name, uint8_t const a_flags, spaghetti::SocketItemType sItemType) override;
  void serialize(Json &a_json) override;
  void deserialize(Json const &a_json) override;

  void calculate();
  void updPBStates();
  PBStates &pbStates() { return m_pbstates; }
  void addPBState() { m_pbstates.emplace_back(false);}

  void set(size_t i, bool a_state);
  bool toggle(size_t i){ if (i<m_pbstates.size()) set(i,!m_pbstates[i]); return m_pbstates[i]; }


  bool currentValue(size_t i) const { return (i<m_pbstates.size())? m_pbstates[i]:false; }

 private:
  //bool m_currentValue{};


};


} //namespace CRPTR


#endif // C65_CRPTR_H
