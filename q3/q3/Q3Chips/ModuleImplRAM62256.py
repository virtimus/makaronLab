#from socket import CAN_J1939
from ..ModuleFactory import *
from .. import bitutils as bu

import sys

import q3c

class ModuleImplRAM62256(ModuleImplBase):
    DEB =  0
    CSB  = 1
    RWB = 2
    D0 = 3
    A0 = 11


    def __init__(self, **kwargs):
        self._ram = bytearray([0x00]*32768)
        self._prevRWB = None
        self._prevADR = None 
        self._prevDTA = None
        super(ModuleImplRAM62256,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from 6522")
        super(ModuleImplRAM62256,self).__del__()

    def init(self,**kwargs) -> dict:
        initParms = {}
        #self._init = q3c.c6522_init(initParms)
        #self._init = q3c.c6522({
        #        'command':'init'
        #        })
        self._init = {}
        return self._init

    def open(self):
        self._pins = 0
        io = {}

        io['A0']=self.newIO(
            name = 'A0',
            size = 15,
            ioType = IoType.INPUT,
            direction = direction.LEFT,
        )

        io['DEB']=self.newIO(
            name = 'DEB',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT
        )

        io['CSB']=self.newIO(
            name = 'CSB',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,          
        )

        io['RWB']=self.newIO(
            name = 'RWB',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.LEFT,            
        )


        io['D0']=self.newIO(
            name = 'D0',
            size = 8,
            ioType = IoType.DYNAMIC,
            direction = direction.LEFT,
        )
 



        self._io = io 
        return self._io

    def calc(self):
        csbv = self.sig('CSB').value()
        debv = self.sig('DEB').value()
        if not csbv and not debv: #active
            rwbv = self.sig('RWB').value()
            sD0 = self.sig('D0')
            dtav = sD0.value()
            sA0 = self.sig('A0')
            adrv = bu.readBits(sA0.value(),0,sA0.size())

            # read or write ? 0 means write from CPU
            #lets do each op once
            deltaOp = self._prevRWB != rwbv
            #has adr changed ?
            adrDelta = self._prevADR != adrv
            #has value changed?
            valDelta = self._prevDTA != dtav
            # do we have any delta ?
            isDelta = deltaOp or adrDelta or valDelta
            if isDelta: # process if delta
                if rwbv: #read
                    sD0.setValue(self._ram[adrv])
                    # reading means our port is master - so change
                    nD0 = self.nod('D0')
                    nD0.setIntSignalAsDrive()
                else: #write 
                    self._ram[adrv]=dtav
            self._prevRWB = rwbv
            self._prevADR = adrv
            self._prevDTA = dtav
           
