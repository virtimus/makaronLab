

#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMessageBox
#from PyQt5.QtCore import *
import wx

from . import consts
from . import Object
from . import Label
from . import Element


class MessageBox(Element.Element):
    def __init__(self, text, object=None, wqImpl=consts.Q3_IMPL):
        super(MessageBox, self).__init__(None, object, wqImpl=wqImpl)
        if self.isQt(wqImpl):
            reply = QMessageBox.information(None,'Info',text, QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)
            '''if reply == QMessageBox.Ok:
                self.la.setText('You have chosen Ok! ')
            else:
                self.la.setText('You chose Close! ')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText(text)
            msg.setInformativeText("This is additional information")
            msg.setWindowTitle("MessageBox demo")
            msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.msgbtn)

            retval = msg.exec_()
            print("value of pressed message box button:", retval)
            '''
        else:
            wx.MessageBox(text)

    def msgbtn(i):
        print( "Button pressed is:",i.text()) 