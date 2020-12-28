
#include <QCheckBox>
#include <QTableWidget>
#include <QGraphicsWidget>
#include <QGraphicsLayout>
#include <QGraphicsScene>
#include <QVBoxLayout>

#include <QGraphicsSceneMouseEvent>

#include "spaghetti/element.h"
#include "CRPTR.h"
#include "CRPTRNode.h"

namespace CRPTR {

class CRPTR;
class CRPTRNode;

enum class PBType { ePush, eToggle };

#define HBUTTON 15
#define HBUTTON_SPACE 5
#define HBUTTON_GLOBAL 25

class PushButtonWidget : public QGraphicsItem {
 public:
	 // explicit PushButtonWidget(QGraphicsItem *const a_parent = nullptr);
	 // ~PushButtonWidget() override;

  QRectF boundingRect() const override { return m_boundingRect; }

  void mousePressEvent(QGraphicsSceneMouseEvent *a_event) override
  {
    (void)a_event;    
    if (m_type == PBType::eToggle){
    	//m_state = true;
        m_CRPTR->toggle(index);
    } else {
        //m_state = true;
        m_CRPTR->set(index,true);
    }
  }

  void mouseReleaseEvent(QGraphicsSceneMouseEvent *a_event) override
  {
    (void)a_event;
    if (m_type == PBType::eToggle){
        //nop
    } else {
        //m_state = false;
        m_CRPTR->set(index,false);
        if (m_CRPTRNode != nullptr){
            m_CRPTRNode->onPBReleased(index);
        }
    }
  }

  void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override
  {
    (void)a_option;
    (void)a_widget;

    updRec();

    QBrush const BRUSH{ (state() ? QColor{ 203, 217, 81 } : QColor{ 244, 53, 64 }) };
    QPen const PEN{ Qt::black };

    a_painter->setPen(PEN);
    a_painter->setBrush(BRUSH);
    //a_painter->drawRect(m_boundingRect);
    a_painter->drawRect(boundingRect());
  }

  void setCRPTR(CRPTR *const rptr) { m_CRPTR = rptr; }
  void setCRPTRNode(CRPTRNode *const node) { m_CRPTRNode = node; }
  void setIndex( size_t n) { index = n; }
  void setType( PBType nType) { m_type = nType; }
  void setState(bool nstate) { if (m_CRPTR != nullptr) m_CRPTR->pbStates()[index] = nstate; }
  bool state() { return (m_CRPTR != nullptr) ? m_CRPTR->pbStates()[index] : false; }

  void updRec(){
      m_boundingRect.setX((m_type == PBType::ePush)?0:40);
      m_boundingRect.setY(index*(HBUTTON+HBUTTON_SPACE));
      m_boundingRect.setHeight(HBUTTON);
      m_boundingRect.setWidth(40);
  }

 private:
  size_t index = 0;
  //bool m_state{};
  PBType m_type{ PBType::ePush };
  QRectF m_boundingRect{ 0, 0, 40, index*(HBUTTON+HBUTTON_SPACE) };
  //QRectF m_boundingRect{ 0, 0, 0, 0 };
  CRPTR *m_CRPTR{};
  CRPTRNode *m_CRPTRNode{};
};

class PushButtonsWidget : public QGraphicsItem {
 public:
  QRectF boundingRect() const override {  return m_boundingRect;/*return m_boundingRect;*/ }

  /*void mousePressEvent(QGraphicsSceneMouseEvent *a_event) override
  {
    //(void)a_event;
    //m_state = true;
    //m_pushButton->set(index,m_state);
  }

  void mouseReleaseEvent(QGraphicsSceneMouseEvent *a_event) override
  {
    //(void)a_event;
    //m_state = false;
    //m_pushButton->set(index,m_state);
  }*/

  void paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget) override
  {
    (void)a_option;
    (void)a_widget;
    updRec();

    //QBrush const BRUSH{ (m_state ? QColor{ 203, 217, 81 } : QColor{ 244, 53, 64 }) };
    //QPen const PEN{ Qt::black };

    //a_painter->setPen(PEN);
    //a_painter->setBrush(BRUSH);
    //a_painter->drawRect(m_boundingRect);
    //a_painter->drawRect(boundingRect());
  }

  void setCRPTR(CRPTR *const a_pushButton) {
      m_crptr = a_pushButton;


                                           }

 private:


  void updRec(){
	  if (m_crptr != nullptr){
          m_boundingRect.setHeight(m_crptr->outputs().size()*(HBUTTON+HBUTTON_SPACE)+HBUTTON_GLOBAL);
	  }
  }
  //size_t index = 0;
  //bool m_state{};
  QRectF m_boundingRect{ 0, 0, 80, 0 };
  CRPTR *m_crptr{};
};

void CRPTRNode::onPBReleased(size_t index){
    // update toggle button
    if (index<m_tbuttons.size()){
        m_tbuttons[index]->setState(false);
        //m_rbuttons[index]->setState(false);
    }
}

