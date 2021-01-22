#include "InfoByteNode.h"
#include <InfoByte.h>

#include <QGraphicsSimpleTextItem>
#include <QTableWidget>
#include <QCheckBox>



InfoByteNode::InfoByteNode()
{
  QFont font{};
  font.setFamily("Consolas");
  font.setPointSize(10);
  auto widget = new QGraphicsSimpleTextItem(valueStr());
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

  m_info->setText(valueStr());

  calculateBoundingRect();
}

void InfoByteNode::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eInputs);
  showIOProperties(spaghetti::IOSocketsType::eOutputs);

  int row = m_properties->rowCount();
  m_properties->insertRow(row);

  QTableWidgetItem *item{};

  item = new QTableWidgetItem{ "HexValue" };
  item->setFlags(item->flags() & ~Qt::ItemIsEditable);
  m_properties->setItem(row, 0, item);

  auto const element = static_cast<InfoByte *>(m_element);
  bool const current = element->hexValue();

  QCheckBox *const value = new QCheckBox;
  m_properties->setCellWidget(row, 1, value);
  value->setChecked(current);

  QObject::connect(value, &QCheckBox::stateChanged, [element](int a_state) { element->setHexValue(a_state == 2); });


}

