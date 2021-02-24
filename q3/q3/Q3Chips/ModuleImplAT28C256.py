
from ..ModuleFactory import *
#from q3 import Timer
class ModuleImplAT28C256(ModuleImplBase):
    def __init__(self,**kwargs):
        super(ModuleImplAT28C256,self).__init__(**kwargs)
        self._moduleType = ModuleType.ATOMIC 

    def init(self,**kwargs):
        return {}


    def open(self,**kwargs):
        self.newIO(
            name = 'A',
            size = 15,
            ioType = IoType.INPUT
        )
        self.newIO(
            name ='I/O',
            size = 8,
            ioType = IoType.DYNAMIC
        )
        self.newIO(
            name = 'CEB',
            desc = 'Chip enable bar',
            size = 1,
            ioType = IoType.INPUT
        )
        return {}


    def calc(self,**kwargs):
        return {}
