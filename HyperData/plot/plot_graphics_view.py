from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QStyleOptionGraphicsItem, QGraphicsTextItem,
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PySide6.QtGui import (QKeyEvent, QMouseEvent, QPainter, QPaintEvent, QPainterPath, QColor, QPen, 
                         QBrush, QTextOption, QCursor)
from PySide6.QtCore import QRectF, Signal, Qt
from matplotlib.axes import Axes
import matplotlib.axis
import matplotlib.backend_tools
import matplotlib.collections
import matplotlib.container
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Wedge, PathPatch, FancyBboxPatch
from matplotlib.collections import Collection, PathCollection, PolyCollection, LineCollection, EventCollection
from matplotlib.widgets import Cursor
from matplotlib.artist import Artist
from matplotlib.text import Text
from plot.canvas import Canvas
import matplotlib, math
import numpy as np
from matplotlib.backend_bases import MouseEvent
from mpl_toolkits.mplot3d.axes3d import Axes3D
from ui.base_widgets.spinbox import _Slider
from ui.utils import isDark
from plot.utilis import get_color, find_mpl_object
from ui.base_widgets.menu import Menu, Action
from config.settings import GLOBAL_DEBUG, config, logger
from plot.plotting.plotting import legend_onMove, legend_onPress, legend_onRelease

