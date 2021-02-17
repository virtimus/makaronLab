
# PYQT

import sys
#from ...TabPanel import TabPanel

import sip 


import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui  as qtg
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt, QPoint, QTimeLine
from PyQt5.QtGui import QBrush, QColor, QIcon, QPainter, QPalette, QPen
from PyQt5.QtWidgets import (QAction, QApplication, QGraphicsItem,
                             QGraphicsScene, QGraphicsView, qApp)

from ... import consts, prop, orientation, direction, colors
from ...moduletype import ModuleType
from ...nodeiotype import NodeIoType
from ...wqvector import WqVector
from ...EventSignal import EventProps

from ..driverBase import WqDriverBase


from enum import Enum


from ...valuetype import ValueType

from .IoLinkView import IoLinkView
from .IoNodeView import IoNodeView

from .ModuleViewImpl import ModuleViewImpl
from .GraphViewImpl import GraphViewImpl

#class IoNode:
#    pass 


class Q3Scene(qtw.QGraphicsScene):
    def __init__(self,*args, **kwargs):
        super(Q3Scene,self).__init__(*args, **kwargs)

    def contextMenuEvent(self, event):
        # Check it item exists on event position
        item = self.itemAt(event.scenePos(),qtg.QTransform()) #.toPoint(),qtg.QTransform.TxNone)
        if item:
            # Try run items context if it has one
            try:
                item.contextMenuEvent(event)
                return
            except:
                pass

        menu = qtw.QMenu()
        action = menu.addAction('ACTION')

class DetailWindowBaseImpl(qtw.QWidget):
    def __init__(self,parent):
        self._parent=parent
        super(qtw.QWidget, self).__init__()


    def resizeEvent(self, event):
        self._parent.parent().events().detailWindowResized.emit(EventProps({'event':event}))
        #print(f'WinResizeEV{dir(event)}')

    #windowDidResize
