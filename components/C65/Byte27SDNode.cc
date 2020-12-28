#include "Byte27SDNode.h"
#include "Byte27SD.h"

#include <QTableWidget>

#include <QSpinBox>

class Byte27SDNodeWidget : public QGraphicsItem {
 public:
	Byte27SDNodeWidget()
    : QGraphicsItem{}
  {
    createSegments();
  }

  QRectF boundingRect() const override { return m_boundingRect; }

  void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override
  {
    (void)a_option;
    (void)a_widget;

    QBrush const ON{ Qt::darkGreen };
    QBrush const OFF{ QColor(30, 30, 30, 128) };
    //QBrush const OFF{ Qt::black };

    a_painter->translate(10.0, 10.0);
    a_painter->setPen(Qt::NoPen);

    a_painter->setBrush(m_states[0] ? ON : OFF);
    a_painter->drawPolygon(m_segments[0]);

    a_painter->setBrush(m_states[1] ? ON : OFF);
    a_painter->drawPolygon(m_segments[1]);

    a_painter->setBrush(m_states[2] ? ON : OFF);
    a_painter->drawPolygon(m_segments[2]);

    a_painter->setBrush(m_states[3] ? ON : OFF);
    a_painter->drawPolygon(m_segments[3]);

    a_painter->setBrush(m_states[4] ? ON : OFF);
    a_painter->drawPolygon(m_segments[4]);

    a_painter->setBrush(m_states[5] ? ON : OFF);
    a_painter->drawPolygon(m_segments[5]);

    a_painter->setBrush(m_states[6] ? ON : OFF);
    a_painter->drawPolygon(m_segments[6]);

    a_painter->setBrush(m_states[7] ? ON : OFF);
    a_painter->drawEllipse(m_segments[7].boundingRect());
  }

  void setState(size_t const a_index, bool const a_value) { m_states[a_index] = a_value; }

 private:
  void createSegments()
  {
    // Segment A
    m_segments[0] << QPointF{ 22.0, 19.0 } << QPointF{ 38.0, 4.0 } << QPointF{ 96.0, 4.0 } << QPointF{ 111.0, 19.0 }
                  << QPointF{ 96.0, 34.0 } << QPointF{ 38.0, 34.0 };

    // Segment B
    m_segments[1] << QPointF{ 115.0, 23.0 } << QPointF{ 131.0, 37.0 } << QPointF{ 131.0, 83.0 }
                  << QPointF{ 115.0, 98.0 } << QPointF{ 99.0, 83.0 } << QPointF{ 99.0, 37.0 };

    // Segment C
    m_segments[2] << QPointF{ 115.0, 105.0 } << QPointF{ 131.0, 119.0 } << QPointF{ 131.0, 165.0 }
                  << QPointF{ 115.0, 180.0 } << QPointF{ 99.0, 165.0 } << QPointF{ 99.0, 119.0 };

    // Segment D
    m_segments[3] << QPointF{ 22.0, 183.0 } << QPointF{ 38.0, 167.0 } << QPointF{ 96.0, 167.0 }
                  << QPointF{ 111.0, 183.0 } << QPointF{ 96.0, 199.0 } << QPointF{ 38.0, 199.0 };

    // Segment E
    m_segments[4] << QPointF{ 19.0, 105.0 } << QPointF{ 35.0, 119.0 } << QPointF{ 35.0, 165.0 }
                  << QPointF{ 19.0, 180.0 } << QPointF{ 4.0, 165.0 } << QPointF{ 4.0, 119.0 };

    // Segment F
    m_segments[5] << QPointF{ 19.0, 23.0 } << QPointF{ 35.0, 37.0 } << QPointF{ 35.0, 83.0 } << QPointF{ 19.0, 98.0 }
                  << QPointF{ 4.0, 83.0 } << QPointF{ 4.0, 37.0 };

    // Segment G
    m_segments[6] << QPointF{ 22.0, 101.0 } << QPointF{ 38.0, 85.0 } << QPointF{ 96.0, 85.0 } << QPointF{ 111.0, 101.0 }
                  << QPointF{ 96.0, 116.0 } << QPointF{ 38.0, 116.0 };

    // Segment DP
    m_segments[7] << QPointF{ 133.0, 162.0 } << QPointF{ 171.0, 162.0 } << QPointF{ 171.0, 199.0 }
                  << QPointF{ 133.0, 199.0 };
  }

