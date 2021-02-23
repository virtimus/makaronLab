#https://www.youtube.com/watch?v=LnzuMJLZRdU

#we'll start here :

#https://youtu.be/LnzuMJLZRdU?t=1038

#api import

from q3.api import *

# Ben is starting logging output from 6502 as binary addr/data, hex addr, R/W flag and hex data

#first add new rootModule with view

modv = modvAdd('Bens video1')

#now we'll need 6502 module from chips
m6502 = modv.modAdd('C6502',
    impl='Q3Chips:/c6502'
    )

#add few inputs
ti1 = modv.module().ioAdd('t1',ioType = IoType.INPUT)
ti2 = modv.module().ioAdd('t2',ioType = IoType.INPUT)
ti3 = modv.module().ioAdd('t3',ioType = IoType.INPUT)

pRDY = m6502.nod('RDY')
pRESB = m6502.nod('RESB')
pNMIB = m6502.nod('NMIB')
pIRQB = m6502.nod('IRQB')
pPHI = m6502.nod('PHI0I')
ti1.con(pRDY)
ti1.con(pIRQB)
ti1.con(pNMIB)
ti2.con(pRESB)
#ti3.con(pPHI)


m6502.setPos(-110.0,-200.0)
m6502.view().expand() #impl().expand()


def monFun(self):
    self.consoleWrite(f'monFun:{hex(self._pins)}\n')
    s = bin(self._pins)[::-1]+'\n'
    #print(s)
    #c = self.console()
    #self.console().write(s)
    #self.cw(s)
    v = m6502.sig('RWB').value()
    adr = m6502.sig('ADR').value()
    dta = m6502.sig('DTA').value()
    rw = self.readBits(self._pins,24,1)
    s = ''
    for i in range(0,15,1):
        bit = self.readBits(adr,i,1)
        s+= '0' if bit == 0 else '1'
    d = ''
    for i in range(0,7,1):
        bit = self.readBits(dta,i,1)
        d+= '0' if bit == 0 else '1'
    #s = bin(adr).zfill(16)[::-1]
    ah = ''.join('%04x'%adr)
    dh = ''.join('%02x'%dta)
    rwc = 'r' if rw>0 else 'W' 
    self.consoleWrite(f'{s} {d} {ah} {rwc} {dh} rwb:{v} rw:{rw}\n')


if (m6502!=None):
    m6502impl = m6502.impl()
    mountMonitor(m6502impl,'updateSignals',monFun)

def mountMonitorM(self,obj, mname, handler):
    mountMonitor(obj, mname, handler)


clock = modv.modAdd('Clock',
    impl='Q3Chips:/Clock'
    )

clock.nod('Y').con(pPHI)

clock.setPos(-40.0,-290.0)


