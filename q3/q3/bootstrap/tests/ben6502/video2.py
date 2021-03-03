

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
    rwb = m6502.sig('RWB').value()
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
    rwc = 'r' if rwb>0 else 'W' 
    self.consoleWrite(f'{s} {d} {ah} {rwc} {dh} rwb:{rwb} rw:{rw} {bin(adr)} {bin(dta)}\n')
    #set data pins
    #self.consoleWrite(f'wbFun:{hex(self._pins)}\n')
    #self._pins = self.writeBits(self._pins,16,8,0xeaea) #write hex eaea directly to data pins (corresponding to set of resistors pined to 6502)
    #self.consoleWrite(f'abFun:{hex(self._pins)}\n')

# ... and connect it to m6502 module
oMonFun = None
if (m6502!=None):
    m6502impl = m6502.impl() # we are connecting to impl nested object representing module implementation
    oMonFun = mountMonitor(m6502impl,'updateSignals',monFun) # put our monitoring staff in place of call 'updateSignals' method 



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

# with views there is some time needed for events to process and pin driveSignals,
# maybe should change to seting driveSignal sync on model level (currently view is null condition)
tm.sleepMs(1000) 


mAT28C256.setPos(-230.0,-60.0)
m.mod('moduleInputs').setPos(-390.0,-200.0)

m.mod('Clock').view().setInvert(True) 
m.mod('Clock').setPos(70.0,-200.0)

# rom file created with makerom.py
if not 'rompath' in globals():
    rompath = '/src/makaronLab/q3/q3/bootstrap/tests/ben6502/rom.bin'
mAT28C256.impl().setMemPath(rompath)

# as in video - we'll need also a not gate and signal maper
adrMap = modv.modAdd('adrMap',
    moduleType = q3.moduletype.ModuleType.GRAPH
    )

pAIN = adrMap.ioAdd(name ='AIN',ioType=IoType.INPUT, size=16)
pAdrY = adrMap.ioAdd(name ='Y15B',ioType=IoType.OUTPUT)

#connect
pADR.connect(pAIN)

#formula
adrMap.setSigFormula('Y15B','=AIN[15]')

#connect to AT28C256 through not gate
#gNot = modv.modAdd('notG',
#    impl = 'local:/NOT'
#    )
#pAdrY.connect(gNot.nod('A'))
#gNot.nod('Y').connect(mAT28C256.nod('CEB'))

# ... or much simpler = just replace formula a little bit ...
adrMap.setSigFormula('Y15B','= not bool(AIN[15])')
pAdrY.connect(mAT28C256.nod('CEB'))

#put it in nice place
adrMap.setPos(-390.0,-40.0)


# .. and seems we're now somewhere in here
# https://youtu.be/yl8vPW5hydQ?t=706

# so - lets go on 
# maybe some speedup of clock

mClock = mod('Clock')
mClock.impl().setInterval(500)

# ... and yet to more programs 
#python makerom1.py
#python makerom2.py

# and we have first working 2 instruction program like here:
# https://youtu.be/yl8vPW5hydQ?t=1119


# next is the part concerned to 6522 chip
#https://youtu.be/yl8vPW5hydQ?t=1386

#instatiate 6522 chip

m6522 = modv.modAdd('C6522',
    impl = 'Q3Chips:/C6522'
    )

# nand gate for adress detection
nand1 = modv.modAdd('nand1',
    impl = 'local:/NAND'
    )

