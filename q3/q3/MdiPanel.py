
from . import consts
from . import Panel


#Not used 
class MdiPanel(Panel):
    def __init__(self, *args, **kwargs):
        ''' 
        tImpl = self._loadImpl(*args, **kwargs)
        if (tImpl==None):
            self._mdiPanel = self.q3D().doMdiPanel_Init() 
            kwargs['impl']=self._mdiPanel
            tParent = self._loadParent(*args, **kwargs)
            if (tParent!=None):
                tParent.impl().setCentralWidget(self._mdiPanel)
        '''        
        super(MdiPanel, self).__init__(*args, **kwargs)