from PySide6.QtWidgets import QVBoxLayout, QWidget, QDialog, QStackedLayout
from ui.base_widgets.button import TransparentComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import ScrollArea
from plot.canvas import Canvas
from matplotlib import colors
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class Margin3D(ScrollArea):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        top = TransparentDoubleSpinBox(
            text  = 'Margin top',
            text2 = "The position of the top edge",
            min = 0, max = 1, step = 0.05,
            getter=self.get_top,
            setter=self.set_top,
            layout=self.vlayout
        )

        bottom = TransparentDoubleSpinBox(
            text  = 'Margin bottom',
            text2 = 'The position of the bottom edge',
            min = 0, max = 1, step = 0.05,
            getter=self.get_bottom,
            setter=self.set_bottom,
            layout=self.vlayout
        )

        left = TransparentDoubleSpinBox(
            text  = 'Margin left',
            text2 ='The position of the left edge',
            min = 0, max = 1, step = 0.05,
            setter=self.set_left,
            getter=self.get_left,
            layout=self.vlayout
        )

        right = TransparentDoubleSpinBox(
            text  = 'Margin right',
            text2 = 'The position of the right edge',
            min = 0, max = 1, step = 0.05,
            setter=self.set_right,
            getter=self.get_right,
            layout=self.vlayout
        )
    
    def set_top(self,value):
        self.canvas.figure.subplots_adjust(top=value)
        self.canvas.draw_idle()
    
    def get_top(self):
        return self.canvas.figure.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.figure.subplots_adjust(bottom=value)
        self.canvas.draw_idle()
    
    def get_bottom(self):
        return self.canvas.figure.subplotpars.bottom
    
    def set_left(self,value):
        self.canvas.figure.subplots_adjust(left=value)
        self.canvas.draw_idle()
    
    def get_left(self):
        return self.canvas.figure.subplotpars.left
    
    def set_right(self,value):
        self.canvas.figure.subplots_adjust(right=value)
        self.canvas.draw_idle()
    
    def get_right(self):
        return self.canvas.figure.subplotpars.right
    
class Grid3D(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas
        
        if   axis == 'XY Pane': self.axinfo = self.canvas.axes.zaxis._axinfo['grid']
        elif axis == 'YZ Pane': self.axinfo = self.canvas.axes.xaxis._axinfo['grid']
        elif axis == 'XZ Pane': self.axinfo = self.canvas.axes.yaxis._axinfo['grid']

        self.linewidth = TransparentDoubleSpinBox(
            text  = 'Line Width',
            text2 = 'Set the width of the grid lines',
            min = 0.1, max = 10, step = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

        self.linestyle = TransparentComboBox(
            text  = 'Line Style',
            text2 = 'Set the style of the grid lines',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=self.vlayout
        )

        self.color = ColorDropdown(
            text  = 'Line Color',
            text2 = 'Set the color of the grid',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

    def set_linewidth(self, value:float):
        self.axinfo.update(linewidth = value)
        self.canvas.draw_idle()
    
    def get_linewidth(self) -> float:
        return self.axinfo.get("linewidth")
    
    def set_linestyle(self, value:str):
        self.axinfo.update(linestyle = value)
        self.canvas.draw_idle()

    def get_linestyle (self) -> str:
        return self.axinfo.get('linestyle')

    def set_color(self, color):
        self.axinfo.update(color = color)
        self.canvas.draw_idle()
       
    def get_color(self) -> str:
        return self.axinfo.get('color')


class Pane3D(ScrollArea):
    def __init__(self, axis:str, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        if   axis == 'XY Pane': self.axis = self.canvas.axes.zaxis.pane
        elif axis == 'XZ Pane': self.axis = self.canvas.axes.yaxis.pane
        elif axis == 'YZ Pane': self.axis = self.canvas.axes.xaxis.pane

        self.visible = Toggle(
            text  = 'Visible',
            text2 = 'Whether to show the color',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.facecolor = ColorDropdown(
            text  = 'Color',
            text2 = 'Set the color of the Pane',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.alpha = TransparentDoubleSpinBox(
            text  = 'Transparency',
            text2 = 'Set the transparency of the Pane',
            step  = 10,
            setter=self.set_patch_alpha,
            getter=self.get_patch_alpha,
            layout=self.vlayout
        )
    
    def set_visible(self, value:bool):
        self.axis.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.axis.get_visible()
    
    def set_color(self, color):
        self.axis.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return colors.rgb2hex(self.axis.get_facecolor())

    def set_patch_alpha (self, value):
        self.axis.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.axis.get_alpha(): return int(self.axis.get_alpha()*100)
        else: return 100


class Axes3D(QDialog):
    def __init__(self, axis:str, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"{axis} settings")
        layout = QVBoxLayout(self)

        self.choose_axis = SegmentedWidget()
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='Margins', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Grid', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Pane', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        margin = Margin3D(canvas, parent)
        self.stackedlayout.addWidget(margin)

        grid = Grid3D(axis, canvas, parent)
        self.stackedlayout.addWidget(grid)

        pane = Pane3D(axis, canvas, parent)
        self.stackedlayout.addWidget(pane)