#standard simulator bootstrap
#from wx.core import Sleep

import q3

import q3.config

import q3.Timer as Timer

from q3.ui.engine import qtw,qtc,qtg

import threading 
import os


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
cPath = os.path.dirname(os.path.realpath(__file__))+'/'
#cPath=dirPath+'/../' #'/src/makaronLab/q3/q3/'

class encImpl:
    def __init__(self):
        self._namespace = None
        self._initialized = False

    def run(self):
        self.process(self._namespace)

    def process(self, _namespace):
        print('Hello world')        
        exec(open(cPath+"regCommands.py").read())
        self._initialized = True
        #exec(open("/src/makaronLab/q3/q3/bootstrap/startup.py").read())        

app = q3.App(q3Impl=q3.consts.Q3_IMPL)
frm = q3.EditorFrame(app, title='makaronLab')
q3.config.consoleInstance = frm.console()
c = frm.console()
q3.config.consoleWidgetInstance = frm.consoleWidget()
cw = frm.consoleWidget()
tga = encImpl()
tga._namespace = frm.consoleNamespace()
#self._initialized = True
tg = threading.Thread(target=tga.run)
tg.start()
while (not tga._initialized):
    Timer.sleepMs(0)




#frm.console().registerCommand('execF',execF,True) 

fileName = cPath+"beforeShow.py"
s=c.execF(fileName)
#cw.write(repr(s.getvalue()) + '\n')   
cw.write('\n===bootstrap/beforeShow.py:\n'+s + '\n') 
#why not register execF as Function ?

frm.Show()

#run "afterShow" in separate thread
''' # moved to test 2
class enc2Impl:
    def __init__(self):
        self._namespace = None
        self._initialized = False

    def run(self):
        fileName = cPath+"bootstrap/afterShow.py"
        s=execF(fileName)
        #cw.write(repr(s.getvalue()) + '\n')   
        cw.write('\n===bootstrap/afterShow.py:\n'+s + '\n')
        self._initialized = True


qor = qtc.Qt.Orientation
tgb = enc2Impl()
tgb._namespace = frm.consoleNamespace()
th2 = threading.Thread(target=tgb.run)
th2.start()
# do not wait for this thread as it can be long ...
#while (not tgb._initialized):
#    Timer.sleepMs(0)
# just keeping handle for frame in case of presenting something to user
frm._afterShowThread = th2

'''
fileName = cPath+"afterShow.py"
s=c.execF(fileName)
#cw.write(repr(s.getvalue()) + '\n')   
cw.write('\n===bootstrap/afterShow.py:\n'+s + '\n')
#'''


#timer = qtc.QTimer()
#timer.timeout.connect(lambda: None)
#timer.start(100)
#app.timerr= timer

#globals()['frm0']=frm
#app.setQuitOnLastWindowClosed(False)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

import sys
sys.excepthook = except_hook


app.MainLoop()



