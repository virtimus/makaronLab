#take everything upto video3
from q3.api import *

#import q3.bootstrap.tests.ben6502.video3 as v3

import q3.bootstrap.tests.ben6502.videos as v

rompath = v.videoCompile('video5.s')

execF(v.fpath+'video2.py')

m = m

print(m.name()) # well, we need a way to change the name of the tab

modv = modv

#modv.setName('Ben\'s video 7')

mRAM = m.modAdd('RAM62256',
    impl = 'Q3Chips:/RAM62256'
    )

m6502 = m.mod('C6502')
m6502.nod('ADR').connect(mRAM.nod('A0'))
m6502.nod('DTA').connect(mRAM.nod('D0'))

adrMap = m.mod('adrMap')


mNAND2 = m.modAdd('NAND2',
    impl = 'local:/NAND'
    )

adrMap.nod('Y15B').connect(mNAND2.nod('B'))

mClock = m.mod('Clock')
mClock.nod('Y').connect(mNAND2.nod('A'))

#connect and enable RAM
m6502.nod('RWB').connect(mRAM.nod('RWB'))
adrMap.nod('Y14').connect(mRAM.nod('DEB'))

#lets try something else
#mNAND2.nod('Y').connect(mRAM.nod('CSB'))
nY15 = adrMap.ioAdd(name ='Y15',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y15','= AIN[15]')
adrMap.nod('Y15').connect(mRAM.nod('CSB'))



# .. and place new elems in some not bad places ..
mNAND2.setPos(140.0,100.0)
mNAND2.view().setRotate(True)
mNAND2.view().setInvert(True)

mRAM.setPos(0.0,230.0)
mRAM.view().expand()
