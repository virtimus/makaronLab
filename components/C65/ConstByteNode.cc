#include "ConstByteNode.h"
#include <ConstByte.h>

#include <QSpinBox>
#include <QTableWidget>

ConstByteNode::ConstByteNode()
{
  QFont font{};
  font.setFamily("Consolas");
  font.setPointSize(10);
  auto widget = new QGraphicsSimpleTextItem(QString::number(0));
  widget->setFont(font);

  auto brush = widget->brush();
  brush.setColor(Qt::white);
  widget->setBrush(brush);

  setCentralWidget(widget);

  m_info = widget;
}

void ConstByteNode::refreshCentralWidget()
{
  if (!m_element) return;
  uint8_t const VALUE{ std::get<uint8_t>(m_element->outputs()[0].value) };
  m_info->setText(QString::number(VALUE));

  calculateBoundingRect();
}

void ConstByteNode::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eOutputs);

  propertiesInsertTitle("Const Byte");

  int row = m_properties->rowCount();
  m_properties->insertRow(row);

  QTableWidgetItem *item{};

  item = new QTableWidgetItem{ "Value" };
  item->setFlags(item->flags() & ~Qt::ItemIsEditable);
  m_properties->setItem(row, 0, item);

  auto const CONST_BYTE = static_cast<ConstByte *>(m_element);
  int const CURRENT = CONST_BYTE->currentValue();

  QSpinBox *const value = new QSpinBox;
  value->setRange(std::numeric_limits<uint8_t>::min(), std::numeric_limits<uint8_t>::max());
  value->setValue(static_cast<int>(CURRENT));
  m_properties->setCellWidget(row, 1, value);

  QObject::connect(value, static_cast<void (QSpinBox::*)(int)>(&QSpinBox::valueChanged),
                   [CONST_BYTE](int a_value) { CONST_BYTE->set(a_value); });
}

