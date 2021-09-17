
from q3.api import *

from q3.bootstrap.tests.benSAP1.common import make74LS163A
from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOE8bitEI



def makeRAM1BITSEL(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    
    nA = m.iAdd('A')
    nB = m.iAdd('B')
    nSEL = m.iAdd('SEL')
    nO = m.oAdd('O')

    #let's create some modules ...
    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )
    mAND0 = m.modAdd('AND0',
        impl = 'local:/AND'
        )
    mAND1 = m.modAdd('AND1',
        impl = 'local:/AND'
        )
    mOR0 = m.modAdd('OR0',
        impl = 'local:/OR'
        )    
    
    nA.c(mAND0.n('A'))
    nSEL.c(mAND0.n('B'))

    nB.c(mAND1.n('A'))
    nSEL.c(mNOT0.n('A'))
    mNOT0.n('Y').c(mAND1.n('B'))

    mAND0.n('Y').c(mOR0.n('A'))
    mAND1.n('Y').c(mOR0.n('B'))

    mOR0.n('Y').c(nO)

    if m.isRoot(): #bother with presentation only for root module
        # put it all in nice places ...
        m.mod('moduleInputs').setPos(-280.0,0.0)
        mNOT0.setPos(-140.0,80.0)
        mAND0.setPos(-40.0,-70.0)
        mAND1.setPos(-40.0,20.0)
        mOR0.setPos(90.0,0.0)
        m.mod('moduleOutputs').setPos(220.0,0.0)


    return m



if __name__ == '__main__':
    makeRAM1BITSEL('cpu-RAM-1bitsel')