 private:
  QPolygonF m_segments[8]{};
  QRectF m_boundingRect{ 0, 0, 194, 222 };
  bool m_states[8]{};
};

Byte27SDNode::Byte27SDNode()
{
  auto const widget = new Byte27SDNodeWidget;
  setCentralWidget(widget);

  m_widget = widget;
  m_color = QColor{ 25, 25, 25, 128 };
}

void Byte27SDNode::setInputsB(bool const a_A, bool const a_B, bool const a_C, bool const a_D,
                                          bool const a_E, bool const a_F, bool const a_G)
{
	m_inputsB[0] = a_A;
	m_inputsB[1] = a_B;
	m_inputsB[2] = a_C;
	m_inputsB[3] = a_D;
	m_inputsB[4] = a_E;
	m_inputsB[5] = a_F;
	m_inputsB[6] = a_G;
}

void Byte27SDNode::refreshCentralWidget()
{
  if (!m_element) return;

  auto const &inputs = m_element->inputs();
  auto const CV = ((Byte27SD *)m_element)->currentValue();

  uint8_t A{ std::get<uint8_t>(inputs[0].value) };
  bool B {  std::get<bool>(inputs[1].value) };
  //int32_t const VALUE { (D << 3) | (C << 2) | (B << 1) | A };

  //uint8_t C = (A/(pow(10,CV)))%10;
  uint8_t C =((int)(A/pow(10,CV)) % 10 );

  switch (C) {
    case 0: setInputsB(true, true, true, true, true, true, false); break;
    case 1: setInputsB(false, true, true, false, false, false, false); break;
    case 2: setInputsB(true, true, false, true, true, false, true); break;
    case 3: setInputsB(true, true, true, true, false, false, true); break;
    case 4: setInputsB(false, true, true, false, false, true, true); break;
    case 5: setInputsB(true, false, true, true, false, true, true); break;
    case 6: setInputsB(true, false, true, true, true, true, true); break;
    case 7: setInputsB(true, true, true, false, false, false, false); break;
    case 8: setInputsB(true, true, true, true, true, true, true); break;
    case 9: setInputsB(true, true, true, true, false, true, true); break;
    default: setInputsB(false, false, false, false, false, false, false); break;
  }

  m_inputsB[7] = B;

  m_widget->setState(0, m_inputsB[0]);
  m_widget->setState(1, m_inputsB[1]);
  m_widget->setState(2, m_inputsB[2]);
  m_widget->setState(3, m_inputsB[3]);
  m_widget->setState(4, m_inputsB[4]);
  m_widget->setState(5, m_inputsB[5]);
  m_widget->setState(6, m_inputsB[6]);
  m_widget->setState(7, m_inputsB[7]);

  calculateBoundingRect();
}

void Byte27SDNode::showProperties()
{
  showCommonProperties();

  propertiesInsertTitle("Byte27SD");

  int row = m_properties->rowCount();
  m_properties->insertRow(row);

  QTableWidgetItem *item{};

  item = new QTableWidgetItem{ "DigitPos" };
  item->setFlags(item->flags() & ~Qt::ItemIsEditable);
  m_properties->setItem(row, 0, item);

  auto const CONST_INT = static_cast<Byte27SD *>(m_element);
  uint8_t const CURRENT = CONST_INT->currentValue();

  QSpinBox *const value = new QSpinBox;
  value->setRange(std::numeric_limits<uint8_t>::min(), std::numeric_limits<uint8_t>::max());
  value->setValue(static_cast<int>(CURRENT));
  m_properties->setCellWidget(row, 1, value);

  QObject::connect(value, static_cast<void (QSpinBox::*)(int)>(&QSpinBox::valueChanged),
                   [CONST_INT](uint8_t a_value) { CONST_INT->set(a_value); });


  showIOProperties(spaghetti::IOSocketsType::eInputs);
  showIOProperties(spaghetti::IOSocketsType::eOutputs);
}


