from q3.api import *

from q3 import bitutils

def makeNtoS(name:str,parent:Module=None, size =8):
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #for this mapper we have 8 1 bit singals on entry
    sformula = '=0'
    for i in range(0,size,1):
        m.iAdd(f'D{i}')
        sformula += f' | D{i}.value()<<{i}'

    # and one 8 bit signal on out
    m.oAdd('Y',size=size)

    # and one formula to make demulti
    m.setSigFormula('Y',sformula)
    return m

def make8toB(name:str,parent:Module=None):
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #for this mapper we have 8 1 bit singals on entry
    sformula = '=0'
    for i in range(0,8,1):
        m.iAdd(f'D{i}')
        sformula += f' | D{i}.value()<<{i}'

    # and one 8 bit signal on out
    m.oAdd('Y',size=8)

    # and one formula to make demulti
    m.setSigFormula('Y',sformula)
    return m


def makeBto8(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    # and one in and 8 out
    m.iAdd('D',size=8)

    for i in range(0,8,1):
        m.oAdd(f'Y{i}')
        m.setSigFormula(f'Y{i}',f'=D[{i}]')
    return m

def makeStoN(name:str,parent:Module=None, size=8):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    # and one in and 8 out
    m.iAdd('D',size=size)

    for i in range(0,size,1):
        m.oAdd(f'Y{i}')
        m.setSigFormula(f'Y{i}',f'=D[{i}]')
    return m
    
def make74LS163A(name:str,parent:Module=None): 
    
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    def calc(mimpl):
        m = mimpl.mdl()
        mProps = m.props()
        if not 'counter74LS163A' in mProps:
            mProps['counter74LS163A']=0
        if not 'counterMax74LS163A' in mProps:
            mProps['counterMax74LS163A']=15
        if not 'clock74LS163A' in mProps:
            mProps['clock74LS163A']=False
            
        counterMax = mProps['counterMax74LS163A'] # //(4 bits)
        counter = mProps['counter74LS163A']  
        nClock = m.n('CLK')
        
        enable = m.n('END').value()
        isRise = nClock.value() != mProps['clock74LS163A'] and nClock.value()
        mProps['clock74LS163A'] = nClock.value()
    
    
        cc = False
        if (isRise):
            if (enable):
               counter=counter+1
               cc=True
               if (counter>counterMax):
                   counter = 0          
            isReset = m.n('CL').value()
            if (isReset):
                counter = 0
        
        isLoad = m.n('LD').value();
        if (isLoad):
            cc = True
            counter = m.n('D0').value()+(m.n('D1').value())*2+(m.n('D2').value())*4+(m.n('D3').value())*8
            #//if (enable && counter+1 > counterMax) {carryOut = true;}
        carryOut = False
        if (enable and counter+1 > counterMax):
            carryOut = True
        m.n('RCO').intSignal().setValue(carryOut)
        #_pins.setPin(P::RCO,carryOut);
    
    
        #counterToPins();
        m.n('Q0').intSignal().setValue(bu.readBits(counter,0,1)>0)
        m.n('Q1').intSignal().setValue(bitutils.readBits(counter,1,1)>0)
        m.n('Q2').intSignal().setValue(bitutils.readBits(counter,2,1)>0)
        m.n('Q3').intSignal().setValue(bitutils.readBits(counter,3,1)>0)
        
        #set current value of counter
        mProps['counter74LS163A'] = counter


    m.iAdd('CL')
    m.iAdd('CLK')
    m.iAdd('D0')
    m.iAdd('D1')
    m.iAdd('D2')
    m.iAdd('D3')
    m.iAdd('END')
    m.iAdd('GND')
    m.iAdd('ENQ')
    m.iAdd('LD')
    
    m.oAdd('RCO')
    m.oAdd('Q0')
    m.oAdd('Q1')
    m.oAdd('Q2')
    m.oAdd('Q3')
    
    #m.impl().calculate = calculate
    #mI = m.mod('moduleInputs')
    #if mI == None: #not expanded
    #md = m.impl()       
    #else:
    #    md = mI.impl()
    #nm = types.MethodType(calc ,md)
    #setattr(md,'calc',nm)  
    m.setCalc(calc)      
    return m

def makeCRAM(name:str,parent:Module=None): 
    
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    def calc(mimpl):
        m = mimpl.mdl()
        mProps = m.props()
        if not 'contentCRAM' in mProps:
            mProps['contentCRAM']=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
        address = 0
        for i in range(0,4,1):
            v = m.n(f'A{i}').value()
            address += v


        
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


    nA0 = m.iAdd('A0')
    nA1 = m.iAdd('A1')
    nA2 = m.iAdd('A2')
    nA3 = m.iAdd('A3')
    nD = m.iAdd('D',size=8)
    nRST = m.iAdd('RST')
    nWEB = m.iAdd('WEB')
    nCSD = m.iAdd('CSB')

    nO = m.oAdd('O',size=8)
    nI = m.oAdd('I',size=8)

    m.setCalc(calc)
    
    return m

def connAll(m:Module,t:Module,viaNot=None):
    tName = t.name()
    yy=0
    for v in t.nodes().values():       
        if v.ioType() == IoType.OUTPUT:
            if v.signals().size()<3:#TODO better way of detect if connected
                n = m.oAdd(tName +'-'+v.name(),size=v.valueType().size())
                v.c(n)
        else:
            if v.signals().size()<2:
                isViaNot = viaNot!=None and v.name() in viaNot
                sname = tName +'-'+ (viaNot[v.name()] if isViaNot else v.name()) 
                n = m.iAdd(sname,size=v.valueType().size())
                if isViaNot:
                    mNot = m.modAdd(f'NOT{tName}{yy}',
                        impl = 'local:/NOT'
                        )
                    yy+=1
                    n.c(mNot.n('A'))
                    mNot.n('Y').c(v)
                    #if m.isRoot():
                    #    mNot.setPos(m.getPos)
                else:
                    n.c(v)


if __name__ == '__main__':
    #make8toB('8toB')
    #makeBto8('Bto8')
    #m = modvAdd('common').module()
    make74LS163A('74LS163A') #, m)