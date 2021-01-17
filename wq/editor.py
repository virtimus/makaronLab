#!/usr/bin/env python
"""
#@ref: https://www.wxpython.org/pages/overview/#hello-world
Hello World, but with more meat.
"""


#from PyQt5.QtCore import Qt 
#from PyQt5.QtGui import QIcon, QPalette, QColor
#from PyQt5.QtWidgets import QProgressBar, QLabel


#wqc.WQ_IMPL = "qt"

import wq

#import wq.consts as wqc
#import wx

#WQ_IMPL=wq.consts.WQ_IMPL_WX

#wq.c.setWqImpl(WQ_IMPL)





if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wq.App(wqImpl=wq.consts.WQ_IMPL)
    frm = wq.EditorFrame(None, title='makaronLab',wqImpl=wq.consts.WQ_IMPL)
    frm.Show()
    

    app.MainLoop()
    



'''
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"));

    darkPalette=QPalette()
    c1 = QColor(55, 55, 55);
    c2 = QColor(25, 25, 25);
    c3 = QColor(45, 130, 220);
    darkPalette.setColor(QPalette.Window, c1);
    darkPalette.setColor(QPalette.WindowText, Qt.white);
    darkPalette.setColor(QPalette.Base, c2);
    darkPalette.setColor(QPalette.AlternateBase, c1);
    darkPalette.setColor(QPalette.ToolTipBase, Qt.white);
    darkPalette.setColor(QPalette.ToolTipText, Qt.white);
    darkPalette.setColor(QPalette.Text, Qt.white);
    darkPalette.setColor(QPalette.Button, c1);
    darkPalette.setColor(QPalette.ButtonText, Qt.white);
    darkPalette.setColor(QPalette.BrightText, Qt.red);
    darkPalette.setColor(QPalette.Link, c3);
    darkPalette.setColor(QPalette.Highlight, c3);
    darkPalette.setColor(QPalette.HighlightedText, Qt.white);
    app.setPalette(darkPalette);
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }");

    box = Frame()
    box.move(60,60)
    l=QtWidgets.QVBoxLayout(box.contentWidget())
    l.setContentsMargins(0, 0, 0, 0)
    edit=QtWidgets.QLabel("""I would've did anything for you to show you how much I adored you
But it's over now, it's too late to save our loveJust promise me you'll think of me
Every time you look up in the sky and see a star 'cuz I'm  your star.""")
    l.addWidget(edit)
    box.show()
    app.exec_()
    '''