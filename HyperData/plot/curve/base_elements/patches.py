from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from config.settings import linestyle_lib
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.text import LineEdit
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from matplotlib import patches
from matplotlib import colors, scale
import matplotlib, numpy
from typing import List

class Rectangle (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()
        self.parent = parent
        self.initUI()

    def initUI (self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.edgewidth = DoubleSpinBox(text='edge width',min=0,max=5,step=0.1)
        self.edgewidth.button.valueChanged.connect(self.set_edgewidth)
        self.edgewidth.button.setValue(self.get_edgewidth())
        layout.addWidget(self.edgewidth)

        self.edgestyle = ComboBox(text='edge style',items=linestyle_lib.values())
        self.edgestyle.button.currentTextChanged.connect(self.set_edgestyle)
        self.edgestyle.button.setCurrentText(self.get_edgestyle().title())
        layout.addWidget(self.edgestyle)

        self.facecolor = ColorDropdown(text='face color',color=self.get_facecolor(), parent=self.parent)
        self.facecolor.button.colorChanged.connect(self.set_facecolor)
        layout.addWidget(self.facecolor)

        self.edgecolor = ColorDropdown(text='edge color',color=self.get_edgecolor(), parent=self.parent)
        self.edgecolor.button.colorChanged.connect(self.set_edgecolor)
        layout.addWidget(self.edgecolor)

        alpha = Slider(text='Transparency',min=0,max=100)
        alpha.button.valueChanged.connect(self.set_alpha)
        alpha.button.setValue(self.get_alpha())
        layout.addWidget(alpha)
    
    def find_object (self) -> List[patches.Rectangle]:
        obj_list = list()
        for obj in self.canvas.fig.findobj(match=patches.Rectangle):
            if obj._gid != None and obj._gid == self.gid:
                obj_list.append(obj)
        return obj_list

    def set_edgestyle(self, value):
        for obj in self.obj:
            obj.set_linestyle(value.lower())
        self.sig.emit()
    
    def get_edgestyle(self):
        return self.obj[0].get_linestyle()
    
    def set_edgewidth(self, value):
        for obj in self.obj:
            obj.set_linewidth(value)
        self.sig.emit()
    
    def get_edgewidth (self):
        return self.obj[0].get_linewidth()
    
    def set_alpha(self, value):
        for obj in self.obj:
            obj.set_alpha(float(value/100))
        self.sig.emit()
    
    def get_alpha (self):
        if self.obj[0].get_alpha() == None:
            return 100
        return int(self.obj[0].get_alpha()*100)

    def set_facecolor (self, value):
        for obj in self.obj:
            obj.set_facecolor(value)
        self.sig.emit()
    
    def get_facecolor(self):
        return colors.to_hex(self.obj[0].get_facecolor())
    
    def set_edgecolor (self, value):
        for obj in self.obj:
            obj.set_edgecolor(value)
        self.sig.emit()
    
    def get_edgecolor (self):
        return colors.to_hex(self.obj[0].get_edgecolor())
    
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()

        return super().paintEvent(a0)