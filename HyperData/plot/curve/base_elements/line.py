from PyQt6.QtGui import QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, Slider, SpinBox
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.text import StrongBodyLabel
from config.settings import linestyle_lib, marker_lib
from plot.canvas import Canvas
from matplotlib.lines import Line2D

class LineBase (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid:str, canvas:Canvas,parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        #self.setStyleSheet('LineBase {background-color:white}')
        layout.setContentsMargins(0,0,0,0)   

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()        

        layout.addWidget(StrongBodyLabel('Line'))
        layout.addWidget(SeparateHLine())
        
        self.linestyle = ComboBox(text='line style',items=linestyle_lib.values())
        self.linestyle.button.setCurrentText(self.get_linestyle())
        self.linestyle.button.currentTextChanged.connect(self.set_linestyle)
        layout.addWidget(self.linestyle)

        self.linewidth = DoubleSpinBox(text='line width',min=0,max=10,step=0.5)
        self.linewidth.button.setValue(self.get_linewidth())
        self.linewidth.button.valueChanged.connect(self.set_linewidth)
        layout.addWidget(self.linewidth)

        self.color = ColorDropdown(text='line color',color=self.get_color(),parent=parent)
        self.color.button.setColor(self.get_color())
        self.color.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.color)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(self.alpha)

        layout.addWidget(StrongBodyLabel('Marker'))
        layout.addWidget(SeparateHLine())

        self.marker = ComboBox(text='marker style',items=marker_lib.values())
        self.marker.button.setCurrentText(self.get_marker())
        self.marker.button.currentTextChanged.connect(self.set_marker)
        layout.addWidget(self.marker)

        self.markevery = SpinBox(text='mark every',min=1,max=100,step=1)
        self.markevery.button.setValue(self.get_markevery())
        self.markevery.button.valueChanged.connect(self.set_markevery)
        layout.addWidget(self.markevery)

        self.markersize = DoubleSpinBox(text='marker size',min=0,max=20,step=2)
        self.markersize.button.setValue(self.get_markersize())
        self.markersize.button.valueChanged.connect(self.set_markersize)
        layout.addWidget(self.markersize)

        self.markeredgewidth = DoubleSpinBox(text='marker edge width',min=0,max=5,step=0.5)
        self.markeredgewidth.button.setValue(self.get_markeredgewidth())
        self.markeredgewidth.button.valueChanged.connect(self.set_markeredgewidth)
        layout.addWidget(self.markeredgewidth)

        self.markerfacecolor = ColorDropdown(text='marker face color',color=self.get_markerfacecolor(),parent=parent)
        self.markerfacecolor.button.setColor(self.get_markerfacecolor())
        self.markerfacecolor.button.colorChanged.connect(self.set_markerfacecolor)
        layout.addWidget(self.markerfacecolor)

        self.markeredgecolor = ColorDropdown(text='marker edge color',color=self.get_markeredgecolor(),parent=parent)
        self.markeredgecolor.button.setColor(self.get_markeredgecolor())
        self.markeredgecolor.button.colorChanged.connect(self.set_markeredgecolor)
        layout.addWidget(self.markeredgecolor)
    
    def find_object (self) -> Line2D:
        for obj in self.canvas.fig.findobj(match=Line2D):
            if obj._gid != None and obj._gid == self.gid:
                return obj

    def set_linestyle(self, value):
        self.obj.set_linestyle(value.lower())
        self.sig.emit()
    
    def get_linestyle(self):
        return self.obj.get_linestyle().title()
    
    def set_linewidth(self, value):
        self.obj.set_linewidth(value)
        self.sig.emit()
    
    def get_linewidth (self):
        return self.obj.get_linewidth()
    
    def set_alpha(self, value):
        self.obj.set_alpha(float(value/100))
        self.sig.emit()
    
    def get_alpha (self):
        if self.obj.get_alpha() == None:
            return 100
        return int(self.obj.get_alpha()*100)

    def set_color(self, color):
        self.obj.set_color(color)
        self.sig.emit()
    
    def get_color(self):
        return self.obj.get_color()
    
    def set_marker (self, marker):
        marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
        self.obj.set_marker(marker)
        self.sig.emit()
    
    def get_marker(self):
        if self.obj.get_marker() == None:
            return "None"
        return self.obj.get_marker()

    def set_markevery(self, value):
        self.obj.set_markevery(value)
        self.sig.emit()
    
    def get_markevery(self):
        if self.obj.get_markevery() == None:
            return 1
        return self.obj.get_markevery()

    def set_markersize (self, value):
        self.obj.set_markersize(value)
        self.sig.emit()
    
    def get_markersize(self):
        return self.obj.get_markersize()

    def set_markeredgewidth(self, value):
        self.obj.set_markeredgewidth(value)
        self.sig.emit()
    
    def get_markeredgewidth(self):
        return self.obj.get_markeredgewidth()

    def set_markerfacecolor(self, color):
        self.obj.set_markerfacecolor(color)
        self.sig.emit()
    
    def get_markerfacecolor(self):
        return self.obj.get_markerfacecolor()

    def set_markeredgecolor(self, color):
        self.obj.set_markeredgecolor(color)
        self.sig.emit()
    
    def get_markeredgecolor(self):
        return self.obj.get_markeredgecolor()
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()

        return super().paintEvent(a0)