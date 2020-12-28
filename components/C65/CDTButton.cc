#include "C65.h"
#include "CDTButton.h"


namespace CDTButton {



CDTButton::CDTButton() : spaghetti::Element{}
{
	  setMinInputs(0);
	  setMaxInputs(0);
	  setMinOutputs(2);
	  setMaxOutputs(2);

    addOutput(spaghetti::ValueType::eBool, "State", IOSocket::eCanHoldBool | IOSocket::eCanChangeName);
    addOutput(spaghetti::ValueType::eBool, "!State", IOSocket::eCanHoldBool | IOSocket::eCanChangeName);
    updState();
}

void CDTButton::toggle()
{
    m_currentValue = !m_currentValue;
    updState();
}

void CDTButton::set(bool a_state)
{
    m_currentValue = a_state;
    updState();
}

void CDTButton::updState(){
    m_outputs[0].value = m_currentValue;
    m_outputs[1].value = !m_currentValue;
}



}//namespace CDTButton
