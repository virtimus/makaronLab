#standard simulator bootstrap
from wx.core import Sleep
import wq

from wq.Timer import Timer

import PyQt5.QtCore as qtc

import threading


keys = globals().keys()
runApp = False

if False and not 'g' in keys:
    g = None
    
    class encImpl(qtc.QThread):
        def __init__(self):
            self._g = None
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

    g = tg._g
    runApp = True

#g.registerCommand('rc',g.registerCommand)

class encImpl:
    def __init__(self):
        self._namespace = None
        self._initialized = False

    def run(self):
        self.process(self._namespace)

    def process(self, _namespace):
        print('Hello world')        
        exec(open("/src/makaronLab/wq/wq/bootstrap/regCommands.py").read())
        self._initialized = True
        #exec(open("/src/makaronLab/wq/wq/bootstrap/startup.py").read())
        


app = wq.App(wqImpl=wq.consts.Q3_IMPL)
frm = wq.EditorFrame(app, title='makaronLab') #,wqImpl=wq.consts.Q3_IMPL)
frm.Show()
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
with stdoutIO() as s:
    exec(open("/src/makaronLab/wq/wq/bootstrap/startup.py").read(),cw.globals(),cw.locals()) 
#cw.write(repr(s.getvalue()) + '\n')   
cw.write('\nstartup.py:\n'+s.getvalue() + '\n') 
app.MainLoop()



