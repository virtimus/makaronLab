
from ..Log import Log
log = Log(__name__)

from ..ModuleFactory import *

import q3c

class ModuleImplCPC(ModuleImplBase):
    def __init__(self, **kwargs):
        self._opened = None
        self._prevPins = None
        self._winid = None
        self._machineType = 'atom'
        super(ModuleImplCPC,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC

    def __del__(self):
        log.warn("Hello from del/CPC")
        super(ModuleImplCPC,self).__del__()
    '''
    def __getattr__(self, name):
        return name

    def __setattr__(self, name:str, value):
        print("setting atrrr:"+str(name)+str(value))   
    '''   
    def onMachineTypeChange(self, event=None):
        print (f'[onMachineTypeChange]:{event}')
        self._machineType = event
        pass

    # used by custom property builder to set default/current value of corresponding property 
    def machineType(self):
        return self._machineType

    def echo(self):
        print("Hello World from CPC")

    def init(self,**kwargs) -> dict:
        initParms = {}
        self._init = q3c.cpc_init(initParms)
        cp = self._init['customProperties'] if 'customProperties' in self._init else {}
        domainValues = {
            'cpc6128':'Amstrad CPC',
            'c64':'Commodore 64',
            'atom':'Acorn ATOM'
            }
        cp['machineType']={
            'desc':f'Type of machine to emulate, currently handled:{domainValues}',
            'required':True,
            'default':'atom',
            'domainValues':domainValues,
            'onChange':self.onMachineTypeChange
        }
        self._customProperties=cp
        return self._init

    
    def open(self):
        pass

    def __afterViewCreated__(self, viewImpl=None):
        self.events().moduleDoubleClicked.connect(self.heModuleDoubleClicked)
        self.events().detailWindowResized.connect(self.heDetailWindowResized)
        self.events().callDetailWindowCloseReq.connect(self.syncDetailWindowCloseReq)
        #super().__afterViewCreated__()

    def syncDetailWindowCloseReq(self,*args,**kwargs):
        if self._winid!=None:#TODO:check winId?
            q3c.cpc_insp({
                'winId':self._winid,
                'command':'closeWindow'
                })
            self._winid = None  
            self._opened = None 
        return True 
               

    def _resizeDtWindowContent(self):
        if self._winid!=None:
            q3c.cpc_insp({
                'winId':self._winid,
                'command':'resizeWindow',
                'width':self._dtWidth,
                'height':self._dtHeight
                })

    def heDetailWindowResized(self,event=None):
        ev = event.props('event')
        twidth = ev.size().width()
        theight = ev.size().height()
        #save h/w for initial resize
        self._dtWidth = twidth
        self._dtHeight = theight
        self._resizeDtWindowContent()

    def heModuleDoubleClicked(self, event=None):
        self.mdlv().showDetailWindow(parent=self.mdlv().impl())
        win = self.mdlv().detailWindow()
        self._winid = win.impl().winId()        
        self._counter=0
        #import threading
        #th = threading.Thread(target=self.startInThread)
        #th.start()
        self.consoleWrite(f'Openning Window:{self._winid}')
        if self._opened == None:
            self._opened = q3c.cpc_open({
                'winId':self._winid,
                'machineType':self._machineType
                })
            Timer.sleepMs(200)
            self._resizeDtWindowContent()

        return self._opened


    #def startInThread(self):
    #    if self._opened == None:
    #         self._opened = q3c.cpc_open({'winId':self._winid})


    def calc(self):
        '''
        self._opened['pins'] = q3c.cpc_calc(self._opened['iv'],self._opened['pins'])
        if self._prevPins != self._opened['pins']:
            self.updateSignals(self._opened['pins'])
        self._counter+=1
        if self._counter>1011: 
            self._counter=0
            pins = self._opened['pins']
            print(f'6502DebugPins:{pins}')
        return self._opened['pins']
        '''
