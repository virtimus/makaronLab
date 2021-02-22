try:
    try:
        from importlib import metadata as importlib_metadata # py3.6+ stdlib
    except ImportError:
        import importlib_metadata # py3.6- 
    __version__ = importlib_metadata.version(__package__)
except ImportError:
    # No importlib_metadata. This shouldn't normally happen, but some people prefer not installing
    # packages via pip at all, instead using PYTHONPATH directly or copying the package files into
    # `lib/pythonX.Y/site-packages`. Although not a recommended way, we still try to support it.
    __version__ = "unknown" # :nocov:

from .consts import *
#from .orientation import *
#from .direction import *
from .MainWindow import *
from .MainWindow import MainWindow as Frame
from .MainWindowTB import MainWindowTB
from .EditorFrame import EditorFrame
from .App import *
from .Object import *
from .Element import * 
from .Panel import * 
from .TabPanel import * 
from .Tab import * 
from .MdiPanel import * 
from .Label import * 
from .Label import Label as StaticText
from .Layout import Layout 
from .Layout import Layout as BoxSizer
from .Menu import Menu
from .MenuBar import MenuBar
from .ModuleFactory import ModuleFactory
from .Timer import Timer


from . import orientation
from . import direction

from .sidePanel.SidePanel import SidePanel



from wx import OK
from wx import ICON_INFORMATION

from wx import EVT_MENU
#from wx import BoxSizer
from wx import SizerFlags
from .MessageBox import MessageBox

__all__ = [
    "App",
    "MainWindow","Frame","MainWindowTB","EditorFrame",
    "Object","Element",
    "Panel","MdiPanel","TabPanel","Tab",
    "Label", "StaticText",
    "BoxSizer","SizerFlags",
    "Menu", "MenuBar",
    "MessageBox",
    "SidePanel",
    "Timer"
]
