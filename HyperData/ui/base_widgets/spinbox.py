from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayout, QWidget, QSpinBox, QDoubleSpinBox, QSlider
from PySide6.QtGui import QCursor
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import HButton
from typing import Callable

class _SpinBox(QSpinBox):
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
    
    def wheelEvent(self, event):
        event.ignore()
    
    def set_value(self, value:int):
        self.setValue(value)
    
    def get_value(self) -> int:
        return self.value()
    
    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter

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
    
    def wheelEvent(self, event):
        event.ignore()

    def set_value(self, value:float):
        self.setValue(value)
    
    def get_value(self) -> float:
        return self.value()

    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter
    
class _TransparentDoubleSpinBox (_DoubleSpinBox):
    """ DoubleSpinBox with no border and background color """

class _Slider (QSlider):
    def __init__(self, min=0, max=100, step=1, setter:Callable=None, getter:Callable=None,
                 orientation=Qt.Orientation.Horizontal, layout:QLayout=None, parent=None):
        super().__init__(parent=parent)

        self.getter = getter
        self.setter = setter

        self.setOrientation(orientation)
        self.setFixedWidth(150)
        self.setRange(min,max)
        self.setSingleStep(step)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

        if getter: self.setValue(getter())
        if setter: self.valueChanged.connect(setter)
        if layout: layout.addWidget(self)

    def set_value(self, value:int):
        self.setValue(value)
    
    def get_value(self) -> int:
        return self.value()

    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter
    
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
    
    def get_value(self) -> int:
        return super().get_value()
    
    def set_value(self, value:int):
        return super().set_value(value)
    
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
    
    def get_value(self) -> int:
        return super().get_value()

    def set_value(self, value:int):
        return super().set_value(value)
    
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
    
    def get_value(self) -> float:
        return super().get_value()

    def set_value(self, value:float):
        return super().set_value(value)

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
    
    def get_value(self) -> float:
        return super().get_value()

    def set_value(self, value:float):
        return super().set_value(value)

class Slider (HButton):
    def __init__(self, min=0, max=100, step=1, setter:Callable=None, getter:Callable=None,
                 orientation=Qt.Orientation.Horizontal, layout:QLayout=None,
                 text:str=None, text2:str=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)
        
        self.orientation = orientation

        self.button = _Slider(
            min=min, max=max, step=step, setter=setter, getter=getter, 
            orientation=orientation, parent=parent)
        self.button.setFixedWidth(150)
        self.butn_layout.addWidget(self.button)

    def get_value(self) -> int:
        return super().get_value()

    def set_value(self, value:int):
        return super().set_value(value)