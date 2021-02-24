
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
        super(ModuleImpl6502,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from del")
        super(ModuleImpl6502,self).__init__()
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
        self._io = io
        #//self._intSignal = Signal(name='internalCom6502',size=64)
        #self._intSignal.setValue(self._opened['pins']) 
        return self._io

    def calc(self):
        #self.updateFromNodes()
        #self.sig('RESB').setValue(True)
        resb = self.sig('RESB').value()
        resbDelta = self._prevReset != resb
        clk = self.sig('PHI0I').value()
        clkDelta = self._prevClock != clk
        rdy = self.sig('RDY').value()
        clkRise = clkDelta and clk
        #rstDown = resbDelta and not resb
        self._prevClock = clk 
        self._prevReset = resb
        if (rdy and clkRise):

            #if self._prevPins != self._pins:
                #if (self._prevPins!=None):
                #    print(f'a0:{bin(self._prevPins)[::-1]}')
                #print(f'a1:{bin(self._pins)[::-1]}')
            self._pins = q3c.c6502_calc(self._opened['iv'],self._pins)
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
            ds = n.driveSignal()
            if ds!=None and n.signals().size()>1:
                for s in n.signals().values():
                    if s!=ds:
                        ssize = s.size()
                        sfrom = s.prop('from')
                        #if (sfrom==None):
                        #    print(f'None for singla:{s.name()}')
                        #ba[sfrom:sfrom+ssize].uint=s.valueAsUInt()
                        self.mutatePins(sfrom,ssize,s.valueAsUInt())
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


    def mutatePins(self,fr,sz,uint):
        #pins = self._pins
        self._pins = self.writeBits(self._pins,fr,sz,uint)




    def updateSignals(self):
        #ba = BitArray(uint=self._pins,length=64)
        for s in self.signals().values():
            ssize = s.size()
            sfrom = s.prop('from')
            #if sfrom == None:
            #    print(f'Nonesssss for singla:{s.name()}')
            cv = self.readPins(sfrom,ssize)
            s.setValue(cv)    
            #vg = ba.cut(ssize,sfrom, None, 1)
            #for v in vg:
            #    cv = v.int if ssize>1 else v.bool
            #    s.setValue(cv)
            #if s.name()=='ADR':
            #    print(f'ad:{bin(s.value())[::-1]}')
        self._prevPins = self._pins
        c = self.console()
        s = bin(self._pins)[::-1]+'\n'
        c.write(s)