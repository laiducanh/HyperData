from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel
from PySide6.QtCore import Qt
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.spinbox import SpinBox, Slider, DoubleSpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import Frame
from plot.canvas import Canvas
from config.settings import linestyle_lib, marker_lib, logger
import matplotlib
from matplotlib import spines, lines, axis
from typing import List
from plot.utilis import find_mpl_object

class SpineBase (Frame):
    def __init__(self, axis, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,10,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()
        self.first_show = True
    
    def initUI(self):

        visible = Toggle(text='Spine visible')
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        self.vlayout.addWidget(visible)

        arrow = ComboBox(text='Arrow Style',items=marker_lib.values())
        arrow.button.setCurrentText(self.get_arrow())
        arrow.button.currentTextChanged.connect(self.set_arrow)
        self.vlayout.addWidget(arrow)

        color = ColorDropdown(text='Spine color')
        color.button.colorChanged.connect(self.set_color)
        color.button.setColor(self.get_color())
        self.vlayout.addWidget(color)

        arrowcolor = ColorDropdown(text="Arrow color")
        arrowcolor.button.colorChanged.connect(self.set_arrowcolor)
        arrowcolor.button.setColor(self.get_arrowcolor())
        self.vlayout.addWidget(arrowcolor)

        alpha = Slider(min=0,max=100,step=1,text='Transparent')
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        self.vlayout.addWidget(alpha)

        linestyle = ComboBox(text='Line style',items=linestyle_lib.values())
        linestyle.button.currentTextChanged.connect(self.set_linestyle)
        linestyle.button.setCurrentText(self.get_linestyle())
        self.vlayout.addWidget(linestyle)

        linewidth = DoubleSpinBox(text='Line width',min=0,max=20,step=0.5)
        linewidth.button.valueChanged.connect(self.set_linewidth)
        linewidth.button.setValue(self.get_linewidth())
        self.vlayout.addWidget(linewidth)
    
    def find_object (self) -> lines.Line2D:
        return find_mpl_object(
            self.canvas.fig, 
            match=[axis.Axis], 
            gid=self.axis
        )[0].line

    def set_visible (self, value:bool):
        self.obj.set_visible(value)
        self.canvas.draw_idle()
    
    def get_visible (self):
        return self.obj.get_visible()  

    def set_arrow(self, marker):
        try:
            marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
            self.obj.set_marker(marker)
            self.obj.set_markevery((1,1))
        except Exception as e:
            logger.exception(e)
        self.canvas.draw_idle()
    
    def get_arrow(self):
        return marker_lib[self.obj.get_marker()]
    
    def set_alpha (self, value):
        self.obj.set_alpha(float(value/100))
        self.canvas.draw_idle()
    
    def get_alpha(self):
        if self.obj.get_alpha() == None:
            return 100
        return self.obj.get_alpha()*100
    
    def set_linestyle(self, value):
        self.obj.set_linestyle(value)
        self.canvas.draw_idle()
    
    def get_linestyle(self):
        return self.obj.get_linestyle()

    def set_linewidth(self, value):
        self.obj.set_linewidth(value)
        self.canvas.draw_idle()
    
    def get_linewidth (self):
        return self.obj.get_linewidth()

    def set_color(self, color):
        self.obj.set_color(color)
        self.canvas.draw_idle()
    
    def get_color(self):
        return matplotlib.colors.rgb2hex(self.obj.get_color())

    def set_arrowcolor(self, color):
        self.obj.set_markerfacecolor(color)
        self.canvas.draw_idle()
    
    def get_arrowcolor(self):
        return matplotlib.colors.rgb2hex(self.obj.get_markerfacecolor())

    def showEvent(self, a0):
        if self.first_show:
            self.initUI()
            self.first_show = False
        return super().showEvent(a0)

    def paintEvent(self, e):
        self.obj = self.find_object()
        return super().paintEvent(e)

class Spine3D (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)
        self.canvas = canvas

        self.choose_axis = SegmentedWidget()
        self.layout.addWidget(self.choose_axis)

        self.choose_axis.addButton(text='X3D', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_axis.addButton(text='Y3D', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_axis.addButton(text='Z3D', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        self.layout.addLayout(self.stackedlayout)

        self.bot = SpineBase('x3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.bot)
        self.left = SpineBase('y3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.left)
        self.top = SpineBase('z3d',self.canvas, parent)
        self.stackedlayout.addWidget(self.top)
    