from PySide6.QtWidgets import (QGraphicsView, QStyleOptionGraphicsItem, QGraphicsTextItem, 
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PySide6.QtGui import (QKeyEvent, QMouseEvent, QPainter, QPainterPath, QColor, QPen, 
                         QBrush, QTextOption)
from PySide6.QtCore import QRectF, Signal, Qt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Wedge, PathPatch, FancyBboxPatch
from matplotlib.collections import Collection, PathCollection, PolyCollection, LineCollection, EventCollection, QuadMesh
from matplotlib.text import Text
from matplotlib.artist import Artist
from plot.canvas import Canvas, Canvas3D
import matplotlib, math
import numpy as np
from matplotlib.backend_bases import MouseEvent
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d.axes3d import Axes3D
from ui.utils import isDark
from plot.utilis import get_color, find_mpl_object
from ui.base_widgets.menu import Menu, Action
from plot.plot_graphics_scene import GraphicsScene

DEBUG = False

class WidgetItem (QGraphicsItem):
    def __init__(self, widget, parent=None):
        super().__init__(parent)

        self.widget = QGraphicsProxyWidget(self)
        self.widget.setWidget(widget)

        self.width = 100
        self.height = 100
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget) -> None:
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
    selected_obj = Signal(str)
    save_figure = Signal()
    def __init__(self, canvas:Canvas,parent=None):
        super().__init__(parent)

        self._scene = GraphicsScene(parent)
        self.setScene(self._scene)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.LosslessImageRendering | QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.canvas = canvas
        self.plotview = WidgetItem(canvas)
        self._scene.addItem(self.plotview) 

        self.initMenu()
        self._scene.draw_ruler() # draw ruler after adding Canvas
        self._scene.margin_updated.connect(self.update_margin)
        # Initialize margin indicator in ruler
        self._scene.top_margin_left.fraction = self.canvas.figure.subplotpars.left
        self._scene.top_margin_right.fraction = self.canvas.figure.subplotpars.right
        self._scene.left_margin_top.fraction = 1-self.canvas.figure.subplotpars.top # orientation of matplotlib is inverse
        self._scene.left_margin_bot.fraction = 1-self.canvas.figure.subplotpars.bottom

        # self.tooltip = ToolTip()
        # self._scene.addItem(self.tooltip)
        # self.tooltip.hide()
        
        self.canvas.mpl_connect('motion_notify_event', self.mpl_mouseMove)
        self.canvas.mpl_connect('button_press_event', self.mpl_mousePress)
        self.canvas.mpl_connect('button_release_event', self.mpl_mouseRelease)
        self.canvas.mpl_connect('draw_event', self.save_mpl_bg)
        self.canvas.mpl_connect('figure_enter_event', self.mpl_enterFigure)
        self.canvas.mpl_connect('figure_leave_event', self.mpl_leaveFigure)

    def initMenu(self):

        self.menu = Menu(parent=self)

        nodeview = Action(text="&Node View", shortcut="Ctrl+N", parent=self.menu)
        nodeview.triggered.connect(self.backtoScene.emit)
        self.menu.addAction(nodeview)
        self.menu.addSeparator()

        save = Action(text="Save Figure", shortcut="Ctrl+F", parent=self.menu)
        save.triggered.connect(self.save_figure.emit)
        self.menu.addAction(save)

        self.menu.addSeparator()

        graph = Menu(text="&Graph", parent=self.menu)
        self.menu.addMenu(graph)
        action = Action(text='Add Graph', parent=graph)
        action.triggered.connect(lambda : self.mouse_released.emit('Add Graph'))
        graph.addAction(action)
        
        axis = Menu(text="&Axis", parent=self.menu)
        self.menu.addMenu(axis)
        if isinstance(self.canvas.axes, Axes3D): 
            axis_list = ["&X Axis","&Y Axis","&Z Axis"]
        else:
            axis_list = ["&Bottom Axis","&Left Axis","&Top Axis","&Right Axis"]
        for text in axis_list:
            action = Action(text=text, parent=axis)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text.replace("&","")))
            axis.addAction(action)

        if isinstance(self.canvas, Canvas3D):
            pane = Menu(text="&Pane", parent=self.menu)
            self.menu.addMenu(pane)
            for text in ["XY Pane","YZ Pane","XZ Pane"]:
                action = Action(text=text, parent=pane)
                action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text))
                pane.addAction(action)
            figure = Action(text="&Figure 3D", parent=self.menu)
            figure.triggered.connect(lambda: self.mouse_released.emit('figure 3d'))
            self.menu.addAction(figure)

        else:
            figure = Action(text="&Grid and Pane", parent=self.menu)
            figure.triggered.connect(lambda: self.mouse_released.emit('figure 2d'))
            self.menu.addAction(figure)

        label = Menu(text="&Label", parent=self.menu)
        self.menu.addMenu(label)
        for text in ["Title", "Legend"]:
            action = Action(text=text, parent=label)
            action.triggered.connect(lambda _, text=text: self.mouse_released.emit(text))
            label.addAction(action)

    def update_margin(self):
        self.canvas.figure.subplots_adjust(
            left = self._scene.top_margin_left.fraction,
            right = self._scene.top_margin_right.fraction,
            top = 1-self._scene.left_margin_top.fraction,
            bottom = 1-self._scene.left_margin_bot.fraction
        )
        self.canvas.draw_idle()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.mouse_position = self.mapToScene(event.pos())   
        self._scene.vcross.setLine(
            self.mouse_position.x(), 
            self.sceneRect().top(),
            self.mouse_position.x(),
            self.sceneRect().bottom()
        )
        self._scene.hcross.setLine(
            self.sceneRect().left(),
            self.mouse_position.y(),
            self.sceneRect().right(),
            self.mouse_position.y()
        )
        return super().mouseMoveEvent(event)
    
    def leaveEvent(self, event):
        self._scene.vcross.hide()
        self._scene.hcross.hide()
        return super().leaveEvent(event)

    def enterEvent(self, event):
        self._scene.vcross.show()
        self._scene.hcross.show()
        return super().enterEvent(event)
    
    def mousePressEvent(self, event:QMouseEvent):
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
            source=self.canvas.figure,
            match=[Line2D,Collection,Rectangle,Wedge,
                   PathPatch,FancyBboxPatch]
        )
        xp, yp, zp = None, None, None
        xs, ys = 0, 0

        for obj in reversed(stack): # the object on top will be picked
            if obj.contains(event)[0]:
                # save the original properties of the picked artist
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

                if isinstance(obj, (Line2D)):
                    # save the original properties of the picked artist
                    _ms = obj.get_markersize()
                    # determine the closest data point to the cursor
                    dist = list()
                    for x, y in zip(obj.get_xdata(), obj.get_ydata()):
                        x, y = obj.axes.transData.transform((x, y))
                        dist.append(math.sqrt(abs(event.x**2 + event.y**2 - x**2 - y**2)))
                    minpos = dist.index(min(dist))
                    xp = obj.get_xdata()[minpos]
                    yp = obj.get_ydata()[minpos]
                    xs, ys = xp, yp
                    # decorate line by increasing markersize
                    obj.set(ms=_ms*2)
                    obj.axes.draw_artist(obj)
                    obj.set(ms=_ms)
                    
                elif isinstance(obj, (Rectangle,FancyBboxPatch,PathPatch,
                                      PolyCollection, EventCollection)):
                    _lw = obj.get_linewidth()
                    xp, yp = obj.Xdata, obj.Ydata
                    xs, ys = obj.Xshow, obj.Yshow
                    print(str(xp), str(yp), str(xs), str(ys))
                    # decorate patch by darkening its facecolor and increasing linewidth
                    obj.set(fc=_c*0.5,lw=_lw*2)
                    obj.axes.draw_artist(obj)
                    obj.set(fc=_c,lw=_lw)
                
                elif isinstance(obj, (LineCollection)):
                    # save the original properties of the picked artist
                    _lw = obj.get_linewidth()
                    xp, yp = obj.Xdata, obj.Ydata
                    xs, ys = obj.Xshow, obj.Yshow
                    # decorate line by increasing linewidth
                    obj.set(lw=_lw*2)
                    obj.axes.draw_artist(obj)
                    obj.set(lw=_lw)
                                
                elif isinstance(obj, PathCollection): 
                    # save the original properties of the picked artist
                    _lw = obj.get_linewidth()
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
                    # decorate pathcollection by darkening its facecolor, and increasing linewidth
                    obj.set(fc=_c*0.5, lw=_lw*4)
                    obj.axes.draw_artist(obj)
                    obj.set(fc=_c,lw=_lw)
                
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

                # make sure the annotation will be removed
                self.tooltip.remove() 

                break

    def save_mpl_bg(self, event=None):
        self._scene.top_margin_left._setPos(self.canvas.figure.subplotpars.left)
        self._scene.top_margin_right._setPos(self.canvas.figure.subplotpars.right)
        self._scene.left_margin_top._setPos(1-self.canvas.figure.subplotpars.top) # orientation of matplotlib is inverse
        self._scene.left_margin_bot._setPos(1-self.canvas.figure.subplotpars.bottom)
        self.mpl_background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)
    
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

        # if config["plot_tooltip"]:
        #     self.tooltip_onShow(event)
            
        self.canvas.blit(self.canvas.figure.bbox)
        #self.canvas.flush_events()

    def mpl_mousePress(self, event: MouseEvent):
        stack = find_mpl_object(
            source=self.canvas.figure,
            match=[Line2D,Collection,Rectangle,Wedge,
                   PathPatch,FancyBboxPatch, Text]
        )
        for rect in find_mpl_object(self.canvas.figure, gid='selected'):
            self.canvas.figure.patches.remove(rect)
        self.selected_obj.emit(None)
        self.canvas.draw_idle()

        if event.button == 1:
            for obj in stack:
                if obj.contains(event)[0] and not obj.get_gid().startswith("_"):
                    self.selected_obj.emit(obj.get_gid())
                    self.select_mpl_obj(obj.get_gid())
                    break # emit when one and only one object is selected
        
        if isinstance(self.canvas.axes, Axes3D) and event.button == 3:
            self.ax_limit = self.canvas.axes.get_xlim() + self.canvas.axes.get_ylim() + self.canvas.axes.get_zlim()
    
    def mpl_mouseRelease(self, event: MouseEvent):
        self.save_mpl_bg(event)
    
    def select_mpl_obj(self, gid:str):        
        stack = find_mpl_object(source=self.canvas.figure,
                                gid=gid)
        shrink_pixels = 5
        for obj in stack:
            # Shrink the bbox of the object
            bbox = obj.get_window_extent()
            x0 = bbox.x0 - shrink_pixels
            y0 = bbox.y0 - shrink_pixels
            width = bbox.width + 2 * shrink_pixels
            height = bbox.height + 2 * shrink_pixels
            # Convert bbox from display coordinates to data coordinates
            bbox_data = Bbox.from_bounds(x0, y0, width, height).transformed(self.canvas.figure.transFigure.inverted())
            # Get coordinates and width/height
            x0, y0 = bbox_data.x0, bbox_data.y0
            width, height = bbox_data.width, bbox_data.height

            # Create rectangle patch
            rect = Rectangle(
                (x0, y0), width, height,
                edgecolor='gray', facecolor='none', 
                lw=1, ls='dashed',
                transform=self.canvas.figure.transFigure,
                gid='selected'
            )
            self.canvas.figure.patches.append(rect)
        self.canvas.draw_idle()
    
    def mouseReleaseEvent(self, event:QMouseEvent):
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
            self.menu.exec(pos)
            
        super().mouseReleaseEvent(event)
    
    def resizePlot(self):
        size = self.viewport().size()
        height = size.height()
        width = size.width()
        self.canvas.resize(int(width), int(height))
        self.plotview.setPos(size.width()/2-width/2,size.height()/2-height/2)
        self.setSceneRect(0,0,size.width(),size.height())
        self._scene.update_rulers()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizePlot()
      
    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.key_pressed.emit(event)
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
    
    def mpl_mouseRelease(self, event: MouseEvent):
        pass
                