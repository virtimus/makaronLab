
from q3.api import *


#if c == None:
#    c = _namespace['c']
#mods = mods
#modvAdd = modvAdd
#mod = mod

#pr = pr

from ssl import SSLSocket
import types
#from .regCommands import *


pr('After show editoFrame')

modv = modvAdd('rootModule')

rootModule = modv.module()

#self._rootModule = rootModule

#andModuleImpl = q3lLib.createModule('AND')       
#andModule = Module(rootModule,'andModule',
#    impl = 'local/AND'
#    )
andModule1 = modv.modAdd('andModule1',
    impl = 'local:/AND'
    )

andModule2 = modv.modAdd('andModule2',
    impl = 'local:/AND'
    )

notModule = modv.modAdd('notModule',
    impl = 'local:/NOT'
    )

norModule1 = modv.modAdd('norModule1',
    impl = 'local:/NOR'
    ) 

norModule2 = modv.modAdd('norModule2',
    impl = 'local:/NOR'
    )  

graphModule1 = modv.modAdd('graphModule1',
    #impl = 'file:/tmp/test'
    moduleType =  q3.moduletype.ModuleType.GRAPH
    )



m6502Module = modv.modAdd('m6502Module',
    #type=ModuleType.ATOMIC,
    impl='Q3Chips:/c6502'
    )

#'''
cpcModule = modv.modAdd('cpcModule',
    #type=ModuleType.ATOMIC,
    impl='Q3Chips:/CPC'
    )




m6502 = c.rm.modules().by('name','m6502Module')



def mountMonitor(obj, mname, handler):
    omethod = getattr(obj,mname)
    def mhandler(self):
        handler(self)
        return omethod()
    nm = types.MethodType(mhandler,obj)
    setattr(obj,mname,nm)

'''
if (m6502!=None):
    m6502impl = m6502.impl() 
    oldUpdateSignals = m6502impl.updateSignals 
    newUpdateSignals = lambda self: ( 
        self.consoleWrite(f'{hex(self._pins)}\n'), 
        oldUpdateSignals())
    def newUpdateSignals2(self):
        self.consoleWrite(f'{hex(self._pins)}\n')
        oldUpdateSignals()
    m6502impl.updateSignals = types.MethodType(newUpdateSignals2,m6502impl) 
'''
def monFun(self):
    self.consoleWrite(f'monFun:{hex(self._pins)}\n')
    s = bin(self._pins)[::-1]+'\n'
    #print(s)
    #c = self.console()
    #self.console().write(s)
    self.cw(s)


if (m6502!=None):
    m6502impl = m6502.impl()
    mountMonitor(m6502impl,'updateSignals',monFun)

def mountMonitorM(self,obj, mname, handler):
    mountMonitor(obj, mname, handler)

c.mountMonitor = types.MethodType(mountMonitorM,c)
c.mm = c.mountMonitor
c.debug =c.write
#c.rm.mods().by('name','moduleInputs') 

#def setSelected(item):
#    c.rm.graphModule().view().impl().setSelected(item.impl())

#def setSelectedM(self,item):
#    setSelected(item)
#c.rm.setSelected = types.MethodType(setSelectedM,c) 

#c.rm.mods().by('name','moduleInputs').view().impl().addInput() 

#c.rm.setSelected(c.rm.mods().by('name','moduleInputs'))


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

