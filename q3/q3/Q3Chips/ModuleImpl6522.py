#from socket import CAN_J1939
from ..ModuleFactory import *
from .. import bitutils as bu

import sys

import q3c

class ModuleImpl6522(ModuleImplBase):
    RS0 =  0
    D0  = 16
    RW  = 24 #B
    PHI2= 25
    IRQ = 26
    CS1 = 40
    CS2 = 41 #B
    CA1 = 42 
    CA2 = 43
    CB1 = 44
    CB2 = 45
    PA0 = 48
    PB0 = 56


    def __init__(self, **kwargs):
        #log.warn("Hello from log")
        #self._6502desc = q3c.c6502_init()
        self._opened = None
        self._pins = 0
        self._prevPins = None
        self._prevResb = None
        self._prevClock = None
        self._iv = None
        super(ModuleImpl6522,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from 6522")
        super(ModuleImpl6522,self).__del__()

    def init(self,**kwargs) -> dict:
        initParms = {}
        #self._init = q3c.c6522_init(initParms)
        #self._init = q3c.c6522({
        #        'command':'init'
        #        })
        self._init = {}
        return self._init

    def open(self):
        self._opened = q3c.c6522({
                'command':'open'
                })
        lebin = self._opened['lebin']
        #self._pins = self._opened['pins']
        self._pins = bu.lebin2dec(lebin)
        self._iv = self._opened['iv']
        io = {}

        io['RESB']=self.newIO(
            name = 'RESB',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT
        )

        io['D0']=self.newIO(
            name = 'D0',
            size = 8,
            ioType = IoType.DYNAMIC,
            direction = direction.LEFT,
            props = {
                'from':self.D0
            }
        )



        io['RWB']=self.newIO(
            name = 'RWB',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.RW
            }            
        )

        io['PHI2']=self.newIO(
            name = 'PHI2',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.RIGHT
        )

        io['CS2B']=self.newIO(
            name = 'CS2B',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.CS2
            }
        )

        io['CS1']=self.newIO(
            name = 'CS1',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.CS1
            }
        )

        io['RS0']=self.newIO(
            name = 'RS0',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.RS0
            }
        )

        io['RS1']=self.newIO(
            name = 'RS1',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.RS0+1
            }
        )

        io['RS2']=self.newIO(
            name = 'RS2',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.RS0+2
            }
        )


        io['RS3']=self.newIO(
            name = 'RS3',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
            props = {
                'from':self.RS0+3
            }
        )

        io['PA']=self.newIO(
            name = 'PA',
            size = 8,
            ioType = IoType.DYNAMIC,
            direction = direction.RIGHT,
            props = {
                'from':self.PA0
            }
        )

        io['PB']=self.newIO(
            name = 'PB',
            size = 8,
            ioType = IoType.DYNAMIC,
            direction = direction.RIGHT,
            props = {
                'from':self.PB0
            }
        )

        self._io = io 
        return self._io

    def readBits(self,pins,fr,sz):
        return bu.readBits(pins,fr,sz)

    def writeBits(self,pins,fr,sz,uint):
        return bu.writeBits(pins,fr,sz,uint)

    def readPins(self,fr,sz):
        pins = self._pins
        return self.readBits(pins,fr,sz)
    
    def writePins(self,fr,sz,uint):
        pins = self._pins
        self._pins = self.writeBits(pins,fr,sz,uint)

    def updateFromNodes(self):
        for n in self.nodes().values():
            if n.ioType() in [IoType.INPUT,IoType.DYNAMIC]:
                ds = n.driveSignal()
                if ds!=None and n.signals().size()>1:
                    for s in n.signals().values():
                        if s!=ds:
                            ssize = s.size() if s.prop('size')==None else s.prop('size')
                            sfrom = s.prop('from')
                            sv = s.valueAsUInt()    
                            # had to invert some signals after long investigation
                            # chips implementation is not compliant with pins specs
                            #if s.name() in ['CS2B','RWB']:  
                            #    sv = ~sv
                            if sfrom !=None:
                                self.writePins(sfrom,ssize,sv)


    def updateSignals(self):
        for s in self.signals().values():
            ssize = s.size()
            sfrom = s.prop('from')
            if sfrom!=None:
                cv = self.readPins(sfrom,ssize)
                s.setValue(cv)    
        self._prevPins = self._pins

    def calc(self):
        resv = self.sig('RESB').value()
        if not resv and self._prevResb != resv: #riseb
            q3c.c6522({
                'command':'reset',
                'iv':self._iv
                })
        self._prevResb = resv

        clkv = self.sig('PHI2').value() 
        clkRise = not clkv and clkv != self._prevClock

        if clkRise: #clkRise
            self.updateFromNodes()
            #pp = pow(2,64)
            #print(f'm6522callCalc {pp} {sys.maxsize} {self._pins}\n',)
            self._calc = q3c.c6522({
                    'command':'calc',
                    'iv':self._iv,
                    #'pins':self._pins
                    'lebin':bu.dec2lebin(self._pins)                    
                    })
            #print('m6522callCalcAfter\n')
            #self._pins = self._calc['pins']
            lebin = self._calc['lebin']
            self._pins = bu.lebin2dec(lebin)
            if self._prevPins != self._pins:
                self.updateSignals()            
        self._prevClock = clkv