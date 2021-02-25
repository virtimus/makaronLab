from q3.ui.engine import qtw,qtc,qtg

class STableWidget(qtw.QTableWidget):
    def __init__(self,parent=None):
        super(STableWidget, self).__init__(parent)
        #tw.width=100
        self.horizontalHeader().hide()
        self.horizontalHeader().setSectionResizeMode(qtw.QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.verticalScrollBar().setDisabled(True)
        self.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setDisabled(True)
        self.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.setRowCount(1)
