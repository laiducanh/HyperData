from PySide6.QtWidgets import (QGraphicsView, QStyleOptionGraphicsItem, QGraphicsTextItem, 
                             QWidget, QGraphicsItem, QGraphicsProxyWidget)
from PySide6.QtGui import (QKeyEvent, QMouseEvent, QPainter, QPainterPath, QColor, QPen, 
                         QBrush, QTextOption)
from PySide6.QtCore import QRectF, Signal, Qt, QPoint, QPointF, QRect, QSize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle, Wedge, PathPatch, FancyBboxPatch, Ellipse
from matplotlib.collections import Collection, PathCollection, PolyCollection, LineCollection, EventCollection, QuadMesh
from matplotlib.text import Text
from matplotlib.artist import Artist
from plot.canvas import Canvas, Canvas3D
import matplotlib, math
import numpy as np
from matplotlib.backend_bases import MouseEvent
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.backend_tools import Cursors
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
    draw_obj = Signal()
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

        self.drawing_index = 0
        self.drawing_shape = None
        self.drawing_start = QPointF()
        self.drawing_item = None

        self.change_item = None
        self.moving_start = None
        self.drawing_resize = None

        self.selected_gid = None
        
        self.canvas.mpl_connect('motion_notify_event', self.mpl_mouseMove)
        self.canvas.mpl_connect('button_press_event', self.mpl_mousePress)
        self.canvas.mpl_connect('button_release_event', self.mpl_mouseRelease)
        self.canvas.mpl_connect('draw_event', self.mpl_onDraw)
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
    
    def drawing_object(self, shape:str):
        self.drawing_shape = shape
    
    def _resizePlot(self):
        size = self.viewport().size()
        height = size.height()
        width = size.width()
        self.canvas.resize(int(width), int(height))
        self.plotview.setPos(size.width()/2-width/2,size.height()/2-height/2)
        self.setSceneRect(0,0,size.width(),size.height())
        self._scene.update_rulers()

    ##### Qt Events

    def mousePressEvent(self, event:QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
    
    def middleMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)
    
    def leftMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)

    def rightMouseButtonPress(self, event:QMouseEvent):
        super().mousePressEvent(event)
    
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
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resizePlot()
      
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self.selected_gid:
                for obj in find_mpl_object(self.canvas.figure, gid=self.selected_gid):
                    obj.remove()
                self.draw_obj.emit()
                self.canvas.draw_idle()
        else:
            self.key_pressed.emit(event)

    def leaveEvent(self, event):
        self._scene.vcross.hide()
        self._scene.hcross.hide()
        return super().leaveEvent(event)

    def enterEvent(self, event):
        self._scene.vcross.show()
        self._scene.hcross.show()
        return super().enterEvent(event)

    ##### Matplotlib helpers

    def _tooltip_onShow(self, event: MouseEvent):
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

    def _save_mpl_bg(self):
        """ save figure background for blitting """
        self.mpl_background = self.canvas.copy_from_bbox(self.canvas.figure.bbox)

    def _set_mpl_cursor(self, event:MouseEvent):
        event_x, event_y = self.canvas.figure.transFigure.inverted().transform(
                        (event.x, event.y)
        )
        self.canvas.set_cursor(Cursors.SELECT_REGION)
        for obj in find_mpl_object(self.canvas.figure, gid='drawing'):
            if isinstance(obj, Patch):
                bbox = obj.get_window_extent()
                bbox_fig = bbox.transformed(self.canvas.figure.transFigure.inverted())
                x0, y0, x1, y1 = bbox_fig.x0, bbox_fig.y0, bbox_fig.x1, bbox_fig.y1
                if event_x >= x0*0.98 and event_x <= x0*1.02 and event_y >= y0 and event_y <= y1:
                    self.canvas.set_cursor(Cursors.RESIZE_HORIZONTAL)
                    break
                elif event_x >= x1*0.98 and event_x <= x1*1.02 and event_y >= y0 and event_y <= y1:
                    self.canvas.set_cursor(Cursors.RESIZE_HORIZONTAL)
                    break
                elif event_y >= y0*0.98 and event_y <= y0*1.02 and event_x >= x0 and event_x <= x1:
                    self.canvas.set_cursor(Cursors.RESIZE_VERTICAL)
                    break
                elif event_y >= y1*0.98 and event_y <= y1*1.02 and event_x >= x0 and event_x <= x1:
                    self.canvas.set_cursor(Cursors.RESIZE_VERTICAL)
                    break
                elif obj.contains(event)[0]:
                    self.canvas.set_cursor(Cursors.MOVE)
                    break
            elif isinstance(obj, Line2D):
                x0, x1 = obj.get_xdata()
                y0, y1 = obj.get_ydata()
                if event_x >= x0*0.98 and event_x <= x0*1.02 and event_y >= y0*0.98 and event_y <= y0*1.02:
                    self.canvas.set_cursor(Cursors.MOVE)
                    break
                elif event_x >= x1*0.98 and event_x <= x1*1.02 and event_y >= y1*0.98 and event_y <= y1*1.02:
                    self.canvas.set_cursor(Cursors.MOVE)
                    break
                elif obj.contains(event)[0]:
                    self.canvas.set_cursor(Cursors.MOVE)
                    break
            elif isinstance(obj, Text):
                if obj.contains(event)[0]:
                    self.canvas.set_cursor(Cursors.MOVE)
                    break
    
    def _drawing_shape(self, x0, y0, x1, y1):
        w, h = x1-x0, y1-y0
        if self.drawing_shape == 'rectangle':
            self.drawing_item = Rectangle(
                (x0, y0), w, h,
                edgecolor='black', facecolor="#454545", 
                lw=1,
                transform=self.canvas.figure.transFigure,
                gid=f'drawing {self.drawing_index}'
            )
            # Temporarily draw the shape
            self.canvas.figure.draw_artist(self.drawing_item)
        elif self.drawing_shape == 'line':
            self.drawing_item = Line2D(
                (x0, x1), (y0, y1),
                lw=1, color="#454545", marker='none',
                transform=self.canvas.figure.transFigure,
                gid=f'drawing {self.drawing_index}'
            )
            # Temporarily draw the shape
            self.canvas.figure.draw_artist(self.drawing_item)
        elif self.drawing_shape == 'ellipse':
            self.drawing_item = Ellipse(
                (x0+w/2, y0+h/2), w, h,
                edgecolor='black', facecolor="#454545", 
                transform=self.canvas.figure.transFigure,
                gid=f'drawing {self.drawing_index}'
            )
            # Temporarily draw the shape
            self.canvas.figure.draw_artist(self.drawing_item)
        elif self.drawing_shape == 'text':
            bbox = Rectangle(
                (x0, y0), w, h, 
                lw=1, ls='dashed',
                edgecolor="#454545", facecolor='none',
                transform=self.canvas.figure.transFigure
            )
            # Temporarily draw the box instead of text
            self.canvas.figure.draw_artist(bbox)
            self.drawing_item = Text(
                x0, y0, 'Sample text',
                figure=self.canvas.figure,
                transform=self.canvas.figure.transFigure,
                gid=f'drawing {self.drawing_index}'
            )
    
    def _resize_shape(self, obj:Artist, a, b, c, d, dx, dy):
        """ a, b, c, d are required coordinates for shapes """

        if isinstance(obj, Rectangle):   
            x0, y0, w, h = a, b, c, d
            obj.set_xy((x0, y0))
            obj.set_width(w)
            obj.set_height(h)
            if self.drawing_resize == 'left':
                obj.set_x(x0+dx)
                obj.set_width(w-dx)
            elif self.drawing_resize == 'right':
                obj.set_width(w+dx)
            elif self.drawing_resize == 'bottom':
                obj.set_y(y0+dy)
                obj.set_height(h-dy)
            elif self.drawing_resize == 'top':                        
                obj.set_height(h+dy)
            else:
                obj.set_xy((x0+dx, y0+dy))
        elif isinstance(obj, Ellipse):
            x, y, w, h = a, b, c, d
            if self.drawing_resize == 'left':
                obj.set_center((x+dx/2, y))
                obj.set_width(w-dx)
            elif self.drawing_resize == 'right':
                obj.set_center((x+dx/2, y))
                obj.set_width(w+dx)
            elif self.drawing_resize == 'bottom':
                obj.set_center((x,y+dy/2))
                obj.set_height(h-dy)
            elif self.drawing_resize == 'top':
                obj.set_center((x,y+dy/2))
                obj.set_height(h+dy)
            else:
                obj.set_center((x+dx, y+dy))
        elif isinstance(obj, Line2D):
            x0, y0, x1, y1 = a, b, c, d
            if self.drawing_resize == 'head':
                obj.set_xdata((x0+dx, x1))
                obj.set_ydata((y0+dy, y1))
            elif self.drawing_resize == 'tail':
                obj.set_xdata((x0, x1+dx))
                obj.set_ydata((y0, y1+dy))
            else:
                obj.set_xdata((x0+dx, x1+dx))
                obj.set_ydata((y0+dy, y1+dy))
        elif isinstance(obj, Text):
            x, y = a, b
            obj.set_x(x+dx)
            obj.set_y(y+dy)
            
        self.canvas.figure.draw_artist(obj)
    
    def _prepare_resize_shape(self, event:MouseEvent):

        event_x, event_y = self.canvas.figure.transFigure.inverted().transform(
                        (event.x, event.y)
        )

        drawing_resize = None
        moving_start = None
        change_item = None

        for obj in reversed(find_mpl_object(self.canvas.figure, gid='drawing')):
            if isinstance(obj, Patch):

                bbox = obj.get_window_extent()
                bbox_fig = bbox.transformed(self.canvas.figure.transFigure.inverted())
                x0, y0, x1, y1 = bbox_fig.x0, bbox_fig.y0, bbox_fig.x1, bbox_fig.y1

                if event_x >= x0*0.98 and event_x <= x0*1.02 and event_y >= y0 and event_y <= y1:
                    drawing_resize = 'left'
                elif event_x >= x1*0.98 and event_x <= x1*1.02 and event_y >= y0 and event_y <= y1:
                    drawing_resize = 'right'
                elif event_y >= y0*0.98 and event_y <= y0*1.02 and event_x >= x0 and event_x <= x1:
                    drawing_resize = 'bottom'
                elif event_y >= y1*0.98 and event_y <= y1*1.02 and event_x >= x0 and event_x <= x1:
                    drawing_resize = 'top'
                elif obj.contains(event)[0]:
                    moving_start = True
                
                if drawing_resize or moving_start:
                    if isinstance(obj, Rectangle):
                        moving_start = [
                            x0, y0,
                            x1-x0, y1-y0,
                            event_x, event_y
                        ]
                    elif isinstance(obj, Ellipse):
                        moving_start = [
                            (x0+x1)/2, (y0+y1)/2,
                            x1-x0, y1-y0,
                            event_x, event_y
                        ]
                    change_item = obj.get_gid()
                    break # emit when one and only one object is selected

            elif isinstance(obj, Line2D):

                x0, x1 = obj.get_xdata()
                y0, y1 = obj.get_ydata()
    
                if event_x >= x0*0.98 and event_x <= x0*1.02 and event_y >= y0*0.98 and event_y <= y0*1.02:
                    drawing_resize = 'head'
                elif event_x >= x1*0.98 and event_x <= x1*1.02 and event_y >= y1*0.98 and event_y <= y1*1.02:
                    drawing_resize = 'tail'
                elif obj.contains(event)[0]:
                    moving_start = True
                if drawing_resize or moving_start:
                    moving_start = [
                        x0, y0, x1, y1,
                        event_x, event_y
                    ] 
                    change_item = obj.get_gid()
                    break # emit when one and only one object is selected
            
            elif isinstance(obj, Text):

                x, y = obj._x, obj._y

                if obj.contains(event)[0]:
                    moving_start = [
                        x, y, None, None,
                        event_x, event_y
                    ]
                    change_item = obj.get_gid()
                    break # emit when one and only one object is selected

        return drawing_resize, moving_start, change_item

    def _draw_selection(self, gid:str):    
        
        stack = find_mpl_object(
            source=self.canvas.figure,
            gid=gid
        )
        shrink_pixels = 5
        for obj in stack:
            # Shrink the bbox of the object
            bbox = obj.get_window_extent()
            bbox = Bbox.from_bounds(
                bbox.x0 - shrink_pixels,
                bbox.y0 - shrink_pixels,
                bbox.width + 2 * shrink_pixels,
                bbox.height + 2 * shrink_pixels
            )
            
            # Convert bbox from display coordinates to figure coordinates
            bbox_fig = bbox.transformed(self.canvas.figure.transFigure.inverted())
            x0, y0, width, height = bbox_fig.bounds

            # Create rectangle patch to denote selection
            rect = Rectangle(
                (x0, y0), width, height,
                edgecolor='gray', facecolor='none', 
                lw=1, ls='dashed',
                transform=self.canvas.figure.transFigure,
                gid='_selected'
            )
            self.canvas.figure.draw_artist(rect)

    ##### Matplotlib events
    
    def mpl_onDraw(self, event:MouseEvent):
        self._scene.top_margin_left._setPos(self.canvas.figure.subplotpars.left)
        self._scene.top_margin_right._setPos(self.canvas.figure.subplotpars.right)
        self._scene.left_margin_top._setPos(1-self.canvas.figure.subplotpars.top) # orientation of matplotlib is inverse
        self._scene.left_margin_bot._setPos(1-self.canvas.figure.subplotpars.bottom)
        if self.selected_gid: self._draw_selection(self.selected_gid)
        self._save_mpl_bg()
    
    def mpl_enterFigure(self, event:MouseEvent):
        """ save original figure when mouse enters the figure """
        self._save_mpl_bg()
    
    def mpl_leaveFigure(self, event:MouseEvent):
        """ restore original figure when mouse leaves the figure """
        self.canvas.restore_region(self.mpl_background)
        self.canvas.draw_idle()

    def mpl_mouseMove(self, event:MouseEvent):

        self.canvas.restore_region(self.mpl_background)

        event_x, event_y = self.canvas.figure.transFigure.inverted().transform(
                        (event.x, event.y)
        )

        # Set Cursor
        self._set_mpl_cursor(event)
        
        # Draw shape
        if self.drawing_start:
            x, y = self.drawing_start
            self._drawing_shape(x, y, event_x, event_y)
        
        # Resize or move shape
        if self.change_item:       
            for obj in find_mpl_object(self.canvas.figure, gid=self.change_item):
                a, b, c, d = self.moving_start[:4]
                dx = event_x - self.moving_start[-2]
                dy = event_y - self.moving_start[-1]
                self._resize_shape(obj, a, b, c, d, dx, dy)
                
        # if config["plot_tooltip"]:
        #     self.tooltip_onShow(event)
            
        # self.canvas.blit(self.canvas.figure.bbox)
        #self.canvas.flush_events()

    def mpl_mousePress(self, event: MouseEvent):

        event_x, event_y = self.canvas.figure.transFigure.inverted().transform(
                            (event.x, event.y)
                        )
        
        self.change_item = None

        if event.button == 1:
            if self.drawing_shape:
                self.drawing_index += 1
                self.drawing_start = (event_x, event_y)
            else:
                self.drawing_resize, \
                self.moving_start, \
                self.change_item = self._prepare_resize_shape(event)
            
        if isinstance(self.canvas.axes, Axes3D) and event.button == 3:
            self.ax_limit = self.canvas.axes.get_xlim() + self.canvas.axes.get_ylim() + self.canvas.axes.get_zlim()
    
    def mpl_mouseRelease(self, event: MouseEvent):
        stack = find_mpl_object(
            source=self.canvas.figure,
            match=[Line2D,Collection,Rectangle,Wedge,Ellipse,
                   PathPatch,FancyBboxPatch,Text]
        )
        for rect in find_mpl_object(self.canvas.figure, gid='_selected'):
            rect.remove()
        self.selected_obj.emit(None)

        if self.drawing_item:
            # add shape permanently
            self.canvas.figure.add_artist(self.drawing_item)
            self.draw_obj.emit()

        if event.button == 1:
            for obj in reversed(stack):
                if self.change_item:
                    # while resizing the item, mouse position may fall outside the item
                    self.selected_gid = self.change_item
                    self.selected_obj.emit(self.change_item)
                    self.change_item = None
                    break
                elif obj.contains(event)[0] and obj.get_gid() and not obj.get_gid().startswith("_"):
                    self.selected_gid = obj.get_gid()
                    self.selected_obj.emit(obj.get_gid())
                    break
                elif self.drawing_item:
                    self.selected_gid = f'drawing {self.drawing_index}'
                    self.selected_obj.emit(f'drawing {self.drawing_index}')
                    break
                else: 
                    self.selected_gid = None
        
        self._save_mpl_bg()
        self.canvas.draw_idle()
        self.drawing_start = QPointF()
        self.drawing_shape = None
        self.drawing_item = None
        self.moving_start = None
        self.drawing_resize = None
           
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
                