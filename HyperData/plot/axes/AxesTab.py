from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from plot.axes.Spine import SpineWidget2D
from plot.axes.Tick import TickWidget2D
from plot.canvas import Canvas
# axis = 'axis bottom', 'axis left'
# type = 'major', 'minor'


class SpineWidget (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        self.spine2d = SpineWidget2D(canvas)
        self.layout.addWidget(self.spine2d)
    
    def choose_axis(self, axis:str):
        self.spine2d.choose_axis_func(axis)
        
    
class TickWidget (QWidget):
    def __init__(self,canvas:Canvas):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        self.tick2d = TickWidget2D(canvas)
        self.layout.addWidget(self.tick2d)
    
    def choose_axis (self, axis:str):
        self.tick2d.choose_axis_func(axis)