class WqDriver(WqDriverBase):

    def doModuleView_Init(self):
        if self.s().isRoot():#@s:PackageView::PackageView
            #sc = qtw.QGraphicsScene(self.pimpl()) 
            sc = Q3Scene(self.pimpl())           
            #result = qtw.QGraphicsView(sc,self.pimpl())
            package = self.s().module().impl() 
            result = GraphViewImpl(sc,self.pimpl(),self.p(), package) #'''EditorFrame'''
            result._self = self.s()
            result._scene = sc
            '''
            wheelEvent = getattr(self.s(), "wheelEvent", None)
            if callable(wheelEvent):
                result.wheelEvent = wheelEvent
            drawBackground = getattr(self.s(), "drawBackground", None)
            if callable(drawBackground):
                result.drawBackground = drawBackground 
            '''               
        else:  
            if isinstance(self.pimpl(), QGraphicsView): #//MODULES FIRST LEVEL
                result = ModuleViewImpl(None)
                result._self = self.s()
                self.pimpl()._scene.addItem(result)
                el = self.s().module().impl()
                result.setElement(el)
            else:
                result = ModuleViewImpl(self.pimpl()) # next levels
                result._self = self.s()
                
        result._self = self.s()
        return result; 

    def doModuleView_AfterInit(self):
        tImpl = self.impl()
        #tImpl._self = self.s()
        #tImpl._element = self.s().module().impl()
        tImpl.setElement(self.s().module().impl())
        if self.s().isRoot():#@s:PackageView::PackageView
            #self.s()._inputsView  = self.s().addModuleView('moduleInputs', type=ModuleType.INPUTS)
            #self.s()._outputsView = self.s().addModuleView('moduleOutputs', type=ModuleType.OUTPUTS)
            #vec2d m_inputsPosition{ -400.0, 0.0 };
            self.s()._inputsView.setProp(prop.PositionX,-400.0)
            self.s()._inputsView.setProp(prop.PositionY,0.0)
            self.s()._outputsView.setProp(prop.PositionX,400.0)
            self.s()._outputsView.setProp(prop.PositionY,0.0)

        else: #Node::Node
            tImpl._nameFont.setFamily("Consolas")
            tImpl._nameFont.setPointSize(8)

            tImpl.setFlags(qtw.QGraphicsItem.ItemIsMovable | qtw.QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

            tImpl.collapse()
            tImpl.setGraphView(self.pimpl())
            pass #nop
        self.callAfterInit(tImpl)

        #if iscallable(tImpl)

       

          

       





    def doApp_Init(self):
        result = qtw.QApplication(sys.argv) 
        app = result
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
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2b8bdb; border: 1px solid white; }");

        '''
        palette = app.palette()
        palette.setColor(QPalette.Window, QColor(239, 240, 241))
        palette.setColor(QPalette.WindowText, QColor(49, 54, 59))
        palette.setColor(QPalette.Base, QColor(252, 252, 252))
        palette.setColor(QPalette.AlternateBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipText, QColor(49, 54, 59))
        palette.setColor(QPalette.Text, QColor(49, 54, 59))
        palette.setColor(QPalette.Button, QColor(239, 240, 241))
        palette.setColor(QPalette.ButtonText, QColor(49, 54, 59))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(41, 128, 185))
        # palette.setColor(QPalette.Highlight, QColor(126, 71, 130))
        # palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Light, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Shadow, QColor(234, 234, 234))
        app.setPalette(palette)
        '''


        return result

    def doMainWindow_Init(self):
        result = qtw.QMainWindow() 
        if 'title' in self._self._kwargs:
            result.setWindowTitle(self._self._kwargs['title'])

        #result = qtw.QFrame()
        result.resize(1200, 980)
        '''
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
        result.setSizePolicy(sizePolicy)
        '''
        showEvent = getattr(self._self, "showEvent", None)
        if callable(showEvent):
            result.showEvent = showEvent
        return result

    def doMainWindow_Show(self):
        result = self.impl().show()  
        return result 


    def doMenu_Init(self):        
        if self._impl == None:    
            self._self._qtMenu = qtw.QMenu(self._parent.implObject())
            self.s()._menu = self._self._qtMenu
            pass
        else:
            self.s()._menu = self._impl
        return self._self._menu         

    def doMenu_AddSeparator(self):
        result = self._self.implObject().addSeparator() 
        return result

    def doMenu_addAction(self, label,id,helpStr,onClick):
        if (label == None and consts.ID_EXIT == id):
            exitAct = QAction(QIcon('exit.png'), '&Exit', self._self.implObject())
            exitAct.setShortcut('Ctrl+Q')
            exitAct.setStatusTip('Exit application')
            exitAct.triggered.connect(qApp.quit)
            result = self._self.implObject().addAction(exitAct)
        else:
            result = self._self.implObject().addAction(label, onClick)
            if onClick != None:
                result.triggered.connect(onClick)
            #!TODO!result.onClick = onClick
        return result 

    def doMenuBar_Init(self):
        return self.pimpl().menuBar()


    def doMenuBar_AddMenu(self,menuTitle):
        return  self.impl().addMenu(menuTitle)
        '''
        else:           
            result = Menu(self._parent)
            self._wxMenuBar.Append(result.implObject(),menuTitle)
            return result  
            '''

    def doMdiPanel_Init(self):      
        result = qtw.QMdiArea(self._parent.impl())
        return result

    def doTabPanel_Init(self):      
        result = qtw.QTabWidget(self._parent.impl())
        '''
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(result.sizePolicy().hasHeightForWidth())
        result.setSizePolicy(sizePolicy)
        '''
        #result.setMinimumSize(QtCore.QSize(2080, 1630))
        result.setTabsClosable(True)
        return result

    def doTabPanel_AddTab(self, obj, title):
        return self.impl().addTab(obj.impl(),title)

    def doTabPanel_CurrentIndex(self):
        return self.impl().currentIndex()
    
    def doTab_Init(self):      
        result = qtw.QWidget()
        self._parent.impl().addTab(result,"test")
        return result

    def doLayout_Init(self):
        orient = self.s()._kwargs['orient'] if 'orient' in self.s()._kwargs else None
        result = qtw.QVBoxLayout() if orient == orientation.VERTICAL else qtw.QHBoxLayout()
        return result
        '''
        if ( wqImpl == None ):
            wqImpl = parent._wqImpl
        if self.isQt(wqImpl):
            if (orientation.VERTICAL == l):
                self._layout = qtw.QVBoxLayout()
                pass
            else:
                self._layout = qtw.QHBoxLayout()
                pass
        else: 
            self._layout = wx.BoxSizer(l)
            parent.implObject().SetSizer(self._layout) 
        '''

    def doLayout_AddElement(self, element):
        result = self.impl().addWidget(element.impl()) 
        return result 

    def doLayout_Add(self,label, sizerFlags):
        result = self.impl().addWidget(label.inpl())  
        return result       
        
    def doElement_Init(self):
        result = qtw.QWidget(self.pimpl())
        return result

    def doElement_Resize(self,w,h):
        result = self.impl().resize(w,h)
        return result

    def doElement_SizePolicy(self):
        result = self.impl().sizePolicy()
        return result

    def doElement_SetSizePolicy(self, sizePolicy):
        result = self.impl().setSizePolicy(sizePolicy)
        return result
         
    def doPanel_Init(self):
        result = qtw.QFrame(self.pimpl())
        return result

    def doLabel_Init(self):
        result = qtw.QLabel(self.pimpl())
        if 'label' in self.s()._kwargs:
            result.setText(self.s()._kwargs['label'])
        return result

    def doLabel_GetFont(self):
        result = self.impl.font()
        return result

    def doLabel_SetFont(self, font):
        result = self.impl().setFont(font)
        return result 
        

    def doDetailWindow_Init(self):
        result = DetailWindowBaseImpl(self.s())
        result._self = self.s()
        return result

    def doDetailWindow_Show(self):
        result = self.impl().show()  
        return result



