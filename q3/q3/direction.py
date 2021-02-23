
#import wx
from enum import Enum

'''
Direction - top/left/righr/down
'''


#from wx import TOP
#from wx import LEFT
#from wx import RIGHT
#from wx import DOWN

class Dir(Enum):
    LEFT = (1, "LEFT","moduleInputs")
    TOP = (2, "TOP","moduleTops")
    RIGHT = (3, "RIGHT","moduleOutputs")
    DOWN = (4,"DOWN","moduleDowns")
    def __init__(self, num, label,graphModName):
        self._num = num
        self._label = label
        self._graphModName = graphModName
    
    def label(self):
        return self._label

    def oposite(self):
        if LEFT == self:
            return RIGHT
        elif RIGHT == self:
            return LEFT
        elif TOP == self:
            return DOWN
        elif DOWN == self:
            return TOP
        return None

    def graphModName(self):
        return self._graphModName
        


LEFT = Dir.LEFT
TOP = Dir.TOP
RIGHT = Dir.RIGHT
DOWN = Dir.DOWN