
from PyQt5.QtWidgets import QTreeWidget

class QHDTreeWidget(QTreeWidget):
    def __init__(self,parent):
        super(QHDTreeWidget, self).__init__(parent)
        self._widgets = ['dupa']
        
    def removeItem(self, iIndex):
        #self._widgets.removeAt(iIndex)
        del self._widgets[iIndex]
    