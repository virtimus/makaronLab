from q3.api import *

#from q3.bootstrap.tests.benSAP1.common import makeCRAM
from q3.bootstrap.tests.benSAP1.common import makeNtoS
from q3.bootstrap.tests.benSAP1.common import makeStoN

from q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei import makeOENbitEI
import q3.bootstrap.tests.benSAP1.cpu_D_latch_1bitreg as dl1bit

def makeDLachNbitreg(name:str,parent:Module=None, size = 16):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    nDA = {}
    nOA = {}
    mDLA = {}
    for i in range(0,size,1):
        iname = f'D{i}'
        oname = f'O{i}'
        dlname = f'DL{i}'
        nDA[iname] = m.iAdd(iname)
        nOA[oname] = m.oAdd(oname)
        mDLA[dlname] = dl1bit.makeDLatch1bitreg(dlname,m)


    nLOAD = m.iAdd('LOAD')
    nCLK = m.iAdd('CLK')

    tm.sleepMs(1000)

    # connections & view
    for i in range(0,size,1):
        dlname = f'DL{i}'
        mDL = mDLA[dlname]
        nLOAD.c(mDL.n('LOAD')) 
        nCLK.c(mDL.n('CLK'))
        iname = f'D{i}'
        nDA[iname].c(mDL.n('DI'))
        oname = f'O{i}'
        mDL.n('Q').c(nOA[oname])

        if m.isRoot():
            mDL.setPos(0.0,-400.0+(100*i))

    #t1 = m.mod('DL0').n('CLK')
    #nCLK.c(t1)
    return m

def makeReg16bitEI(name:str,parent:Module=None,dataOutput=False, asB=True):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    #nDA = {} # well - we use 8bit singal
    n8D = m.iAdd('D',
        size = 16
        )
    mnamesuff = 'B' if asB else '' 
    nLOADB = m.iAdd('LOAD'+mnamesuff)
    nENABLEB = m.iAdd('ENABLE'+mnamesuff)
    if dataOutput:
        m.iAdd('ENABLED'+mnamesuff)

    nCLK = m.iAdd('CLK')

    n8O = m.oAdd('O',
        size = 16
        )
    if dataOutput:
        m.oAdd('DO', size=16)
    n8I = m.oAdd('I',
        size = 16
        )

    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )

    mDLATCH= makeDLachNbitreg('DLATCH16',m, size = 16)
    mOE = makeOENbitEI('OE',m, size = 16)
    if dataOutput:
        makeOENbitEI('OED',m, size = 16)
    '''
    mBto8Da = cmn.makeBto8('Bto8Da',m)
    m8toBOa = cmn.make8toB('8toBOa',m)
    m8toBIa = cmn.make8toB('8toBIa',m)
    mBto8Db = cmn.makeBto8('Bto8Db',m)
    m8toBOb = cmn.make8toB('8toBOb',m)
    m8toBIb = cmn.make8toB('8toBIb',m)
    '''
    if m.isRoot():
        #view
        #mBto8D.setPos(-200.0,-20.0)
        #mBto8Db.setPos(-210.0,-20.0)
        mNOT0.setPos(-200.0,220.0)

        mDLATCH.setPos(-60.0,-20.0)
        #mDLATCH8a.setPos(-70.0,-20.0)

        #m8toBOa.setPos(280.0,-40.0)
        #m8toBOb.setPos(270.0,-40.0)
        #m8toBIa.setPos(210.0,120.0)
        #m8toBIb.setPos(200.0,120.0)
        mOE.setPos(60.0,-40.0)
        #mOEb.setPos(50.0,-40.0)

    #connect
    #n8D.c(mBto8D.nod('D'))
    #n8D.c(mBto8Db.nod('D'))
    mStoN0 = makeStoN('SToN(16)',m, size = 16)
    mNtoS0 = makeNtoS('NToS(16)',m, size = 16)
    n8D.c(mStoN0.n('D'))
    for i in range(0,16,1):      
        mStoN0.n(f'Y{i}').c(mDLATCH.n(f'D{i}'))
        mDLATCH.n(f'O{i}').c(mNtoS0.n(f'D{i}'))
    mNtoS0.n('Y').c(mOE.n('D'))
    if dataOutput:
        mOED = m.mod('OED')
        mNtoS0.n('Y').c(mOED.n('D')) 

    if asB:
        nLOADB.c(mNOT0.n('A'))
        mNOT0.n('Y').c(mDLATCH.n('LOAD'))
    else:
        nLOADB.c(mDLATCH.n('LOAD'))

    nCLK.c(mDLATCH.n('CLK'))

    if asB:
        nENABLEB.c(mOE.n('ENABLEB'))
        if dataOutput:
            nENABLEDB=m.n('ENABLEDB')
            mOED = m.mod('OED')
            nENABLEDB.c(mOED.n('ENABLEB'))
    else:
        nENABLEB.c(mNOT0.n('A'))    
        mNOT0.n('Y').c(mOE.n('ENABLEB'))
        if dataOutput:
            mNOT1 = m.modAdd('NOT1',
                impl = 'local:/NOT'
                )
            nENABLEDB=m.n('ENABLED')
            mOED = m.mod('OED')
            nENABLEDB.c(mNOT1.n('A'))
            mNOT1.n('Y').c(mOED.n('ENABLEB'))

    #mDLATCH.n(f'O').c(mOE.n(f'D'))
    mOE.n('O').c(n8O)
    if dataOutput:
        m.mod('OED').n('O').c(m.nod('DO'))
    mOE.n('I').c(n8I)

    return m