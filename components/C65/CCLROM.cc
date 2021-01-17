#include "C65.h"
#include "CCLROM.h"

#include "spaghetti/logger.h"
#include "spaghetti/node.h"
#include "spaghetti/registry.h"
#include "spaghetti/package.h"



namespace CCLROM {

#include <stdexcept>
#include <sstream>

class Formatter
{
public:
    Formatter() {}
    ~Formatter() {}

    template <typename Type>
    Formatter & operator << (const Type & value)
    {
        stream_ << value;
        return *this;
    }

    std::string str() const         { return stream_.str(); }
    operator std::string () const   { return stream_.str(); }

    enum ConvertToString
    {
        to_str
    };
    std::string operator >> (ConvertToString) { return stream_.str(); }

private:
    std::stringstream stream_;

    Formatter(const Formatter &);
    Formatter & operator = (Formatter &);
};



CCLROM::CCLROM() : C65{}
{
	  setPinsAllSize(CPins::allSize);
	  C65::addAllIO(CPins::all);

	  compileBatch();
}

std::string  toBinary(uint64_t n)
{
    std::string s = "";
    while (n > 0)
    {
        s =  ( (n % 2 ) == 0 ? "0" : "1") +s;
        n = n / 2;
    }
    return s;
}

#include <algorithm>
#include <cctype>
#include <locale>

// trim from start (in place)
static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !std::isspace(ch);
    }));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
    ltrim(s);
    rtrim(s);
}


template < typename T>
short findInVector(const std::vector<T>  & vecOfElements, const T  & element)
{
    short result;
    // Find given element in vector
    auto it = std::find(vecOfElements.begin(), vecOfElements.end(), element);
    if (it != vecOfElements.end())
    {
        result = distance(vecOfElements.begin(), it);
    }
    else
    {
        result = -1;
    }
    return result;
}

std::vector<std::string> vectorise(std::string s,std::string delimiter){
	std::vector<std::string> result{};
	size_t pos = 0;
	std::string token;
	while ((pos = s.find(delimiter)) != std::string::npos) {
	    token = s.substr(0, pos);
	    //std::cout << token << std::endl;
	    result.push_back(token);
	    s.erase(0, pos + delimiter.length());
	}
	result.push_back(s);
	return result;
}

void setBit(uint32_t &value, short bitPos){
	value |= ((uint32_t)1) << bitPos;
}

uint32_t CCLROM::compileOMap(std::vector<std::string> const oMap, std::string stepDef){
	uint32_t result{};
	trim(stepDef);
	std::vector<std::string> vMap = vectorise(stepDef," ");
	for(int i=0;i<vMap.size();i++){
		std::string sdef = vMap[i];
		trim(sdef);
        if (sdef != ""){//ignore multiple spaces?
            short j = findInVector(oMap,sdef);
            if (j>31){
                throw std::runtime_error(Formatter() << "Wrong sdef item  :" << sdef << "(oMap Array out of bounds):" << j);
            } else if (j<0) {
                throw std::runtime_error(Formatter() << "Wrong sdef item :" << sdef);
            } else {
                setBit(result,j);
            }
        }
	}
	return result;
}

void  CCLROM::putRom(size_t addr,uint32_t value){
	while (romContent.size()<=addr){
		romContent.push_back(0);
	}
	romContent[addr] = value;
}

void  CCLROM::compileBatch(){
	std::vector<std::string> oMap{};
	std::vector<std::string> oInit{};
	std::vector<std::string> oPcodes{};
	//std::string oPCod{};
	uint8_t oStep = 0;
	uint8_t oPC = 0;
    ///uint8_t nPC = 0;//boot
	//std::vector<std::string> oInit{};

	for(int i = 0; i<romContentBatch.size();i++){
		std::string const s = romContentBatch[i];
		std::vector<std::string> v = vectorise(s,":");
		if (v.size()<2) throw std::runtime_error(Formatter() << "Wrong bcBatch instruction size (no ':'?): " << s);

		std::string instr = v[0];
		trim(instr);
		if (instr == "oMap"){
			//std::vector<std::string> v2 = vectorise(v[1]," ");
			oMap.push_back(v[1]);
		} else if (instr == "oInit"){
			oInit.push_back(v[1]);
		} else if (instr == "oPCod") {
            //oPC=nPC;
            //nPC++;
            oPC++;//
            oPcodes.push_back(v[1]);
			oStep = 0;
			for (int j=0;j<oInit.size();j++){
                putRom((oPC<<4)+oStep,compileOMap(oMap,oInit[oStep]));
				oStep++;
			}
		} else if (instr == "oStep") {
            if (oStep>12){
				throw std::runtime_error(Formatter() << "bcBatch opcode step vector size overflow:" << oStep);
			}
            putRom((oPC<<4)+oStep,compileOMap(oMap,v[1]));
			oStep++;
		} else {
			throw std::runtime_error(Formatter() << "Wrong bcBatch instruction:" << instr);
		}
	}

    // rom boot
    oStep = 0;
    for (int j=0;j<oInit.size();j++){
        putRom(/*(oPC<<4)+*/oStep,compileOMap(oMap,oInit[oStep]));
        oStep++;
    }
    oStep=0;
    _pcodesVec = oPcodes;

}

