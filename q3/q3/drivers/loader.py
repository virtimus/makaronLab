
from .ui.pyqt5 import Q3Driver
from .sim.default import Q3Driver

import imp
import sys


def loadQ3Driver(q3Impl):
    namea = q3Impl.split('.')
    folder = namea[0]
    name = namea[1]

    mylib = __import__(folder, globals(), locals(), [], 1)
    return getattr(mylib, name).Q3Driver
    