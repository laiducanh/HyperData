from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QStyleOptionGraphicsItem, QGraphicsTextItem,
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPainter, QPaintEvent, QPainterPath, QColor, QPen, QBrush, QTextOption
from PyQt6.QtCore import QRectF, pyqtSignal, Qt
import matplotlib.artist
import matplotlib.axes
import matplotlib.axis
import matplotlib.backend_tools
import matplotlib.collections
import matplotlib.container
from plot.canvas import Canvas
import matplotlib
from ui.base_widgets.spinbox import _Slider
from ui.utils import isDark
from plot.utilis import get_color
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
    sig_keyPressEvent = pyqtSignal(object)
    sig_MouseRelease = pyqtSignal(object)
    sig_backtoScene = pyqtSignal()
    sig_backtoHome = pyqtSignal()
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

        self.canvas.mpl_connect('motion_notify_event', self.mouseMove)
        #self.canvas.mpl_connect('button_press_event', self.mouseClick)
        #self.canvas.mpl_connect('figure_leave_event', self.mouseLeave)

        self.zoom_slider = _Slider(orientation=Qt.Orientation.Horizontal,step=10)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setStyleSheet("background-color:transparent;")
        self.zoom_item = WidgetItem(self.zoom_slider)
        self._scene.addItem(self.zoom_item)

    def Menu(self, graph_list=list()):
        self.menu.clear()

        nodeview = Action(text="&Node View", parent=self.menu)
        nodeview.triggered.connect(self.sig_backtoScene.emit)
        self.menu.addAction(nodeview)
        home = Action(text="&Home", parent=self.menu)
        home.triggered.connect(self.sig_backtoHome.emit)
        self.menu.addAction(home)

        self.menu.addSeparator()

        graph = Menu(text="&Graph", parent=self.menu)
        self.menu.addMenu(graph)
        _graph_list = [i.title() for i in graph_list]
        for text in ["Manage Graph"] + _graph_list:
            action = Action(text=text, parent=graph)
            action.triggered.connect(lambda checked, text=text: self.sig_MouseRelease.emit(text))
            graph.addAction(action)
        
        tick = Menu(text="&Tick", parent=self.menu)
        self.menu.addMenu(tick)
        for text in ["Tick &Bottom", "Tick &Left", "Tick &Top", "Tick &Right"]:
            action = Action(text=text, parent=tick)
            action.triggered.connect(lambda checked, text=text: self.sig_MouseRelease.emit(text.replace("&","")))
            tick.addAction(action)

        spine = Menu(text="&Spine", parent=self.menu)
        self.menu.addMenu(spine)
        for text in ["Spine &Bottom", "Spine &Left", "Spine &Top", "Spine &Right"]:
            action = Action(text=text, parent=spine)
            action.triggered.connect(lambda checked, text=text: self.sig_MouseRelease.emit(text.replace("&","")))
            spine.addAction(action)
        
        figure = Menu(text="&Figure", parent=self.menu)
        self.menu.addMenu(figure)
        for text in ["Plot Size", "Grid"]:
            action = Action(text=text, parent=figure)
            action.triggered.connect(lambda checked, text=text: self.sig_MouseRelease.emit(text))
            figure.addAction(action)

        label = Menu(text="&Label", parent=self.menu)
        self.menu.addMenu(label)
        for text in ["Title", "Axis Label", "Legend", "Data Annotation"]:
            action = Action(text=text, parent=label)
            action.triggered.connect(lambda checked, text=text: self.sig_MouseRelease.emit(text))
            label.addAction(action)
    
    def find_graph_object(self) -> list:
        fig = self.canvas.fig
        lines = fig.findobj(match=matplotlib.lines.Line2D)
        collections = fig.findobj(match=matplotlib.collections.Collection)
        container = fig.findobj(match=matplotlib.patches.Rectangle)

        return lines+collections+container

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.mouse_position = self.mapToScene(event.pos())
        if self.mouse_position.y() > self.viewport().size().height()-40:
            self.zoom_item.setOpacity(1)
        else: self.zoom_item.setOpacity(0.4)

        return super().mouseMoveEvent(event)
               
    def mouseMove(self, event):
        stack = self.find_graph_object()  
        
        x_increment, y_increment = 30, 30
        if self.mouse_position.x() + x_increment + self.tooltip.width < self.width():
            self.tooltip.setX(self.mouse_position.x() + x_increment)
        else: self.tooltip.setX(self.width() - 10 - self.tooltip.width)
        if self.mouse_position.y() + y_increment + self.tooltip.height < self.height():
            self.tooltip.setY(self.mouse_position.y() + y_increment)
        else: self.tooltip.setY(self.height() - 10 - self.tooltip.height)
        
        for obj in stack:
            if obj._gid != None and obj.contains(event)[0]:
                if not self.tooltip.isVisible():
                    self.tooltip.setText(obj._gid.title())
                    self.tooltip.setColor(get_color(obj))
                    self.tooltip.show()
                break
            else: self.tooltip.hide()
    
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
        self.sig_keyPressEvent.emit(event)
        return super().keyPressEvent(event)
    
    