import sys

from q3.ui.engine import qtw,qtc,qtg

from . import consts
from . import Object

class App(Object.Object):
    def __init__(self, *args, **kwargs):
        #self._app = qtw.QApplication(sys.argv) if self.isQt(q3Impl) else wx.App()
        self._app=self._loadImpl(*args, **kwargs) 
        if (self._app==None):
            self._app=self.q3D().doApp_Init()
            kwargs['impl']=self._app 
        super(App,self).__init__(None, self._app)
        #super(App,self).__init__( *args, **kwargs)

    @classmethod
    def fromArgs(argc,argv):
        return App()
    
    def _mainLoop(self):
        result = self._app.exec_() if self.isQt() else self._app.MainLoop()
        return result

    def MainLoop(self):
        return self._mainLoop()

    def exec_(self):
        return self._mainLoop()

       