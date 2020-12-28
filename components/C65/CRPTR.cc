#include "C65.h"
#include "CRPTR.h"

namespace CRPTR {

CRPTR::CRPTR() : spaghetti::Element{}
{
	  //setPinsAllSize(CPins::allSize);
	  //C65::addAllIO(CPins::all);

	  //initROM
	  //romPart2_11();
	  //romPart2_14();
	  //romPart2_16();
       setMinInputs(0);
	   setMaxInputs(255);
       setMinOutputs(0);
	   setMaxOutputs(255);
	   //m_orient = spaghetti::EOrientation::eLeft;

       addInput(spaghetti::ValueType::eBool, "#0", IOSocket::eCanHoldBool | IOSocket::eCanHoldWord64  | IOSocket::eCanChangeName,spaghetti::SocketItemType::eInput);
       addOutput(spaghetti::ValueType::eBool, "#0", IOSocket::eCanHoldBool | IOSocket::eCanHoldWord64 | IOSocket::eCanChangeName,spaghetti::SocketItemType::eOutput);
       updPBStates();
}


void CRPTR::serialize(Json &a_json) {
	 Element::serialize(a_json);
	  auto &jsonElement = a_json["element"];
	  auto jsonPbStates = Json::array();
	  size_t const PBS_COUNT{ m_pbstates.size() };
	  for (size_t i = 0; i < PBS_COUNT; ++i) {
		  Json jsState{};
		  jsState["index"] = i;
		  bool b = m_pbstates[i];
		  jsState["state"] = b;
		  jsonPbStates.push_back(jsState);
	  }

	  auto &jsonRPTR = jsonElement["rptr"];
	  jsonRPTR["pbStates"] = jsonPbStates;
}


void CRPTR::deserialize(Json const &a_json){
	Element::deserialize(a_json);
	auto const &ELEMENT = a_json["element"];
	if ((ELEMENT.find("rptr")!=ELEMENT.end())){
			auto const &IO = ELEMENT["rptr"];
			auto const &PBS = IO["pbStates"];

            /*auto add_pbStates = [&](Json const &a_socket, PBStates &pbStates) {
				auto const INDEX = a_socket["index"].get<size_t>();
				auto const pbSTATE = a_socket["state"].get<bool>();
				pbStates[INDEX]=pbSTATE;
            };*/

            for (auto &&state : PBS){
                //add_pbStates(state, m_pbstates);
                auto const INDEX = state["index"].get<size_t>();
                auto const pbSTATE = state["state"].get<bool>();
                set(INDEX,pbSTATE);
            }
	}
}



size_t CRPTR::addInputS(spaghetti::ValueType const a_type, std::string const &a_name, uint8_t const a_flags, spaghetti::SocketItemType sItemType)
{
	//if (!m_adding){
		//m_adding = true;
	    size_t result = Element::addInputS(a_type, a_name, a_flags | IOSocket::eCanHoldBool | IOSocket::eCanHoldWord64 | IOSocket::eCanChangeName,spaghetti::SocketItemType::eInput);
        updPBStates();
		/*if (m_inputs.size()>m_outputs.size()){
			Element::addOutput(a_type, a_name, a_flags | IOSocket::eCanHoldBool,spaghetti::SocketItemType::eOutput);
		}*/
	//}
        return result;
}

void CRPTR::updPBStates(){
    while (m_outputs.size()>m_pbstates.size()){
        addPBState();
    }
    while (m_outputs.size()<m_pbstates.size()){
        m_pbstates.pop_back();
    }
}

void CRPTR::set(size_t i, bool a_state){
   updPBStates();
   if (i<m_pbstates.size())
       m_pbstates[i]=a_state;
}

size_t CRPTR::addOutputS(spaghetti::ValueType const a_type, std::string const &a_name, uint8_t const a_flags, spaghetti::SocketItemType sItemType)
{
	//if (!m_adding){
		//m_adding = true;
	    size_t result = Element::addOutputS(a_type, a_name, a_flags | IOSocket::eCanHoldBool | IOSocket::eCanHoldWord64 | IOSocket::eCanChangeName ,spaghetti::SocketItemType::eOutput);
        updPBStates();

		/*if (m_outputs.size()>m_inputs.size()){
			Element::addInput(a_type, a_name, a_flags,spaghetti::SocketItemType::eInput);
		}*/
	//}
        return result;
}

void CRPTR::calculate()
  {
	// read inputs
	//inpToPins(CPins::all);

	size_t s = m_inputs.size();
	uint64_t out64 = 0;
    bool pbEnabled = true;
	for (size_t i=0;i<s;i++){
		if (i<m_outputs.size()){
            if (0 == m_inputs[i].value.index()){//bool
				bool val = std::get<bool>(m_inputs[i].value);
				if (i<m_pbstates.size() && pbEnabled){
					val = val || m_pbstates[i];
				}
                                if (0 == m_outputs[i].value.index()){
                                   m_outputs[i].value = val;
                                }
			} else {//W64
				const uint64_t  val{ std::get<uint64_t>(m_inputs[i].value) };
				out64 |= val;
			}
		}
	}

	for (size_t i=0;i<s;i++){
		if (i<m_outputs.size()){
            if (0 == m_outputs[i].value.index()){//bool
				//nop
			} else {
				m_outputs[i].value = out64;
			}
		}
	}


  }




}//namespace CRPTR
