from q3.api import *


import q3.bootstrap.tests.benSAP1.cpu_D_latch as dlatch

#modv = modvAdd('')
#m = modv.module()

def makeALU1bitAdder(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    # add inputs/outputs
    nA = m.iAdd('A')
    nB = m.iAdd('B')
    nCI = m.iAdd('CI')
    nS = m.oAdd('S')
    nCO = m.oAdd('CO')
    mI = nA.parent()
    
    mXOR0 = m.modAdd('XOR0',
        impl = 'local:/XOR'
        )

    mXOR1 = m.modAdd('XOR1',
        impl = 'local:/XOR'
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
    
    nA.c(mXOR0.n('A'))
    nA.c(mAND0.n('A'))
    nB.c(mXOR0.n('B'))
    nB.c(mAND0.n('B'))
    #nB.c(mAND1.n('B'))
    
    
    mXOR0.n('Y').c(mXOR1.n('A'))
    mXOR0.n('Y').c(mAND1.n('A'))
    
    nCI.c(mXOR1.n('B'))
    nCI.c(mAND1.n('B'))
    
    mAND0.n('Y').c(mOR0.n('B'))
    mAND1.n('Y').c(mOR0.n('A'))

    mXOR1.n('Y').c(nS)
    mOR0.n('Y').c(nCO)
    mO=nCO.parent()


    if m.isRoot(): #view needed for root only
        mI.setPos(-500.0,-90.0)
        mO.setPos(130.0,-40.0)
        mOR0.setPos(0.0,10.0)
        mXOR0.setPos(-360.0,-120.0)
        mXOR1.setPos(-200.0,-120.0)
        mAND0.setPos(-290.0,30.0)
        mAND1.setPos(-190.0,-20.0)
    
    return m


if __name__ == '__main__':
    makeALU1bitAdder('cpu-ALU-1bitAdder')
    