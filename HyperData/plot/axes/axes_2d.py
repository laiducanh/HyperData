from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QStackedLayout
from ui.base_widgets.button import TransparentComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from matplotlib import lines, rcParams
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class Margin2D (QWidget):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.canvas = canvas

        top = TransparentDoubleSpinBox(
            text  = 'Margin top',
            text2 = "The position of the top edge",
            min = 0, max = 1, step = 0.05,
            getter=self.get_top,
            setter=self.set_top,
            layout=layout
        )

        bottom = TransparentDoubleSpinBox(
            text  = 'Margin bottom',
            text2 = 'The position of the bottom edge',
            min = 0, max = 1, step = 0.05,
            getter=self.get_bottom,
            setter=self.set_bottom,
            layout=layout
        )

        left = TransparentDoubleSpinBox(
            text  = 'Margin left',
            text2 ='The position of the left edge',
            min = 0, max = 1, step = 0.05,
            setter=self.set_left,
            getter=self.get_left,
            layout=layout
        )

        right = TransparentDoubleSpinBox(
            text  = 'Margin right',
            text2 = 'The position of the right edge',
            min = 0, max = 1, step = 0.05,
            setter=self.set_right,
            getter=self.get_right,
            layout=layout
        )
    
    def set_top(self,value):
        self.canvas.fig.subplots_adjust(top=value)
        self.canvas.draw_idle()
    
    def get_top(self):
        return self.canvas.fig.subplotpars.top
    
    def set_bottom(self,value):
        self.canvas.fig.subplots_adjust(bottom=value)
        self.canvas.draw_idle()
    
    def get_bottom(self):
        return self.canvas.fig.subplotpars.bottom
    
    def set_left(self,value):
        self.canvas.fig.subplots_adjust(left=value)
        self.canvas.draw_idle()
    
    def get_left(self):
        return self.canvas.fig.subplotpars.left
    
    def set_right(self,value):
        self.canvas.fig.subplots_adjust(right=value)
        self.canvas.draw_idle()
    
    def get_right(self):
        return self.canvas.fig.subplotpars.right

class Grid2D (QWidget):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.visible = Toggle(
            text  = 'Visible',
            text2 = 'Whether to show the grid lines',
            setter=self.set_grid,
            getter=self.get_visible,
            layout=layout
        )

        self.which = TransparentComboBox(
            items = ['Major','Minor','Both'],
            text  = 'Type',
            text2 = 'The grid lines to apply the changes on',
            setter=self.set_gridtype,
            getter=self.get_gridtype,
            layout=layout
        )

        self.axis = TransparentComboBox(
            text  = 'Axis',
            text2 = 'The axis to apply the changes on',
            items = ['X','Y','Both'],
            getter=self.get_gridaxis,
            setter=self.set_gridaxis,
            layout=layout
        )

        self.linewidth = TransparentDoubleSpinBox(
            text  = 'Line Width',
            text2 = 'Set the width of the grid lines',
            min = 0.1, max = 10, step = 0.5,
            setter=self.set_linewidth,
            getter=self.get_linewidth,
            layout=layout
        )

        self.linestyle = TransparentComboBox(
            text  = 'Line Style',
            text2 = 'Set the style of the grid lines',
            items = linestyle_lib.values(),
            getter=self.get_linestyle,
            setter=self.set_linestyle,
            layout=layout
        )

        self.color = ColorDropdown(
            text  = 'Line Color',
            text2 = 'Set the color of the grid',
            getter=self.get_color,
            setter=self.set_color,
            layout=layout
        )

        self.alpha = TransparentDoubleSpinBox(
            text  = 'Transparency',
            text2 = 'Set the transparency of the grid lines',
            step  = 10,
            setter=self.set_alpha,
            getter=self.get_alpha,
            layout=layout
        )
    
    def set_grid(self):
        try:
        # Need to redraw grid after any changes
            self.canvas.axes.grid(visible=False)
            if self.visible.button.isChecked():
                self.canvas.axes.grid(
                    which     = self.which.button.currentText().lower(), 
                    axis      = self.axis.button.currentText().lower(), 
                    alpha     = self.alpha.button.value()/100,
                    linewidth = self.linewidth.button.value(),
                    linestyle = self.linestyle.button.currentText().lower(), 
                    color     = self.color.button.color.name(),
                    gid       = "_grid"
                )

        # Idle Redraw
            self.canvas.draw_idle()

        except Exception as e:
            logger.exception(e)
    
    def get_visible(self) -> bool:
        for obj in find_mpl_object(self.canvas.fig, [lines.Line2D], gid='_grid'):
            return obj.get_visible()
        return False

    def set_gridtype(self, value:str):
        #rcParams['axes.grid.which'] = value.lower()
        self.set_grid()
    
    def get_gridtype (self) -> str:
        return rcParams['axes.grid.which'].title()
    
    def set_gridaxis(self, value:str):
        #rcParams['axes.grid.axis'] = value.lower()
        self.set_grid()

    def get_gridaxis (self):
        return rcParams['axes.grid.axis'].title()

    def set_alpha(self, value:int):
        #rcParams['grid.alpha'] = value/100
        self.set_grid()

    def get_alpha(self):
        return int(rcParams['grid.alpha']*100)
    
    def set_linewidth(self, value:float):
        #rcParams['grid.linewidth'] = value
        self.set_grid()
    
    def get_linewidth(self) -> float:
        return rcParams['grid.linewidth']
    
    def set_linestyle(self, value:str):
        #linestyle_lib[rcParams['grid.linestyle']] = value
        self.set_grid()

    def get_linestyle (self) -> str:
        return linestyle_lib[rcParams['grid.linestyle']].lower()

    def set_color(self, color):
        #rcParams['grid.color'] = color
        self.set_grid()
       
    def get_color(self) -> str:
        return rcParams['grid.color']
    
class Pane2D (QWidget):
    def __init__(self, canvas: Canvas, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        self.canvas = canvas

        self.visible = Toggle(
            text  = 'Visible',
            text2 = 'Whether to show the color',
            setter=self.set_visible,
            getter=self.get_visible,
            layout=layout
        )

        self.facecolor = ColorDropdown(
            text  = 'Color',
            text2 = 'Set the color of the Pane',
            getter=self.get_color,
            setter=self.set_color,
            layout=layout
        )

        self.alpha = TransparentDoubleSpinBox(
            text  = 'Transparency',
            text2 = 'Set the transparency of the Pane',
            step  = 10,
            setter=self.set_patch_alpha,
            getter=self.get_patch_alpha,
            layout=layout
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
        try: return self.canvas.axes.patch.get_color()
        except: return rcParams['axes.facecolor']

    def set_patch_alpha (self, value):
        self.canvas.axes.patch.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.canvas.axes.patch.get_alpha() != None: return int(self.canvas.axes.patch.get_alpha()*100)
        else: return 100

class Axes2D (QDialog):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Axes settings")
        layout = QVBoxLayout(self)

        self.choose_axis = SegmentedWidget()
        layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='Margins', func=lambda: self.stackedlayout.setCurrentIndex(0))
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
