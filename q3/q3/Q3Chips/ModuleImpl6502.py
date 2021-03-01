
from ..ModuleFactory import *
from .. import bitutils as bu

import q3c

class ModuleImpl6502(ModuleImplBase):
    def __init__(self, **kwargs):
        #log.warn("Hello from log")
        #self._6502desc = q3c.c6502_init()
        self._opened = None
        self._pins = 0
        self._prevPins = None
        self._winid = None
        self._prevClock = None
        self._prevReset = None
        self._prevDTADrive = None
        super(ModuleImpl6502,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from del")
        super(ModuleImpl6502,self).__del__()
    '''
    def __getattr__(self, name):
        return name

    def __setattr__(self, name:str, value):
        print("setting atrrr:"+str(name)+str(value))   
    '''   

    def echo(self):
        print("Hello World from 6502")

    def init(self,**kwargs) -> dict:
        initParms = {}
        self._init = q3c.c6502_init(initParms)
        return self._init
    
    def open(self):
        self._counter=0
        if self._opened == None:
            self._opened = q3c.c6502_open()
            self._pins = self._opened['pins']
        io = {}
        pname = None
        ci=0
        tsize = None
        tdic = self._init['signalMap'] 
        halfSize = round(len(tdic)/2)
        for name in tdic:
            if name == '@size':
                tsize = tdic[name]
                halfSize = round(tsize/2)
            else:
                if pname!=None: 
                    cdic =  tdic[pname]                  
                    stype = cdic['ioType'] if 'ioType' in cdic else None
                    frn = cdic['from'] #if 'type' in tdic[pname] else None
                    ioType = IoType.fromString(stype) if stype !=None else IoType.INPUT
                    dir = direction.LEFT if frn < halfSize else direction.RIGHT
                    size = tdic[pname]['size'] if 'size' in tdic[pname] else tdic[name]['from'] - frn 
                    if size >consts.MAX_SIGNAL_SIZE:
                        size = 1
                    io[pname] = self.newIO(
                        name=pname,
                        size=size,
                        ioType = ioType,
                        direction = dir,
                        props={'from':frn,'cdic':cdic}
                    )
                    ci+=1
                pname = name
        io['PHI0I'] = self.newIO(
            name = 'PHI0I',
            size = 1,
            ioType = IoType.INPUT,
            direction = direction.RIGHT
        )
        self._io = io
        #//self._intSignal = Signal(name='internalCom6502',size=64)
        #self._intSignal.setValue(self._opened['pins']) 
        return self._io

    def calc(self):
        
        #self.sig('RESB').setValue(True)
        resb = self.sig('RESB').value()
        resbDelta = self._prevReset != resb
        #if (resbDelta and not resb): #low active rise
        #    self._pins = bu.writeBits(self._pins,30,1,0)
        clk = self.sig('PHI0I').value()
        clkDelta = self._prevClock != clk
        rdy = self.sig('RDY').value()
        clkRise = clkDelta and clk
        #rstDown = resbDelta and not resb
        self._prevClock = clk 
        self._prevReset = resb
        if (rdy and clkRise):
            #self.consoleWrite(f'calca:{bu.binlend(self._pins)}\n')
            self.updateFromNodes()
            #print('clkrise\n')
            #if self._prevPins != self._pins:
                #if (self._prevPins!=None):
                #    print(f'a0:{bin(self._prevPins)[::-1]}')
                #print(f'a1:{bin(self._pins)[::-1]}')
            #self.consoleWrite(f'calcb:{bu.binlend(self._pins)}\n')
            self._pins = q3c.c6502_calc(self._opened['iv'],self._pins)
            #self.consoleWrite(f'calcc:{bu.binlend(self._pins)}\n')
            #self.consoleWrite('calc\n')
            if self._prevPins != self._pins:
                self.updateSignals()
                #print(f'zd:{bin(self._pins)[::-1]}')
            #self._counter+=1
            #if self._counter>1011: 
            #    self._counter=0
            #    pins = self._opened['pins']
            #    #print(f'6502DebugPins:{pins}')
        return self._opened['pins']

    def updateFromNodes(self):
        #ba = BitArray(uint=self._pins,length=64)
        for n in self.nodes().values():
            if n.ioType() in [IoType.INPUT,IoType.DYNAMIC]:
                ds = n.driveSignal()
                if ds!=None and n.signals().size()>1:
                    for s in n.signals().values():
                        if s!=ds:
                            ssize = s.size() if s.prop('size')==None else s.prop('size')
                            sfrom = s.prop('from')
                            #if (sfrom==None):
                            #    print(f'None for singla:{s.name()}')
                            #ba[sfrom:sfrom+ssize].uint=s.valueAsUInt()
                            sv = s.valueAsUInt()    
                            # had to invert some signals after long investigation
                            # chips implementation is not compliant with pins specs
                            if s.name() in ['RDY','NMIB','IRQB','RESB']:  
                                sv = ~sv
                            if sfrom !=None:
                                self.writePins(sfrom,ssize,sv)
        #self._pins = ba.uint
        #if (self._pins!=self._prevPins):
        #    print(f'6502INPins:{self._pins} ba:{ba.bin}')
        #0b10101010101

    def readBits(self,pins,fr,sz):
        return bu.readBits(pins,fr,sz)
        '''
        b = bin(pins)
        ones = pow(2, sz)-1
        ones_sh = ones << fr
        pins = pins & ones_sh
        pins = pins >> fr
        return pins
        '''


    def readPins(self,fr,sz):
        pins = self._pins
        return self.readBits(pins,fr,sz)

    def writeBits(self,pins,fr,sz,uint):
        return bu.writeBits(pins,fr,sz,uint)
        '''
        #b = bin(pins)[::-1]
        #b = bin(uint)[::-1]
        ones = pow(2, sz)-1
        #b = bin(ones)[::-1]
        ones_sh = ones << fr
        #b = bin(ones_sh)[::-1]
        cuint = uint & ones
        #b=bin(cuint)[::-1]
        cuint = cuint << fr
        #b=bin(cuint)[::-1]
        pins = pins & ~ones_sh
        #b=bin(pins)[::-1]
        pins = pins | cuint
        #b=bin(pins)[::-1]
        return pins
        '''


    def writePins(self,fr,sz,uint):
        #pins = self._pins
        pinsb = self._pins
        self._pins = self.writeBits(self._pins,fr,sz,uint)
        #if pinsb != self._pins:
        #    print(f'mutatePins:{fr} {sz} {uint}\n')
        #    print(f'pinsbefore:{bu.binlend(pinsb)}')
        #    print(f' pinsafter:{bu.binlend(self._pins)}')


    def updateSignals(self):

        #ba = BitArray(uint=self._pins,length=64)
        for s in self.signals().values():
            ssize = s.size()
            sfrom = s.prop('from')
            #if sfrom == None:
            #    print(f'Nonesssss for singla:{s.name()}')
            if sfrom!=None:
                cv = self.readPins(sfrom,ssize)
                '''
                if s.name()=='DTA':
                    self.consoleWrite(f'updateDTA:{bu.hex(cv,2)}\n')
                if s.name()=='ADR':
                    self.consoleWrite(f'updateADR:{bu.hex(cv,4)}\n')
                '''
                s.setValue(cv)    
            #vg = ba.cut(ssize,sfrom, None, 1)
            #for v in vg:
            #    cv = v.int if ssize>1 else v.bool
            #    s.setValue(cv)
            #if s.name()=='ADR':
            #    print(f'ad:{bin(s.value())[::-1]}')

        #check if write
        rwb = self.sig('RWB').value()
        dtaSig = self.sig('DTA')
        dtaNod = self.nod('DTA')
        if rwb:#read
            #dtaSig.dvIn(True)
            if dtaNod.driveSignal()==dtaSig: #change to prev
                dtaNod.setDriveSignal(self._prevDTADrive)
            elif dtaNod.driveSignal()!=None and self._prevDTADrive==None: #set initial read signal
                self._prevDTADrive = dtaNod.driveSignal()
            pass
        else:#write
            #dtaSig.dvOut(True)
            if dtaNod.driveSignal()!=dtaSig:
                if dtaNod.driveSignal()!=None:
                    self._prevDTADrive = dtaNod.driveSignal()
                dtaNod.setDriveSignal(dtaSig)
            pass
        
        self._prevPins = self._pins
        #c = self.console()
        #s = bin(self._pins)[::-1]+'\n'
        #c.write(s)