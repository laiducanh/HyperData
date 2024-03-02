from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox, Slider, DoubleSpinBox
from ui.base_widgets.color import ColorPicker
from plot.canvas import Canvas
from config.settings import linestyle_lib
import qfluentwidgets, matplotlib
from matplotlib.spines import Spine


class SpineBase (qfluentwidgets.CardWidget):
    def __init__(self, axis, canvas:Canvas):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        #layout.setContentsMargins(0,10,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.axis = axis
        self.canvas = canvas
        self.obj = self.find_object()

        visible = Toggle(text='spine visible')
        visible.button.checkedChanged.connect(self.set_visible)
        visible.button.setChecked(self.get_visible())
        layout.addWidget(visible)

        color = ColorPicker(text='color',title='color')
        color.button.colorChanged.connect(self.set_color)
        color.button.setColor(self.get_color())
        layout.addWidget(color)

        alpha = Slider(min=0,max=100,step=1,text='transparent')
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)

        linestyle = ComboBox(text='line style',items=linestyle_lib.values())
        linestyle.button.currentTextChanged.connect(self.set_linestyle)
        linestyle.button.setCurrentText(self.get_linestyle())
        layout.addWidget(linestyle)

        linewidth = DoubleSpinBox(text='line width',min=0,max=20,step=0.5)
        linewidth.button.valueChanged.connect(self.set_linewidth)
        linewidth.button.setValue(self.get_linewidth())
        layout.addWidget(linewidth)
    
    def find_object (self) -> list:
        list_obj = list()
        for obj in self.canvas.fig.findobj(match=Spine):
            if obj.spine_type == self.axis:
                list_obj.append(obj)
        return list_obj

    def set_visible (self, value:bool):
        for obj in self.obj:
            obj.set_visible(value)
        self.canvas.draw()
    
    def get_visible (self):
        return self.obj[0].get_visible()    
    
    def set_alpha (self, value):
        for obj in self.obj:
            obj.set_alpha(float(value/100))
        self.canvas.draw()
    
    def get_alpha(self):
        if self.obj[0].get_alpha() == None:
            return 100
        return self.obj[0].get_alpha()*100
    
    def set_linestyle(self, value):
        for obj in self.obj:
            obj.set_linestyle(value.lower())
        self.canvas.draw()
    
    def get_linestyle(self):
        return self.obj[0].get_linestyle().title()

    def set_linewidth(self, value):
        for obj in self.obj:
            obj.set_linewidth(value)
        self.canvas.draw()
    
    def get_linewidth (self):
        return self.obj[0].get_linewidth()

    def set_color(self, color):
        for obj in self.obj:
            obj.set_color(color.name())
        self.canvas.draw()
    
    def get_color(self):
        return matplotlib.colors.rgb2hex(self.obj[0].get_edgecolor())

class SpineWidget2D (QWidget):
    def __init__(self, canvas:Canvas):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)
        self.canvas = canvas

        self.choose_axis = qfluentwidgets.SegmentedWidget()
        self.layout.addWidget(self.choose_axis)

        self.choose_axis.addItem(routeKey='bottom', text='Bottom',
                            onClick=lambda: self.choose_axis_func('bottom'))
        self.choose_axis.addItem(routeKey='left', text='Left',
                            onClick=lambda: self.choose_axis_func('left'))
        self.choose_axis.addItem(routeKey='top', text='Top',
                            onClick=lambda: self.choose_axis_func('top'))
        self.choose_axis.addItem(routeKey='right', text='Right',
                            onClick=lambda: self.choose_axis_func('right'))

        self.stackedlayout = QStackedLayout()
        self.layout.addLayout(self.stackedlayout)

        #self.layout.addStretch(1000)
    
    def choose_axis_func (self, axis:str):
        self.choose_axis.setCurrentItem(axis)
        if axis == 'bottom': 
            if not hasattr(self, 'bot'):
                self.bot = SpineBase('bottom',self.canvas)
                self.stackedlayout.addWidget(self.bot)
            self.stackedlayout.setCurrentWidget(self.bot)
        elif axis == 'left': 
            if not hasattr(self,'left'):
                self.left = SpineBase('left',self.canvas)
                self.stackedlayout.addWidget(self.left)
            self.stackedlayout.setCurrentWidget(self.left)
        elif axis == 'top': 
            if not hasattr(self, 'top'):
                self.top = SpineBase('top',self.canvas)
                self.stackedlayout.addWidget(self.top)
            self.stackedlayout.setCurrentWidget(self.top)
        elif axis == 'right': 
            if not hasattr(self,'right'):
                self.right = SpineBase('right',self.canvas)
                self.stackedlayout.addWidget(self.right)
            self.stackedlayout.setCurrentWidget(self.right)

class SpineWidget3D (QWidget):
    sig = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10,0,10,15)

        choose_axis = qfluentwidgets.SegmentedWidget()
        self.layout.addWidget(choose_axis)

        choose_axis.addItem(routeKey='x', text='X Axis',
                            onClick=lambda: self.stackedlayout.setCurrentIndex(0))
        choose_axis.addItem(routeKey='y', text='Y Axis',
                            onClick=lambda: self.stackedlayout.setCurrentIndex(1))
        choose_axis.addItem(routeKey='z', text='Z Axis',
                            onClick=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        self.layout.addLayout(self.stackedlayout)
        self.bot = SpineBase('x3d')
        self.bot.sig.connect(lambda: self.sig.emit())
        self.stackedlayout.addWidget(self.bot)
        self.left = SpineBase('y3d')
        self.left.sig.connect(lambda: self.sig.emit())
        self.stackedlayout.addWidget(self.left)
        self.top = SpineBase('z3d')
        self.top.sig.connect(lambda: self.sig.emit())
        self.stackedlayout.addWidget(self.top)