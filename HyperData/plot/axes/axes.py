from PySide6.QtWidgets import QVBoxLayout, QWidget
from plot.axes import spine_2d, spine_3d
from plot.axes import tick_2d, tick_3d
from plot.canvas import Canvas
# axis = 'axis bottom', 'axis left'
# type = 'major', 'minor'


class Spine (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.spine2d = spine_2d.Spine2D(canvas, parent)
        self.vlayout.addWidget(self.spine2d)
    
    def choose_axis_func(self, axis):
        self.spine2d.choose_axis._onClick(axis)

class Spine3D (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.spine3d = spine_3d.Spine3D(canvas, parent)
        self.vlayout.addWidget(self.spine3d)
    
    def choose_axis_func(self, axis):
        self.spine3d.choose_axis._onClick(axis)
        
    
class Tick (QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.tick2d = tick_2d.Tick2D(canvas, parent)
        self.vlayout.addWidget(self.tick2d)

    def choose_axis_func(self, axis):
        self.tick2d.choose_axis._onClick(axis)

class Tick3D(QWidget):
    def __init__(self, canvas:Canvas, parent=None):
        super().__init__(parent)
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.tick3d = tick_3d.Tick3D(canvas, parent)
        self.vlayout.addWidget(self.tick3d)

    def choose_axis_func(self, axis):
        self.tick3d.choose_axis._onClick(axis)