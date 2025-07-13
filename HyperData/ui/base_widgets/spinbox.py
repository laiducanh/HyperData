from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayout, QSpinBox, QDoubleSpinBox, QSlider
from PySide6.QtGui import QCursor
from ui.base_widgets.button import HButton, VButton
from typing import Callable

class SpinBox(QSpinBox):
    def __init__(self, getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setter = setter
        self.getter = getter

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

class TransparentSpinBox(SpinBox):
    """ SpinBox with no border and background color """

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.getter = getter
        self.setter = setter

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
    
class TransparentDoubleSpinBox (DoubleSpinBox):
    """ DoubleSpinBox with no border and background color """

class Slider(QSlider):
    def __init__(self, setter:Callable=None, getter:Callable=None,
                 orientation=Qt.Orientation.Horizontal, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(orientation=orientation, parent=parent, *args, **kwargs)

        self.getter = getter
        self.setter = setter

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
    
class HSpinBox(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = SpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VSpinBox(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = SpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HTransparentSpinBox(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = TransparentSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VTransparentSpinBox(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = TransparentSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HDoubleSpinBox(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = DoubleSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VDoubleSpinBox(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = DoubleSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HTransparentDoubleSpinBox(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = TransparentDoubleSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VTransparentDoubleSpinBox(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent) 

        self.button = TransparentDoubleSpinBox(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HSlider(HButton):
    def __init__(self, setter:Callable=None, getter:Callable=None,
                 orientation=Qt.Orientation.Horizontal, layout:QLayout=None,
                 label:str=None, label2:str=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)
        
        self.button = Slider(setter=setter, getter=getter, orientation=orientation, 
                             layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VSlider(VButton):
    def __init__(self, setter:Callable=None, getter:Callable=None,
                 orientation=Qt.Orientation.Horizontal, layout:QLayout=None,
                 label:str=None, label2:str=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)
        
        self.button = Slider(setter=setter, getter=getter, orientation=orientation, 
                             layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)
