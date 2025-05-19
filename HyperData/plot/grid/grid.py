from PySide6.QtCore import QSize
from PySide6.QtWidgets import QTreeWidgetItem, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtGui import QColor
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import Slider, DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.list import TreeWidget
from plot.utilis import TreeWidgetItem
from plot.canvas import Canvas
from matplotlib import lines, rcParams
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class PlotSize2D (TreeWidgetItem):
    def __init__(self, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.setText(0, 'Plot Size')
        self.canvas = canvas

        child = QTreeWidgetItem(self)
        top = DoubleSpinBox(
            text  = 'Margin top',
            text2 = "The position of the top edge",
            min = 0, max = 1, step = 0.05
        )
        top.button.valueChanged.connect(self.set_top)
        top.button.setValue(self.get_top())
        treeview.setItemWidget(child, 0, top)

        child = QTreeWidgetItem(self)
        bottom = DoubleSpinBox(
            text  = 'Margin bottom',
            text2 = 'The position of the bottom edge',
            min = 0, max = 1, step = 0.05
        )
        bottom.button.valueChanged.connect(self.set_bottom)
        bottom.button.setValue(self.get_bottom())
        treeview.setItemWidget(child, 0, bottom)

        child = QTreeWidgetItem(self)
        left = DoubleSpinBox(
            text  = 'Margin left',
            text2 ='The position of the left edge',
            min = 0, max = 1, step = 0.05
        )
        left.button.valueChanged.connect(self.set_left)
        left.button.setValue(self.get_left())
        treeview.setItemWidget(child, 0, left)

        child = QTreeWidgetItem(self)
        right = DoubleSpinBox(
            text  = 'Margin right',
            text2 = 'The position of the right edge',
            min = 0, max = 1, step = 0.05
        )
        right.button.valueChanged.connect(self.set_right)
        right.button.setValue(self.get_right())
        treeview.setItemWidget(child, 0, right)
    
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

class Grid2D (TreeWidgetItem):
    def __init__(self, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.setText(0, 'Grid')
        self.setExpanded(True)

        self.canvas = canvas

        child = QTreeWidgetItem(self)
        self.visible = Toggle(
            text  = 'Visible',
            text2 = 'Whether to show the grid lines'
        )
        self.visible.button.checkedChanged.connect(self.set_grid)
        self.visible.button.setChecked(self.get_visible())
        treeview.setItemWidget(child, 0, self.visible)

        child = QTreeWidgetItem(self)
        self.which = ComboBox(
            items = ['Major','Minor','Both'],
            text  = 'Type',
            text2 = 'The grid lines to apply the changes on'
        )
        self.which.button.currentTextChanged.connect(self.set_gridtype)
        self.which.button.setCurrentText(self.get_gridtype())
        treeview.setItemWidget(child, 0, self.which)

        child = QTreeWidgetItem(self)
        self.axis = ComboBox(
            text  = 'Axis',
            text2 = 'The axis to apply the changes on',
            items = ['X','Y','Both']
        )
        self.axis.button.currentTextChanged.connect(self.set_gridaxis)
        self.axis.button.setCurrentText(self.get_gridaxis())
        treeview.setItemWidget(child, 0, self.axis)

        child = QTreeWidgetItem(self)
        self.linewidth = DoubleSpinBox(
            text  = 'Line Width',
            text2 = 'Set the width of the grid lines',
            min = 0.1, max = 10, step = 0.5
        )
        self.linewidth.button.valueChanged.connect(self.set_linewidth)
        self.linewidth.button.setValue(self.get_linewidth())
        treeview.setItemWidget(child, 0, self.linewidth)

        child = QTreeWidgetItem(self)
        self.linestyle = ComboBox(
            text  = 'Line Style',
            text2 = 'Set the style of the grid lines',
            items = linestyle_lib.values()
        )
        self.linestyle.button.currentTextChanged.connect(self.set_linestyle)
        self.linestyle.button.setCurrentText(self.get_linestyle())
        treeview.setItemWidget(child, 0, self.linestyle)

        child = QTreeWidgetItem(self)
        self.color = ColorDropdown(
            text  = 'Line Color',
            text2 = 'Set the color of the grid',
            color = self.get_color(),
        )
        self.color.button.colorChanged.connect(self.set_color)
        treeview.setItemWidget(child, 0, self.color)

        child = QTreeWidgetItem(self)
        self.alpha = Slider(
            text  = 'Transparency',
            text2 = 'Set the transparency of the grid lines'
        )
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self.alpha.button.setValue(self.get_alpha())
        treeview.setItemWidget(child, 0, self.alpha)
    
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
    
    def get_visible(self):
        for obj in self.canvas.fig.findobj(match=lines.Line2D):
            if obj.get_gid() and '_grid' in obj.get_gid():
                return obj.get_visible()
        return False

    def set_gridtype(self, value:str):
        rcParams['axes.grid.which'] = value.lower()
        self.canvas.draw_idle()
    
    def get_gridtype (self):
        return rcParams['axes.grid.which'].title()
    
    def set_gridaxis(self, value:str):
        rcParams['axes.grid.axis'] = value.lower()
        self.set_grid()

    def get_gridaxis (self):
        return rcParams['axes.grid.axis'].title()

    def set_alpha(self, value:int):
        rcParams['grid.alpha'] = value/100
        self.set_grid()

    def get_alpha(self):
        return int(rcParams['grid.alpha']*100)
    
    def set_linewidth(self, value:float):
        rcParams['grid.linewidth'] = value
        self.set_grid()
    
    def get_linewidth(self) -> float:
        return rcParams['grid.linewidth']
    
    def set_linestyle(self, value:str):
        linestyle_lib[rcParams['grid.linestyle']] = value
        self.set_grid()

    def get_linestyle (self) -> str:
        return linestyle_lib[rcParams['grid.linestyle']].lower()

    def set_color(self, color):
        rcParams['grid.color'] = color
        self.set_grid()
       
    def get_color(self) -> str:
        return rcParams['grid.color']
    
class Pane (TreeWidgetItem):
    def __init__(self, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.setText(0, 'Pane')
        self.setExpanded(True)

        self.canvas = canvas

        child = QTreeWidgetItem(self)
        self.visible = Toggle(
            text  = 'Visible',
            text2 = 'Whether to show the color'
        )
        self.visible.button.checkedChanged.connect(self.set_visible)
        self.visible.button.setChecked(self.get_visible())
        treeview.setItemWidget(child, 0, self.visible)
    
        child = QTreeWidgetItem(self)
        self.facecolor = ColorDropdown(
            text  = 'Color',
            text2 = 'Set the color of the Pane',
            color = self.get_color())
        self.facecolor.button.colorChanged.connect(self.set_color)
        treeview.setItemWidget(child, 0, self.facecolor)

        child = QTreeWidgetItem(self)
        self.alpha = Slider(
            text  = 'Transparency',
            text2 = 'Set the transparency of the Pane')
        self.alpha.button.valueChanged.connect(self.set_patch_alpha)
        self.alpha.button.setValue(self.get_patch_alpha())
        treeview.setItemWidget(child, 0, self.alpha)

    def set_visible(self,value):
        self.canvas.axes.patch.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible(self):
        return self.canvas.axes.patch.get_visible()
    
    def set_color(self, color):
        self.canvas.axes.patch.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        try: return QColor(self.canvas.axes.patch.get_facecolor())
        except: return QColor(rcParams['axes.facecolor'])

    def set_patch_alpha (self, value):
        self.canvas.axes.patch.set_alpha(value/100)
        self.canvas.draw_idle()
    
    def get_patch_alpha (self):
        if self.canvas.axes.patch.get_alpha(): 
            return int(self.canvas.axes.patch.get_alpha()*100)
        return 100

class Grid (QMainWindow):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
    # Layout
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
    
    # Create a QTreeWidget
        self.tree = TreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setUniformRowHeights(True)
        plotsize = PlotSize2D(canvas, self.tree)
        grid = Grid2D(canvas, self.tree)
        pane = Pane(canvas, self.tree)
        layout.addWidget(self.tree)