
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
    LEFT = (1, "LEFT")
    TOP = (2, "TOP")
    RIGHT = (3, "RIGHT")
    DOWN = (4,"DOWN")
    def __init__(self, num, label):
        self._num = num
        self._label = label
    
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
        


LEFT = Dir.LEFT
TOP = Dir.TOP
RIGHT = Dir.RIGHT
DOWN = Dir.DOWN