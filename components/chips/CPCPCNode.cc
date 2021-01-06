#include "CPCPC.h"
#include <CPCPCNode.h>

#include <QGraphicsSimpleTextItem>
#include <QTableWidget>
#include <QGraphicsItem>
#include <QTextBrowser>
#include <QLayout>
#include <QVBoxLayout>
#include <QGraphicsLinearLayout>
//#include <LayoutItem>
#include <QGraphicsWidget>

namespace makaron::chips {

CPCPCNode::CPCPCNode()
{
  QFont font{};
  font.setFamily("Consolas");
  font.setPointSize(10);
  auto widget = new QGraphicsSimpleTextItem("0");
  widget->setFont(font);

  auto brush = widget->brush();
  brush.setColor(Qt::white);
  widget->setBrush(brush);

  QGraphicsTextItem *tb = new QGraphicsTextItem();
  tb->setOpenExternalLinks(true);
  std::string formatted = formatS("<html><>{}<html>","dupa");
  QString htmlString = formatted.c_str();// = formatted;//"<html>Hello Wordl!!<html>";
  tb->setHtml(htmlString);

  //QVBoxLayout *gi = new QVBoxLayout();
  //QGraphicsWidget *gi = new QGraphicsWidget();
  //tb->setParent(gi);
 // widget->setParentItem(gi);
 // gi->addWidget(tb);
 // QLayoutItem *item = new QLayoutItem(tb);
  //item->widget()
  //gi->insertWidget(0,tb);
  //item->addWidget(tb)
  //QWidget w1 = new QWidget;
  //w1->in
  //gi->insertItem(0,widget);

  //QWidget w = new QWidget;
  //w.setLayout(gi);


  setCentralWidget(tb);

  _info = tb;
}

std::string formatInfo(cpc_t *cpc){
    const std::string fRow = "<tr><td>{}</td><td>:</td><td><span style='color:yellow;'>{}</span></td></tr>";
    std::string result = "<table>";
    result += formatS(fRow,"z80.Pins",cpc->cpu.pins);
    result += "</table>";
    return result;
}

void CPCPCNode::refreshCentralWidget()
{
  if (!m_element) return;
  uint64_t const value = ((CPCPC*)m_element)->currentValue();//{ std::get<uint64_t>(((CPCPC*)m_element)->currentValue()) };
  cpc_t* pcpc = ((CPCPC*)m_element)->currentCpc();
  //if (m_max < value) {
 //    m_max = value;
 // uint64_t value = 0;
  QString ss = "PIN state:<span style='color:yellow;'>";
  ss+=QString::number(value)+"</span>"+formatInfo(pcpc).c_str();
  _info->setHtml(ss);
 //}

  calculateBoundingRect();
}

void CPCPCNode::showProperties()
{
  showCommonProperties();
  //showIOProperties(spaghetti::IOSocketsType::eInputs);
  //showIOProperties(spaghetti::IOSocketsType::eOutputs);
}


}//namespace makaron::chips

