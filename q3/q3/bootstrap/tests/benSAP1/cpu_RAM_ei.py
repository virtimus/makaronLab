
from q3.api import *

from q3.bootstrap.tests.benSAP1.common import makeCRAM
from q3.bootstrap.tests.benSAP1.common import make8toB
from q3.bootstrap.tests.benSAP1.common import makeBto8
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI
from q3.bootstrap.tests.benSAP1.cpu_RAM_4bitsel import makeRAM4BITSEL
import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei as dlatch8bitRegEI

def makeRAMEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #m.iAdd('PA0')
    #m.iAdd('PA1')
    #m.iAdd('PA2')
    #m.iAdd('PA3')
    m.iAdd('PA',size=8)

    m.iAdd('PD',size=8)

    #m.iAdd('A0')
    ##m.iAdd('A1')
    #m.iAdd('A2')
    #m.iAdd('A3')
    m.iAdd('A',size=8)

    nD = m.iAdd('D',size=8)

    nRAMIN = m.iAdd('RAMIN')
    nMRIN = m.iAdd('MRIN')
    nPRMOD = m.iAdd('PRMOD')
    nRAMOUT = m.iAdd('RAMOUT')
    nRST = m.iAdd('RST')
    nCLK = m.iAdd('CLK')

    nO = m.oAdd('O',size=8)
    nI = m.oAdd('I',size=8)

    mCRAM = makeCRAM('CRAM0',m)
    m4bsAddress = makeRAM4BITSEL('4bsAddress',m)
    m4bsData0 = makeRAM4BITSEL('4bsData0',m)
    m4bsData1 = makeRAM4BITSEL('4bsData1',m)
    
    mRegAdr = dlatch8bitRegEI.makeReg4bitEI('4bRegAddress',m)

    #mEI = makeOE8bitEI('OE',m)

    #m8toB0 = make8toB('8toB0',m)
    m8toB1 = make8toB('8toB1',m)
    mBto80 = makeBto8('Bto80',m)
    mBto81 = makeBto8('Bto81',m)
    mBto82 = makeBto8('Bto82',m)
    mBto83 = makeBto8('Bto83',m)

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
    mI.n('PA').c(mBto83.n('D'))
    for i in range(0,4,1):
        mBto83.n(f'Y{i}').c(m4bsAddress.n(f'A{i}'))
    #    mI.n(f'A{i}').c(m8toB0.n(f'D{i}'))
    #    mI.n(f'PA{i}').c(m4bsAddress.n(f'A{i}'))
    
    mI.n('PD').c(mBto81.n('D'))
    mI.n('PD').c(mBto82.n('D'))
    #m8toB0.n('Y').c(mRegAdr.n('D'))

    mRegAdr.n('O').c(mBto80.n('D'))
    for i in range(0,4,1):
        mBto80.n(f'Y{i}').c(m4bsAddress.n(f'B{i}'))
        m4bsAddress.n(f'O{i}').c(mCRAM.n(f'A{i}'))

    #mI.n('D').c(mBto81.n('D'))
    #mI.n('D').c(mBto82.n('D'))
    for i in range(0,4,1):
        ip=i+4
        mBto81.n(f'Y{i}').c(m4bsData0.n(f'A{i}'))
        mBto81.n(f'Y{ip}').c(m4bsData1.n(f'A{i}'))
        mBto82.n(f'Y{i}').c(m4bsData0.n(f'B{i}'))
        mBto82.n(f'Y{ip}').c(m4bsData1.n(f'B{i}'))
        m4bsData0.n(f'O{i}').c(m8toB1.n(f'D{i}'))
        m4bsData1.n(f'O{i}').c(m8toB1.n(f'D{ip}'))
    
    m8toB1.n('Y').c(mCRAM.n('D'))
    #nD.c(mCRAM.n('D'))
    
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
    m.n('PRMOD').c(m4bsAddress.n('SEL'))
    #m.n('PRMOD').c(m4bsData0.n('SEL'))
    #m.n('PRMOD').c(m4bsData1.n('SEL'))

    m.n('RAMOUT').c(mNOT1.n('A'))
    mNOT1.n('Y').c(mCRAM.n('CSB'))

    m.n('CLK').c(mRegAdr.n('CLK'))
    m.n('RST').c(mCRAM.n('RST'))

    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        mI.setPos(-540.0,-260.0)
        mRegAdr.setPos(-300.0,-160.0)
        m4bsAddress.setPos(-50.0,-240.0)
        m4bsData0.setPos(-50.0,-20.0)
        m4bsData1.setPos(-50.0,200.0)
        mCRAM.setPos(240.0,-100.0)
        #mEI.setPos(170.0,-100.0)
        #m8toB0.setPos(-400.0,-160.0)
        m8toB1.setPos(110.0,60.0)
        mBto80.setPos(-150.0,-160.0)
        mBto81.setPos(-400.0,50.0)
        mBto82.setPos(-400.0,260.0)
        mBto83.setPos(-400.0,-370.0)
        mO.setPos(370.0,-100.0)
        mNAND0.setPos(40.0,-60.0)
        mCRIED.setPos(-300.0,-40.0)
        mNOT0.setPos(-480.0,-40.0)
        mNOT1.setPos(180.0,40.0)

    return m

if __name__ == '__main__':
    makeRAMEI('cpu-RAM-ei') 