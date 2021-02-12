g = _namespace['g']
rc = g.registerCommand
rc('rc',g.registerCommand, True)
pr = print
rc('pr',print,True)

#editorFrame
ed = editorFrame = g.parent()
rc('editorFrame',g.parent,True)
rc('ed',g.parent,True)

#rootModule
rms = ed.rootModuleSelected()
rc('rms',ed.rootModuleSelected, True)
