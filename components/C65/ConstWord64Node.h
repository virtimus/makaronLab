#pragma once
#ifndef C65_CONSTWORD64NODE_H
#define C65_CONSTWORD64NODE_H

#include "spaghetti/node.h"

class ConstWord64Node : public spaghetti::Node {
 public:
	ConstWord64Node();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsSimpleTextItem *m_info{};
};



#endif // C65_CONSTWORD64NODE_H
