from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QStyleOptionGraphicsItem, QGraphicsTextItem,
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PyQt6.QtGui import (QKeyEvent, QMouseEvent, QPainter, QPaintEvent, QPainterPath, QColor, QPen, 
                         QBrush, QTextOption, QCursor)
from PyQt6.QtCore import QRectF, pyqtSignal, Qt
import matplotlib.axes
import matplotlib.axis
import matplotlib.backend_tools
import matplotlib.collections
import matplotlib.container
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Wedge, PathPatch
from matplotlib.collections import Collection
from matplotlib.widgets import Cursor
from matplotlib.artist import Artist
from plot.canvas import Canvas
import matplotlib
from matplotlib.backend_bases import MouseEvent
from ui.base_widgets.spinbox import _Slider
from ui.utils import isDark
from plot.utilis import get_color, find_mpl_object
from ui.base_widgets.menu import Menu, Action

class WidgetItem (QGraphicsItem):
    def __init__(self, widget, parent=None):
        super().__init__(parent)

        self.widget = QGraphicsProxyWidget(self)
        self.widget.setWidget(widget)

        self.width = 100
        self.height = 100
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        pass

    def boundingRect(self) -> QRectF:
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()     
    
class ToolTip (QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.width = 180
        self.height = 30

        self.setColor()
        self.setText()
    
    def setText (self, text=""):
        for obj in self.childItems():
            if isinstance(obj, QGraphicsTextItem):
                obj.deleteLater()
        self.title_item = QGraphicsTextItem(text, parent=self)
        self.title_item.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
        self.title_item.setTextWidth(self.width)
        
    def setColor(self, color=Qt.GlobalColor.lightGray):
                
        self._pen_default = QPen(QColor(color))
        self._pen_default.setWidthF(1.0)

        if isDark():
            self._brush_background = QBrush(QColor("#232323"))
        else:
            self._brush_background = QBrush(Qt.GlobalColor.white)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()     

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
            
        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRect(0, 0, self.width, self.height)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRect(0, 0, self.width, self.height)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen_default)
        painter.drawPath(path_outline.simplified())

    
