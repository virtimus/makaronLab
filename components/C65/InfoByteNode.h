#pragma once
#ifndef C65_INFOBYTENODE_H
#define C65_INFOBYTENODE_H

#include "spaghetti/node.h"
#include "InfoByte.h"
#include <sstream>
#include <iostream>
#include <iomanip>
#include <iostream>
#include <cctype>
#include <clocale>


class InfoByteNode : public spaghetti::Node {
 public:
	InfoByteNode();

        QString valueStr(){
                  QString result = "";
		  if (!m_element) return result;
		  uint8_t const value{ std::get<uint8_t>(m_element->inputs()[0].value) };
		  auto const element = static_cast<InfoByte *>(m_element);
		  if (element->hexValue()){
                      std::ostringstream ret;
                      ret << std::hex << +value;
                      std::string s = ret.str();
                      //s = std::toupper(s);
                      std::transform(s.begin(), s.end(),s.begin(), ::toupper);
                      result = QString::fromStdString(s);
		  } else {

                      result = QString::number(value);//.toStdString();
		  }
		  return result;
	}

 private:
  void refreshCentralWidget() override;
  void showProperties() override;

 private:
  QGraphicsSimpleTextItem *m_info{};
};



#endif // C65_INFOBYTENODE_H
