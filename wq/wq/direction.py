
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

LEFT = Dir.LEFT
TOP = Dir.TOP
RIGHT = Dir.RIGHT
DOWN = Dir.DOWN