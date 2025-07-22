from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QPen, QIcon, QColor, QFont
from ui.base_widgets.color import ColorToolButton
from ui.base_widgets.button import TransparentToolButton, TransparentComboBox, CheckBox, ToggleToolButton
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from ui.base_widgets.menu import Menu, Action
from config.settings import linestyle_lib, marker_lib, font_lib
from plot.canvas import Canvas
from plot.utilis import find_mpl_object, set_zorder
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.collections import Collection
from matplotlib.text import Text
from matplotlib.artist import Artist
from matplotlib.colors import to_hex

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

class DrawObject(TransparentToolButton):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.setIcon('draw.png')

        menu = Menu(parent=self)
        for text in ['rectangle','line','ellipse','text']:
            action = Action(text=text, parent=menu)
            action.triggered.connect(lambda _, text=text: self.setter(text))
            menu.addAction(action)

        self.setMenu(menu)

class Arrange(TransparentToolButton):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.setIcon('arrange.png')

        action_list = ['Bring to Front','Send to Back','Bring Forward','Send Backward']
        icon_list = ['bring_to_front.png','send_to_back.png','bring_forward.png','send_backward.png']

        menu = Menu(parent=self)
        for text, icon in zip(action_list, icon_list):
            action = Action(text=text, icon=icon, parent=menu)
            action.triggered.connect(lambda _, text=text: self.setter(text))
            menu.addAction(action)

        self.setMenu(menu)

