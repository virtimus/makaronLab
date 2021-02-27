

#https://www.youtube.com/watch?v=yl8vPW5hydQ


#first created a function "video1" from what was made in previous part to easilly share the work
from http.client import NOT_MODIFIED
from q3.api import *
from q3.bootstrap.tests.ben6502.videos import video1 

modv = modvAdd('Ben\'s video2')

video1(modv)

m = modv.module()

m6502 = m.mod('C6502')

#monFun moved and NOT_MODIFIED
# let's create a monitoring function 
def monFun(self):
    # put some header with base info - name of function and 6502 current pins in hex
    self.consoleWrite(f'monFun:{hex(self._pins)}\n')
    s = bin(self._pins)[::-1]+'\n'
    # read some singals from the chip (standard way - not directly from pins)
    v = m6502.sig('RWB').value()
    adr = m6502.sig('ADR').value()
    dta = m6502.sig('DTA').value()
    # read RW signal also directly from pins (I've had some problems with reading it from signals as signal type was wrongly set)
    rw = self.readBits(self._pins,24,1)
    s = '' # read binary string bit by bit as in Ben's aproach
    for i in range(15,-1,-1):
        bit = self.readBits(adr,i,1)
        s+= '0' if bit == 0 else '1'
    d = '' # same here for data byte
    for i in range(7,-1,-1):
        bit = self.readBits(dta,i,1)
        d+= '0' if bit == 0 else '1'
    # some formatting 4/2 hex
    ah = ''.join('%04x'%adr)
    dh = ''.join('%02x'%dta)
    rwc = 'r' if rw>0 else 'W' 
    self.consoleWrite(f'{s} {d} {ah} {rwc} {dh} rwb:{v} rw:{rw} {bin(adr)} {bin(dta)}\n')
    #set data pins
    #self.consoleWrite(f'wbFun:{hex(self._pins)}\n')
    #self._pins = self.writeBits(self._pins,16,8,0xeaea) #write hex eaea directly to data pins (corresponding to set of resistors pined to 6502)
    #self.consoleWrite(f'abFun:{hex(self._pins)}\n')

# ... and connect it to m6502 module
if (m6502!=None):
    m6502impl = m6502.impl() # we are connecting to impl nested object representing module implementation
    mountMonitor(m6502impl,'updateSignals',monFun) # put our monitoring staff in place of call 'updateSignals' method 



# now looks like we have to prepare a AT28C256 simulator ...
# so created ModuleImplAT28C256

mAT28C256 = modv.modAdd(
    'AT28C256',
    impl = 'Q3Chips:/AT28C256'
)



s = pADR = m6502.nod('ADR') 
t = mAT28C256.nod('ADR')
s.connect(t)

s = mAT28C256.nod('I/O')
t = m6502.nod('DTA') 
s.connect(t)


mAT28C256.setPos(-230.0,-60.0)
m.mod('moduleInputs').setPos(-390.0,-200.0)

m.mod('Clock').view().setInvert(True) 
m.mod('Clock').setPos(70.0,-200.0)

# rom file created with makerom.py
mAT28C256.impl().setMemPath('/src/makaronLab/q3/q3/bootstrap/tests/ben6502/rom.bin')

# as in video - we'll need also a not gate and signal maper
adrMap = modv.modAdd('adrMap',
    moduleType = q3.moduletype.ModuleType.GRAPH
    )

pAIN = adrMap.ioAdd(name ='AIN',ioType=IoType.INPUT, size=16)
pAdrY = adrMap.ioAdd(name ='Y',ioType=IoType.OUTPUT)

#connect
pADR.connect(pAIN)

#formula
adrMap.setSigFormula('Y','=AIN[15]')

#connect to AT28C256 through not gate
#gNot = modv.modAdd('notG',
#    impl = 'local:/NOT'
#    )
#pAdrY.connect(gNot.nod('A'))
#gNot.nod('Y').connect(mAT28C256.nod('CEB'))

# ... or much simpler = just replace formula a little bit ...
adrMap.setSigFormula('Y','= not bool(AIN[15])')
pAdrY.connect(mAT28C256.nod('CEB'))

#put it in nice place
adrMap.setPos(-390.0,-40.0)


# .. and seems we're now somwhere in here
# https://youtu.be/yl8vPW5hydQ?t=706
