from ui.base_widgets.button import HButton, VButton
from ui.base_buttons.color import *
from typing import Callable

class HColorDropdown(HButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None,
                 layout:QLayout=None, parent=None):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ColorPickerButton(setter=setter, getter=getter, layout=self.butn_layout, parent=parent)

class VColorDropdown(VButton):
    def __init__(self, label:str=None, label2:str=None, getter:Callable=None, setter:Callable=None,
                 layout:QLayout=None, parent=None):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ColorPickerButton(setter=setter, getter=getter, layout=self.butn_layout, parent=parent)