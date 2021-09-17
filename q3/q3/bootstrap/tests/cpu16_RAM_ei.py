
from q3.api import *

#from q3.bootstrap.tests.benSAP1.common import makeCRAM
from q3.bootstrap.tests.benSAP1.common import makeNtoS
from q3.bootstrap.tests.benSAP1.common import makeStoN
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI
from q3.bootstrap.tests.benSAP1.cpu_RAM_4bitsel import makeRAM4BITSEL
import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei as dlatch8bitRegEI
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOENbitEI
from q3.bootstrap.tests.cpu16_REG import makeReg16bitEI

def makeCRAM16(name:str,parent:Module=None): 
    
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    def ramContent(m):
        mProps = m.props()
        return mProps['contentCRAM'] if 'contentCRAM' in mProps else None

    def calc(mimpl):
        m = mimpl.mdl()
        mProps = m.props()
        if not 'contentCRAM' in mProps:
            mProps['contentCRAM']= [0] * 65536 #[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        content = mProps['contentCRAM']
        #if not 'counterMax74LS163A' in mProps:
        #    mProps['counterMax74LS163A']=15
        #if not 'clock74LS163A' in mProps:
        #    mProps['clock74LS163A']=False
        #bool rst = _pins.getPinS(CPins::RST);
        rst = m.n('RST').value()
        #if (rst){
        if rst:
            '''
            /*  read program on reset
            *
            *
            */
            '''

            #std::vector<uint8_t>& c = content;
            c=content
            '''
            /*
            //prg
            c[0]=0b00011110;// LDA 14
            c[1]=0b00101111;// ADD 15
            c[2]=0b00111000;// SUB 8
            c[3]=0b11110000;// HLT
            c[4]=0b00000000;// NOP
            // data
            c[8]= 0b00000010;
            c[14]=0b00011100;
            c[15]=0b00001110;
        */  
            '''
            '''
                /*
            //prg
            c[0]=0b01010001;// ldi 1   //d81
            c[1]=0b00101110;// add $14 //d46
            c[2]=0b01001110;// sta $14 //d78
            c[3]=0b11100000;// out     //d224
            c[4]=0b01100000;// jmp 0   //d96
            c[5]=0b11110000;// hlt
            //data
            c[15]=0b00001110;
            */
            '''

            #//https://youtu.be/Zg1NdPKoosU?t=1843
            content[0]=0b00101111 #;// ADD $15
            content[1]=0b11100000 #;// out
            content[2]=0b01110100 #;// JC 4
            content[3]=0b01100000 #;// JMP 0
            content[4]=0b00111111 #;// SUB $15
            content[5]=0b11100000 #;// OUT
            content[6]=0b10000000 #;// JZ 0
            content[7]=0b01100100 #;// JMP 4
            #//data
            content[15]=0b0000001 #;
            mProps['contentCRAM']=content

            #}

        #short a0 = _pins.getPinS(CPins::A0);
        #short a1 = _pins.getPinS(CPins::A1);
        #short a2 = _pins.getPinS(CPins::A2);
        #short a3 = _pins.getPinS(CPins::A3);
        #size_t address = a0 + 2*a1 + 4*a2 + 8 *a3;
        
        #address = 0
        #for i in range(0,4,1):
        #    v = m.n(f'A{i}').value()
        #    address += v
        address = m.n('A').value()

        
        #bool we = !_pins.getPin(CPins::WE_);
        v = m.n('WEB').value()
        we =  not v 
        #uint8_t value = content[address];
        value = content[address]
        #if (we){
        if we:
            #value =  _pins.getPinS(CPins::D0)
            #        + 2 *  _pins.getPinS(CPins::D1)
            #        + 4 *  _pins.getPinS(CPins::D2)
            #        + 8 *  _pins.getPinS(CPins::D3)
            #        + 16*  _pins.getPinS(CPins::D4)
            #        + 32*  _pins.getPinS(CPins::D5)
            #        + 64*  _pins.getPinS(CPins::D6)
            #        +128*  _pins.getPinS(CPins::D7)
            value = m.n('D').value()        ;
            content[address]=value
            mProps['contentCRAM']=content
        


        #bool cs = !_pins.getPin(CPins::CS_);
        v = m.n('CSB').value()
        cs = not v
        if cs:
            m.n('O').setValue(value)
        m.n('I').setValue(value)


        #//_pins.setPin(CPins::D4,_pins.getPin(CPins::A0));
        #///std::string s = toBinary(_pins.tmpPinsG());
        #//consoleAppendF("s:{}",s);
        #pinsToOut(CPins::all);


    nA = m.iAdd('A',size=16)
    #nA1 = m.iAdd('A1')
    #nA2 = m.iAdd('A2')
    #nA3 = m.iAdd('A3')
    nD = m.iAdd('D',size=16)
    nRST = m.iAdd('RST')
    nWEB = m.iAdd('WEB')
    nCSD = m.iAdd('CSB')

    nO = m.oAdd('O',size=16)
    nI = m.oAdd('I',size=16)
    m.addMethod('ramContent',ramContent)
    m.setCalc(calc)
    
    return m






