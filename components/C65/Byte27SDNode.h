#pragma once
#ifndef C65_BYTE27SDNODE_H
#define C65_BYTE27SDNODE_H

#include "spaghetti/node.h"


class Byte27SDNode : public spaghetti::Node {
 public:
	Byte27SDNode();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;
  void setInputsB(bool const a_A, bool const a_B, bool const a_C, bool const a_D,
                                            bool const a_E, bool const a_F, bool const a_G);
 private:
  class Byte27SDNodeWidget *m_widget{};
  std::vector<bool> m_inputsB{false,false,false,false,false,false,false,false};
};



#endif // C65_BYTE27SDNODE_H
