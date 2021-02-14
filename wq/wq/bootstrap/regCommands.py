g = _namespace['g']
rc = g.registerCommand
rc('rc',g.registerCommand, True)
pr = print
rc('pr',print,True)

#editorFrame
ed = editorFrame = g.parent()
rc('editorFrame',g.parent(),True)
rc('ed',g.parent(),True)

app = application = ed.app()
rc('application',ed.app(),True)
rc('app',ed.app(),True)

#rootModule - selected
rm = rootModule = ed.rootModule
rc('rootModule',ed.rootModule, True)
rc('rm',ed.rootModule, True)

#rootModule - wqvector
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


