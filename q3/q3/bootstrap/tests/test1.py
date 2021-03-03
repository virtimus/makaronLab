
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


inputs = c.rm.mods().by('name','moduleInputs')
outputs = c.rm.mods().by('name','moduleOutputs')
inp = inputs
inputsViewImpl = inputs.view().impl()

for i in range(0,10,1):
    inputsViewImpl.addInput()

for i in range(0,10,1):
    outputs.view().impl().addOutput()

#tm.sleepMs(1000) #has to wait in mt mode

#replaced by non view operations - safer in mthread env (objects on view created async)
#s = inputsViewImpl.module().nodes().by('name','#0').view()
s = inputsViewImpl.module().nodes().by('name','#0')
#t = m6502.nodes().by('name','RDY').view()
t = m6502.nodes().by('name','RDY')
s.connect(t)

#s = inputsViewImpl.module().nodes().by('name','#9').view()
s = inputsViewImpl.module().nodes().by('name','#9')
#t = m6502.nodes().by('name','PHI0I').view()
t = m6502.nodes().by('name','PHI0I')
s.connect(t)


s = inputs.nodes().by('name','#0')
t = m6502.nodes().by('name','IRQB') 
s.connect(t)

s = inp.nodes().by('name','#0')
t= m6502.nodes().by('name','NMIB') 
s.connect(t) 

m6502.setPos(-240.0,-240.0) #6502
cpcModule.setPos(-420.0,-140.0) #cpc
graphModule1.setPos(-380.0,-190.0) #graph
#c.rm.modulesBy('id',12).setPos(-440.0,-80.0) #downs
#c.rm.modulesBy('id',11).setPos(-470.0,-170.0) #tops
norModule1.setPos(180.0,-100.0) #nor up
norModule2.setPos(190.0,80.0) #nor down
andModule1.setPos(50.0,-100.0) # andup
andModule2.setPos(50.0,100.0) # anddown
notModule.setPos(-80.0,-100.0) # notup
mo = rootModule.mod('moduleOutputs')
mo.setPos(390.0,-100.0) #outputs
mi = rootModule.mod('moduleInputs')
mi.setPos(-380.0,40.0) #inputs

#c.rm.connect(8,13) #nor2nor # here to have more lag to stabilize
norModule1.nod('Y').connect(norModule2.nod('A'))

#c.rm.connect(26,7) # inp #3 to not
mi.nod('#3').connect(notModule.nod('A'))
#c.rm.connect(6,1) #not2and
notModule.nod('Y').connect(andModule1.nod('A'))

#c.rm.connect(0,12) #and2nor
andModule1.nod('Y').connect(norModule1.nod('A'))

#c.rm.connect(11,33) #nor2out
norModule1.nod('Y').connect(mo.nod('#0'))

#c.rm.connect(26,4) # inp #3 to and down
mi.nod('#3').connect(andModule2.nod('A'))

#c.rm.connect(3,10) # and2nor
andModule2.nod('Y').connect(norModule2.nod('B'))

#c.rm.connect(8,42) # nor2 out
norModule2.nod('Y').connect(mo.nod('#9'))

#c.rm.connect(27,2) #inp #4 to and
mi.nod('#4').connect(andModule1.nod('B'))

#c.rm.connect(27,5) #inp #4 to and
mi.nod('#4').connect(andModule2.nod('B'))

#c.rm.connect(11,9) #nor2nor # and the second feedback
norModule2.nod('Y').connect(norModule1.nod('B'))

mainRootModule = c.rm

#tm.sleepMs(3000)
#new module
moduleView = modvAdd()

m = moduleView.module()

#mod(3).setPos(0.0,-400.0)
#mod(4).setPos(0.0,400.0)

#from ..moduletype import ModuleType as ModuleType

import q3.moduletype
from q3.nodeiotype import NodeIoType

minputs = m.mods('moduleInputs')
moutputs = m.mods('moduleOutputs')
minputsViewImpl = minputs.view().impl()
mi0 = minputsViewImpl.addInput()
mi1 = minputsViewImpl.addInput()
mi2 = minputsViewImpl.addInput()
mi3 = minputsViewImpl.addInput()

moutputsViewImpl = moutputs.view().impl()
mo0 = moutputsViewImpl.addOutput()
mo1 = moutputsViewImpl.addOutput()

def norGraph(parent, name:str, A,B,Y):
    graphModule1 = parent.modAdd(name,
        moduleType = q3.moduletype.ModuleType.GRAPH
        )
    i0 = graphModule1.view().impl().addInput()
    i1 = graphModule1.view().impl().addInput()
    o0 = graphModule1.view().impl().addOutput()
    #o1 = graphModule1.view().impl().addOutput()


    #mi0 = minputs.nods('#0')
    #mi0 = minputs.nods('#0')
    A.connect(i0)
    B.connect(i1)

    #i0.connect(o0) #wrong

    #this is just connecting input/output signals across graph module
    #i0.addSignal(o1.driveSignal())
    #i1.addSignal(o0.driveSignal())

    #let's try create a 3rd level module (not visible) inside the 2nd level graph module ...
    nor1 = graphModule1.modAdd('nor1',
        impl = 'local:/NOR'
        ) 
    #local/nor gate has A/B input and Y output - connect it...

    i0.connect(nor1.nod('A'))
    i1.connect(nor1.nod('B'))
    #nor1.nod('Y').connect(o0) #currently invalid 
    nor1.nod('Y').addSignal(o0.driveSignal())

    o0.connect(Y)
    return graphModule1

#rmsel('rootModule')
#rmsel(mainRootModule)
#tm.sleepMs(3000)

gr1 = norGraph(moduleView,'gr1',mi0,mi1,mo0)

graphParent = moduleView.modAdd('graphParent',
    moduleType = q3.moduletype.ModuleType.GRAPH
    )
igp0 = graphParent.ioAdd(name = '#0', ioType = NodeIoType.INPUT) #graphParent.view().impl().addInput()
igp1 = graphParent.view().impl().addInput()
ogp0 = graphParent.view().impl().addOutput()
mi2.connect(graphParent.nodl('#0'))
mi3.connect(graphParent.nodl('#1'))
graphParent.nodr('#0').connect(mo1)
    
igp0.addSignal(ogp0.driveSignal())
    #i1.addSignal(o0.driveSignal())
graphParent.setPos(0.0,110.0)

#gr2 = norGraph(graphParent,'gr2',mi2,mi3,mo1)
