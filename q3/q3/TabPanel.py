
from .Object import Object
from .Panel import Panel


class TabPanel(Panel):
    def __init__(self,  *args, **kwargs):
        super(TabPanel, self).__init__( *args, **kwargs)

    def addTab(self,obj,title):
        return self.q3D().doTabPanel_AddTab(obj, title)
    
    def currentIndex(self):
        return self.q3D().doTabPanel_CurrentIndex()
