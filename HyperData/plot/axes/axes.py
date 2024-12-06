from PyQt6.QtWidgets import QVBoxLayout, QWidget
from plot.axes.spine import Spine2D
from plot.axes.tick import Tick2D
from plot.canvas import Canvas
# axis = 'axis bottom', 'axis left'
# type = 'major', 'minor'


class Spine (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        self.spine2d = Spine2D(canvas, parent)
        self.layout.addWidget(self.spine2d)
    
    def choose_axis_func(self, axis):
        self.spine2d.choose_axis._onClick(axis)
        
    
class Tick (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        self.tick2d = Tick2D(canvas, parent)
        self.layout.addWidget(self.tick2d)

    def choose_axis_func(self, axis):
        self.tick2d.choose_axis._onClick(axis)