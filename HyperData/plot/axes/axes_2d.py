from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QStackedLayout
from PySide6.QtGui import QColor
from ui.base_widgets.button import HTransparentComboBox, HToggle, SegmentedWidget
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from ui.base_widgets.color import HColorDropdown
from ui.base_widgets.frame import ScrollArea
from plot.utilis import find_mpl_object, grid
from plot.canvas import Canvas
from matplotlib import rcParams, colors, lines
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class Margin2D(ScrollArea):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        top = HTransparentDoubleSpinBox(
            label  = 'Margin top',
            label2 = "The position of the top edge",
            minimum = 0, maximum = 1, singleStep = 0.05,
            getter=self.get_top,
            setter=self.set_top,
            layout=self.vlayout
        )

        bottom = HTransparentDoubleSpinBox(
            label  = 'Margin bottom',
            label2 = 'The position of the bottom edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            getter=self.get_bottom,
            setter=self.set_bottom,
            layout=self.vlayout
        )

        left = HTransparentDoubleSpinBox(
            label  = 'Margin left',
            label2 ='The position of the left edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            setter=self.set_left,
            getter=self.get_left,
            layout=self.vlayout
        )

        right = HTransparentDoubleSpinBox(
            label  = 'Margin right',
            label2 = 'The position of the right edge',
            minimum = 0, maximum = 1, singleStep = 0.05,
            setter=self.set_right,
            getter=self.get_right,
            layout=self.vlayout
        )
    
    def set_top(self,value):
        self.canvas.figure.subplots_adjust(top=1-value)
        self.canvas.draw_idle()
    
    def get_top(self):
        return 1-self.canvas.figure.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.figure.subplots_adjust(bottom=1-value)
        self.canvas.draw_idle()
    
    def get_bottom(self):
        return 1-self.canvas.figure.subplotpars.bottom
    
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

