
from q3.api import *
from q3.bootstrap.tests.benSAP1.common import make8toB
from q3.bootstrap.tests.benSAP1.common import makeBto8
from q3.bootstrap.tests.benSAP1.common import make74LS163A
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI



def makePCEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    #nD0 = m.iAdd('D0')
    #nD1 = m.iAdd('D1')
    #nD2 = m.iAdd('D2')
    #nD3 = m.iAdd('D3')
    nD = m.iAdd('D',size=8)

    nCLEAR = m.iAdd('CLEAR')
    nCLK = m.iAdd('CLK')
    nLOADB = m.iAdd('LOADB')
    nENCB = m.iAdd('ENCB')
    nENABLEB = m.iAdd('ENABLEB')

    m.oAdd('O',size=8)
    m.oAdd('I',size=8)

    m8toB0 = make8toB('8toB0',m)
    m8toB1 = make8toB('8toB1',m)
    mBto80 = makeBto8('Bto80',m)

    m74LS163A = make74LS163A('74LS163A',m)
    m8bitEI = makeOE8bitEI('8bit-ei',m)

    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )

    mNOT1 = m.modAdd('NOT1',
        impl = 'local:/NOT'
        )

    nENCB.c(mNOT0.n('A'))
    mNOT0.n('Y').c(m74LS163A.n('END'))
    mNOT0.n('Y').c(m74LS163A.n('ENQ'))

    #i=0
    #while i <4:
    #    m.oAdd(f'O{i}')
    #    i=i+1

    nD.c(mBto80.n('D'))
    i=0
    while i <4:
        #m.oAdd(f'I{i}')     
        #m.n(f'D{i}').c(m74LS163A.n(f'D{i}'))
        mBto80.n(f'Y{i}').c(m74LS163A.n(f'D{i}'))
        m74LS163A.n(f'Q{i}').c(m8bitEI.n(f'D{i}'))     
        #m8bitEI.n(f'O{i}').c(m.n(f'O{i}'))
        #m8bitEI.n(f'I{i}').c(m.n(f'I{i}'))
        m8bitEI.n(f'O{i}').c(m8toB0.n(f'D{i}'))
        m8bitEI.n(f'I{i}').c(m8toB1.n(f'D{i}'))
        i=i+1
    m8toB0.n('Y').c(m.n('O'))
    m8toB1.n('Y').c(m.n('I'))

    nCLEAR.c(m74LS163A.n('CL'))
    nCLK.c(m74LS163A.n('CLK'))
    nLOADB.c(mNOT1.n('A'))
    mNOT1.n('Y').c(m74LS163A.n('LD'))
    nENABLEB.c(m8bitEI.n('ENABLEB'))

    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        m74LS163A.setPos(-160.0,-40.0)
        mNOT0.setPos(-310.0,140.0)
        mNOT1.setPos(-310.0,70.0)
        m8bitEI.setPos(70.0,-40.0)
        mBto80.setPos(-250.0,0.0)
        m8toB0.setPos(220.0,-40.0)
        m8toB1.setPos(150.0,120.0)
        

    return m



if __name__ == '__main__':
    makePCEI('cpu-PC-ei')