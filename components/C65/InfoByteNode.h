#pragma once
#ifndef C65_INFOBYTENODE_H
#define C65_INFOBYTENODE_H

#include "spaghetti/node.h"



class InfoByteNode : public spaghetti::Node {
 public:
	InfoByteNode();

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsSimpleTextItem *m_info{};
};



#endif // C65_INFOBYTENODE_H
