#pragma once
#ifndef CHIPS_CPCPCNODE_H
#define CHIPS_CPCPCNODE_H

#include "ChipsNode.h"

namespace makaron::chips {

class CPCPCNode : public ChipsNode {
 public:
	CPCPCNode();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsTextItem *_info{};

};

}//namespace makaron::chips

#endif // CHIPS_CPCPCNODE_H
