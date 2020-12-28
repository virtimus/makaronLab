#pragma once
#ifndef C65_CONSTBYTENODE_H
#define C65_CONSTBYTENODE_H

#include "spaghetti/node.h"

class ConstByteNode : public spaghetti::Node {
 public:
	ConstByteNode();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsSimpleTextItem *m_info{};
};



#endif // C65_CONSTBYTENODE_H