DEBUG = False

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
    key_pressed = Signal(object)
    mouse_released = Signal(object)
    backtoScene = Signal()
    backtoHome = Signal()
    mpl_pressed = Signal(str)
    save_figure = Signal()
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
    
        # self.tooltip = ToolTip()
        # self._scene.addItem(self.tooltip)
        # self.tooltip.hide()
        
        self.canvas.mpl_connect('motion_notify_event', self.mpl_mouseMove)
        self.canvas.mpl_connect('button_press_event', self.mpl_mousePress)
        self.canvas.mpl_connect('button_release_event', self.mpl_mouseRelease)
        self.canvas.mpl_connect('draw_event', self.save_mpl_bg)
        self.canvas.mpl_connect('figure_enter_event', self.mpl_enterFigure)
        self.canvas.mpl_connect('figure_leave_event', self.mpl_leaveFigure)

        self.zoom_slider = _Slider(orientation=Qt.Orientation.Horizontal,step=10)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setStyleSheet("background-color:transparent;")
        self.zoom_item = WidgetItem(self.zoom_slider)
        self._scene.addItem(self.zoom_item)

    def Menu(self):
        self.menu.clear()
  
        nodeview = Action(text="&Node View", shortcut="Ctrl+N", parent=self.menu)
        nodeview.triggered.connect(self.backtoScene.emit)
        self.menu.addAction(nodeview)
        home = Action(text="&Home", shortcut="Ctrl+H", parent=self.menu)
        home.triggered.connect(self.backtoHome.emit)
        self.menu.addAction(home)
        self.menu.addSeparator()

        save = Action(text="Save Figure", shortcut="Ctrl+F", parent=self.menu)
        save.triggered.connect(self.save_figure.emit)
        self.menu.addAction(save)

        self.menu.addSeparator()

        graph = Menu(text="&Graph", parent=self.menu)
        self.menu.addMenu(graph)
        plot_list = [s for s in find_mpl_object(self.canvas.fig,gid="graph ")]
        _graph_list = list()
        for gid in set([s.get_gid() for s in plot_list]):
            _graph_list.append(gid.split("/")[0].title())
        for text in ["Manage Graph"] + _graph_list:
            action = Action(text=text, parent=graph)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text))
            graph.addAction(action)
        
        tick = Menu(text="&Tick", parent=self.menu)
        self.menu.addMenu(tick)
        if isinstance(self.canvas.axes, Axes3D): 
            tick_list = ["Tick &X3D", "Tick &Y3D", "Tick &Z3D"]
        else:
            tick_list = ["Tick &Bottom", "Tick &Left", "Tick &Top", "Tick &Right"]
        for text in tick_list:
            action = Action(text=text, parent=tick)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text.replace("&","")))
            tick.addAction(action)

        spine = Menu(text="&Spine", parent=self.menu)
        self.menu.addMenu(spine)
        if isinstance(self.canvas.axes, Axes3D):
            spine_list = ["Spine &X3D", "Spine &Y3D", "Spine &Z3D"]
        else: 
            spine_list = ["Spine &Bottom", "Spine &Left", "Spine &Top", "Spine &Right"]
        for text in spine_list:
            action = Action(text=text, parent=spine)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text.replace("&","")))
            spine.addAction(action)
        
        figure = Menu(text="&Figure", parent=self.menu)
        self.menu.addMenu(figure)
        for text in ["Plot Size", "Grid"]:
            action = Action(text=text, parent=figure)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text))
            figure.addAction(action)

        label = Menu(text="&Label", parent=self.menu)
        self.menu.addMenu(label)
        for text in ["Title", "Axis Label", "Legend", "Data Annotation"]:
            action = Action(text=text, parent=label)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text))
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
    
    def tooltip_onShow(self, event: MouseEvent):
        stack = find_mpl_object(
            source=self.canvas.fig,
            match=[Line2D,Collection,Rectangle,Wedge,PathPatch,FancyBboxPatch])
        xp, yp, zp = None, None, None
        xs, ys = 0, 0

        for obj in reversed(stack): # the object on top will be picked
            if obj.contains(event)[0]:
                # save the original properties of the picked artist
                _lw = obj.get_linewidth()
                _alp = obj.get_alpha() if obj.get_alpha() else 1
                _c = np.array(matplotlib.colors.to_rgba(get_color(obj)))
                # create tooltip
                bbox_props = dict(
                    boxstyle="round,pad=0.3", 
                    fc="white", 
                    ec=_c, 
                    lw=2
                )
                self.tooltip = self.canvas.figure.text(
                    x=0, y=0, s="", 
                    bbox=bbox_props,
                    horizontalalignment="center",
                )
                # decorate the artist when it is hovered
                obj.set(alpha=_alp*0.3)
                obj.axes.draw_artist(obj)

                if isinstance(obj, (Line2D)):
                    # determine the closest data point to the cursor
                    dist = list()
                    for x, y in zip(obj.get_xdata(), obj.get_ydata()):
                        x, y = obj.axes.transData.transform((x, y))
                        dist.append(math.sqrt(abs(event.x**2 + event.y**2 - x**2 - y**2)))
                    minpos = dist.index(min(dist))
                    xp = obj.get_xdata()[minpos]
                    yp = obj.get_ydata()[minpos]
                    xs, ys = xp, yp
                    # decorate line by darken its color
                    obj.set(linewidth=_lw+4, color = _c*0.5)
                    obj.axes.draw_artist(obj)
                    obj.set(linewidth=_lw, color=_c)
                    
                elif isinstance(obj, (Rectangle,FancyBboxPatch,PathPatch,
                                      PolyCollection, EventCollection)):
                    xp, yp = obj.Xdata, obj.Ydata
                    xs, ys = obj.Xshow, obj.Yshow
                    # decorate patch by darken its facecolor
                    obj.set(facecolor=_c*0.5)
                    obj.axes.draw_artist(obj)
                    obj.set(facecolor=_c)
                
                elif isinstance(obj, (LineCollection)):
                    xp, yp = obj.Xdata, obj.Ydata
                    xs, ys = obj.Xshow, obj.Yshow
                    # decorate line by darken its color
                    obj.set(linewidth=_lw+4, color = _c*0.5)
                    obj.axes.draw_artist(obj)
                    obj.set(linewidth=_lw, color=_c)
                                
                elif isinstance(obj, PathCollection):              
                    # determine the closest data point to the cursor
                    dist = list()
                    for x, y in zip(obj.Xshow, obj.Yshow):
                        x, y = obj.axes.transData.transform((x, y))
                        dist.append(math.sqrt(abs(event.x**2 + event.y**2 - x**2 - y**2)))
                    minpos = dist.index(min(dist))
                    xs = obj.Xshow[minpos]
                    ys = obj.Yshow[minpos]
                    xp = obj.Xdata[minpos]
                    yp = obj.Ydata[minpos]
                    # decorate pathcollection by darken its facecolor
                    obj.set(facecolor = _c*0.5)
                    obj.axes.draw_artist(obj)
                    obj.set(facecolor = _c)
                
                elif isinstance(obj, Wedge):
                    # tooltip will be placed at cursor
                    xp, yp = obj.Xdata, obj.Ydata
                    xs, ys = obj.Xshow, obj.Yshow
                    # decorate wedge by shifting a bit
                    _r = obj.r
                    obj.set_radius(_r*1.1)
                    obj.axes.draw_artist(obj)
                    obj.set_radius(_r)

                # determine the information from the picked artist
                s = f"{obj.get_gid().title()}\n"
                if xp: s += f"{xp:.3f}"
                if yp: s += f", {yp:.3f}"
                if zp: s += f", {zp:.3f}"
                self.tooltip.set_text(s)
                
                # determine where to put tooltip on canvas
                xs, ys = obj.axes.transData.transform([xs, ys])
                xs, ys = self.canvas.figure.transFigure.inverted().transform((xs, ys))
                
                # xs += self.tooltip.get_window_extent()*0.2
                # ys -= self.tooltip.get_height()*1.2
                # if xs < 0 : xs = 0.02
                # if ys < 0 : ys = 0.02
                # if xs + self.tooltip.get_width() > 1: xs = 1 - self.tooltip.get_width() - 0.02
                # if ys + self.tooltip.get_height() > 1: ys = 1 - self.tooltip.get_height() - 0.02
                #self.canvas.figure.add_artist(self.tooltip)
                self.tooltip.set_x(xs)
                self.tooltip.set_y(ys)
                self.canvas.figure.draw_artist(self.tooltip)

                # update the artist to the original properties
                obj.set(alpha=_alp)

                # make sure the annotation will be removed
                self.tooltip.remove() 

                break
        
    
    def save_mpl_bg(self, event=None):
        self.mpl_background = self.canvas.copy_from_bbox(self.canvas.fig.bbox)
        
    def mpl_enterFigure(self, event:MouseEvent):
        """ save original figure when mouse enters the figure """
        self.save_mpl_bg(event)
    
    def mpl_leaveFigure(self, event:MouseEvent):
        """ restore original figure when mouse leaves the figure """
        self.canvas.restore_region(self.mpl_background)
        self.canvas.draw_idle()
    
    def mpl_mouseMove(self, event:MouseEvent):

        self.canvas.restore_region(self.mpl_background)
        #self.canvas.set_cursor(matplotlib.backend_tools.cursors.WAIT)

        self.legend_picked = legend_onMove(event, self.canvas)

        if not self.legend_picked and config["plot_tooltip"]:
            self.tooltip_onShow(event)
            
        self.canvas.blit(self.canvas.fig.bbox)
        #self.canvas.flush_events()

    def mpl_mousePress(self, event: MouseEvent):
        stack = find_mpl_object(source=self.canvas.fig,
                                match=[Artist])
        
        self.legend_picked = legend_onPress(event, self.canvas)
        
        if not self.legend_picked:
            if event.button == 1:
                for obj in stack:
                    if obj.contains(event)[0]:
                        self.mpl_pressed.emit(obj.get_gid())
                        break # emit when one and only one object is selected
        
        if isinstance(self.canvas.axes, Axes3D) and event.button == 3:
            self.ax_limit = self.canvas.axes.get_xlim() + self.canvas.axes.get_ylim() + self.canvas.axes.get_zlim()
    
    def mpl_mouseRelease(self, event: MouseEvent):
        self.save_mpl_bg(event)
        self.legend_picked = legend_onRelease(event, self.canvas)
    
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
        if isinstance(self.canvas.axes, Axes3D):
            ax_limit = self.canvas.axes.get_xlim() + self.canvas.axes.get_ylim() + self.canvas.axes.get_zlim()
            exec_menu = self.ax_limit == ax_limit
        else: exec_menu = True
        
        if exec_menu: 
            pos = self.mapToGlobal(event.pos())
            self.menu = Menu(parent=self)
            self.Menu()
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
        #self.key_pressed.emit(event)
        return super().keyPressEvent(event)
    
class GraphicsViewMultiFig(GraphicsView):
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)

    def Menu(self):
        self.menu.clear()
  
        nodeview = Action(text="&Node View", shortcut="Ctrl+N", parent=self.menu)
        nodeview.triggered.connect(self.backtoScene.emit)
        self.menu.addAction(nodeview)
        home = Action(text="&Home", shortcut="Ctrl+H", parent=self.menu)
        home.triggered.connect(self.backtoHome.emit)
        self.menu.addAction(home)
        self.menu.addSeparator()

        save = Action(text="Save Figure", shortcut="Ctrl+F", parent=self.menu)
        save.triggered.connect(self.save_figure.emit)
        self.menu.addAction(save)

        self.menu.addSeparator()
    
    def tooltip_onShow(self, event: MouseEvent):
        pass
        
    def mpl_enterFigure(self, event:MouseEvent):
        pass

    def mpl_leaveFigure(self, event:MouseEvent):
        pass
    
    def mpl_mouseMove(self, event:MouseEvent):
        pass

    def mpl_mousePress(self, event: MouseEvent):
        if event.inaxes:
            ax = event.inaxes
            print(ax)
    
    def mpl_mouseRelease(self, event: MouseEvent):
        pass
                