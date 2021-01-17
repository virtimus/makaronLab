from nmigen import Module

#from .HDElaborative import *

class HDModule(Module):
    def __init__(self):
        super().__init__()
        
    def addComb(self, other):
        self._statements.append(other)
        #p = super()
        #p.__class__ = Module
        #p.d += other    