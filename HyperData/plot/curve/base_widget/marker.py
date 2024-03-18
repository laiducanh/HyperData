from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtGui import QPaintEvent
from config.settings import marker_lib, color_lib
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.color import ColorDropdown
from plot.canvas import Canvas
from matplotlib.lines import Line2D

class MarkerBase (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.gid = gid
        self.canvas = canvas  
        self.obj = self.find_object()      

        style = ComboBox(text='marker style',items=marker_lib.values())
        style.button.currentTextChanged.connect(self.set_marker)
        style.button.setCurrentText(self.get_marker())
        layout.addWidget(style)

        every = SpinBox(text='mark every',min=1,max=100,step=1)
        every.button.valueChanged.connect(self.set_markevery)
        every.button.setValue(self.get_markevery())
        layout.addWidget(every)

        markersize = DoubleSpinBox(text='marker size',min=0,max=20,step=2)
        markersize.button.valueChanged.connect(self.set_markersize)
        markersize.button.setValue(self.get_markersize())
        layout.addWidget(markersize)

        width = DoubleSpinBox(text='marker edge width',min=0,max=5,step=0.5)
        width.button.setValue(self.get_markeredgewidth())
        width.button.valueChanged.connect(self.set_markeredgewidth)
        layout.addWidget(width)

        facecolor = ColorDropdown(text='marker face color',color=self.get_markerfacecolor(),parent=parent)
        facecolor.button.colorChanged.connect(self.set_markerfacecolor)
        layout.addWidget(facecolor)

        edgecolor = ColorDropdown(text='marker edge color',color=self.get_markeredgecolor(),parent=parent)
        edgecolor.button.colorChanged.connect(self.set_markeredgecolor)
        layout.addWidget(edgecolor)

    def find_object (self) -> Line2D:
        for obj in self.canvas.fig.findobj(match=Line2D):
            if obj._gid != None and obj._gid == self.gid:
                return obj
        
    def set_marker (self, marker):
        marker = list(marker_lib.keys())[list(marker_lib.values()).index(marker.lower())]
        self.obj.set_marker(marker)
        self.canvas.draw()
    
    def get_marker(self):
        if self.obj.get_marker() == None:
            return "None"
        return self.obj.get_marker()

    def set_markevery(self, value):
        self.obj.set_markevery(value)
        self.canvas.draw()
        self.sig.emit()
    
    def get_markevery(self):
        if self.obj.get_markevery() == None:
            return 1
        return self.obj.get_markevery()

    def set_markersize (self, value):
        self.obj.set_markersize(value)
        self.canvas.draw()
        self.sig.emit()
    
    def get_markersize(self):
        return self.obj.get_markersize()

    def set_markeredgewidth(self, value):
        self.obj.set_markeredgewidth(value)
        self.canvas.draw()
        self.sig.emit()
    
    def get_markeredgewidth(self):
        return self.obj.get_markeredgewidth()

    def set_markerfacecolor(self, color):
        self.obj.set_markerfacecolor(color)
        self.canvas.draw()
        self.sig.emit()
    
    def get_markerfacecolor(self):
        return self.obj.get_markerfacecolor()

    def set_markeredgecolor(self, color):
        self.obj.set_markeredgecolor(color)
        self.canvas.draw()
        self.sig.emit()
    
    def get_markeredgecolor(self):
        return self.obj.get_markeredgecolor()

    def paintEvent(self, a0: QPaintEvent) -> None:
        # update self.obj as soon as possible
        self.obj = self.find_object()
        return super().paintEvent(a0)