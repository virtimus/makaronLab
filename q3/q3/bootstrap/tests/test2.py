from q3.api import *

import threading

cPath='/src/makaronLab/q3/q3/'

class enc2Impl:
    def __init__(self):
        self._namespace = None
        self._initialized = False

    def run(self):#thos also works - infinite mirror ...
        fileName = cPath+"bootstrap/tests/ben6502/video3.py"
        s=execF(fileName)
        #cw.write(repr(s.getvalue()) + '\n')   
        cw.write('\n===bootstrap/afterShow.py:\n'+s + '\n')
        self._initialized = True

    def makeTest(self):
        modv = self._modv
        m = modv.module()

        nI0 = m.ioAdd(ioType = IoType.INPUT)
        nO0 = m.ioAdd(ioType = IoType.OUTPUT)
        nI0.connect(nO0)






modv = modvAdd('Test2 - run in background')


tgb = enc2Impl()
tgb._modv = modv
#tgb._namespace = frm.consoleNamespace()
th2 = threading.Thread(target=tgb.run)
th2.start()
# do not wait for this thread as it can be long ...
#while (not tgb._initialized):
#    Timer.sleepMs(0)
# just keeping handle for frame in case of presenting something to user
#frm._afterShowThread = th2