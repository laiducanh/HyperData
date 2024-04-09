from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QSpinBox, QDoubleSpinBox, QSlider
from PyQt6.QtGui import QCursor
from ui.base_widgets.text import BodyLabel

class _SpinBox (QSpinBox):
    def __init__(self, min:int=0, max:int=100, step:int=1, parent=None) -> None:
        super().__init__(parent)

        self.setRange(min, max)
        self.setSingleStep(step)

class _DoubleSpinBox (QDoubleSpinBox):
    def __init__(self, min:int=0, max:int=100, step:int=1, parent=None) -> None:
        super().__init__(parent)

        self.setRange(min, max)
        self.setSingleStep(step)

class _Slider (QSlider):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(parent=parent)

        self.setOrientation(orientation)
        self.setFixedWidth(150)
        self.setRange(min,max)
        self.setSingleStep(step)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))




class SpinBox (QWidget):
    def __init__(self, min:int=0, max:int=100, step:int=1, text:str=None, parent=None):
        super().__init__(parent=parent) 
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text
        self.min = min
        self.max = max
        self.step = step

        if self.text != None:
            layout.addWidget(BodyLabel(self.text))
        self.button = _SpinBox(min, max, step, parent=parent)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)
    
class DoubleSpinBox (QWidget):
    def __init__(self, min:int=0, max:int=100, step:int=1, text:str=None, parent=None):
        super().__init__(parent) 
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text
        self.min = min
        self.max = max
        self.step = step
        if self.text != None:
            layout.addWidget(BodyLabel(self.text))
        self.button = _DoubleSpinBox(min, max, step, parent=parent)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)

class Slider (QWidget):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal, text:str=None, parent=None):
        super().__init__(parent=parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text

        if self.text != None:
            layout.addWidget(BodyLabel(self.text))
        layout.addStretch()
        self.button = _Slider(min, max, step, orientation, parent=parent)
        self.button.setOrientation(orientation)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)

        
