from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLayout
from ui.base_widgets.button import HButton, VButton
from ui.base_buttons.spinbox import *
from typing import Callable
    
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
