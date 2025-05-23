from PySide6.QtCore import QSize
from PySide6.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QTreeWidgetItem
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import Slider, DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.window import ProgressDialog
from ui.base_widgets.list import TreeWidget, TreeWidgetItem
from plot.canvas import Canvas
import matplotlib
from config.settings import linestyle_lib, GLOBAL_DEBUG, logger

DEBUG = False

class PlotSize3D (TreeWidgetItem):
    def __init__(self, canvas: Canvas, treeview:TreeWidget):
        super().__init__(treeview)

        self.setText(0, 'Plot Size')
        self.setExpanded(True)

        self.canvas = canvas

        child = QTreeWidgetItem(self)
        top = DoubleSpinBox(
            text='Margin top',
            text2="The position of the top edge",
            min=0,max=1,step=0.05
        )
        top.button.valueChanged.connect(self.set_top)
        top.button.setValue(self.get_top())
        treeview.setItemWidget(child, 0, top)

        child = QTreeWidgetItem(self)
        bottom = DoubleSpinBox(
            text='Margin bottom',
            text2='The position of the bottom edge',
            min=0,max=1,step=0.05
        )
        bottom.button.valueChanged.connect(self.set_bottom)
        bottom.button.setValue(self.get_bottom())
        treeview.setItemWidget(child, 0, bottom)

        child = QTreeWidgetItem(self)
        left = DoubleSpinBox(
            text='Margin left',
            text2='The position of the left edge',
            min=0,max=1,step=0.05
        )
        left.button.valueChanged.connect(self.set_left)
        left.button.setValue(self.get_left())
        treeview.setItemWidget(child, 0, left)

        child = QTreeWidgetItem(self)
        right = DoubleSpinBox(
            text='Margin right',
            text2='The position of the right edge',
            min=0,max=1,step=0.05
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

class Grid3D (QMainWindow):
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
        plotsize = PlotSize3D(canvas, self.tree)
        # grid = Grid2D(canvas, self.tree)
        # pane = Pane(canvas, self.tree)
        layout.addWidget(self.tree)