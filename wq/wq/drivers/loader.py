
from .ui.pyqt5 import WqDriver
from .sim.default import WqDriver

import imp
import sys


def loadWqDriver(wqImpl):
    namea = wqImpl.split('.')
    folder = namea[0]
    name = namea[1]

    mylib = __import__(folder, globals(), locals(), [], 1)
    return getattr(mylib, name).WqDriver
    '''
    try:
        return sys.modules[name]
    except KeyError:
        pass

    fp, pathname, description = imp.find_module(name,['/src/makaronLab/wq/wq/drivers/'+folder])

    try:
        wqImpl =  imp.load_module(name, fp, pathname, description)
        return wqImpl.WqDriver
    finally:
        # Since we may exit via an exception, close fp explicitly.
        if fp:
            fp.close()
    #package = ".drivers.ui.pyqt5"
    #print(f'package:{package}')  
    #name = "WqDriver"
    #WqDriver = getattr(__import__(package, fromlist=[name]), name)
    '''