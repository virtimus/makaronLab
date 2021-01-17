
from .Object import Object
from .Panel import Panel


class TabPanel(Panel):
    def __init__(self,  *args, **kwargs):
        self._tabPanel=self._loadImpl(*args, **kwargs) 
        if (self._tabPanel==None):
            self._tabPanel=self.wqD().doTabPanel_Init()
            kwargs['impl']=self._tabPanel
        super(TabPanel, self).__init__( *args, **kwargs)

    def addTab(self,obj,title):
        result = self.wqD().doTabPanel_AddTab(obj, title)
        return result
    
    def currentIndex(self):
        return self.wqD().doTabPanel_CurrentIndex()