class Grid2D(ScrollArea):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        self.visible = HToggle(
            label  = 'Visible',
            label2 = 'Whether to show the grid lines',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.coord = HTransparentComboBox(
            items=['bottom-left','bottom-right','top-left'],
            label='Axes',
            label2='Choose the base axes to visualize the grid lines',
            setter=self.set_coord,
            getter=self.get_coord,
            layout=self.vlayout
        )

        self.which = HTransparentComboBox(
            items = ['major','minor','both'],
            label  = 'Type',
            label2 = 'The grid lines to apply the changes on',
            setter=self.set_gridtype,
            getter=self.get_gridtype,
            layout=self.vlayout
        )

        self.axis = HTransparentComboBox(
            label  = 'Axis',
            label2 = 'The axis to apply the changes on',
            items = ['x','y','both'],
            getter=self.get_gridaxis,
            setter=self.set_gridaxis,
            layout=self.vlayout
        )

        self.linewidth = HTransparentDoubleSpinBox(
            label  = 'Line Width',
            label2 = 'Set the width of the grid lines',
            minimum = 0.1, maximum = 10, singleStep = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=self.vlayout
        )

        self.linestyle = HTransparentComboBox(
            label  = 'Line Style',
            label2 = 'Set the style of the grid lines',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=self.vlayout
        )

        self.color = HColorDropdown(
            label  = 'Line Color',
            label2 = 'Set the color of the grid',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.alpha = HTransparentSpinBox(
            label  = 'Transparency',
            label2 = 'Set the transparency of the grid lines',
            singleStep  = 10, maximum = 100, minimum = 0,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=self.vlayout
        )
    
    def findobj(self) -> list[lines.Line2D]:
        return find_mpl_object(
            self.canvas.figure, [lines.Line2D],
            gid='_grid', rule='exact'
        )
    
    def set_grid(self):
        try:
            self.canvas._config["grid"].update(
                visible   = self.visible.button.isChecked(),
                coord     = self.coord.button.currentText(),
                which     = self.which.button.currentText(), 
                axis      = self.axis.button.currentText(), 
            )

            grid(self.canvas.figure)
            self.canvas.draw_idle()

        except Exception as e:
            logger.exception(e)
    
    def set_visible(self, value:bool):
        self.set_grid()
    
    def get_visible(self) -> bool:
        return self.canvas._config["grid"]["visible"]

    def set_coord(self, value:str):
        self.set_grid()
    
    def get_coord(self) -> str:
        return self.canvas._config["grid"]["coord"] 

    def set_gridtype(self, value:str):
        self.set_grid()
    
    def get_gridtype (self) -> str:
        return self.canvas._config["grid"]["which"]
    
    def set_gridaxis(self, value:str):
        self.set_grid()

    def get_gridaxis (self):
        return self.canvas._config["grid"]["axis"]

    def set_alpha(self, value:int):
        try:
            for obj in self.findobj():
                obj.set_alpha(value/100)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def get_alpha(self):
        lines = self.findobj()
        if lines: 
            if lines[0].get_alpha():
                return int(lines[0].get_alpha()*100)
        return int(rcParams['grid.alpha']*100)
    
    def set_linewidth(self, value:float):
        try:
            for obj in self.findobj():
                obj.set_linewidth(value)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_linewidth(self) -> float:
        lines = self.findobj()
        if lines:
            return lines[0].get_linewidth()
        return rcParams['grid.linewidth']
    
    def set_linestyle(self, value:str):
        try:
            for obj in self.findobj():
                obj.set_linestyle(value)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)

    def get_linestyle (self) -> str:
        lines = self.findobj()
        if lines:
            return linestyle_lib[lines[0].get_linestyle()]
        return linestyle_lib[rcParams['grid.linestyle']]

    def set_color(self, color):
        try:
            for obj in self.findobj():
                obj.set_color(color)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
       
    def get_color(self) -> str:
        lines = self.findobj()
        if lines:
            return colors.to_hex(lines[0].get_color())
        return rcParams['grid.color']
    
class Pane2D(ScrollArea):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent=parent)

        self.canvas = canvas

        self.visible = HToggle(
            label  = 'Visible',
            label2 = 'Whether to show the color',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=self.vlayout
        )

        self.facecolor = HColorDropdown(
            label  = 'Color',
            label2 = 'Set the color of the Pane',
            getter=self.get_color,
            setter=self.set_color,
            layout=self.vlayout
        )

        self.edgecolor = HColorDropdown(
            label='Frame color',
            label2='Set the frame color of the Figure',
            getter=self.get_framecolor,
            setter=self.set_framecolor,
            layout=self.vlayout
        )

        self.alpha = HTransparentSpinBox(
            label  = 'Transparency',
            label2 = 'Set the transparency of the Pane',
            singleStep  = 10, minimum = 0, maximum = 100,
            setter=self.set_patch_alpha,
            getter=self.get_patch_alpha,
            layout=self.vlayout
        )
    
    def set_visible(self,value):
        self.canvas.axes.patch.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.canvas.axes.patch.get_visible()
    
    def set_color(self, color):
        self.canvas.axes.patch.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        try: return colors.to_hex(self.canvas.axes.patch.get_facecolor())
        except: return rcParams['axes.facecolor']

    def set_patch_alpha (self, value):
        self.canvas.axes.patch.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.canvas.axes.patch.get_alpha() != None: return int(self.canvas.axes.patch.get_alpha()*100)
        else: return 100
    
    def set_framecolor(self, color):
        self.canvas.figure.set_facecolor(color)
        self.canvas.draw_idle()
    
    def get_framecolor(self):
        return colors.to_hex(self.canvas.figure.get_facecolor())

class Axes2D(QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Axes settings")
        layout = QVBoxLayout(self)

        self.choose_axis = SegmentedWidget()
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='Plot size', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Grid', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Pane', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.choose_axis.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        margin = Margin2D(canvas, parent)
        self.stackedlayout.addWidget(margin)

        grid = Grid2D(canvas, parent)
        self.stackedlayout.addWidget(grid)

        pane = Pane2D(canvas, parent)
        self.stackedlayout.addWidget(pane)
