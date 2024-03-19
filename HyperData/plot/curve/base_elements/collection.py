from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from config.settings import linestyle_lib
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.text import LineEdit
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from matplotlib.collections import Collection
from matplotlib import colors

class SingleColorCollection (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()        

        self.edgewidth = DoubleSpinBox(text='edge width',min=0,max=5,step=0.1)
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self.edgewidth.button.setValue(self.get_edgewidth())
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='edge style',items=linestyle_lib.values())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self.edgestyle.button.setCurrentText(self.get_edgestyle().title())
        layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='face color',color=self.get_facecolor(), parent=parent)
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='edge color',color=self.get_edgecolor(), parent=parent)
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        alpha = Slider(text='Transparency',min=0,max=100)
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
    
    def find_object (self) -> Collection:
        for obj in self.canvas.fig.findobj(match=Collection):
            if obj._gid != None and obj._gid == self.gid:
                return obj
    
    def set_edgewidth (self, value):
        self.obj.set_linewidth(value)
        self.sig.emit()
    
    def get_edgewidth (self):
        return self.obj.get_linewidth()

    def set_edgestyle (self, value):
        self.obj.set_linestyle(value.lower())
        self.sig.emit()
    
    def get_edgestyle (self):
        return linestyle_lib[self.obj.get_linestyle()[0]]
    
    def set_facecolor (self, value):
        self.obj.set_facecolor(value)
        self.sig.emit()
    
    def get_facecolor(self):
        return colors.to_hex(self.obj.get_facecolor())
    
    def set_edgecolor (self, value):
        self.obj.set_edgecolor(value)
        self.sig.emit()
    
    def get_edgecolor (self):
        if len(self.obj.get_edgecolor()) > 1:
            return colors.to_hex(self.obj.get_edgecolor())
        self.set_edgecolor(self.get_facecolor())
        return self.get_facecolor()

    def set_alpha (self, value):
        self.obj.set_alpha(value/100)
        self.sig.emit()

    def get_alpha (self):
        if self.obj.get_alpha() != None:
            return int(self.obj.get_alpha()*100)
        return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()

        return super().paintEvent(a0)