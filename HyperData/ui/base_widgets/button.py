from PyQt6.QtCore import (pyqtSignal, Qt, QSize, QPoint, QPointF, QRectF)
from PyQt6.QtWidgets import QHBoxLayout,QCheckBox, QWidget, QColorDialog, QPushButton
from PyQt6.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter
import os, qfluentwidgets
from ui.base_widgets.text import BodyLabel

class _PushButton (qfluentwidgets.PushButton):
    def __init__(self):
        super().__init__()

class _PrimaryPushButton (qfluentwidgets.PrimaryPushButton):
    def __init__(self):
        super().__init__()

class _DropDownPushButton (qfluentwidgets.DropDownPushButton):
    def __init__(self):
        super().__init__()

class _DropDownToolButton (qfluentwidgets.DropDownToolButton):
    def __init__(self):
        super().__init__()
    
class _ToolButton (qfluentwidgets.ToolButton):
    def __init__(self):
        super().__init__()

class _PrimaryDropDownPushButton (qfluentwidgets.PrimaryDropDownPushButton):
    def __init__(self):
        super().__init__()

class _ComboBox (qfluentwidgets.ComboBox):
    def __init__(self, items:list=None):
        super().__init__()

        if items != None:
            for item in items:
                self.addItem(item.title())

class _Toggle (qfluentwidgets.SwitchButton):
    def __init__(self):
        super().__init__()

class Toggle (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))

        layout.addStretch()
        
        self.button = _Toggle()

        layout.addWidget(self.button)


class PushButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _PushButton()
        layout.addWidget(self.button)
    
        
class DropDownPushButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _DropDownPushButton()
        layout.addWidget(self.button)
    
    

class DropDownToolButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _DropDownToolButton()
        layout.addWidget(self.button)
    



class PrimaryDropDownPushButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _PrimaryDropDownPushButton()
        layout.addWidget(self.button)
    

class PrimaryPushButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _PrimaryPushButton()
        layout.addWidget(self.button)
    

class ToolButton (QWidget):
    def __init__(self, text:str=None):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))
        
        self.button = _ToolButton()
        layout.addWidget(self.button)

class _ToggleToolButton (qfluentwidgets.ToggleToolButton):
    def __init__(self):
        super().__init__()    
    
class ComboBox (QWidget):
    def __init__(self, items:list=[], text:str=None):
        super().__init__()
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.text = text

        if text != None:
            self._layout.addWidget(BodyLabel(self.text.title()))
        self._layout.addStretch()
        self.button = _ComboBox()
        self.button.setFixedWidth(150)
        self.button.addItems([i.title() for i in items])

        self._layout.addWidget(self.button)
    
