#standard simulator bootstrap
#from wx.core import Sleep
import wq

from wq.Timer import Timer

import PyQt5.QtCore as qtc

import threading


keys = globals().keys()
runApp = False

if False and not 'c' in keys:
    c = None
    
    class encImpl(qtc.QThread):
        def __init__(self):
            self._c = None
            self._initialized = False
            super(encImpl, self).__init__()
        def run(self):
            while (not self._initialized):
                Timer.sleepMs(0)
            pass
            #exec(open("./../../editor.py").read())
            #g = console.newConsoleWidget

    
    tg = threading.Thread(target=tga.run)
    #t = qtc.QThread(tg.main)
    #t.daemon = True
    #tg.finished.connect(app.exit)
    tg.start()

    c = tg._c
    runApp = True

#c.registerCommand('rc',c.registerCommand)
cPath='/src/makaronLab/wq/wq/'

class encImpl:
    def __init__(self):
        self._namespace = None
        self._initialized = False

    def run(self):
        self.process(self._namespace)

    def process(self, _namespace):
        print('Hello world')        
        exec(open(cPath+"bootstrap/regCommands.py").read())
        self._initialized = True
        #exec(open("/src/makaronLab/wq/wq/bootstrap/startup.py").read())        

app = wq.App(wqImpl=wq.consts.Q3_IMPL)
frm = wq.EditorFrame(app, title='makaronLab') #,wqImpl=wq.consts.Q3_IMPL)
tga = encImpl()
tga._namespace = frm.consoleNamespace()
#self._initialized = True
tg = threading.Thread(target=tga.run)
tg.start()
while (not tga._initialized):
    Timer.sleepMs(0)
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

cw = frm.consoleWidget()

def execF(fileName:str):
    with stdoutIO() as s:
        exec(open(fileName).read(),cw.globals(),cw.locals())
    result = s if isinstance(s,str) else s.getvalue()
    return result

frm.console().registerCommand('execF',execF,True) 

fileName = cPath+"bootstrap/beforeShow.py"
s=execF(fileName)
#cw.write(repr(s.getvalue()) + '\n')   
cw.write('\n===bootstrap/beforeShow.py:\n'+s + '\n') 
#why not register execF as Function ?

frm.Show()

fileName = cPath+"bootstrap/afterShow.py"
s=execF(fileName)
#cw.write(repr(s.getvalue()) + '\n')   
cw.write('\n===bootstrap/afterShow.py:\n'+s + '\n')

app.MainLoop()



