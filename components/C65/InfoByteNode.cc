#include "InfoByteNode.h"
#include <InfoByte.h>

#include <QGraphicsSimpleTextItem>
#include <QTableWidget>


InfoByteNode::InfoByteNode()
{
  QFont font{};
  font.setFamily("Consolas");
  font.setPointSize(10);
  auto widget = new QGraphicsSimpleTextItem("0");
  widget->setFont(font);

  auto brush = widget->brush();
  brush.setColor(Qt::white);
  widget->setBrush(brush);

  setCentralWidget(widget);

  m_info = widget;
}

void InfoByteNode::refreshCentralWidget()
{
  if (!m_element) return;
  uint8_t const value{ std::get<uint8_t>(m_element->inputs()[0].value) };
  m_info->setText(QString::number(value));

  calculateBoundingRect();
}

void InfoByteNode::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eInputs);
  showIOProperties(spaghetti::IOSocketsType::eOutputs);
}