void CRPTRNode::addPButtons(){
    bool delta = false;
	while (m_pbuttons.size()<outputs().size()){
		auto const button = new PushButtonWidget;//{ static_cast<PushButtonsWidget *>(m_centralWidget) };
		button->setType(PBType::ePush);
        button->setCRPTR(static_cast<CRPTR *>(m_element));
		button->setIndex(m_pbuttons.size());
		button->setParentItem(static_cast<PushButtonsWidget *>(m_centralWidget));
        button->setCRPTRNode(this);
		m_pbuttons.push_back(button);
        delta=true;
	}
    while (m_pbuttons.size()>outputs().size()){
        delete m_pbuttons.back();
        m_pbuttons.pop_back();
        delta=true;
    }
    while (m_tbuttons.size()<outputs().size()){
		auto const button = new PushButtonWidget;//{ static_cast<PushButtonsWidget *>(m_centralWidget) };
		button->setType(PBType::eToggle);
        button->setCRPTR(static_cast<CRPTR *>(m_element));
        button->setIndex(m_tbuttons.size());
		button->setParentItem(static_cast<PushButtonsWidget *>(m_centralWidget));
        button->setCRPTRNode(this);
        m_tbuttons.push_back(button);
        delta=true;
	}
    while (m_tbuttons.size()>outputs().size()){
        delete m_tbuttons.back();
        m_tbuttons.pop_back();
        delta=true;
    }
    /*if (delta){
        expand();
        iconify();
        expand();
        QGraphicsSceneMouseEvent me{};// = new QGraphicsSceneMouseEvent();
        mouseDoubleClickEvent(&me);
    }*/

}


CRPTRNode::CRPTRNode()
{
  auto const widget = new PushButtonsWidget;//{ this };  
  //widget->layout()->setAlignment(Qt::AlignTop);
  //QVBoxLayout layout = QVBoxLayout();
  //QVBoxLayout *playout = new chips/CRPTRQVBoxLayout;
  //layout.setAlignment(Qt.AlignTop)
  //playout->setAlignment(Qt::AlignTop);
  //widget->setLayout((QGraphicsLayout *)playout);
  setCentralWidget(widget);
  //QGraphicsLayout layout = new QGraphicsLayout;
  m_widget = widget;

}

void CRPTRNode::paint(QPainter *a_painter, QStyleOptionGraphicsItem const *a_option, QWidget *a_widget)
{
  (void)a_option;
  (void)a_widget;

  paintBorder(a_painter);

}

void CRPTRNode::elementSet()
{
  auto const pushButtonsWidget = static_cast<PushButtonsWidget *>(m_centralWidget);
  pushButtonsWidget->setCRPTR(static_cast<CRPTR *>(m_element));
  addPButtons();
  //removeInput();

  /*(m_mode == Mode::eIconified) ?*/ //expand();// : iconify();
  //calculateBoundingRect();
  //pvShowProperties();
  //scene()->update();
  //expand();
  //updateOutputs();

  //refreshCentralWidget();

  //update();
}

void CRPTRNode::refreshCentralWidget()
{
  if (!m_element) return;
  calculateBoundingRect();
}

void CRPTRNode::showProperties()
{
  spaghetti::Node::showProperties();
  //showIOProperties(spaghetti::IOSocketsType::eOutputs);

}

//void removeInput() override;
//void removeOutput() override;


void CRPTRNode::addOutput(){
	Node::addOutput();
	while (element()->outputs().size() > element()->inputs().size()){
		Node::addInput();
	}
	addPButtons();
}

void CRPTRNode::addInput(){
	Node::addInput();
	while (element()->inputs().size() > element()->outputs().size()){
		Node::addOutput();
	}
    addPButtons();
}

void CRPTRNode::removeInput(){
	Node::removeInput();
	while (element()->inputs().size() < element()->outputs().size()){
		Node::removeOutput();
	}
	addPButtons();
}

void CRPTRNode::removeOutput(){
	Node::removeOutput();
	while (element()->outputs().size() < element()->inputs().size()){
		Node::removeInput();
	}
	addPButtons();
}
/*void CRPTRNode::addSocket(spaghetti::IOSocketsType ioType, uint8_t const a_id, QString const &a_name, spaghetti::ValueType const a_valueType, SocketType const a_type)
{
	//!TODO! dynamic?
	//if (IOSocketsType::eInputs == ioType){
	Node::addSocket(spaghetti::IOSocketsType::eInputs,a_id, a_name+"(i)", a_valueType, spaghetti::SocketItemType::eInput);
	Node::addSocket(spaghetti::IOSocketsType::eOutputs,a_id, a_name+"(o)", a_valueType, spaghetti::SocketItemType::eOutput);
	//} else {

	//}


}*/

} // namespace spaghetti::nodes::values
