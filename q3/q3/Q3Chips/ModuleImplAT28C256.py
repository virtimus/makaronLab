import os
from ..ModuleFactory import *
from .. import bitutils as bu 
#from q3 import Timer
class ModuleImplAT28C256(ModuleImplBase):
    def __init__(self,**kwargs):
        super(ModuleImplAT28C256,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC
        self._memData = bytearray([0x0]*32768) 
        self._memPath = None
        self._prevCEV = None
        self._prevADRC = None

    def init(self,**kwargs):
        self._customProperties['memPath'] ={
            'desc':'Path to rom memory',
            'onChange':self.onMemPathChange,
            'default':self._memPath
        }
        return {}

    def setMemPath(self, path):
        self.onMemPathChange(path)


    def onMemPathChange(self, event):
        self._memPath = event
        self._customProperties['memPath']['default']=self._memPath
        if os.path.exists(self._memPath): # read rom
            with open(self._memPath, 'rb') as inFile:
                # Read the whole file at once
                self._memData = inFile.read()

    def open(self,**kwargs):
        self.newIO(
            name = 'ADR',
            size = 15,
            ioType = IoType.INPUT
        )
        self.newIO(
            name ='I/O',
            size = 8,
            ioType = IoType.DYNAMIC
        )
        self.newIO(
            name = 'CEB',
            desc = 'Chip enable bar',
            size = 1,
            ioType = IoType.INPUT
        )
        return {}


    def calc(self,**kwargs):
        ce = self.sig('CEB').value()
        cev = bu.readBits(ce,0,1)
        #!temp!
        adrs = self.sig('ADR').value()
        #cev = bu.readBits(adrs,15,1)
        #cev = 0 if cev > 0 else 1 #not gate
        cev = self.sig('CEB').value()
        if cev == 0 or cev == False: #active low
            adr = self.sig('ADR').value()
            adrc = bu.readBits(adr,0,15)
            #lets do each op once
            deltaCEV = self._prevCEV != cev
            #has adr changed ?
            adrDelta = self._prevADRC != adrc
            # do we have any delta ?
            isDelta = deltaCEV or adrDelta
            if isDelta:
                ov = self._memData[adrc]
                sIO = self.sig('I/O')
                sIO.setValue(ov)
                nIO = self.nod('I/O') #change driveSignal to send change
                nIO.setIntSignalAsDrive()
                self._prevCEV = cev
                self._prevADRC = adrc

        else:
            #self.sig('I/O').setValue(0)
            pass # not active == nop
        return {}