void CCLROM::calculate()
  {
	// read inputs
	inpToPins(CPins::all);

	//step
	short a0 = _pins.getPinS(CPins::A0);
	short a1 = _pins.getPinS(CPins::A1);
	short a2 = _pins.getPinS(CPins::A2);
	short a3 = _pins.getPinS(CPins::A3);

	//opcode
	short a4 = _pins.getPinS(CPins::A4);
	short a5 = _pins.getPinS(CPins::A5);
	short a6 = _pins.getPinS(CPins::A6);
	short a7 = _pins.getPinS(CPins::A7);


	// a0-3 - step
	// a4-a7 - opcode
	bool isNextStep=false;
	bool isNextNextStep=false;
	uint32_t value=0;
	bool isReset = _pins.getPin(CPins::RST);
	if (isReset){
		// leave at 0
		isNextStep = true;
		isNextNextStep = true;
	} else {
	    size_t address = a0 + 2*a1 + 4*a2 + 8*a3 + 16*a4 + 32*a5 + 64*a6 + 128*a7;

	    //	throw std::runtime_error(Formatter() << "Wrong bcBatch instruction code (bcRom size overflow): " << address);
	    //}


	    if (address<romContent.size()){
	        value = romContent[address];
	        isNextStep = (address+1<romContent.size() && romContent[address+1]>0);
	        isNextNextStep = (address+2<romContent.size() && romContent[address+2]>0);
	    }

	}

	uint64_t pins = _pins.tmpPinsG();
    pins &= CPins::clearMask;
    pins |= value<<CPins::outIndex;
	_pins.tmpPinsS(pins);
	_pins.setPin(CPins::NXS,isNextStep);
	_pins.setPin(CPins::NNXS,isNextNextStep);
	pinsToOut(CPins::all);

  /*  bool we = !_pins.getPin(CPins::WE_);
    uint8_t value = content[address];
    if (we){
         value =  _pins.getPinS(CPins::D0)
                 + 2 *  _pins.getPinS(CPins::D1)
                 + 4 *  _pins.getPinS(CPins::D2)
                 + 8 *  _pins.getPinS(CPins::D3)
                 + 16*  _pins.getPinS(CPins::D4)
                 + 32*  _pins.getPinS(CPins::D5)
                 + 64*  _pins.getPinS(CPins::D6)
                 +128*  _pins.getPinS(CPins::D7)
                 ;
         content[address]=value;
    }

    bool cs = !_pins.getPin(CPins::CS_);


        short bv = getBit(value,0);
        _pins.setPin(CPins::O0,(cs)?bv>0:false);
        _pins.setPin(CPins::I0,bv>0);
        bv = getBit(value,1);
        _pins.setPin(CPins::O1,(cs)?bv>0:false);
        _pins.setPin(CPins::I1,bv>0);
        bv = getBit(value,2);
        _pins.setPin(CPins::O2,(cs)?bv>0:false);
        _pins.setPin(CPins::I2,bv>0);
        bv = getBit(value,3);
        _pins.setPin(CPins::O3,(cs)?bv>0:false);
        _pins.setPin(CPins::I3,bv>0);
        bv = getBit(value,4);
        _pins.setPin(CPins::O4,(cs)?bv>0:false);
        _pins.setPin(CPins::I4,bv>0);
        bv = getBit(value,5);
        _pins.setPin(CPins::O5,(cs)?bv>0:false);
        _pins.setPin(CPins::I5,bv>0);
        bv = getBit(value,6);
        _pins.setPin(CPins::O6,(cs)?bv>0:false);
        _pins.setPin(CPins::I6,bv>0);
        bv = getBit(value,7);
        _pins.setPin(CPins::O7,(cs)?bv>0:false);
        _pins.setPin(CPins::I7,bv>0);*/

    //_pins.setPin(CPins::D4,_pins.getPin(CPins::A0));
    ///std::string s = toBinary(_pins.tmpPinsG());
    //consoleAppendF("s:{}",s);
	//pinsToOut(CPins::all);
  }

}//namespace CCLROM