class PlotView_ToolBar(QToolBar):
    sig_back_to_grScene = Signal()
    sig_ruler = Signal(bool)
    def __init__(self, canvas:Canvas, parent=None, *args, **kwargs): # parent is PlotView instance
        super().__init__(parent, *args, **kwargs)

        self.gid = None
        self.canvas = canvas
        self._parent = parent
        self.obj = []
        self.initActions()

        self.setFloatable(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
    
    def findobj(self) -> list[Artist]:
        return find_mpl_object(self.canvas.figure, gid=self.gid)
    
    def initActions(self):

        self.graphicscreen_btn = TransparentToolButton(
            icon="node.png",
            setter=self.sig_back_to_grScene.emit,
            layout=self
        )
        self.save_img = TransparentToolButton(
            icon='save_img.png',
            setter=self._parent.save_figure,
            layout=self
        )
        self.add_graph = TransparentToolButton(
            icon='curve.png',
            setter=self._parent.insertplot.show,
            layout=self
        )
        self.add_object = DrawObject(
            setter=self._parent.plot_visual.drawing_object,
            layout=self
        )
        self.arrange = Arrange(
            setter=self.set_zorder,
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

        self.labelfont = TransparentComboBox(
            items = font_lib,
            setter=self.set_fontname,
            layout=self
        )

        self.labelsize = TransparentDoubleSpinBox(
            minimum = 1, maximum = 100, singleStep = 2, decimals = 1,
            setter=self.set_fontsize,
            value=10,
            layout=self
        )
        
        self.labelstyle = CheckBox(
            setter=self.set_italic,
            text='Italic',
            layout=self
        )
        
        self.labelweight = CheckBox(
            setter=self.set_bold,
            text='Bold',
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
            if isinstance(self.obj[0], Collection):
                return to_hex(self.obj[0].get_edgecolor()[0])
            return to_hex(self.obj[0].get_edgecolor())
        except:
            self.get_facecolor()
    
    def set_edgecolor(self, value):
        if self.gid:
            for obj in self.obj:
                try: obj.set_edgecolor(value)
                except: obj.set_color(value)
            self._parent.update_plotlist()
            self.canvas.draw_idle()
            
    def get_facecolor(self):
        try:
            if isinstance(self.obj[0], Collection):
                return to_hex(self.obj[0].get_facecolor()[0])
            return to_hex(self.obj[0].get_facecolor())
        except:
            if isinstance(self.obj[0], Collection):
                return to_hex(self.obj[0].get_color()[0])
            return to_hex(self.obj[0].get_color())
    
    def set_facecolor(self, value):
        if self.gid:
            for obj in self.obj:
                try: obj.set_facecolor(value)
                except: pass
            self._parent.update_plotlist()
            self.canvas.draw_idle()
    
    def get_linewidth(self):
        try:
            return self.obj[0].get_linewidth()
        except Exception as e: print(e)
    
    def set_linewidth(self, value):
        if self.gid:
            for obj in self.obj:
                try: obj.set_linewidth(value)
                except: pass
            self.canvas.draw_idle()
    
    def get_linestyle(self):
        try:
            ls = self.obj[0].get_linestyle()
            if isinstance(self.obj[0], Line2D):
                return linestyle_lib[ls]
            elif isinstance(self.obj[0], Collection):
                if ls[0][1] == [3.7, 1.6]:
                    return "dashed"
                elif ls[0][1] == [6.4, 1.6, 1.0, 1.6]:
                    return "dashdot"
                elif ls[0][1] == [1.0, 1.65]:
                    return "dotted"
                else:
                    return "solid"
            return ls
        except Exception as e: print(e)
    
    def set_linestyle(self, value):
        if self.gid:
            for obj in self.obj:
                try: obj.set_linestyle(value)
                except: pass
            self.canvas.draw_idle()
    
    def get_marker(self):
        try:
            if not self.obj[0].get_marker():
                return "None"
            return marker_lib[self.obj[0].get_marker()]
        except Exception as e: print(e)
    
    def set_marker(self, value):
        if self.gid:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(value.lower())]
            for obj in self.obj:
                try: obj.set_marker(marker)
                except: pass
            self.canvas.draw_idle()     

    def set_fontname (self, font:str):
        if self.gid:
            for obj in self.obj:
                try: obj.set_fontname(font.lower())
                except: pass
            self.canvas.draw_idle()
    
    def get_fontname(self):
        try: 
            return self.obj[0].get_fontname()
        except Exception as e: print(e)

    def set_fontsize(self, value):
        if self.gid:
            for obj in self.obj:
                try: obj.set_fontsize(value)
                except: pass
            self.canvas.draw_idle()
    
    def get_fontsize(self):
        try: 
            return self.obj[0].get_fontsize()
        except Exception as e: print(e)
    
    def set_italic (self, bool):
        if self.gid:
            for obj in self.obj:
                try: 
                    if bool: obj.set_fontstyle('italic')
                    else: obj.set_fontstyle('normal')
                except: pass
            self.canvas.draw_idle()
    
    def get_italic (self):
        try:
            if self.obj[0].get_fontstyle() == 'normal':
                return False
            return True
        except Exception as e: print(e)

    def set_bold (self, bool):
        if self.gid:
            for obj in self.obj:
                try: 
                    if bool: obj.set_fontweight('bold')
                    else: obj.set_fontweight('normal')
                except: pass
            self.canvas.draw_idle()

    def get_bold (self):
        try:
            if self.obj[0].get_fontweight() == 'normal':
                return False
            return True
        except Exception as e: print(e)
    
    def set_zorder(self, value:str):
        set_zorder(self.canvas.figure, self.gid, value)
        self.canvas.draw_idle()
    
    def update(self, gid:str):
        self.gid = gid
        if gid:
            self.obj = self.findobj()
            if isinstance(self.obj[0], Text):
                self.edgecolor.set_value(self.get_edgecolor())
                self.labelfont.set_value(self.get_fontname())
                self.labelsize.set_value(self.get_fontsize())
                self.labelstyle.set_value(self.get_italic())
                self.labelweight.set_value(self.get_bold())
            elif isinstance(self.obj[0], Artist):
                self.edgecolor.set_value(self.get_edgecolor())
                self.facecolor.set_value(self.get_facecolor())
                self.linewidth.set_value(self.get_linewidth())
                self.linestyle.set_value(self.get_linestyle())
            if isinstance(self.obj[0], Line2D):
                self.marker.set_value(self.get_marker())
        else: self.obj = []

    
