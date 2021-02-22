
if c == None:
    c = _namespace['c']
mods = mods

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

#def setSelected(item):
#    c.rm.graphModule().view().impl().setSelected(item.impl())

#def setSelectedM(self,item):
#    setSelected(item)
#c.rm.setSelected = types.MethodType(setSelectedM,c) 

#c.rm.mods().by('name','moduleInputs').view().impl().addInput() 

#c.rm.setSelected(c.rm.mods().by('name','moduleInputs'))

inputs = c.rm.mods().by('name','moduleInputs')
outputs = c.rm.mods().by('name','moduleOutputs')
inp = inputs
inputsViewImpl = inputs.view().impl()

for i in range(0,10,1):
    inputsViewImpl.addInput()

for i in range(0,10,1):
    outputs.view().impl().addOutput()

s = inputsViewImpl.module().nodes().by('name','#0').view()
t = m6502.nodes().by('name','RDY').view()
s.connect(t)

s = inputsViewImpl.module().nodes().by('name','#9').view()
t = m6502.nodes().by('name','PHI0I').view()
s.connect(t)


s = inputs.nodes().by('name','#0')
t = m6502.nodes().by('name','IRQB') 
s.connect(t)

s = inp.nodes().by('name','#0')
t= m6502.nodes().by('name','NMIB') 
s.connect(t) 

c.rm.modulesBy('id',7).setPos(-240.0,-240.0) #6502
c.rm.modulesBy('id',8).setPos(-420.0,-140.0) #cpc
c.rm.modulesBy('id',6).setPos(-380.0,-190.0) #graph
c.rm.modulesBy('id',12).setPos(-440.0,-80.0) #downs
c.rm.modulesBy('id',11).setPos(-470.0,-170.0) #tops
c.rm.modulesBy('id',5).setPos(180.0,-100.0) #nor up
mods(4).setPos(190.0,80.0) #nor down
c.rm.modulesBy('id',1).setPos(50.0,-100.0) # andup
mods(2).setPos(50.0,100.0) # anddown
c.rm.modulesBy('id',3).setPos(-80.0,-100.0) # notup
mods(10).setPos(390.0,-100.0) #outputs
mods(9).setPos(-380.0,40.0) #inputs

c.rm.connect(8,13) #nor2nor # here to have more lag to stabilize

c.rm.connect(26,7) # inp #3 to not
c.rm.connect(6,1) #not2and
c.rm.connect(0,12) #and2nor
c.rm.connect(11,33) #nor2out

c.rm.connect(26,4) # inp #3 to and
c.rm.connect(3,10) # and2nor
c.rm.connect(8,42) # nor2 out

c.rm.connect(27,2) #inp #4 to and
c.rm.connect(27,5) #inp #4 to and

c.rm.connect(11,9) #nor2nor # and the second feedback
