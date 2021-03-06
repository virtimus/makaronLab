
#########################################################
## customize Title bar
## dotpy.ir
## iraj.jelo@gmail.com
## @ref: https://stackoverflow.com/questions/9377914/how-to-customize-title-bar-and-window-of-desktop-application
#########################################################
import sys
from q3.ui.engine import qtw,qtc,qtg

class MainWindowTB(qtw.QDialog):
    def __init__(self, parent=None):
        qtw.QDialog.__init__(self, parent)
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """
        
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        #self.setStyleSheet(css)
        self.minimize=QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('img/min.png'))
        self.maximize=QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('img/max.png'))
        close=QtWidgets.QToolButton(self)
        close.setIcon(QtGui.QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QtWidgets.QLabel(self)
        label.setText("Window Title")
        self.setWindowTitle("Window Title")
        hbox=QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

        if parent!=None:
            parent.setWindowFlags(Qt.FramelessWindowHint)
            
            parent.setMouseTracking(True)
            parent._titleBar=self;#TitleBar(parent)
            parent._content= QtWidgets.QWidget(parent)
            vbox=QtWidgets.QVBoxLayout(parent)
            vbox.addWidget(parent._titleBar)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(0)
            layout=QtWidgets.QVBoxLayout()
            layout.addWidget(parent._content)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(0)
            vbox.addLayout(layout)    
            self._parent = parent    

    def showSmall(self):
        self._parent.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            self._parent.showNormal()
            self.maxNormal= False
            self.maximize.setIcon(QtGui.QIcon('img/max.png'))
            print('1')
        else:
            self._parent.showMaximized()
            self.maxNormal=  True
            print('2')
            self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

    def close(self):
        self._parent.close()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self._parent.moving = True
            self._parent.offset = event.pos()

    def mouseMoveEvent(self,event):
        if self._parent.moving: self._parent.move(event.globalPos()-boself._parent.offset)

'''
class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        
        css = """
        QFrame{
            Background:  #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        

        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== Qt.LeftButton

    def mouseMoveEvent(self,event):
        x=event.x()
        y=event.y()

    def mouseReleaseEvent(self,event):
        m_mouse_down=False

'''