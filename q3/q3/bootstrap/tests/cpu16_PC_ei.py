
from q3.api import *
from q3.bootstrap.tests.benSAP1.common import make8toB
from q3.bootstrap.tests.benSAP1.common import makeBto8
#from q3.bootstrap.tests.benSAP1.common import make74LS163AW16
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOENbitEI

def make74LS163AW(name:str,parent:Module=None,size = 16): 
    
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    cm = 2 ** size -1

    def calc(mimpl):
        m = mimpl.mdl()
        mProps = m.props()
        if not 'counter74LS163A' in mProps:
            mProps['counter74LS163A']=0
        if not 'counterMax74LS163A' in mProps:
            mProps['counterMax74LS163A']=cm
        if not 'clock74LS163A' in mProps:
            mProps['clock74LS163A']=False
            
        counterMax = mProps['counterMax74LS163A'] # //(16 bits)
        counter = mProps['counter74LS163A']  
        nClock = m.n('CLK')
        
        enableInc = m.n('END').value()
        enableDec = m.n('DEC').value()
        isRise = nClock.value() != mProps['clock74LS163A'] and nClock.value()
        mProps['clock74LS163A'] = nClock.value()
    
    
        cc = False
        if (isRise):
            if (enableInc):
               counter=counter+1
               cc=True
               if (counter>counterMax):
                   counter = 0 
            if (enableDec):
               counter=counter-1
               cc=True
               if (counter<0):
                   counter = 0                             
            isReset = m.n('CL').value()
            if (isReset):
                counter = 0
        
        isLoad = m.n('LD').value();
        if (isLoad):
            cc = True
            counter = m.n('D').value() #m.n('D0').value()+(m.n('D1').value())*2+(m.n('D2').value())*4+(m.n('D3').value())*8
            #//if (enable && counter+1 > counterMax) {carryOut = true;}
        carryOut = False
        if (enableInc and counter+1 > counterMax):
            carryOut = True
        if (enableDec and counter-1 < 0):
            carryOut = True
        m.n('RCO').intSignal().setValue(carryOut)
        #_pins.setPin(P::RCO,carryOut);
    
    
        #counterToPins();
        #m.n('Q0').intSignal().setValue(bitutils.readBits(counter,0,1)>0)
        #m.n('Q1').intSignal().setValue(bitutils.readBits(counter,1,1)>0)
        #m.n('Q2').intSignal().setValue(bitutils.readBits(counter,2,1)>0)
        #m.n('Q3').intSignal().setValue(bitutils.readBits(counter,3,1)>0)
        m.n('Q').intSignal().setValue(counter)

        #set current value of counter
        mProps['counter74LS163A'] = counter


    m.iAdd('CL')
    m.iAdd('CLK')
    m.iAdd('D',size=size)
    #m.iAdd('D1')
    #m.iAdd('D2')
    #m.iAdd('D3')
    m.iAdd('END')
    m.iAdd('DEC')
    m.iAdd('GND')
    m.iAdd('ENQ')
    m.iAdd('LD')
    
    m.oAdd('RCO')
    m.oAdd('Q',size=size)
    #m.oAdd('Q1')
    #m.oAdd('Q2')
    #m.oAdd('Q3')
    
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

def makePCEI(name:str,parent:Module=None,spc=False,asB=True):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #nD0 = m.iAdd('D0')
    #nD1 = m.iAdd('D1')
    #nD2 = m.iAdd('D2')
    #nD3 = m.iAdd('D3')
    tsize = 16
    if spc:
        tsize = 16
    nD = m.iAdd('D',size=tsize)

    nCLEAR = m.iAdd('CLEAR')
    nCLK = m.iAdd('CLK')
    nLOAD = m.iAdd('LOAD')
    nINC = m.iAdd('INC')
    nDEC = None
    if spc:
        nDEC = m.iAdd('DEC')
    snamesuff = 'B' if asB else ''
    nENABLEB = m.iAdd('ENABLE'+snamesuff)
    nENABLEDB = m.iAdd('ENABLED'+snamesuff)

    m.oAdd('O',size=tsize)
    m.oAdd('DO',size=tsize)
    m.oAdd('I',size=tsize)

    #m8toB0 = make8toB('8toB0',m)
    #m8toB1 = make8toB('8toB1',m)
    #mBto80 = makeBto8('Bto80',m)

    m74LS163A = make74LS163AW('74LS163AW16',m,size=tsize)
    m8bitEI = None

    m8bitEI = makeOENbitEI('8bit-ei',m, size = tsize)
    m8bitEID = makeOENbitEI('8bit-eiD',m, size = tsize)

    mOR0 = m.modAdd('OR',
        impl = 'local:/OR'
        )

    nD.c(m74LS163A.n('D'))

    nINC.c(m74LS163A.n('END'))
    nINC.c(mOR0.n('A'))
    if nDEC!=None:
        nDEC.c(m74LS163A.n('DEC'))
        nDEC.c(mOR0.n('B'))
    else:
        nINC.c(mOR0.n('B'))


    mOR0.n('Y').c(m74LS163A.n('ENQ'))

    tn = m8bitEI.n('D')
    tnd = m8bitEID.n('D')

    m74LS163A.n('Q').c(tn)
    m74LS163A.n('Q').c(tnd)


    m8bitEI.n('O').c(m.n('O'))
    m8bitEID.n('O').c(m.n('DO'))
    m8bitEI.n('I').c(m.n('I'))

    nCLEAR.c(m74LS163A.n('CL'))
    nCLK.c(m74LS163A.n('CLK'))
    nLOAD.c(m74LS163A.n('LD'))
    if asB:
        nENABLEB.c(m8bitEI.n('ENABLEB'))
        nENABLEDB.c(m8bitEID.n('ENABLEB'))
    else:
        mNOT0 = m.modAdd('NOT0',
            impl = 'local:/NOT'
            )
        mNOT1 = m.modAdd('NOT1',
            impl = 'local:/NOT'
            )
        nENABLEB.c(mNOT0.n('A'))
        mNOT0.n('Y').c(m8bitEI.n('ENABLEB'))
        nENABLEDB.c(mNOT1.n('A'))
        mNOT1.n('Y').c(m8bitEID.n('ENABLEB'))
        
    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        m74LS163A.setPos(-160.0,-40.0)
        mOR0.setPos(-310.0,140.0)
        m8bitEI.setPos(70.0,-40.0)
        ##mBto80.setPos(-250.0,0.0)
        ##m8toB0.setPos(220.0,-40.0)
        ##m8toB1.setPos(150.0,120.0)
        

    return m



if __name__ == '__main__':
    makePCEI('cpu16-PC-ei')
    makePCEI('cpu16-SPC-ei',spc=True)