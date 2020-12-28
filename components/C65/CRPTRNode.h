#pragma once
#ifndef C65_CRPTRNODE_H
#define C65_CRPTRNODE_H

#include "spaghetti/node.h"
#include "spaghetti/element.h"
namespace CRPTR {

class PushButtonWidget;

class CRPTRNode : public  spaghetti::Node {
	using PButtons = QVector<PushButtonWidget *>;
private:
 void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override;
 void elementSet() override;
 void refreshCentralWidget() override;
 void addPButtons();
 PButtons m_pbuttons{};
 PButtons m_tbuttons{};
 class PushButtonsWidget *m_widget{};
public:

  CRPTRNode();
  void showProperties() override;
  //void addSocket(IOSocketsType ioType, uint8_t const a_id, QString const &a_name, ValueType const a_valueType, SocketType const a_type) override;

  //void addSocket(IOSocketsType ioType, uint8_t const a_id, QString const &a_name, ValueType const a_valueType, SocketType const a_type) override;

  //void addSocket(spaghetti::IOSocketsType ioType, uint8_t const a_id, QString const &a_name, spaghetti::ValueType const a_valueType, SocketType const a_type) override;
  void addOutput() override;
  void addInput() override;
  void removeInput() override;
  void removeOutput() override;
  void onPBReleased(size_t index);
};

} // namespace CRPTR

#endif // C65_CRPTRNODE_H
