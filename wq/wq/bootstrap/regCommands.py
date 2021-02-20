import types

c = _namespace['c']
cw = _namespace['cw']

#g=c



rc = c.registerCommand
rp = c.registerProp
rc('rc',c.registerCommand, True)
rc('rp',c.registerProp, True)
pr = print
rc('pr',print,True)

#cw write
wr = write = cw.write
rc('write',cw.write,True)
rc('wr',cw.write,True)
rc('write',cw.write)
rc('wr',cw.write)

#editorFrame
ed = editorFrame = c.parent()
rc('editorFrame',c.parent(),True)
rc('ed',c.parent(),True)

app = application = ed.app()
rc('application',ed.app(),True)
rc('app',ed.app(),True)

#rootModule - selected
rm = rootModule = ed.rootModule
rc('rootModule',ed.rootModule, True)
rc('rm', ed.rootModule, True)
rp('rm',ed.rootModule)

#rootModule - q3vector
rms = rootModules = ed.rootModules
rc('rootModules',ed.rootModules, True)
rc('rms',ed.rootModules, True)

#rootModule - select
rmsel = rootModuleSelect = ed.rootModuleSelect
rc('rootModuleSelect',ed.rootModuleSelect, True)
rc('rmsel',ed.rootModuleSelect, True)

#rootModule - signals
sigs = signals = ed.rootModuleSignals  
rc('signals', ed.rootModuleSignals, True)
rc('sigs', ed.rootModuleSignals, True)

#rootModule - nodes
sigs = signals = ed.rootModuleNodes  
rc('nodes', ed.rootModuleNodes, True)
rc('nods', ed.rootModuleNodes, True)

#rootModule - modules
sigs = signals = ed.rootModuleModules  
rc('modules', ed.rootModuleModules, True)
rc('mods', ed.rootModuleModules, True)



#imports 


