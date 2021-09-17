from q3.api import *

import q3.bootstrap.tests.benSAP1.common as cmn

import q3.bootstrap.tests.benSAP1.cpu_D_latch_8bitreg_ei as reg8bit

if __name__ == '__main__':
    modv = modvAdd('testtt1')
    m =modv.module()
    m1 = reg8bit.makeDlatch8bitregEI('cpu-D-latch-8bitreg-ei1',m)
    m2 = reg8bit.makeDlatch8bitregEI('cpu-D-latch-8bitreg-ei2',m)
    m3 = reg8bit.makeDlatch8bitregEI('cpu-D-latch-8bitreg-ei3',m)
    mb1 = m.modAdd('BUSI')
    mb2 = m.modAdd('BUSO')
    mb1.iAdd('I1',size=8)
    mb1.oAdd('O1',size=8)
    mb2.ioAdd('I1',size=8, ioType = IoType.DYNAMIC, direction = direction.LEFT)
    mb2.oAdd('O1',size=8 )

    mb1.view().setInvert(True)
    mb2.view().setInvert(True)

    m.iAdd('ID',size=8)
    e1 = m.iAdd('ENABLEB1')
    l1 =m.iAdd('LOADB1')
    e2 = m.iAdd('ENABLEB2')
    l2 = m.iAdd('LOADB2')
    e3 = m.iAdd('ENABLEB3')
    l3 = m.iAdd('LOADB3')
    clk = m.iAdd('CLK')

    m1.setPos(0,-200)
    m2.setPos(0,-50)
    m3.setPos(0,100)

    mb1.setPos(-140,-300)
    mb2.setPos(140.0,-300.0)

    mb1.setSigFormula('O1','=I1.value()')
    mb2.setSigFormula('O1','=I1.value()')



    m1.nod('O').c(mb2.n('I1'))
    m2.nod('O').c(mb2.n('I1'))
    m3.nod('O').c(mb2.n('I1'))
    m.nod('ID').c(mb2.n('I1'))

    mb2.n('O1').c(mb1.n('I1'))

    mb1.n('O1').c(m1.n('D'))
    mb1.n('O1').c(m2.n('D'))
    mb1.n('O1').c(m3.n('D'))

    e1.c(m1.n('ENABLEB'))
    e2.c(m2.n('ENABLEB'))
    e3.c(m3.n('ENABLEB'))

    e1.intSignal().setValue(True)
    e2.intSignal().setValue(True)
    e3.intSignal().setValue(True)

    l1.c(m1.n('LOADB'))
    l2.c(m2.n('LOADB'))
    l3.c(m3.n('LOADB'))

    l1.intSignal().setValue(True)
    l2.intSignal().setValue(True)
    l3.intSignal().setValue(True)

    clk.c(m1.n('CLK'))
    clk.c(m2.n('CLK'))
    clk.c(m3.n('CLK'))

#mod('cpu-D-latch-8bitreg-ei1').n('8O').setIntSignalAsDrive()




