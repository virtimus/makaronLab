#pragma once
#ifndef C65_INFOWORD64NODE_H
#define C65_INFOWORD64NODE_H

#include "spaghetti/node.h"



class InfoWord64Node : public spaghetti::Node {
 public:
	InfoWord64Node();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsSimpleTextItem *m_info{};
  uint64_t m_max = 0;
};



#endif // C65_INFOWORD64NODE_H