pAdrY14 = adrMap.ioAdd(name ='Y14',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y14','= AIN[14]')

# connect detection part of adress to nand
pAdrY.connect(nand1.nod('A'))
pAdrY14.connect(nand1.nod('B'))
nand1.nod('Y').connect(m6522.nod('CS2B'))

# put it to nice position ...
nand1.setPos(-230.0,40.0)
adrMap.setPos(-380.0,40.0)

# now A13 - out of adr ..
pAdrY13 = adrMap.ioAdd(name ='Y13',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y13','= AIN[13]')
# connect to CS1 of 6522
pAdrY13.connect(m6522.nod('CS1'))


# https://youtu.be/yl8vPW5hydQ?t=1976
# connect RWB and Clock
m6502.nod('RWB').connect(m6522.nod('RWB'))
mClock.nod('Y').connect(m6522.nod('PHI2'))

# reset
mInp = mod('moduleInputs')
pRes = mInp.nod('i2')
pRes.connect(m6522.nod('RESB'))

# connect D0-8 pins
m6502.nod('DTA').connect(m6522.nod('D0'))

# https://youtu.be/yl8vPW5hydQ?t=2075
# RS part

pAdrY00 = adrMap.ioAdd(name ='Y00',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y00','= AIN[0]')
pAdrY00.connect(m6522.nod('RS0'))

pAdrY01 = adrMap.ioAdd(name ='Y01',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y01','= AIN[1]')
pAdrY01.connect(m6522.nod('RS1'))

pAdrY02 = adrMap.ioAdd(name ='Y02',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y02','= AIN[2]')
pAdrY02.connect(m6522.nod('RS2'))

pAdrY03 = adrMap.ioAdd(name ='Y03',ioType=IoType.OUTPUT)
adrMap.setSigFormula('Y03','= AIN[3]')
pAdrY03.connect(m6522.nod('RS3'))

# prepared and run makerom3

# after connecting pins got problem P1
# unmount monitor from 6502
#setattr(m6502impl,'updateSignals',oMonFun)
#m6522Impl = m6522.impl()
#def monFun6522(self):
#    self.consoleWrite(f'monFun6522:{hex(self._pins)}\n')
# mount it to 6522 and wel check again
#oMonFun = mountMonitor(m6522Impl,'updateSignals',monFun6522)

#try to pin after updatefromNodes
#setattr(m6502impl,'updateSignals',oMonFun)
#m6502impl = m6502.impl()
#mountMonitor(m6502impl,'updateFromNodes',monFun)

#big mistake P2-MonitoringPoint - should pin to rootmodule after calc



def monCalcFun(self):
    m = self.mdl()
    # put some header with base info - name of function and 6502 current pins in hex
    mClock = m.mod('Clock')
    if mClock.impl().riseDelay()==5: #maybe delay needed
        m6502 = m.mod('C6502')
        m6502Impl = m6502.impl()
        m6502Impl.consoleWrite(f'monFun:{hex(m6502Impl._pins)}\n')
        s = bin(m6502Impl._pins)[::-1]+'\n'
        # read some singals from the chip (standard way - not directly from pins)
        rwb = m6502.sig('RWB').value()
        adr = m6502.sig('ADR').value()
        dta = m6502.sig('DTA').value()
        # read RW signal also directly from pins (I've had some problems with reading it from signals as signal type was wrongly set)
        rw = m6502Impl.readBits(m6502Impl._pins,24,1)
        s = '' # read binary string bit by bit as in Ben's aproach
        for i in range(15,-1,-1):
            bit = m6502Impl.readBits(adr,i,1)
            s+= '0' if bit == 0 else '1'
        d = '' # same here for data byte
        for i in range(7,-1,-1):
            bit = m6502Impl.readBits(dta,i,1)
            d+= '0' if bit == 0 else '1'
        # some formatting 4/2 hex
        ah = ''.join('%04x'%adr)
        dh = ''.join('%02x'%dta)
        rwc = 'r' if rwb>0 else 'W' 
        m6502Impl.consoleWrite(f'{s} {d} {ah} {rwc} {dh} rwb:{rwb} rw:{rw} {bin(adr)} {bin(dta)}\n')    

setattr(m6502impl,'updateSignals',oMonFun)
mImpl = m.impl()
mountMonitor(mImpl,'calculate',monCalcFun)

# well - it's better now but still getting 0x00 on write instead of 55 or aa P3-ZeroOnWrite?
# can be something with lda but it's rather a problem with dynamic io DTA/IO/D0 connection
# somewhere here signal is reset to zero (because it leaves cpu as correct) 
# so - we'll pin some additional monitoring points ...
# first - on DTA
def monDTASetValue(self,nval):
    v = self.value()
    if v!=nval: # change only I think
        self.consoleWrite(f'DTA changed from:{bu.hex(v,2)} to {bu.hex(nval,2)}\n')

pDTA = m6502.sig('DTA')
mountMonitor(pDTA,'setValue',monDTASetValue,putBefore=True)

# here occured problem P4-  crash on monitor - too much sync communication occurred as problem source ...
# so changed Signal.setupValueChanged to work on events/signal emitting 


# When P4- is fixed - I can clearly see (using properties monitor I/O Hex) that signal is reseting to zero
# Probably


# at the end -  pins some 'diodes' to PB output...
diodes = modv.modAdd('diodes',
    moduleType = q3.moduletype.ModuleType.GRAPH
    )

pDIN = diodes.ioAdd(name ='DIN',ioType=IoType.INPUT, size=8)
nPB = m6522.nod('PB')
nPB.connect(pDIN)
#pAdrY = adrMap.ioAdd(name ='Y15B',ioType=IoType.OUTPUT)

for i in range(0,8,1):
    n = diodes.ioAdd(name =f'Y0{i}',ioType=IoType.OUTPUT)
    diodes.setSigFormula(f'Y0{i}',f'= DIN[{i}]')

# and now put it in some nice place ...
diodes.setPos(170.0,-30.0)
diodes.view().setRotate(True)
m6522.view().expand()


# fasten clock, reset circuit , wait 3 secs set it back
mClock.impl().setInterval(200)
sRes = mInp.sig('i2')
sRes.setValue(False)
tm.sleepMs(3000)
sRes.setValue(True)

