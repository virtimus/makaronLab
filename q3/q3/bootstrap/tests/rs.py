
#@refs:https://www.youtube.com/watch?v=1SdbChxltTU

from q3.api import *

def makeRS(m:Module):
    assert m.mType() == MType.GRAPH, '[makeRS] ModuleType has to be GRAPH'
    nI0 = m.ioAdd('I0',ioType=IoType.INPUT)
    nI1 = m.ioAdd('I1',ioType=IoType.INPUT)

    nO0 = m.ioAdd('O0',ioType=IoType.OUTPUT)
    nO1 = m.ioAdd('O1',ioType=IoType.OUTPUT)

    mNAND0 = m.modAdd('NAND0',
        impl = 'local:/NAND'
        )

    mNAND1 = m.modAdd('NAND1',
        impl = 'local:/NAND'
        )

    mNAND0.nod('Y').connect(mNAND1.nod('A'))
    mNAND1.nod('Y').connect(mNAND0.nod('B'))

    nI0.connect(mNAND0.nod('A'))
    nI1.connect(mNAND1.nod('B'))

    mNAND0.nod('Y').connect(nO0)
    mNAND1.nod('Y').connect(nO1)

    #view
    mNAND0.setPos(-20.0,-100.0)
    mNAND1.setPos(-20.0,30.0)
    ml =  m.modL()
    if ml!=None:
        ml.setPos(-210,-40)
    mr =  m.modR()
    if mr!=None:
        mr.setPos(210,-40)


modv = modvAdd('RS')
makeRS(modv.module())

# https://youtu.be/1SdbChxltTU?t=790

def makeFFD(m:Module):
    assert m.mType() == MType.GRAPH, '[makeFFD] ModuleType has to be GRAPH'
    nD = m.ioAdd('D',ioType=IoType.INPUT)
    nCLK = m.ioAdd('CLK',ioType=IoType.INPUT)

    nQ = m.ioAdd('Q',ioType=IoType.OUTPUT)

    mRS0 = m.modAdd('RS0')
    makeRS(mRS0)

    mNOT0 = m.modAdd('NOT0',
        impl = 'local:/NOT'
        )

    mNAND0 = m.modAdd('NAND0',
        impl = 'local:/NAND'
        )

    mNAND1 = m.modAdd('NAND1',
        impl = 'local:/NAND'
        )

    nD.connect(mNAND0.nod('A'))
    nCLK.con(mNAND0.nod('B'))
    nCLK.con(mNAND1.nod('B'))

    nD.con(mNOT0.nod('A'))
    mNOT0.nod('Y').con(mNAND1.nod('A'))

    mNAND0.nod('Y').con(mRS0.nod('I0'))
    mNAND1.nod('Y').con(mRS0.nod('I1'))

    mRS0.nod('O0').connect(nQ)

    # view
    ml =  m.modL()
    if ml!=None:
        ml.setPos(-290.0,-80.0)

    mNOT0.setPos(-120.0,-40.0)
    mNAND0.setPos(0.0,-140.0)
    mNAND1.setPos(0.0,30.0)
    mRS0.setPos(170.0,-70.0)

    mr =  m.modR()
    if mr!=None:
        mr.setPos(270.0,-70.0)



modv = modvAdd('FF-D')
makeFFD(modv.module())