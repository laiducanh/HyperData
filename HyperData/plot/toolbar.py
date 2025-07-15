from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QPen, QIcon, QColor
from ui.base_widgets.color import ColorToolButton
from ui.base_widgets.button import TransparentToolButton, TransparentComboBox, CheckBox
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from config.settings import linestyle_lib, marker_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object

class EdgeColor(ColorToolButton):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        
        self.set_value()
    
    def set_value(self, color=None):
        if not color: color = self.color
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        pen = QPen(QColor(color), 5)  # line thickness = 5 px
        painter.setPen(pen)
        # Draw diagonal from bottom-left to top-right
        painter.drawLine(2, pixmap.height()-2, pixmap.width()-2, 2)
        painter.end()

        icon = QIcon(pixmap)
        icon.path = None
        self.setIcon(icon)
        self.setIconSize(pixmap.size())
    
    def onColorChanged(self, color):
        super().onColorChanged(color)
        self.set_value()
    
    def _update(self):
        pass

class FaceColor(EdgeColor):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
            
    def set_value(self, color=None):
        if not color: color = self.color
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        # Define square size
        square_size = self.height() - 2

        # Calculate position to center the square in the pixmap
        x = (pixmap.width() - square_size) // 2
        y = (pixmap.height() - square_size) // 2

        # Set brush to fill the square with the selected color
        painter.setBrush(QColor(color))
        # painter.setPen(Qt.GlobalColor.black)  # optional: outline color

        # Draw the square
        painter.drawRect(x, y, square_size, square_size)
        painter.end()

        icon = QIcon(pixmap)
        icon.path = None
        self.setIcon(icon)
        self.setIconSize(pixmap.size())

class PlotView_ToolBar(QToolBar):
    sig_back_to_grScene = Signal()
    sig_ruler = Signal(bool)
    def __init__(self, canvas:Canvas, parent=None, *args, **kwargs): # parent is PlotView instance
        super().__init__(parent, *args, **kwargs)

        self.gid = None
        self.canvas = canvas
        self._parent = parent
        self.initActions()
    
    def initActions(self):

        self.graphicscreen_btn = TransparentToolButton(
            icon="stack.png",
            setter=self.sig_back_to_grScene.emit,
            layout=self
        )

        self.addSeparator()

        self.edgecolor = EdgeColor(
            setter=self.set_edgecolor,
            layout=self
        )
        self.facecolor = FaceColor(
            setter=self.set_facecolor,
            layout=self
        )
        self.linewidth = TransparentDoubleSpinBox(
            setter=self.set_linewidth,
            decimals=1,
            value=3,
            layout=self
        )
        self.linestyle = TransparentComboBox(
            items = linestyle_lib.values(),
            setter=self.set_linestyle,
            layout=self
        )

        self.marker = TransparentComboBox(
            items = marker_lib.values(),
            setter=self.set_marker,
            layout=self
        )

        self.addSeparator()

        CheckBox(
            text='Ruler',
            setter=self._parent.plot_visual._scene.toggle_ruler,
            getter=lambda: self._parent.plot_visual._scene.rulerOn,
            layout=self
        )
    
    def get_edgecolor(self):
        try:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_edgecolor()
        except:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_color()
    
    def set_edgecolor(self, value):
        if self.gid:
            for obj in find_mpl_object(self.canvas.figure, gid=self.gid):
                try: obj.set_edgecolor(value)
                except: obj.set_color(value)
            self._parent.update_plotlist()
            self.canvas.draw_idle()
            
    def get_facecolor(self):
        try:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_facecolor()
        except:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_color()
    
    def set_facecolor(self, value):
        if self.gid:
            for obj in find_mpl_object(self.canvas.figure, gid=self.gid):
                try: obj.set_facecolor(value)
                except: pass
            self._parent.update_plotlist()
            self.canvas.draw_idle()
    
    def get_linewidth(self):
        try:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_linewidth()
        except Exception as e: print(e)
    
    def set_linewidth(self, value):
        if self.gid:
            for obj in find_mpl_object(self.canvas.figure, gid=self.gid):
                try: obj.set_linewidth(value)
                except: pass
            self.canvas.draw_idle()
    
    def get_linestyle(self):
        try:
            return find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_linestyle()
        except Exception as e: print(e)
    
    def set_linestyle(self, value):
        if self.gid:
            for obj in find_mpl_object(self.canvas.figure, gid=self.gid):
                try: obj.set_linestyle(value)
                except: pass
            self.canvas.draw_idle()
    
    def get_marker(self):
        try:
            if not find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_marker():
                return "None"
            return marker_lib[find_mpl_object(self.canvas.figure, gid=self.gid)[0].get_marker()]
        except Exception as e: print(e)
    
    def set_marker(self, value):
        if self.gid:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(value.lower())]
            for obj in find_mpl_object(self.canvas.figure, gid=self.gid):
                try: obj.set_marker(marker)
                except: pass
            self.canvas.draw_idle()        
    
    def update(self):
        self.edgecolor.set_value(self.get_edgecolor())
        self.facecolor.set_value(self.get_facecolor())
        self.linewidth.set_value(self.get_linewidth())
        self.linestyle.set_value(self.get_linestyle())
        self.marker.set_value(self.get_marker())