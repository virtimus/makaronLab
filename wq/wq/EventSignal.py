

from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, pyqtSignal as EventSignalBase
import PyQt5.QtWidgets as qtw

EventSignal = EventSignalBase

EventBase = qtw.QGraphicsObject

class EventProps:
    def __init__(self, props={}):
        self._props = props
    
    def props(self, name:str=None):
        result = self._props[name] if name != None and name in self._props else self._props
        return result