
from .Object import Object
from .MainWindow import MainWindow
from .Module import Module

from .moduletype import ModuleType

from enum import Enum


from PyQt5.QtGui import QBrush, QColor, QPen

from PyQt5.QtCore import QPointF

class GridDensity(Enum):
    LARGE = 1
    SMALL = 2


class ModuleView(Object):
    def __init__(self, *args, **kwargs):
        self._gridDensity = None
        self._selectedModule = None 
        self._scheduledScalings = None;  
        args = self._loadInitArgs(args)
        d1 = isinstance(args[0],ModuleView)
        d2 = isinstance(args[0],MainWindow)
        #d3 = args[0] != None
        if not (d1 or d2):
            self.raiseExc('[ModuleView] Parent has to be descendant of wq.ModuleView or wq.MainWindow')
        self._module = kwargs['module'] if 'module' in kwargs else None
        if self._module == None:
            self.raiseExc('[ModuleView] keyword argument module required')
        self._module._view = self    
        d3 = isinstance(self._module,Module)
        if (not d3):
            self.raiseExc('[ModuleView] module given has to be descendant or class of Module')
        #args = (args[0], None) 
        self._moduleView = self.wqD().doModuleView_Init()
        args = (args[0],self._moduleView) #impl
        kwargs.pop('module', None)         
        super(ModuleView, self).__init__(*args, **kwargs)
        self.wqD().doModuleView_AfterInit()


    # add-sumodule
    def addModuleView(self,name, type=ModuleType.SIMPLE, module=None):
        if (module == None):
            module = Module(self.module(),name,type=type)
        result = ModuleView(self,module=module)
        return result


    def module(self):
        return self._module

    def isRoot(self):
        return self._module.isRoot()

    def open(self):
        result = self.wqD().doModuleView_Open()
        return result
    
    #@s:PackageView::setSelectedNode
    def setSelectedModule(self, module):
        self._selectedModule = module if module != None else self.module()
        return self._selectedModule

    #@s:PackageView::showProperties()
    def showProperties(self):
        '''
        m_properties->clear();
        m_properties->setColumnCount(2);
        m_properties->setHorizontalHeaderLabels(QString("Name;Value").split(";"));

        m_selectedNode->showProperties();
        m_properties->horizontalHeader()->setStretchLastSection(true);
        '''
        pass



    #@s:PackageView::wheelEvent(QWheelEvent *a_event)
    def wheelEvent(self, event):
        self.wqD().doModuleView_wheelEvent(event)


    #@s:PackageView::updateGrid(qreal const a_scale)
    def updateGrid(self, scale):
        newDensity = GridDensity.LARGE if scale >= 0.85 else GridDensity.SMALL 
        self._gridDensity = newDensity

    #@s:PackageView::drawBackground(QPainter *a_painter, QRectF const &a_rect)
    def drawBackground(self, painter, rect):
        penNormal = QPen(QColor(156, 156, 156, 32))
        penAxis = QPen(QColor(156, 156, 156, 128)) 

        #qreal const LEFT{ a_rect.left() };
        LEFT = rect.left()
        #qreal const RIGHT{ a_rect.right() };
        RIGHT = rect.right()
        #qreal const TOP{ a_rect.top() };
        TOP = rect.top()
        #qreal const BOTTOM{ a_rect.bottom() };
        BOTTOM = rect.bottom()

        #qreal const GRID_DENSITY{ (m_gridDensity == GridDensity::eSmall ? 100.0 : 10.0) };
        GRID_DENSITY = 100.0 if self._gridDensity == GridDensity.SMALL else 10.0

        #qreal const START_X{ std::round(LEFT / GRID_DENSITY) * GRID_DENSITY };
        START_X = round(LEFT / GRID_DENSITY) * GRID_DENSITY
        #qreal const START_Y{ std::round(TOP / GRID_DENSITY) * GRID_DENSITY };
        START_Y = round(TOP / GRID_DENSITY) * GRID_DENSITY

        if self._gridDensity == GridDensity.SMALL:
            penAxis.setWidth(2)
            penNormal.setWidth(2)
        
        
        #for x in range(START_X,RIGHT,GRID_DENSITY):
        x = START_X
        while x<RIGHT:
            PEN = penAxis if (x >= -0.1 and x <= 0.1) else penNormal
            painter.setPen(PEN)
            painter.drawLine(QPointF(x, TOP), QPointF(x, BOTTOM))
            x+=GRID_DENSITY

        #for y in range(START_Y,BOTTOM,GRID_DENSITY):
        y=START_Y
        while y<BOTTOM:
            PEN = penAxis if (y >= -0.1 and y <= 0.1) else penNormal 
            painter.setPen(PEN)
            painter.drawLine(QPointF(LEFT, y), QPointF(RIGHT, y))
            y+=GRID_DENSITY
  

