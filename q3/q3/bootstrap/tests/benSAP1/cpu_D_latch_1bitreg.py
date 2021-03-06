from q3.api import *


import q3.bootstrap.tests.benSAP1.cpu_D_latch as dlatch

#modv = modvAdd('')
#m = modv.module()

def makeDLatch1bitreg(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    nLOAD = m.iAdd('LOAD')
    nDI = m.iAdd('DI')
    nCLK = m.iAdd('CLK')
    nQ = m.oAdd('Q')

    mDLATCH = dlatch.makeDLatch('DLATCH',m)
    #mDLatch.nod('D').setDriveSignal(None)
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

    nLOAD.c(mNOT0.n('A'))
    nLOAD.c(mAND0.n('A'))
    nDI.c(mAND0.n('B'))
    nCLK.c(mDLATCH.n('CLK'))

    mNOT0.n('Y').c(mAND1.n('A'))
    mAND0.n('Y').c(mOR0.n('B'))

    mAND1.n('Y').c(mOR0.n('A'))
    mOR0.n('Y').c(mDLATCH.n('D'))
    mDLATCH.n('Q').c(mAND1.n('B'))

    mDLATCH.n('Q').c(nQ)

    if m.isRoot(): #view needed for root only
        mNOT0.setPos(-180.0,-150.0)
        mAND0.setPos(-180.0,0.0)
        mAND1.setPos(0.0,-150.0)
        mOR0.setPos(-40.0,-20.0)
        mDLATCH.setPos(70.0,70.0)
    
    return m


if __name__ == '__main__':
    makeDLatch1bitreg('cpu-D-latch-1bitreg')