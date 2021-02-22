  
  #https://docs.python.org/3/library/enum.html
  
from enum import Enum

import PyQt5.QtGui  as qtg

PEN_NORMAL = qtg.QColor(156, 156, 156, 32)
PEN_AXIS = qtg.QColor(156, 156, 156, 128)
MODULE_COLOR = qtg.QColor(105, 105, 105, 128)

class C(Enum):
      NAMEBACKGROUND=( 95, 124, 136, 255 ) #// Color::eNameBackground
      FONTNAME=( 255, 245, 238, 255 ) #// Color::eFontName
      FONTTYPE=( 169, 169, 169, 255 ) #// Color::eFontType
      NODEHEADER=( 105, 105, 105, 64 ) #// Color::eNodeHeader
      NODECONTENT=( 105, 105, 105, 128 ) #// Color::eNodeContent
      SOCKETBORDER=( 54, 54, 54, 255 ) #// Color::eSocketBorder
      SOCKETINPUT=( 255, 99, 71, 255 ) #// Color::eSocketInput
      SOCKETOUTPUT=( 135, 206, 235, 255 ) #// Color::eSocketOutput
      SOCKETDROP=( 173, 255, 47, 255 ) #// Color::eSocketDrop
      SOCKETHOVER=( 255, 215, 0, 255 ) #// Color::eSocketHover
      BOOLSIGNALOFF=( 244, 53, 64, 255 ) #// Color::eBoolSignalOff
      BOOLSIGNALON=( 75, 173, 88, 255 ) #// Color::eBoolSignalOn
      INTEGERSIGNALOFF=( 62, 84, 174, 255 ) #// Color::eIntegerSignalOff
      INTEGERSIGNALON=( 0, 170, 238, 255 ) #// Color::eIntegerSignalOn
      FLOATSIGNALOFF=( 111, 80, 96, 255 ) #// Color::eFloatSignalOff
      FLOATSIGNALON=( 254, 144, 50, 255 ) #// Color::eFloatSignalOn
      LINK=( 165, 165, 165, 64 ) #// Color::eLink
      SELECTED=( 255, 255, 255, 255 ) #// Color::eSelected
      WORD64SIGNALON=( 0, 170, 238, 255 ) #// Color::eWord64SignalOn
      WORD64SIGNALOFF=( 62, 84, 174, 255 ) #// Color::eWord64SignalOff
      BYTESIGNALON=( 254, 144,  50, 255 ) #//Color::eByteSignalOn
      BYTESIGNALOFF=( 254,  74,  53, 255 ) #//Color::eByteSignalOff

      GRAPH_BACKGROUND=(169, 169, 169, 32)

      def __init__(self, r, g, b, a):
          self._color = qtg.QColor(r,g,b,a)

      def qColor(self):
          return self._color
  #ECOUNT



      
   
    
    
    
    
    
   
    
    
    
    
    
    
     
   
    
    
    
    
    
    

