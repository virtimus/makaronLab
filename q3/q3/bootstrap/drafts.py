'''

for i in c.rm.mods().values(): 
  print(i.name()) 


rootModule
andModule1
andModule2
notModule
norModule1
norModule2
graphModule1
m6502Module
cpcModule
moduleInputs
moduleOutputs
moduleTops
moduleDowns


c.rm.modules().by('name','m6502Module') 

<q3.Module.Module object at 0x7f9506418390>


c.rm.modules().by('name','m6502Module').impl() 

<q3.ModuleLibraryQ3Chips.ModuleImpl6502 object at 0x7f950641d278>


c.rm.modules().by('name','m6502Module').impl().events().dyn('test') 

<unbound PYQT_SIGNAL PyQt_PyObject)>


m6502 = c.rm.modules().by('name','m6502Module') 

m6502impl = c.rm.modules().by('name','m6502Module').impl() 

oldUpdateSignals = m6502impl.updateSignals 

oldUpdateSignals 

<bound method ModuleImpl6502.updateSignals of <q3.ModuleLibraryQ3Chips.ModuleImpl6502 object at 0x7f950641d278>>


def newUpdateSignals: 

    Traceback (most recent call last):
      File "/home/ths/.local/lib/python3.6/site-packages/pyqtgraph/console/Console.py", line 178, in execSingle
        exec(cmd, self.globals(), self.locals())
      File "<string>", line 1
        def newUpdateSignals:
                            ^
    SyntaxError: invalid syntax
    

newUpdateSignals = lambda self: ( 
self.consoleWrite(hex(self._pins)), 
oldUpdateSignals(self)) 
'''

