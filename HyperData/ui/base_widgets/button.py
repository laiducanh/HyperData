from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QWidget, 
                              QGridLayout, QScrollArea, QVBoxLayout, QLayout)
from PySide6.QtGui import QIcon
from typing import Iterable, Union
from ui.base_buttons.button import *
from ui.base_widgets.text import BodyLabel, InfoLabel
from ui.base_widgets.frame import SeparateHLine, HFrame
from ui.utils import isDark
from config.settings import config
from typing import Callable, Union

class VButton(QWidget):
    """" Button Widget in vertical layout """
    def __init__(self, label:str=None, label2:str=None, layout:QLayout=None, parent:QWidget=None):
        super().__init__(parent)

        self.label  = BodyLabel(parent=parent, text=label)
        self.label2 = InfoLabel(parent=parent, text=label2, wordWrap=False)
        if not label2: self.label2.hide()

        self.vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        self.vlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        self.vlayout.addLayout(self.butn_layout)

        if layout: layout.addWidget(self)

    def setText(self, value:str):
        self.label.setText(value)
    
    def setText2(self, value:str):
        self.label2.setText(value)
    
    def get_value(self):
        return self.button.get_value()

    def set_value(self, value):
        self.button.set_value(value)
    
    def set_setter(self, setter:Callable):
        self.button.set_setter(setter)
    
    def get_setter(self) -> Callable:
        return self.button.setter
    
    def set_getter(self, getter:Callable):
        self.button.set_getter(getter)

    def get_getter(self) -> Callable:
        return self.button.getter
    
class HButton(QWidget): 
    """" Button Widget in horizontal layout """
    def __init__(self, label:str=None, label2:str=None, layout:QLayout=None, parent:QWidget=None):
        super().__init__(parent)

        self.label  = BodyLabel(parent=parent, text=label)
        self.label2 = InfoLabel(parent=parent, text=label2, wordWrap=False)
        if not label2: self.label2.hide()

        self.hlayout = QHBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        self.hlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QHBoxLayout()
        self.hlayout.addLayout(self.butn_layout)

        if layout: layout.addWidget(self)

    def setText(self, value:str):
        self.label.setText(value)
    
    def setText2(self, value:str):
        self.label2.setText(value)
    
    def get_value(self):
        return self.button.get_value()

    def set_value(self, value):
        self.button.set_value(value)
    
    def set_setter(self, setter:Callable):
        self.button.set_setter(setter)
    
    def get_setter(self) -> Callable:
        return self.button.setter
    
    def set_getter(self, getter:Callable):
        self.button.set_getter(getter)

    def get_getter(self) -> Callable:
        return self.button.getter
    
class HPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)
           
class HTransparentPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VTransparentPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HPrimaryPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VPrimaryPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HDropDownPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = DropDownPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VDropDownPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = DropDownPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HDropDownTransparentPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = DropDownTransparentPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VDropDownTransparentPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = DropDownTransparentPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HDropDownPrimaryPushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VDropDownPrimaryPushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = DropDownTransparentPushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HTogglePushButton(HButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TogglePushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VTogglePushButton(VButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, 
                 parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TogglePushButton(text=text, icon=icon, menu=menu, setter=setter, getter=getter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VToolButton(VButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HTransparentToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VTransparentToolButton(VButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HPrimaryToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VPrimaryToolButton(VButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HPrimaryToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HToggleToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ToggleToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class VToggleToolButton(VButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ToggleToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HToggleToolButton(HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 label:str=None, label2:str=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ToggleToolButton(icon=icon, menu=menu, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)

class HComboBox(HButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VComboBox(VButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = ComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HTransparentComboBox(HButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VTransparentComboBox(VButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = TransparentComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class HPrimaryComboBox(HButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)

class VPrimaryComboBox(VButton):
    def __init__(self, items:Iterable[str]=None, label:str=None, label2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)

        self.button = PrimaryComboBox(items=items, getter=getter, setter=setter, layout=self.butn_layout, parent=parent, *args, **kwargs)
        self.button.setFixedWidth(150)
    
class HToggle(HButton):
    def __init__(self, label:str=None, label2:str=None, setter:Callable=None, 
                 getter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)
        
        self.button = Toggle(setter=setter, getter=getter, layout=self.butn_layout, parent=parent)

class VToggle(VButton):
    def __init__(self, label:str=None, label2:str=None, setter:Callable=None, 
                 getter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(label=label, label2=label2, layout=layout, parent=parent)
        
        self.button = Toggle(setter=setter, getter=getter, layout=self.butn_layout, parent=parent)

class VGroupRadioButton(QWidget):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 setter:Callable=None, getter:Callable=None, layout:QLayout=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=False)
        if not label2: self.label2.hide()

        hlayout = QHBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        hlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        hlayout.addLayout(self.butn_layout)

        for item in items:
            btn = RadioButton(text=item, parent=self, layout=self.butn_layout)
            btn.clicked.connect(lambda: self.checkChanged.emit(self.get_value()))

        if layout: layout.addWidget(self)
        if getter: self.set_value(getter())
        if setter: self.checkChanged.connect(setter)

    def get_value(self) -> str:
        for btn in self.findChildren(RadioButton):
            if btn.get_value(): return btn.text()
    
    def set_value(self, value:str): 
        for btn in self.findChildren(RadioButton):
            if btn.text() == value: btn.set_value(True)
    
class HGroupRadioButton(QWidget):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=False)
        if not label2: self.label2.hide()

        hlayout = QHBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        hlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QHBoxLayout()
        hlayout.addLayout(self.butn_layout)

        for item in items:
            btn = RadioButton(text=item, parent=self, layout=self.butn_layout)
            btn.clicked.connect(lambda: self.checkChanged.emit(self.get_value()))

        if layout: layout.addWidget(self)
        if getter: self.set_value(getter())
        if setter: self.checkChanged.connect(setter)

    def get_value(self) -> str:
        for btn in self.findChildren(RadioButton):
            if btn.get_value(): return btn.text()
    
    def set_value(self, value:str): 
        for btn in self.findChildren(RadioButton):
            if btn.text() == value: btn.set_value(True)

class GridGroupRadioButton(QWidget):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 grid:tuple[float,float]=(0,0), layout:QLayout=None, 
                 setter:Callable=None, getter:Callable=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=False)
        if not label2: self.label2.hide()

        vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        vlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QGridLayout()
        vlayout.addLayout(self.butn_layout)

        row, col = 0, 0
        for item in items:
            btn = RadioButton(text=item, parent=self)
            self.butn_layout.addWidget(btn, row, col)
            if row < grid[0]-1: 
                row += 1
            else: 
                col += 1
                row = 0
            btn.clicked.connect(lambda: self.checkChanged.emit(self.get_value()))

        if layout: layout.addWidget(self)
        if getter: self.set_value(getter())
        if setter: self.checkChanged.connect(setter)

    def get_value(self) -> str:
        for btn in self.findChildren(RadioButton):
            if btn.get_value(): return btn.text()
    
    def set_value(self, value:str): 
        for btn in self.findChildren(RadioButton):
            if btn.text() == value: btn.set_value(True)

class SegmentedWidget(HFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.hlayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.buttons = list()
        self.funcs = list()
    
    def addButton (self, text:str, func):
        button = TransparentPushButton()
        button.setText(text)
        button.clicked.connect(lambda: self._onClick(text))
        self.buttons.append(button.text())
        self.funcs.append(func)
        self.hlayout.addWidget(button)

    def _onClick (self, button_text:str):
        self.setCurrentWidget(button_text)
        fn = self.funcs[self.buttons.index(button_text)]
        fn()
    
    def setCurrentWidget (self, button_text:str):
        for btn in self.findChildren(TransparentPushButton):
            # btn.setStyleSheet("font-weight:normal")
            btn.setStyleSheet('background-color: transparent;')
            if isDark(): btn.setStyleSheet('color: white;')
            else: btn.setStyleSheet('color: black;')
            if btn.text() == button_text:
                self.currentWidget = btn
                # btn.setStyleSheet("font-weight:bold")
                btn.setStyleSheet(f"""
                    background-color: {config['themecolor']};
                    color: white""")
                self.update()
    
    def setCurrentIndex (self, index:int):
        for idx, btn in enumerate(self.findChildren(TransparentPushButton)):
            # btn.setStyleSheet("font-weight:normal")
            btn.setStyleSheet('background-color: transparent;')
            if isDark(): btn.setStyleSheet('color: white;')
            else: btn.setStyleSheet('color: black;')
            if idx == index:
                self.currentWidget = btn
                # btn.setStyleSheet("font-weight:bold")
                btn.setStyleSheet(f"""
                    background-color: {config['themecolor']};
                    color: white""")
                self.update()

class ListCheckBox(QWidget):
    def __init__(self, list_btn=list(), states=list(), text:str=None, parent=None):
        super().__init__(parent)

        self.states = states
        self.list_btn = list_btn

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.vlayout.addWidget(BodyLabel(text))
        self.vlayout.addWidget(SeparateHLine())

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        btn_widget = QWidget()
        self.btn_layout = QVBoxLayout(btn_widget) 
        self.btn_layout.setContentsMargins(0,0,20,0)
        self.vlayout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(btn_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(150)

        self.setButtons(list_btn, states)

    def setButtons(self, list_btn=list(), states=list()):
        self.list_btn = list_btn
        self.states = states
        for btn in self.findChildren(CheckBox):
            self.btn_layout.removeWidget(btn)
            btn.deleteLater()
        
        for idx, btn in enumerate(list_btn):
            btn = CheckBox(text=btn)
            btn.pressed.connect(lambda i=idx, b=btn: self.changeState(i, b.isChecked()))
            btn.setChecked(self.states[idx])
            self.btn_layout.addWidget(btn)
    
    def changeState(self, idx:int, state:bool):
        self.states[idx] = not state
       
    

