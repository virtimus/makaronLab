
from .Panel import Panel

class Tab(Panel):
    def __init__(self,  *args, **kwargs):
        '''
        self._tab=self._loadImpl(*args, **kwargs) 
        if (self._tab==None):
            self._tab=self.wqD().doTab_Init()
            kwargs['impl']=self._tab
        '''    
        super(Tab, self).__init__( *args, **kwargs)