
import wx

WQ_IMPL_QT="ui.pyqt5"
WQ_IMPL_WX="ui.wx"

#WQ_IMPL="wx"
#default impl
#global WQ_IMPL 
WQ_IMPL=WQ_IMPL_QT

WQ_IMPL_SIM='sim.default'



from wx import ID_EXIT
from wx import ID_ABOUT

MAX_PINS = 256
MAX_INPUTS = 256
MAX_OUTPUTS = 256
MAX_DYNAMICS = 256

MAX_SIGNAL_SIZE = 64
 
