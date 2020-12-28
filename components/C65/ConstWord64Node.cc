#include "ConstWord64Node.h"
#include <ConstWord64.h>

#include <QSpinBox>
#include <QTableWidget>

ConstWord64Node::ConstWord64Node()
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

void ConstWord64Node::refreshCentralWidget()
{
  if (!m_element) return;
  uint64_t const VALUE{ std::get<uint64_t>(m_element->outputs()[0].value) };
  m_info->setText(QString::number(VALUE));

  calculateBoundingRect();
}

void ConstWord64Node::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eOutputs);

  propertiesInsertTitle("Const Word64");

  int row = m_properties->rowCount();
  m_properties->insertRow(row);

  QTableWidgetItem *item{};

  item = new QTableWidgetItem{ "Value" };
  item->setFlags(item->flags() & ~Qt::ItemIsEditable);
  m_properties->setItem(row, 0, item);

  auto const CONST_W64 = static_cast<ConstWord64 *>(m_element);
  int const CURRENT = CONST_W64->currentValue();

  QSpinBox *const value = new QSpinBox;
  value->setRange(std::numeric_limits<int32_t>::min(), std::numeric_limits<int32_t>::max());
  value->setValue(static_cast<int>(CURRENT));
  m_properties->setCellWidget(row, 1, value);

  QObject::connect(value, static_cast<void (QSpinBox::*)(int)>(&QSpinBox::valueChanged),
                   [CONST_W64](int a_value) { CONST_W64->set(a_value); });
}

