from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget, QSpinBox, QDoubleSpinBox, QSlider
from PySide6.QtGui import QCursor
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import HButton

class _SpinBox (QSpinBox):
    def __init__(self, min:int=0, max:int=100, step:int=1, parent=None):
        super().__init__(parent)

        self.setRange(min, max)
        self.setSingleStep(step)

class _DoubleSpinBox (QDoubleSpinBox):
    def __init__(self, min:int=0, max:int=100, step:int=1, parent=None):
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




class SpinBox (HButton):
    def __init__(self, min:int=0, max:int=100, step:int=1, 
                 text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent) 
        
        self.text = text
        self.min = min
        self.max = max
        self.step = step

        self.button = _SpinBox(min, max, step, parent=parent)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)
        self.butn_layout.addWidget(self.button)
    
class DoubleSpinBox (HButton):
    def __init__(self, min:int=0, max:int=100, step:int=1, 
                 text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent) 
        
        self.min = min
        self.max = max
        self.step = step
        
        self.button = _DoubleSpinBox(min, max, step, parent=parent)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)
        self.butn_layout.addWidget(self.button)

class Slider (HButton):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal, 
                 text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)
        
        self.orientation = orientation

        self.button = _Slider(min, max, step, orientation, parent=parent)
        self.button.setOrientation(orientation)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)
        self.butn_layout.addWidget(self.button)

        
