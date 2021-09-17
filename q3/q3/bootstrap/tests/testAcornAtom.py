
from q3.api import *

from ssl import SSLSocket
import types

def makeAcornAtom(name:str,parent:Module=None):
    #make root if parent is None
    m = parent.modAdd(name) if parent!=None else modvAdd(name).module()

    rootModule = m
    modv = m.view()

    cpcModule = modv.modAdd('cpcModule',
        #type=ModuleType.ATOMIC,
        impl='Q3Chips:/CPC'
        )

    def mountMonitor(obj, mname, handler):
        omethod = getattr(obj,mname)
        def mhandler(self):
            handler(self)
            return omethod()
        nm = types.MethodType(mhandler,obj)
        setattr(obj,mname,nm)

    def monFun(self):
        self.consoleWrite(f'monFun:{hex(self._pins)}\n')
        s = bin(self._pins)[::-1]+'\n'
        #print(s)
        #c = self.console()
        #self.console().write(s)
        self.cw(s)


    #if (m6502!=None):
    #    m6502impl = m6502.impl()
    #    mountMonitor(m6502impl,'updateSignals',monFun)

    #def mountMonitorM(self,obj, mname, handler):
    #    mountMonitor(obj, mname, handler)

    mInp = c.rm.mods().by('name','moduleInputs')
    mOut = c.rm.mods().by('name','moduleOutputs')
    inputs = mInp
    inp = mInp

    #inputsViewImpl = inputs.view().impl()

    for i in range(0,10,1):
        #mInp.oAdd()
        rootModule.iAdd()


    for i in range(0,10,1):
        #mOut.iAdd()
        rootModule.oAdd()


    #tm.sleepMs(1000) #has to wait in mt mode
    

    if m.isRoot():
        cpcModule.setPos(-220.0,-140.0) #cpc

    return m    

    
if __name__ == '__main__':
    makeAcornAtom('AcornAtom')