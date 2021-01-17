import wq

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import sp_math as m
import sp_helpers as h
from SidePanel import SidePanel
from SidePanelLeft import SidePanelLeft

class MainWindow(qtw.QMainWindow):
    def __init__(self,parent):
        super(MainWindow,self).__init__()
        btn_open  = qtw.QPushButton("Open",  self)
        btn_close = qtw.QPushButton("Close", self)

        btn_open.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        btn_close.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

        def central():
            lay = qtw.QHBoxLayout()
            lay.addWidget(btn_open)
            lay.addWidget(btn_close)

            proxy = qtw.QWidget()
            proxy.setLayout(lay)
            self.setCentralWidget(proxy)
        central()

        def testPanel():
            panel_left = SidePanel(self, 
                side=wq.direction.LEFT
                )
            self._testPanel = panel_left
        #testPanel()

        #    // Left panel with simple label in it
        def leftPanel():
        
            panel_left = SidePanel(self, 
                side=wq.direction.LEFT
                )
            panel_left.setOpenEasingCurve(qtc.QEasingCurve.Type.OutElastic);
            panel_left.setCloseEasingCurve(qtc.QEasingCurve.Type.InElastic);
            panel_left.init()

            label = qtw.QLabel("Left")
            label.setAlignment(qtc.Qt.AlignCenter)
            
            panel_left.setWidgetResizable(True)
            panel_left.setWidget(label)
            self._panelLeft = panel_left
        leftPanel()

        #// Right panel with buttons list in it
        def rightPanel():
            panel_right = SidePanel(self,
                side=wq.direction.RIGHT
                )
            panel_right.setOpenEasingCurve(qtc.QEasingCurve.Type.OutExpo)
            panel_right.setCloseEasingCurve(qtc.QEasingCurve.Type.InExpo)
            panel_right.setPanelSize(200)
            panel_right.init()

            lay = qtw.QVBoxLayout()
            label = qtw.QLabel("Right", self)
            label.setAlignment(qtc.Qt.AlignCenter)
            lay.addWidget(label)

            #for(int i = 0; i < 20; ++i)
            for i in range(0,20,1):
                btn = qtw.QPushButton("Button " + str(i), self)
                btn.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
                btn.setMinimumHeight(60)
                lay.addWidget(btn)
            
            proxy = qtw.QWidget(self)
            proxy.setLayout(lay)
            #proxy.setFixedWidth(0)

            panel_right.setWidgetResizable(True)
            panel_right.setWidget(proxy)


            #// Extra behavior (for example) - scrolling by gestures. Notice, that
            #// QScroller binded to `panel_right->viewport()`, not to `panel_right`
            qtw.QScroller.grabGesture(panel_right.viewport(), qtw.QScroller.ScrollerGestureType.LeftMouseButtonGesture)

            scroller = qtw.QScroller.scroller(panel_right.viewport())

            #// Improve buttons pressing. But still not good
            props = scroller.scrollerProperties()
            props.setScrollMetric(qtw.QScrollerProperties.ScrollMetric.MousePressEventDelay, 0)
            scroller.setScrollerProperties(props)
            self._panelRight = panel_right
        rightPanel()

        #// Top panel with text edit widget
        def topPanel():
            panel_top = SidePanel(self,
            side=wq.direction.TOP
            )
            panel_top.setPanelSize(150)
            panel_top.init()

            panel_top.setWidgetResizable(True)
            panel_top.setWidget( qtw.QTextEdit("> Pseudo top terminal", self) )




            #// Nested panel with animated handler
            def topRightPanel():
                panel_top_right = SidePanel(panel_top,
                side=wq.direction.RIGHT
                )

                def getOpenedRect(parent_rect):
                    return h.rect_opened_half_right(panel_top_right.getHandlerSize().width(), parent_rect) #; // Half size from right

                def initialHandlerSize():
                    return qtc.QSize(60, 60)

                def alignedHandlerRect(panel_geom, handler_size, t):
                    if(t > 0.5):
                        t = 0.5
                    rect = qtc.QRect(0, 0, handler_size.width(), m.scale(t, 0, 0.5, panel_top_right.initialHandlerSize().height(), panel_geom.height())) #; // Aligned Top Left
                    rect.moveTopRight(panel_geom.topLeft())
                    return rect

                panel_top_right.getOpenedRect = getOpenedRect
                panel_top_right.initialHandlerSize = initialHandlerSize
                panel_top_right.alignedHandlerRect = alignedHandlerRect

                panel_top_right.setOpenEasingCurve (qtc.QEasingCurve.Type.OutBack)
                panel_top_right.setCloseEasingCurve(qtc.QEasingCurve.Type.InBack)
                panel_top_right.setPanelSize(300)#; // Well ... this is ignored :)
            
                panel_top_right.init()

                panel_top_right.setWidgetResizable(True)
                panel_top_right.setWidget( qtw.QTextEdit("> Pseudo top-right terminal") )
            topRightPanel()
        topPanel()


        #// Bottom panel with two nested panels
        def bottomPanel():
            panel_bottom = SidePanel(self,
            side=wq.direction.DOWN
            )

            panel_bottom.setPanelSize(150)
            panel_bottom.init()

            label = qtw.QLabel("Bottom", self)
            label.setAlignment(qtc.Qt.AlignCenter)

            panel_bottom.setWidgetResizable(True)
            panel_bottom.setWidget(label)

            def bottomLeftPanel():
                panel_bottom_left = SidePanel(panel_bottom,
                wq.direction.LEFT
                )
                panel_bottom_left.init()

                label = qtw.QLabel("Bottom\nleft", self)
                label.setAlignment(qtc.Qt.AlignCenter)

                panel_bottom_left.setWidgetResizable(True)
                panel_bottom_left.setWidget(label)
            bottomLeftPanel()

            def bottomRightPanel():
                panel_bottom_right = SidePanel(panel_bottom,
                wq.direction.RIGHT
                )
                panel_bottom_right.init()

                label = qtw.QLabel("Bottom\nright", self)
                label.setAlignment(qtc.Qt.AlignCenter)

                panel_bottom_right.setWidgetResizable(True)
                panel_bottom_right.setWidget(label)
            bottomRightPanel()
        bottomPanel()        
        
        self.resize(800, 600)


app = wq.App()

# Then a frame.
frm = MainWindow(app)

# Show it.
frm.show()

# Start the event loop.
app.MainLoop()