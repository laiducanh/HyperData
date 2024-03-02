from PyQt6.QtCore import pyqtSignal, Qt, QStandardPaths, QDir, QSettings
from PyQt6.QtWidgets import QHBoxLayout,QVBoxLayout, QWidget, QSpinBox, QLabel, QDoubleSpinBox, QSlider
import os, qfluentwidgets
from ui.base_widgets.text import BodyLabel

class SpinBox (QWidget):
    def __init__(self, min:int, max:int, step:int=1, text:str=None):
        super().__init__() 
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text
        self.min = min
        self.max = max
        self.step = step

        if self.text != None:
            layout.addWidget(BodyLabel(self.text.title()))
        self.button = qfluentwidgets.SpinBox()
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)
    
class DoubleSpinBox (QWidget):
    def __init__(self, min:int, max:int, step:int=1, text:str=None):
        super().__init__() 
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text
        self.min = min
        self.max = max
        self.step = step
        if self.text != None:
            layout.addWidget(BodyLabel(self.text.title()))
        self.button = qfluentwidgets.DoubleSpinBox()
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)

    
class _Slider (qfluentwidgets.Slider):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal):
        super().__init__()

        self.setOrientation(orientation)
        self.setFixedWidth(150)
        self.setRange(min,max)
        self.setSingleStep(step)

class Slider (QWidget):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal, text:str=None):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.text = text

        if self.text != None:
            layout.addWidget(BodyLabel(self.text.title()))
        layout.addStretch()
        self.button = _Slider()
        self.button.setOrientation(orientation)
        self.button.setFixedWidth(150)
        self.button.setRange(min,max)
        self.button.setSingleStep(step)

        layout.addWidget(self.button)

        
