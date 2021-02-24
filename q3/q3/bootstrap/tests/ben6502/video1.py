#https://www.youtube.com/watch?v=LnzuMJLZRdU

#we'll start here :

#https://youtu.be/LnzuMJLZRdU?t=1038

#api import

from traceback import print_stack
from q3.api import *

# Ben is starting logging output from 6502 as binary addr/data, hex addr, R/W flag and hex data

#first add new rootModule with view

modv = modvAdd('Bens video1')

#now we'll need 6502 module from chips
m6502 = modv.modAdd('C6502',
    impl='Q3Chips:/c6502'
    )

# add few inputs to the module (they will be seen as outputs socket as module is in detail "inside" view state)
ti1 = modv.module().ioAdd('i1',ioType = IoType.INPUT)
ti2 = modv.module().ioAdd('i2',ioType = IoType.INPUT)
ti3 = modv.module().ioAdd('i3',ioType = IoType.INPUT)

# now we'll get some socket/node handles ...
pRDY = m6502.nod('RDY')
pRESB = m6502.nod('RESB')
pNMIB = m6502.nod('NMIB')
pIRQB = m6502.nod('IRQB')
pPHI = m6502.nod('PHI0I')

# ... and connect the inputs to them
ti1.con(pRDY)
ti1.con(pIRQB)
ti1.con(pNMIB)
ti2.con(pRESB)
#ti3.con(pPHI)

# some view tweeking
m6502.setPos(-110.0,-200.0)
m6502.view().expand() #impl().expand()

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
    self._pins = self.writeBits(self._pins,16,8,0xeaea) #write hex eaea directly to data pins (corresponding to set of resistors pined to 6502)
    #self.consoleWrite(f'abFun:{hex(self._pins)}\n')

# ... and connect it to m6502 module
if (m6502!=None):
    m6502impl = m6502.impl() # we are connecting to impl nested object representing module implementation
    mountMonitor(m6502impl,'updateSignals',monFun) # put our monitoring staff in place of call 'updateSignals' method 

#this is no longer needed i think
#def mountMonitorM(self,obj, mname, handler):
#    mountMonitor(obj, mname, handler)

# now create a clock to tick the CPU
clock = modv.modAdd('Clock',
    impl='Q3Chips:/Clock'
    )

# connect it ti timer slot
clock.nod('Y').con(pPHI)

# set position
clock.setPos(-40.0,-290.0)

# ... and interval
mod('Clock').impl().setInterval(1000) 

# put some signals to the net...
ti1.driveSignal().setValue(1)

sig('i2').setValue(1) 
# here above is the difference between variable name 'ti2' or 'ti1' and slot name 'i2'
# as a standard most of the api methods can handle element id/ element name or element ref as argument
# the code just checks if it is int, str or object ref 
# so the line above could also be:
# sig(ti2).setValue(1)

# voila - should work fine ...