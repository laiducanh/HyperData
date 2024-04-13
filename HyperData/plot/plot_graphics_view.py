from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QStyleOptionGraphicsItem, QWidget,
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPainter, QPaintEvent
from PyQt6.QtCore import QRectF, pyqtSignal, Qt
from plot.canvas import Canvas
import matplotlib
from ui.base_widgets.spinbox import _Slider
from node_editor.node_node import Node

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
    
class GraphicsView (QGraphicsView):
    sig_sidebar = pyqtSignal(str) # to call when sidebar needs to be updated
    sig_edit_graphtitle = pyqtSignal()
    sig_edit_xbottom = pyqtSignal()
    sig_edit_xtop = pyqtSignal()
    sig_edit_yleft = pyqtSignal()
    sig_edit_yright = pyqtSignal()
    sig_edit_legendtitle = pyqtSignal()
    sig_edit_legend = pyqtSignal(str) # string is the current plot being edited legend
    sig_keyPressEvent = pyqtSignal(object)
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
    
        self.tooltip = Node(parent=parent)
        self._scene.addItem(self.tooltip)
        self.tooltip.hide()

        self.canvas.mpl_connect('motion_notify_event', self.mouseMove)
        #self.canvas.mpl_connect('button_press_event', self.mouseClick)
        #self.canvas.mpl_connect('figure_leave_event', self.mouseLeave)

        self.zoom_slider = _Slider(orientation=Qt.Orientation.Horizontal,step=10)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setStyleSheet("background-color:transparent;")
        self.zoom_item = WidgetItem(self.zoom_slider)
        self._scene.addItem(self.zoom_item)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.mouse_position = self.mapToScene(event.pos())
        if self.mouse_position.y() > self.viewport().size().height()-40:
            self.zoom_item.setOpacity(1)
        else: self.zoom_item.setOpacity(0.4)

        return super().mouseMoveEvent(event)
               
    def mouseMove(self, event):
        stack = self.canvas.fig.findobj(match=matplotlib.lines.Line2D)        
        self.tooltip.setPos(self.mouse_position.x()+30, self.mouse_position.y()+30)
        for obj in stack:
            if obj._gid != None and obj.contains(event)[0]:
                if not self.tooltip.isVisible():
                    self.tooltip.show()
                break
            else: self.tooltip.hide()
                
                
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
    
    