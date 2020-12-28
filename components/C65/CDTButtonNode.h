#pragma once
#ifndef C65_CDTBUTTONNODE_H
#define C65_CDTBUTTONNODE_H

#include "spaghetti/node.h"

namespace CDTButton {

class CDTButtonNode : public spaghetti::Node {
 public:
  CDTButtonNode();

 private:
  void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override;

  void showProperties() override;

  void elementSet() override;

};

} // CDTButton

#endif // C65_CDTBUTTONNODE_H
