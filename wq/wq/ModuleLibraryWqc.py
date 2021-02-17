
from .ModuleFactory import *

from .Log import Log
import logging
import sys


import wqc

from .Signal import Signal

log = Log(__name__)

from bitstring import BitStream, BitArray
class ModuleImpl6502(ModuleImplBase):
    def __init__(self, **kwargs):
        #log.warn("Hello from log")
        #self._6502desc = wqc.c6502_init()
        self._opened = None
        self._pins = 0
        self._prevPins = None
        self._winid = None
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
        self._init = wqc.c6502_init(initParms)
        return self._init
    
    def open(self):
        self._counter=0
        if self._opened == None:
            self._opened = wqc.c6502_open()
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
        self.updateFromNodes()
        if self._prevPins != self._pins:
            if (self._prevPins!=None):
                print(f'a0:{bin(self._prevPins)[::-1]}')
            print(f'a1:{bin(self._pins)[::-1]}')
        self._pins = wqc.c6502_calc(self._opened['iv'],self._pins)
        if self._prevPins != self._pins:
            self.updateSignals()
            print(f'zd:{bin(self._pins)[::-1]}')
        self._counter+=1
        if self._counter>1011: 
            self._counter=0
            pins = self._opened['pins']
            #print(f'6502DebugPins:{pins}')
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
                        if (sfrom==None):
                            print(f'None for singla:{s.name()}')
                        #ba[sfrom:sfrom+ssize].uint=s.valueAsUInt()
                        self.mutatePins(sfrom,ssize,s.valueAsUInt())
        #self._pins = ba.uint
        #if (self._pins!=self._prevPins):
        #    print(f'6502INPins:{self._pins} ba:{ba.bin}')
        #0b10101010101

    def readPins(self,fr,sz):
        pins = self._pins
        b = bin(pins)
        ones = pow(2, sz)-1
        ones_sh = ones << fr
        pins = pins & ones_sh
        pins = pins >> fr
        return pins

    def mutatePins(self,fr,sz,uint):
        pins = self._pins
        b = bin(pins)[::-1]
        b = bin(uint)[::-1]
        ones = pow(2, sz)-1
        b = bin(ones)[::-1]
        ones_sh = ones << fr
        b = bin(ones_sh)[::-1]
        cuint = uint & ones
        b=bin(cuint)[::-1]
        cuint = cuint << fr
        b=bin(cuint)[::-1]
        pins = pins & ~ones_sh
        b=bin(pins)[::-1]
        pins = pins | cuint
        b=bin(pins)[::-1]
        self._pins = pins




    def updateSignals(self):
        #ba = BitArray(uint=self._pins,length=64)
        for s in self.signals().values():
            ssize = s.size()
            sfrom = s.prop('from')
            if sfrom == None:
                print(f'Nonesssss for singla:{s.name()}')
            cv = self.readPins(sfrom,ssize)
            s.setValue(cv)    
            #vg = ba.cut(ssize,sfrom, None, 1)
            #for v in vg:
            #    cv = v.int if ssize>1 else v.bool
            #    s.setValue(cv)
            if s.name()=='ADR':
                print(f'ad:{bin(s.value())[::-1]}')
        self._prevPins = self._pins

class ModuleImplCPC(ModuleImplBase):
    def __init__(self, **kwargs):
        self._opened = None
        self._prevPins = None
        self._winid = None
        super(ModuleImplCPC,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from del/CPC")
        super(ModuleImplCPC,self).__init__()
    '''
    def __getattr__(self, name):
        return name

    def __setattr__(self, name:str, value):
        print("setting atrrr:"+str(name)+str(value))   
    '''   

    def echo(self):
        print("Hello World from CPC")

    def init(self,**kwargs) -> dict:
        initParms = {}
        self._init = wqc.cpc_init(initParms)
        return self._init
    
    def open(self):
        pass

    def __afterViewCreated__(self):
        self.events().moduleDoubleClicked.connect(self.heModuleDoubleClicked)
        self.events().detailWindowResized.connect(self.heDetailWindowResized)

    def heDetailWindowResized(self,event=None):
        if self._winid!=None:
            ev = event.props('event')
            twidth = ev.size().width()
            theight = ev.size().height()
            wqc.cpc_insp({
                'winId':self._winid,
                'command':'resizeWindow',
                'width':twidth,
                'height':theight
                })

    def heModuleDoubleClicked(self, event=None):
        self.mdlv().showDetailWindow(parent=self.mdlv().impl())
        win = self.mdlv().detailWindow()
        self._winid = win.impl().winId()        
        self._counter=0
        #import threading
        #th = threading.Thread(target=self.startInThread)
        #th.start()
        if self._opened == None:
            self._opened = wqc.cpc_open({'winId':self._winid})
        return self._opened


    #def startInThread(self):
    #    if self._opened == None:
    #         self._opened = wqc.cpc_open({'winId':self._winid})


    def calc(self):
        '''
        self._opened['pins'] = wqc.cpc_calc(self._opened['iv'],self._opened['pins'])
        if self._prevPins != self._opened['pins']:
            self.updateSignals(self._opened['pins'])
        self._counter+=1
        if self._counter>1011: 
            self._counter=0
            pins = self._opened['pins']
            print(f'6502DebugPins:{pins}')
        return self._opened['pins']
        '''




@ModuleFactory.registerLibrary('wqc')
class ModuleLibraryWqc(ModuleLibraryBase):

    _modules = {
        "c6502":ModuleImpl6502,
        "CPC":ModuleImplCPC
    }

    @classmethod
    def createModule(cls, moduleName: str, **kwargs) -> 'ModuleImplBase':
        """ Runs the given command using subprocess """

        if moduleName not in cls._modules:
            #log.warn('Module %s does not exist in the library', name)
            return None


        module_class = cls._modules[moduleName]
        moduleImpl = module_class(**kwargs)
        return moduleImpl

if __name__ == '__main__':
    #for handler in logger.handlers:
    #    filename = handler.baseFilename
    #    print(filename)
    # Creates a local library
    print
    wqcLib = ModuleFactory.loadLibrary('wqc')
    # ... then some modules ...
    test1 = wqcLib.createModule('test1')
    test2 = wqcLib.createModule('test2')
    c6502 = wqcLib.createModule('c6502')
    # ... and finally access some methods ...
    test1.echo()
    test2.echo()
    c6502.echo() 

    #res = c6502.testAttr

    print(res)

    res = c6502.init({
        'empty':"dupa"
        })

    print(res) 

    cpu = c6502.open() 

    import time

    def set_bit(value, bit):
        return value | (1<<bit)

    def clear_bit(value, bit):
        return value & ~(1<<bit)

    def hex64(n):
        return hex (n & 0xffffffffffffffff) #[:-1]    

    print(cpu) 
    start = time.time()
    for i in range(0,40,1):
        cpu = c6502.calc()
        print(f'hex64:{hex64(cpu)}')  
        cpu = set_bit(cpu,63)
    stop = time.time()
    print(f'Calculated in {stop-start}s')   