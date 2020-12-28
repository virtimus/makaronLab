#include "CDTButtonNode.h"
#include "CDTButton.h"

#include <QCheckBox>
#include <QTableWidget>

namespace CDTButton {

//class CDTButton;

class CDTButtonNodeWidget : public QGraphicsItem {
 public:
   QRectF boundingRect() const override { return m_boundingRect; }

   void mousePressEvent(QGraphicsSceneMouseEvent *a_event) override { (void)a_event; }

  void mouseReleaseEvent(QGraphicsSceneMouseEvent *a_event) override
  {
    (void)a_event;
    m_state = !m_state;
    m_cdtButton->set(m_state);
  }

  void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override
  {
    (void)a_option;
    (void)a_widget;

    auto innerRect = m_boundingRect.adjusted(5.0, 10.0, -5.0, -20.0).translated(0.0, 5.0);
    QBrush brush{ (m_state ? QColor{ 203, 217, 81 } : QColor{ 244, 53, 64 }) };
    QPen pen{ Qt::black };
    a_painter->setPen(pen);
    a_painter->setBrush(brush);
    a_painter->drawRect(innerRect);

    QSizeF const toggleSize{ 30.0, m_boundingRect.height() };
    qreal const toggleX{ (m_state ? m_boundingRect.right() - toggleSize.width() : m_boundingRect.left()) };
    QRectF const toggleRect{ QPointF{ toggleX, m_boundingRect.top() }, toggleSize };

    //    brush.setColor(QColor{ 120,  83,  74, 255 });
    brush.setColor(Qt::lightGray);
    pen.setColor(Qt::black);
    a_painter->setPen(pen);
    a_painter->setBrush(brush);
    a_painter->drawRect(toggleRect);
  }

  void setCDTButton(CDTButton *const a_toggleButton) { m_cdtButton = a_toggleButton; }

 private:
  bool m_state{};
  QRectF m_boundingRect{ 0, 0, 80, 20 };
  CDTButton *m_cdtButton{};
};

CDTButtonNode::CDTButtonNode()
{
  auto const widget = new CDTButtonNodeWidget;
  setCentralWidget(widget);
}

void CDTButtonNode::paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget)
{
  (void)a_option;
  (void)a_widget;

  paintBorder(a_painter);
}

void CDTButtonNode::showProperties()
{
  showCommonProperties();
  showIOProperties(spaghetti::IOSocketsType::eOutputs);

  propertiesInsertTitle("Double Toggle Button");

  int row = m_properties->rowCount();
  m_properties->insertRow(row);

  QTableWidgetItem *item{};

  item = new QTableWidgetItem{ "Value" };
  item->setFlags(item->flags() & ~Qt::ItemIsEditable);
  m_properties->setItem(row, 0, item);

  auto const element = static_cast<CDTButton *>(m_element);
  bool const current = element->currentValue();

  QCheckBox *const value = new QCheckBox;
  m_properties->setCellWidget(row, 1, value);
  value->setChecked(current);

  QObject::connect(value, &QCheckBox::stateChanged, [element](int a_state) { element->set(a_state == 2); });
}

void CDTButtonNode::elementSet()
{
  auto const widget = static_cast<CDTButtonNodeWidget *>(m_centralWidget);
  widget->setCDTButton(static_cast<CDTButton *>(m_element));
}

} // CDTButtonNode
