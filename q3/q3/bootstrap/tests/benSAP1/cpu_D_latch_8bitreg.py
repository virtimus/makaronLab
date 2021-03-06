from q3.api import *


import q3.bootstrap.tests.benSAP1.cpu_D_latch_1bitreg as dl1bit


def makeDLach8bitreg(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()
    nDA = {}
    nOA = {}
    mDLA = {}
    for i in range(0,8,1):
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
    for i in range(0,8,1):
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




if __name__ == '__main__':
    makeDLach8bitreg('cpu-D-latch-8bitreg')

