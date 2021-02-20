
if c == None:
    c = _namespace['c']

from ssl import SSLSocket
import types


pr('After show editoFrame')




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

def setSelected(item):
    c.rm.graphModule().view().impl().setSelected(item.impl())

def setSelectedM(self,item):
    setSelected(item)
c.rm.setSelected = types.MethodType(setSelectedM,c) 

#c.rm.mods().by('name','moduleInputs').view().impl().addInput() 

#c.rm.setSelected(c.rm.mods().by('name','moduleInputs'))

imputsImpl = c.rm.mods().by('name','moduleInputs').view().impl()

for i in range(0,10,1):
    imputsImpl.addInput()

s = imputsImpl.module().nodes().by('name','#0').view()
t = m6502.nodes().by('name','RDY').view()
s.connect(t)

s = imputsImpl.module().nodes().by('name','#9').view()
t = m6502.nodes().by('name','PHI0I').view()
s.connect(t)