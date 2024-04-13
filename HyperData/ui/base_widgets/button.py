from PyQt6.QtCore import QObject, Qt, pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QMenu, QWidget, QComboBox, QPushButton, QFrame, 
                             QSizePolicy, QGridLayout, QToolButton)
from PyQt6.QtGui import QCursor, QIcon, QPaintEvent
from typing import Iterable
from ui.base_widgets.text import BodyLabel
from ui.utils import icon

class _PushButton (QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._icon = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
    def setIcon(self, icon:str) -> None:
        self._icon = icon
        self.update()
    
    def update(self):
        if self._icon: super().setIcon(icon(self._icon))
        super().update()

class _TransparentPushButton (_PushButton):
    """ PushButton with no border and background color """

class _PrimaryPushButton (_PushButton):
    """ PushButton with highlight color """

class _DropDownPushButton (QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._icon = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    
    def setIcon(self, icon:str) -> None:
        self._icon = icon
        self.update()
    
    def update(self):
        if self._icon: super().setIcon(icon(self._icon))
        super().update()

class _DropDownTransparentPushButton (_DropDownPushButton):
    """ DropDownPushButton with no border and background color """

class _DropDownPrimaryPushButton (_DropDownPushButton):
     """ DropDownPushButton with highlight color """

class _TogglePushButton (_PushButton):
    """ checkable PushButton """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCheckable(True)
    
class _ToolButton (QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._icon = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    
    def setMenu(self, menu: QMenu) -> None:
        self.setProperty("hasMenu",True)
        return super().setMenu(menu)

    def setIcon(self, icon:str) -> None:
        self._icon = icon
        self.update()
    
    def update(self):
        if self._icon: super().setIcon(icon(self._icon))
        super().update()

class _TransparentToolButton (_ToolButton):
    """ ToolButton with no border and background color """
    
class _PrimaryToolButton (_ToolButton):
    """ PushButton with highlight color """

class _ToggleToolButton (_ToolButton):
    """ checkable ToolButton """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCheckable(True)

class _ComboBox (QComboBox):
    def __init__(self, items:Iterable[str]=None, parent=None):
        super().__init__(parent)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.view().window().setWindowFlags(Qt.WindowType.Popup | 
                                            Qt.WindowType.FramelessWindowHint |
                                            Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        if items != None: self.addItems(items)

class _TransparentComboBox (_ComboBox):
    """ """

class _PrimaryComboBox (_ComboBox):
    """ """

class _Toggle(QFrame):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, width = 60, height = 40, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        if self.width < self.height * 2 -20:
            self.width = self.height * 2 -20
        self.setFixedSize(self.width, self.height)
        self.toggle_on = False
        self.initUI()

    def initUI(self):
        
        self.button_1 = QPushButton()
        self.button_1.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.button_2 = QPushButton()
        self.button_3 = QPushButton()

        self.button_2.setFixedSize(self.height - 28, self.height - 28)
        self.button_3.setFixedSize(self.height - 28, self.height - 28)

        self.button_1.setStyleSheet(
            "border-radius : %d; border : 1px solid black; background-color: rgb(255, 255, 255)"%((self.height-20)//2))
        
        self.button_2.setStyleSheet(
            "border-radius : %d; background-color: rgb(0, 0, 0)"%((self.height - 28)//2))
        
        self.button_3.setStyleSheet(
            "border-radius : %d; background-color: rgb(255, 255, 255)"%((self.height - 28)//2))
        self.button_3.setVisible(False)
        
        self.button_1.clicked.connect(self.setChecked)
        self.button_2.clicked.connect(self.setChecked)
        self.button_3.clicked.connect(self.setChecked)

        layout = QGridLayout()
        layout.addWidget(self.button_1, 0, 0, 1, 2)
        layout.addWidget(self.button_2, 0, 0, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_3, 0, 1, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def setChecked(self, check:bool=False):

        if check:
            self.toggle_on = check
        else:
            self.toggle_on = not self.toggle_on
            

        match self.toggle_on:
            case True:
                self.button_1.setStyleSheet("border-radius : %d; border : none; background-color: rgb(0, 120, 215)"%((self.height - 20)//2))
                self.button_2.setVisible(False)
                self.button_3.setVisible(True)
            case False:
                self.button_1.setStyleSheet("border-radius : %d; border : 1px solid black; background-color: rgb(255, 255, 255)"%((self.height - 20)//2))
                self.button_2.setVisible(True)
                self.button_3.setVisible(False)
        
        self.checkedChanged.emit(self.toggle_on)

    def isChecked(self):
        return self.toggle_on


class PushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _PushButton(parent=parent)
        layout.addWidget(self.button)
    
class TransparentPushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _TransparentPushButton(parent=parent)
        layout.addWidget(self.button)

class PrimaryPushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _PrimaryPushButton(parent=parent)
        layout.addWidget(self.button)

class DropDownPushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _DropDownPushButton(parent=parent)
        layout.addWidget(self.button)

class DropDownTransparentPushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _DropDownTransparentPushButton(parent=parent)
        layout.addWidget(self.button)

class DropDownPrimaryPushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _DropDownPrimaryPushButton(parent=parent)
        layout.addWidget(self.button)

class TogglePushButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _TogglePushButton(parent=parent)
        layout.addWidget(self.button)

class ToolButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _ToolButton(parent=parent)
        layout.addWidget(self.button)

class TransparentToolButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _TransparentToolButton(parent=parent)
        layout.addWidget(self.button)

class PrimaryToolButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _PrimaryToolButton(parent=parent)
        layout.addWidget(self.button)

class ToggleToolButton (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))
        
        self.button = _ToggleToolButton(parent=parent)
        layout.addWidget(self.button)

class ComboBox (QWidget):
    def __init__(self, items:Iterable[str]=None, text:str=None, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.text = text

        if text != None:
            self._layout.addWidget(BodyLabel(self.text))
        self._layout.addStretch()
        self.button = _ComboBox(items, parent=parent)
        self.button.setFixedWidth(150)

        self._layout.addWidget(self.button)

class TransparentComboBox (QWidget):
    def __init__(self, items:Iterable[str]=None, text:str=None, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.text = text

        if text != None:
            self._layout.addWidget(BodyLabel(self.text))
        self._layout.addStretch()
        self.button = _TransparentComboBox(items, parent=parent)
        self.button.setFixedWidth(150)

        self._layout.addWidget(self.button)

class PrimaryComboBox (QWidget):
    def __init__(self, items:Iterable[str]=None, text:str=None, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.text = text

        if text != None:
            self._layout.addWidget(BodyLabel(self.text))
        self._layout.addStretch()
        self.button = _PrimaryComboBox(items, parent=parent)
        self.button.setFixedWidth(150)

        self._layout.addWidget(self.button)
    
class Toggle (QWidget):
    def __init__(self, text:str=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))

        layout.addStretch()
        
        self.button = _Toggle(parent=parent)
        layout.addWidget(self.button)

class SegmentedWidget (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.buttons = list()
        self.funcs = list()
    
    def addButton (self, text:str, func):
        button = _TogglePushButton()
        button.setText(text)
        button.clicked.connect(lambda: self._onClick(text))
        self.buttons.append(button.text())
        self.funcs.append(func)
        self._layout.addWidget(button)
    
    def _onClick (self, button_text:str):
        self.setCurrentWidget(button_text)
        fn = self.funcs[self.buttons.index(button_text)]
        fn()
    
    def setCurrentWidget (self, button_text:str):
        for btn in self.findChildren(_TogglePushButton):
            btn.setChecked(False)
            if btn.text() == button_text:
                btn.setChecked(True)

        