class GraphicsView (QGraphicsView):
    key_pressed = pyqtSignal(object)
    mouse_released = pyqtSignal(object)
    backtoScene = pyqtSignal()
    backtoHome = pyqtSignal()
    mpl_pressed = pyqtSignal(str)
    def __init__(self, canvas:Canvas,parent=None):
        super().__init__(parent)

        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.LosslessImageRendering | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        self.canvas = canvas
        self.plotview = WidgetItem(canvas)
        self._scene.addItem(self.plotview) 
    
        self.tooltip = ToolTip()
        self._scene.addItem(self.tooltip)
        self.tooltip.hide()

        self.menu = Menu(parent=self)
        self.Menu()

        self.canvas.mpl_connect('motion_notify_event', self.mpl_mouseMove)
        self.canvas.mpl_connect('button_press_event', self.mpl_mousePress)
        #self.canvas.mpl_connect('figure_leave_event', self.mouseLeave)

        self.zoom_slider = _Slider(orientation=Qt.Orientation.Horizontal,step=10)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setStyleSheet("background-color:transparent;")
        self.zoom_item = WidgetItem(self.zoom_slider)
        self._scene.addItem(self.zoom_item)

    def Menu(self, graph_list=list()):
        self.menu.clear()

        nodeview = Action(text="&Node View", parent=self.menu)
        nodeview.triggered.connect(self.backtoScene.emit)
        self.menu.addAction(nodeview)
        home = Action(text="&Home", parent=self.menu)
        home.triggered.connect(self.backtoHome.emit)
        self.menu.addAction(home)

        self.menu.addSeparator()

        graph = Menu(text="&Graph", parent=self.menu)
        self.menu.addMenu(graph)
        _graph_list = [i.title() for i in graph_list]
        for text in ["Manage Graph"] + _graph_list:
            action = Action(text=text, parent=graph)
            action.triggered.connect(lambda checked, text=text: self.mouse_released.emit(text))
            graph.addAction(action)
        
        tick = Menu(text="&Tick", parent=self.menu)
        self.menu.addMenu(tick)
        for text in ["Tick &Bottom", "Tick &Left", "Tick &Top", "Tick &Right"]:
            action = Action(text=text, parent=tick)
            action.triggered.connect(lambda checked, text=text: self.mouse_released.emit(text.replace("&","")))
            tick.addAction(action)

        spine = Menu(text="&Spine", parent=self.menu)
        self.menu.addMenu(spine)
        for text in ["Spine &Bottom", "Spine &Left", "Spine &Top", "Spine &Right"]:
            action = Action(text=text, parent=spine)
            action.triggered.connect(lambda checked, text=text: self.mouse_released.emit(text.replace("&","")))
            spine.addAction(action)
        
        figure = Menu(text="&Figure", parent=self.menu)
        self.menu.addMenu(figure)
        for text in ["Plot Size", "Grid"]:
            action = Action(text=text, parent=figure)
            action.triggered.connect(lambda checked, text=text: self.mouse_released.emit(text))
            figure.addAction(action)

        label = Menu(text="&Label", parent=self.menu)
        self.menu.addMenu(label)
        for text in ["Title", "Axis Label", "Legend", "Data Annotation"]:
            action = Action(text=text, parent=label)
            action.triggered.connect(lambda checked, text=text: self.mouse_released.emit(text))
            label.addAction(action)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.mouse_position = self.mapToScene(event.pos())
        if self.mouse_position.y() > self.viewport().size().height()-40:
            self.zoom_item.setOpacity(1)
        else: self.zoom_item.setOpacity(0.4)

        return super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
    
    def middleMouseButtonPress(self, event):
        super().mousePressEvent(event)
    
    def leftMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
    
    def mpl_mouseMove(self, event:MouseEvent):
        stack = find_mpl_object(figure=self.canvas.fig,
                                match=[Line2D,Collection,Rectangle,Wedge,PathPatch])
        
        x_increment, y_increment = 30, 30
        if self.mouse_position.x() + x_increment + self.tooltip.width < self.width():
            self.tooltip.setX(self.mouse_position.x() + x_increment)
        else: self.tooltip.setX(self.width() - 10 - self.tooltip.width)
        if self.mouse_position.y() + y_increment + self.tooltip.height < self.height():
            self.tooltip.setY(self.mouse_position.y() + y_increment)
        else: self.tooltip.setY(self.height() - 10 - self.tooltip.height)

        #self.canvas.set_cursor(matplotlib.backend_tools.cursors.WAIT)

        # refresh canvas before showing any changes
        self.canvas.draw()

        for obj in reversed(stack): # the object on top will be picked
            _alpha = obj.get_alpha() if obj.get_alpha() else 1
            if obj.contains(event)[0]:
                if not self.tooltip.isVisible():
                    self.tooltip.setText(obj.get_gid().title())
                    self.tooltip.setColor(get_color(obj))
                    # self.canvas.set_cursor(matplotlib.backend_tools.cursors.POINTER)
                    self.tooltip.show()
                obj.set_alpha(_alpha*0.6)
                self.canvas.draw()
                obj.set_alpha(_alpha)
                break
            else: self.tooltip.hide()

    def mpl_mousePress(self, event: MouseEvent):
        stack = find_mpl_object(figure=self.canvas.fig,
                                match=[Artist])
        if event.button == 1 and event.dblclick:
            for obj in stack:
                if obj.contains(event)[0]:
                    self.mpl_pressed.emit(obj.get_gid())
                    break # emit when one and only one object is selected
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)
    
    def leftMouseButtonRelease(self, event:QMouseEvent):
        super().mouseReleaseEvent(event)
    
    def rightMouseButtonRelease(self, event:QMouseEvent):
        self.tooltip.hide()
        pos = self.mapToGlobal(event.pos())
        self.menu.exec(pos)       
        super().mouseReleaseEvent(event)
                
                
    def paintEvent(self, a0: QPaintEvent) -> None:
        super().paintEvent(a0)
        self.resizePlot()
   
    def resizePlot (self):
        ratio = self.zoom_slider.value()/100
        size = self.viewport().size()
        height = size.height()*ratio
        width = size.width()*ratio
        self.canvas.resize(int(width), int(height))
        self.plotview.setPos(size.width()/2-width/2,size.height()/2-height/2)
        self.zoom_item.setPos(20, size.height()-30)
        self.setSceneRect(0,0,size.width(),size.height())
        
      
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.key_pressed.emit(event)
        return super().keyPressEvent(event)
    
    