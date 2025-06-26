from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayout, QWidget, QSpinBox, QDoubleSpinBox, QSlider
from PySide6.QtGui import QCursor
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import HButton
from typing import Callable

class _SpinBox (QSpinBox):
    def __init__(self, min=0, max=100, step=1, suffix='', prefix='',
                 getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None):
        super().__init__(parent)

        self.setter = setter
        self.getter = getter

        self.setRange(min, max)
        self.setSingleStep(step)
        self.setSuffix(suffix)
        self.setPrefix(prefix)
        if getter: self.setValue(getter())
        if setter: self.valueChanged.connect(setter)
        if layout: layout.addWidget(self)

class _TransparentSpinBox (_SpinBox):
    """ SpinBox with no border and background color """

class _DoubleSpinBox (QDoubleSpinBox):
    def __init__(self, min=0, max=100, step=1, decimals=2, suffix='', prefix='',
                 getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None):
        super().__init__(parent)

        self.getter = getter
        self.setter = setter

        self.setRange(min, max)
        self.setSingleStep(step)
        self.setDecimals(decimals)
        self.setPrefix(prefix)
        self.setSuffix(suffix)
        if getter: self.setValue(getter())
        if setter: self.valueChanged.connect(setter)
        if layout: layout.addWidget(self)
    
class _TransparentDoubleSpinBox (_DoubleSpinBox):
    """ DoubleSpinBox with no border and background color """

class _Slider (QSlider):
    def __init__(self, min:int=0, max:int=100, step:int=1, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(parent=parent)

        self.setOrientation(orientation)
        self.setFixedWidth(150)
        self.setRange(min,max)
        self.setSingleStep(step)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))




class SpinBox (HButton):
    def __init__(self, min=0, max=100, step=1, suffix='', prefix='', text:str=None, text2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent) 
        
        self.text = text
        self.min = min
        self.max = max
        self.step = step

        self.button = _SpinBox(
            min=min, max=max, step=step, suffix=suffix, prefix=prefix,
            getter=getter, setter=setter, parent=parent)
        self.button.setFixedWidth(150)
        self.butn_layout.addWidget(self.button)

class TransparentSpinBox (HButton):
    def __init__(self, min=0, max=100, step=1, suffix='', prefix='', text:str=None, text2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent) 
        
        self.text = text
        self.min = min
        self.max = max
        self.step = step

        self.button = _TransparentSpinBox(
            min=min, max=max, step=step, suffix=suffix, prefix=prefix,
            getter=getter, setter=setter, parent=parent)
        self.button.setFixedWidth(150)
        self.butn_layout.addWidget(self.button)
    
class DoubleSpinBox (HButton):
    def __init__(self, min=0, max=100, step=1, decimals=2, suffix='', prefix='',
                 text:str=None, text2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent) 
        
        self.min = min
        self.max = max
        self.step = step
        
        self.button = _DoubleSpinBox(
            min=min, max=max, step=step, decimals=decimals, suffix=suffix, 
            prefix=prefix, getter=getter, setter=setter, parent=parent)
        self.button.setFixedWidth(150)
        self.butn_layout.addWidget(self.button)

class TransparentDoubleSpinBox (HButton):
    def __init__(self, min=0, max=100, step=1, decimals=2, suffix='', prefix='',
                 text:str=None, text2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent) 
        
        self.min = min
        self.max = max
        self.step = step
        
        self.button = _TransparentDoubleSpinBox(
            min=min, max=max, step=step, decimals=decimals, prefix=prefix, suffix=suffix,
            getter=getter, setter=setter, parent=parent)
        self.button.setFixedWidth(150)
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

        
