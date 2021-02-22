import q3


import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.QtCore import Qt, QFileSystemWatcher, QSettings, pyqtSignal as EventSignal

from q3.sidePanel.SidePanelState import SidePanelState

import q3.sidePanel.sp_math as m
import q3.sidePanel.sp_helpers as h

#header assignments
HandlerWidgetT = qtw.QPushButton
base_t = qtw.QScrollArea



class SidePanel(qtw.QScrollArea):
    stateChanged = EventSignal(SidePanelState)

    #def parentWidget(self):
    #    return self._parentWidget

    def anim_func(self, t):
        #const QRect parent_rect = this->parentWidget()->rect();
        parent_rect = self.parentWidget().rect()

        geom_start = self.getClosedRect(parent_rect)
        geom_end = self.getOpenedRect(parent_rect)

        new_geom = m.lerp(t, geom_start, geom_end).toRect()
        self.setGeometry( new_geom )

        self.updateHandlerRect(self._anim_progress, new_geom)

        #qDebug() << new_geom << t;

    def timeoutFunc(self):
        #const auto time_now = std::chrono::system_clock::now();
        time_now = m.time()
        if((time_now - self._time_start) >= self._duration):
            self._timer.stop()

            #// This setGeometry() for cases when duration=200ms, interval_time=100ms;
            if self._state == SidePanelState.Opening:
                geom = self.getOpenedRect(self.parentWidget().rect())
                self.setGeometry( geom )
                self._anim_progress = 1.0
                self.updateHandlerRect(self._anim_progress, geom)
            if self._state == SidePanelState.Closing:
                geom = self.getClosedRect(self.parentWidget().rect())
                self.setGeometry( geom )
                self._anim_progress = 0.0
                self.updateHandlerRect(self._anim_progress, geom)

            if self._state == SidePanelState.Opening:
                self.show()
                self._setState(SidePanelState.Opened)
            if self._state == SidePanelState.Closing:
                self.hide()
                self._setState(SidePanelState.Closed)

            return 

        time_end = (self._time_start + self._duration)

        #// [t_start .. t_now .. t_end] -> [0.0 .. t .. 1.0]
        t = m.scale(
            #time_now.time_since_epoch().count(),
            m.timeSinceEpoch(time_now),
            #self._time_start.time_since_epoch().count(),
            m.timeSinceEpoch(self._time_start),
            #time_end.time_since_epoch().count(),
            m.timeSinceEpoch(time_end),
            0.0, 1.0)

        if(self._state == SidePanelState.Closing): # // On closing - reverse it
            t = (1.0 - t)

        self._anim_progress = t

        #// Pass normalized value through easing functions
        if(self._state == SidePanelState.Opening):
            t = self.curve_on_open.valueForProgress(t)
        elif(self._state == SidePanelState.Closing):
            t = self.curve_on_close.valueForProgress(t)
        self.anim_func(t)

    #[this](const QRect& parent_rect) -> QRect
    def getOpenedRect(self,parent_rect):
        if (self._side == q3.direction.LEFT):
            return h.rect_opened_left(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.RIGHT):
            return h.rect_opened_right(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.TOP):    
            return h.rect_opened_top(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.DOWN):    
            return h.rect_opened_bottom(self.getPanelSize(), parent_rect)
        else:
            return h.rect_opened_left(self.getPanelSize(), parent_rect)

    def getClosedRect(self,parent_rect):
        if (self._side == q3.direction.LEFT):
            return h.rect_closed_left(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.RIGHT):
            return h.rect_closed_right(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.TOP):    
            return h.rect_closed_top(self.getPanelSize(), parent_rect)
        elif (self._side == q3.direction.DOWN):   
            return h.rect_closed_bottom(self.getPanelSize(), parent_rect)
        else:
            return h.rect_closed_left(self.getPanelSize(), parent_rect)

    def alignedHandlerRect(self,panel_geom, handler_size, progress=None):
        if (self._side == q3.direction.LEFT):
            return h.rect_aligned_right_center(panel_geom, handler_size)
        elif (self._side == q3.direction.RIGHT):
            return h.rect_aligned_left_center(panel_geom, handler_size)
        elif (self._side == q3.direction.TOP):
            return h.rect_aligned_bottom_center(panel_geom, handler_size)
        elif (self._side == q3.direction.DOWN):
            return h.rect_aligned_top_center(panel_geom, handler_size)
        else:
            return h.rect_aligned_right_center(panel_geom, handler_size)

    def initialHandlerSize(self):
        if (self._side == q3.direction.LEFT or self._side == q3.direction.RIGHT):
            return qtc.QSize(25, 240)
        if (self._side == q3.direction.TOP or self._side == q3.direction.DOWN):
            return qtc.QSize(240, 25)
        else:
            return self._handler.size()

    def updateHandler(self,state, handler):
        if (state == SidePanelState.Opening):
            handler.setText("...")
        elif (state == SidePanelState.Opened):
            handler.setText("C")
        elif (state == SidePanelState.Closing):
            handler.setText("...") 
        elif (state == SidePanelState.Closed):  
            handler.setText("O")

    def onInit(self):
        self._handler.resize( self.initialHandlerSize() )
        self.updateHandler(self._state, self._handler)
    
    def onClicked(self):
        if (self._emitedOpen or self._emitedClose):
            if (self._fixedState != None):
                self.__clearEmited()
                return
        else:
            self._fixedState = None
        if(self._timer.isActive()):
            if self._state == SidePanelState.Opening:
                self._setState(SidePanelState.Closing)        
            elif self._state == SidePanelState.Closing:
                self._setState(SidePanelState.Opening)
        else:
            if self._state == SidePanelState.Closed:
                self.show()
                self._setState(SidePanelState.Opening)
                #self._fixedState = None if self._emitedOpen else SidePanelState.Opened 
                self._fixedState = SidePanelState.Opened 
            elif self._state == SidePanelState.Opened:
                self.show()
                self._setState(SidePanelState.Closing)
                #self._fixedState = None if self._emitedClose else SidePanelState.Closed 
            self._time_start = m.time() 
            self._timer.start()
        self.__clearEmited()

    def __clearEmited(self):
        self._emitedOpen = False
        self._emitedClose = False

    def __init__(self,parent:qtw.QWidget,side=q3.direction.LEFT):
        #super(SidePanel,self).__init__(parent)
        self._side = side
        self._parentWidget = parent
        self._fixedState = None
        #SidePanelState _state = SidePanelState::Closed;
        self._state = SidePanelState.Closed
        #std::chrono::milliseconds _duration {1000};
        self._duration = 0.001000
        #std::chrono::system_clock::time_point _time_start;
        self._time_start = None
        #QEasingCurve curve_on_open  = {QEasingCurve::Type::OutBounce};
        self.curve_on_open  = qtc.QEasingCurve(qtc.QEasingCurve.Type.OutBounce)
        self.curve_on_close = qtc.QEasingCurve(qtc.QEasingCurve.Type.InBounce)
        #QTimer* _timer = nullptr;
        self._timer = None
        #HandlerWidgetT* _handler = nullptr;
        self._handler = None
        #qreal _anim_progress = 0.0;
        self._anim_progress = 0.0
        #int _panel_size = 100; // px
        self._panel_size = 100 #// px


        #// =========================================================================
        #// Callbacks for behaviour customization

        #using rect_func_t = std::function<QRect(const QRect& /*parent_rect*/)>;

        #rect_func_t getOpenedRect;

        #rect_func_t getClosedRect;

        #// -------------------------------------------------------------------------

        #using handler_align_func_t = std::function<QRect(const QRect& /*panel_geom*/, const QSize& /*handler_size*/, qreal /*progress*/)>;

        #handler_align_func_t alignedHandlerRect;

        #// -------------------------------------------------------------------------

        #using handler_size_func_t = std::function<QSize()>;

        #handler_size_func_t initialHandlerSize;

        #// -------------------------------------------------------------------------

        #using handler_update_func_t = std::function<void(const SidePanelState, HandlerWidgetT*)>;

        #handler_update_func_t updateHandler;

        #// =========================================================================


  

        self._handler = qtw.QPushButton(parent)
        self._handler.setObjectName("SidePanel_handler")

        self._handler.enterEvent = self.handlerEnterEvent
        self._handler.leaveEvent = self.handlerLeaveEvent


        super(SidePanel,self).__init__(parent)

        self._timer = qtc.QTimer(self)
        self._timer.setInterval(10)

        #connect(_timer, &QTimer::timeout, this, [this, anim_func]
        self._timer.timeout.connect(self.timeoutFunc)
        self.hide()
        
        #// =========================================================================
        #// Default behaviour basically the same as PanelLeftSide

        #super(SidePanel,self).__init__(parent)

    #def __del__(self):
        '''
        if(self._timer != None):
            self._timer.stop()
            #delete _timer
            self._timer = None

        if(self._handler != None):
            #delete _handler
            self._handler = None

        if(self.parentWidget()):
            self.removeEventFilter(self)
        '''
        #super(SidePanel,self).__del__()

    def onStateChanged(self, state):
        self.updateHandler(state, self._handler)
        self._emitedOpen = False
        self._emitedClose = False

    def onInit2(self):
        geom = self.getClosedRect(self.parentWidget().rect())
        self.setGeometry( geom )
        self._anim_progress = 0.0
        self.updateHandlerRect(self._anim_progress, geom)


    def init(self):
        #timer = qtc.QTimer(self)
        #timer.setInterval(1)
        #timer.setSingleShot(True)
        #timer.timeout.connect(self.onInit)
        qtc.QTimer.singleShot(0,self.onInit)

        self._handler.clicked.connect(self.onClicked)  

        self.stateChanged.connect(self.onStateChanged)  
        self.parentWidget().installEventFilter(self)
        #//    this->hide();
        #timer = qtc.QTimer(self)
        #timer.setInterval(1)
        #timer.setSingleShot(True)
        #timer.timeout.connect(self.onInit2)
        qtc.QTimer.singleShot(0,self.onInit2)

    def openPanel(self):
        self._timer.stop() #// Stop animation, if it's running
        self.show()
        new_geom = self.getOpenedRect(self.parentWidget().rect())
        self.setGeometry( new_geom )
        self._anim_progress = 1.0
        self.updateHandlerRect(self._anim_progress, new_geom)
        self._setState(SidePanelState.Opened)

    def closePanel(self):
        self._timer.stop() #// Stop animation, if it's running
        self.hide()
        new_geom = self.getClosedRect(self.parentWidget().rect())
        self.setGeometry( new_geom )
        self._anim_progress = 0.0
        self.updateHandlerRect(self._anim_progress, new_geom)
        self._setState(SidePanelState.Closed)

    def setDuration(self,duration):
        self._duration = duration
    
    def getDuration(self): 
        return self._duration


    def setPanelSize(self, size):
        self._panel_size = size
    
    def getPanelSize(self): 
        return self._panel_size

    def setOpenEasingCurve(self, curve):
        if isinstance(curve,qtc.QEasingCurve):
            self.curve_on_open = curve
        else:
            self.curve_on_open = qtc.QEasingCurve(curve)

    def setCloseEasingCurve(self, curve):
        if isinstance(curve,qtc.QEasingCurve):
            self.curve_on_close = curve
        else:
            self.curve_on_close = qtc.QEasingCurve(curve)

    def getHandlerSize(self):
        return self._handler.size()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateHandlerRect(self._anim_progress, self.geometry())

    def _setState(self, new_state):
        if(self._state == new_state):
            return
        self._state = new_state
        #emit stateChanged(_state);
        self.stateChanged.emit(self._state)

    def eventFilter(self, watched, event):
        #// Important note: DONT RETURN TRUE here, on event receive, because it's
        #// blocks events handling, if few panels binded to the same parent widget

        if(event.type() == qtc.QEvent.Resize):
            if (self._state == SidePanelState.Opened):
                geom = self.getOpenedRect(self.parentWidget().rect())
                self.setGeometry( geom ) 
                self.updateHandlerRect(self._anim_progress, geom)
            elif (self._state == SidePanelState.Closed): 
                geom = self.getClosedRect(self.parentWidget().rect()) 
                self.setGeometry( geom ) 
                self.updateHandlerRect(self._anim_progress, geom)
            else:
                geom = self.getClosedRect(self.parentWidget().rect())
        elif(event.type() == qtc.QEvent.Move):
            if (self._state == SidePanelState.Opened):
                geom = self.getOpenedRect(self.parentWidget().rect())
                self.setGeometry( geom )
                self.updateHandlerRect(self._anim_progress, geom)
            elif (self._state == SidePanelState.Closed):
                geom = self.getClosedRect(self.parentWidget().rect())
                self.setGeometry( geom )
                self.updateHandlerRect(self._anim_progress, geom)

        return super().eventFilter(watched, event)

    def handlerEnterEvent(self, event): #QEvent *
        if (self._state == SidePanelState.Closed):
            self._emitedOpen = True
            self._handler.clicked.emit()           
        super().enterEvent(event)
        
    def handlerLeaveEvent(self, event):
        if (self._state == SidePanelState.Opened):
            self._emitedClose = True
            self._handler.clicked.emit()           
        super().leaveEvent(event)



    def updateHandlerRect(self, progress, geom):
        handle_geom = self.alignedHandlerRect( geom, self._handler.size() , progress)
        self._handler.setGeometry( handle_geom )