from q3.api import *

from q3.bootstrap.tests.benSAP1.common import makeCRAM
from q3.bootstrap.tests.benSAP1.common import make8toB
from q3.bootstrap.tests.benSAP1.common import makeBto8
from q3.bootstrap.tests.benSAP1.common import makeBBUS 
from q3.bootstrap.tests.benSAP1.common import connAll 

from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI
from q3.bootstrap.tests.benSAP1.cpu_RAM_4bitsel import makeRAM4BITSEL
from q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei import makeReg8bitEI

from q3.bootstrap.tests.benSAP1.cpu_RAM_ei import makeRAMEI
from q3.bootstrap.tests.benSAP1.cpu_PC_ei import makePCEI
from q3.bootstrap.tests.benSAP1.cpu_ALU_AB_ei import makeALUABEI


def makeCPUZEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    mPC = makePCEI('PC', m)
    mRAM = makeRAMEI('RAM', m)
    mALU = makeALUABEI('ALU', m)
    mIREG = makeReg8bitEI('IREG', m)
    mDBUS = makeBBUS('DBUS', m, size=8)
    mIBUS0 = makeBBUS('IBUS0', m, size=1)
    #m8toB = make8toB('8toB', m)
    #mBto8 = makeBto8('Bto8', m)
    mDBUS.n('O').c(mIBUS0.n('I0'))
    ndd = mIBUS0.n('O')
    ndd.c(mALU.n("BI"))
    ndd.c(mRAM.n('A'))
    ndd.c(mRAM.n('D'))
    ndd.c(mPC.n('D'))
    ndd.c(mIREG.n('D'))

    mALU.n('BO').c(mDBUS.n('I0'))
    mRAM.n('O').c(mDBUS.n('I1'))
    mPC.n('O').c(mDBUS.n('I2'))
    mIREG.n('O').c(mDBUS.n('I3'))
    connAll(m,mALU,viaNot=None)
    connAll(m,mRAM)
    connAll(m,mPC,viaNot={ 'LOADB':'LOAD','ENCB':'ENC','ENABLEB':'ENABLE'})
    connAll(m,mIREG,viaNot={'LOADB':'LOAD','ENABLEB':'ENABLE'})


    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        mALU.setPos(-310.0,0.0)
        mRAM.setPos(-110.0,0.0)
        mPC.setPos(80.0,0.0)
        mIREG.setPos(80.0,170.0)
        mDBUS.setPos(270.0,-190.0)
        mIBUS0.setPos(-460.0,-90.0)

    return m

if __name__ == '__main__':
    makeCPUZEI('cpu-Z-ei') 