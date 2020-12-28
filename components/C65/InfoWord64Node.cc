#include "InfoWord64.h"
#include <InfoWord64Node.h>

#include <QGraphicsSimpleTextItem>
#include <QTableWidget>


InfoWord64Node::InfoWord64Node()
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

void InfoWord64Node::refreshCentralWidget()
{
  if (!m_element) return;
  uint64_t const value{ std::get<uint64_t>(m_element->inputs()[0].value) };
 //if (m_max < value) {
 //    m_max = value;
  m_info->setText(QString::number(value));
 //}

  calculateBoundingRect();
}

void InfoWord64Node::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eInputs);
  showIOProperties(spaghetti::IOSocketsType::eOutputs);
}