def makeRAM16bitSel(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    #nDA = {} # well - we use 8bit singal
    nA = m.iAdd('A', size = 16)
    nB = m.iAdd('B', size = 16)
    
    nSELB = m.iAdd('SELA')

    nO = m.oAdd('O', size = 16)
    #m.setSigFormula('O','= B if SELB else A')
    def calc(mimpl):
        m = mimpl.mdl()
        val = None
        if m.n('SELA').value():
            val =m.n('A').value()
        else:
            val = m.n('B').value()
        m.n('O').intSignal().setValue(val)

    m.setCalc(calc)

    return m

def makeRAMEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #m.iAdd('PA0')
    #m.iAdd('PA1')
    #m.iAdd('PA2')
    #m.iAdd('PA3')
    tsize = 16
    m.iAdd('PA',size=tsize)

    m.iAdd('PD',size=tsize)

    #m.iAdd('A0')
    ##m.iAdd('A1')
    #m.iAdd('A2')
    #m.iAdd('A3')
    m.iAdd('A',size=tsize)

    nD = m.iAdd('D',size=tsize)

    nRAMIN = m.iAdd('RAMIN')
    nMRIN = m.iAdd('MRIN')
    nPRMOD = m.iAdd('PRMOD')
    nRAMOUT = m.iAdd('RAMOUT')
    nRST = m.iAdd('RST')
    nCLK = m.iAdd('CLK')

    nO = m.oAdd('O',size=tsize)
    nI = m.oAdd('I',size=tsize)

    mCRAM = makeCRAM16('CRAM16',m)
    mBsAddress = makeRAM16bitSel('bsAddress',m)
    mBsData = makeRAM16bitSel('bsData',m)
    
    mRegAdr = makeReg16bitEI('regAddress',m) #dlatch8bitRegEI.makeReg16bitEI('4bRegAddress',m)

    #mEI = makeOE8bitEI('OE',m)

    mNAND0 = m.modAdd('NAND0',
        impl = 'local:/NAND'
        )

    mCRIED = m.modAdd('CRIED0',
        impl = 'local:/CRIED'
        )

    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )

    mNOT1 = m.modAdd('NOT1',
        impl = 'local:/NOT'
        )
    mI = m 
    mO = m
    if m.isRoot():
        mI = m.mod('moduleInputs')
        mO = m.mod('moduleOutputs')

    mI.n('A').c(mRegAdr.n('D'))
    mI.n('PA').c(mBsAddress.n('A'))
    
    mI.n('PD').c(mBsData.n('A'))

    mRegAdr.n('O').c(mBsAddress.n('B'))
    mBsAddress.n('O').c(mCRAM.n('A'))
    mBsData.n('O').c(mCRAM.n('D'))
    nD.c(mBsData.n('B'))
    
    mCRAM.n('O').c(mO.n('O'))
    mCRAM.n('I').c(mO.n('I'))

    #control signals
    m.n('RAMIN').c(mNAND0.n('A'))
    mNAND0.n('Y').c(mCRAM.n('WEB'))
    nCLK.c(mCRIED.n('A'))
    mCRIED.n('Y').c(mNAND0.n('B'))

    m.n('MRIN').c(mNOT0.n('A'))
    mNOT0.n('Y').c(mRegAdr.n('LOADB'))

    m.n('PRMOD').c(mRegAdr.n('ENABLEB'))
    m.n('PRMOD').c(mBsAddress.n('SELA'))
    m.n('PRMOD').c(mBsData.n('SELA'))

    m.n('RAMOUT').c(mNOT1.n('A'))
    mNOT1.n('Y').c(mCRAM.n('CSB'))

    m.n('CLK').c(mRegAdr.n('CLK'))
    m.n('RST').c(mCRAM.n('RST'))

    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        mI.setPos(-540.0,-260.0)
        mRegAdr.setPos(-300.0,-160.0)
        mBsAddress.setPos(-50.0,-240.0)
        mBsData.setPos(-50.0,-20.0)
        mCRAM.setPos(240.0,-100.0)
        mO.setPos(370.0,-100.0)
        mNAND0.setPos(40.0,-60.0)
        mCRIED.setPos(-300.0,-40.0)
        mNOT0.setPos(-480.0,-40.0)
        mNOT1.setPos(180.0,40.0)

    def ramContent(m):
        return m.mod('CRAM16').ramContent()

    m.addMethod('ramContent',ramContent)
    return m

if __name__ == '__main__':
    makeRAMEI('cpu-RAM-ei') 