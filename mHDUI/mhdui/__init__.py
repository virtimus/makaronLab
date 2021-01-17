import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    pass


#from nmigen import *

from .HDModule import HDModule

#hdmodule = HDModule();

__all__ = [
    #"Shape", "unsigned", "signed",
    #"Value", "Const", "C", "Mux", "Cat", "Repl", "Array", "Signal", "ClockSignal", "ResetSignal",
    "HDModule",
    #"ClockDomain",
    #"HDElaborative",
    # "Fragment", "Instance",
    #"Memory",
    #"Record",
    #"DomainRenamer", "ResetInserter", "EnableInserter",
]
