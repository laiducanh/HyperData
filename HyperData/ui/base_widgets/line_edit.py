from PySide6.QtWidgets import QLayout
from ui.base_widgets.button import HButton, VButton
from ui.base_buttons.line_edit import *
from typing import Callable

class HLineEdit(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None,
                 setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = LineEdit(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VLineEdit(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None,
                 setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = LineEdit(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HTextEdit(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, 
                 setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TextEdit(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VTextEdit(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None,
                 setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TextEdit(getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        
class HCompleterLineEdit(HButton):
    def __init__(self, items=None, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = CompleterLineEdit(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VCompleterLineEdit(VButton):
    def __init__(self, items=None, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = CompleterLineEdit(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)


