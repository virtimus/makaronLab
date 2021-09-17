from q3.api import *

import q3.bootstrap.tests.benSAP1.common as cmn

import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg as dl8bit
import q3.bootstrap.tests.benSAP1.cpu_OE_8bit_ei as oe






def makeDlatch8bitregEI(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    #nDA = {} # well - we use 8bit singal
    n8D = m.iAdd('D',
        size = 8
        )

    nLOADB = m.iAdd('LOADB')
    nENABLEB = m.iAdd('ENABLEB')
    nCLK = m.iAdd('CLK')

    n8O = m.oAdd('O',
        size = 8
        )
    n8I = m.oAdd('I',
        size = 8
        )

    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )

    mDLATCH8 = dl8bit.makeDLach8bitreg('DLATCH8',m)
    mOE = oe.makeOE8bitEI('OE',m)

    mBto8D = cmn.makeBto8('Bto8D',m)
    m8toBO = cmn.make8toB('8toBO',m)
    m8toBI = cmn.make8toB('8toBI',m)

    #view
    mBto8D.setPos(-200.0,-20.0)
    mNOT0.setPos(-200.0,220.0)

    mDLATCH8.setPos(-60.0,-20.0)

    m8toBO.setPos(280.0,-40.0)
    m8toBI.setPos(210.0,120.0)
    mOE.setPos(60.0,-40.0)

    #connect
    n8D.c(mBto8D.nod('D'))
    nLOADB.c(mNOT0.n('A'))
    mNOT0.n('Y').c(mDLATCH8.n('LOAD'))
    nCLK.c(mDLATCH8.n('CLK'))
    nENABLEB.c(mOE.n('ENABLEB'))


    for i in range(0,8,1):
        mBto8D.nod(f'Y{i}').c(mDLATCH8.n(f'D{i}'))
        mDLATCH8.n(f'O{i}').c(mOE.n(f'D{i}'))
        mOE.n(f'O{i}').c(m8toBO.n(f'D{i}'))
        mOE.n(f'I{i}').c(m8toBI.n(f'D{i}'))



    m8toBO.n('Y').c(n8O)
    m8toBI.n('Y').c(n8I)
    return m





def makeReg8bitEI(name:str,parent:Module=None):
    return makeDlatch8bitregEI(name,parent)

def makeReg4bitEI(name:str,parent:Module=None):
    return makeDlatch8bitregEI(name,parent)

if __name__ == '__main__':
    makeDlatch8bitregEI('cpu-D-latch-8bitreg-ei')

