from PySide6.QtCore import QObject, Qt, Signal, QEvent, QPoint, QRectF
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QWidget, QComboBox, QPushButton, QFrame, 
                             QSizePolicy, QGridLayout, QToolButton, QFileIconProvider, QVBoxLayout)
from PySide6.QtGui import QCursor, QPainter, QColor, QIcon
from PySide6.QtSvg import QSvgRenderer
from typing import Iterable
from ui.base_widgets.text import BodyLabel, InfoLabel
from ui.base_widgets.menu import Menu
from ui.utils import icon as Icon
import os

class _PushButton (QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._icon = None
    
    def setIcon(self, icon:QIcon|str) -> None:
        if isinstance(icon, QIcon):
            self._icon = icon
        else: self._icon = Icon(icon)
        super().setIcon(self._icon)
    
    def update(self):
        if self._icon: super().setIcon(self._icon)
        super().update()

class _TransparentPushButton (_PushButton):
    """ PushButton with no border and background color """

class _PrimaryPushButton (_PushButton):
    """ PushButton with highlight color """

class _DropDownPushButton (_PushButton):
    """ PushButton with dropdown menu """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)

        self._menu = None
    
    def setMenu(self, menu: QMenu):
        self._menu = menu
        return super().setMenu(menu)
    
    def mousePressEvent(self, e):
        if self._menu:
            self._menu.setMinimumWidth(self.width())
            self._menu.triggered.connect(lambda s: self.setText(s.text()))
            self._menu.exec(self.mapToGlobal(QPoint(0,self.height())))
            self.clearFocus()
        
        self.pressed.emit()
        self.clicked.emit()

class _DropDownTransparentPushButton (_DropDownPushButton):
    """ DropDownPushButton with no border and background color """

class _DropDownPrimaryPushButton (_DropDownPushButton):
     """ DropDownPushButton with highlight color """

class _TogglePushButton (_PushButton):
    """ checkable PushButton """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCheckable(True)
        self.textOn = "Enable"
        self.textOff = "Disable"

    def paintEvent(self, a0):
        if self.isChecked(): self.setText(self.textOn)
        else: self.setText(self.textOff)
        return super().paintEvent(a0)
    
class _ToolButton (QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._icon = None
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    
    def setMenu(self, menu: QMenu) -> None:
        self.setProperty("hasMenu",True)
        return super().setMenu(menu)

    def mousePressEvent(self, a0):
        self.clearFocus()
        self.pressed.emit()
        self.clicked.emit()

    def setIcon(self, icon:QIcon|str) -> None:
        if isinstance(icon, QIcon):
            self._icon = icon
        else: self._icon = Icon(icon)
        super().setIcon(self._icon)
    
    def update(self):
        if self._icon: super().setIcon(self._icon)
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
        self.view().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.view().window().setWindowFlags(Qt.WindowType.Popup | 
                                            Qt.WindowType.FramelessWindowHint |
                                            Qt.WindowType.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        if items: self.addItems(items)

class _TransparentComboBox (_ComboBox):
    """ """

class _PrimaryComboBox (_ComboBox):
    """ """

class _Toggle(QFrame):

    checkedChanged = Signal(bool)

    def __init__(self, width = 60, height = 40, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
        if self.width < self.height * 2 -20:
            self.width = self.height * 2 -20
        self.setFixedSize(self.width, self.height)
        self.toggle_on = False
        self.initUI()
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def initUI(self):
        
        self.button_1 = QPushButton()
        self.button_1.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.button_1.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.button_2 = QPushButton()
        self.button_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_3 = QPushButton()
        self.button_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.button_2.setFixedSize(self.height - 28, self.height - 28)
        self.button_3.setFixedSize(self.height - 28, self.height - 28)

        self.button_1.setStyleSheet(
            "border-radius : %d; border : 1px solid black; background-color: rgb(255, 255, 255)"%((self.height-20)//2))
        
        self.button_2.setStyleSheet(
            "border-radius : %d; background-color: rgb(0, 0, 0)"%((self.height - 28)//2))
        
        self.button_3.setStyleSheet(
            "border-radius : %d; background-color: rgb(255, 255, 255)"%((self.height - 28)//2))
        self.button_3.setVisible(False)
        
        self.button_1.clicked.connect(self._toggle)
        self.button_2.clicked.connect(self._toggle)
        self.button_3.clicked.connect(self._toggle)

        layout = QGridLayout()
        layout.addWidget(self.button_1, 0, 0, 1, 2)
        layout.addWidget(self.button_2, 0, 0, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_3, 0, 1, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def setChecked(self, check:bool):
        if check != self.toggle_on:
            self.toggle_on = check
            self.checkChange()
        
    
    def _toggle (self):
        self.toggle_on = not self.toggle_on
        self.checkChange()
    
    def checkChange (self):
        
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

class HButton(QWidget): 
    """" Button Widget in horizontal layout """
    def __init__(self, text:str=None, text2:str=None, 
                 parent:QWidget=None, flags:Qt.WindowType=Qt.WindowType.Widget):
        super().__init__(parent, flags)

        self.text = text
        self.text2 = text2

        self.label  = BodyLabel(text, parent)
        self.label2 = InfoLabel(text2, parent)
        self.label2.setWordWrap(True)
        self.label2.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        layout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        layout.addLayout(self.butn_layout)

    def setText(self, value:str):
        self.label.setText(value)
        self.text = value
    
    def setText2(self, value:str):
        self.label2.setText(value)
        self.text2 = value
    
    def enterEvent(self, event):
        self.label2.show()
        return super().enterEvent(event)

    def leaveEvent(self, a0):
        self.label2.hide()
        return super().leaveEvent(a0)

class PushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _PushButton(parent=parent)
        self.butn_layout.addWidget(self.button)
           
class TransparentPushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)
        
        self.button = _TransparentPushButton(parent=parent)
        self.butn_layout.addWidget(self.button)
        
class PrimaryPushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)
        
        self.button = _PrimaryPushButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownPushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _DropDownPushButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownTransparentPushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _DropDownTransparentPushButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownPrimaryPushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _DropDownPrimaryPushButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class TogglePushButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _TogglePushButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class ToolButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _ToolButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class TransparentToolButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _TransparentToolButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class PrimaryToolButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _PrimaryToolButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class ToggleToolButton (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _ToggleToolButton(parent=parent)
        self.butn_layout.addWidget(self.button)

class ComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _ComboBox(items, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)

class TransparentComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)
        
        self.button = _TransparentComboBox(items, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)

class PrimaryComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)

        self.button = _PrimaryComboBox(items, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)
    
class Toggle (HButton):
    def __init__(self, text:str=None, text2:str=None, parent=None):
        super().__init__(text, text2, parent)
        
        self.button = _Toggle(parent=parent)
        self.butn_layout.addWidget(self.button)

class SegmentedWidget (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,5)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.buttons = list()
        self.funcs = list()
    
    def addButton (self, text:str, func):
        button = _TransparentPushButton()
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
        for btn in self.findChildren(_TransparentPushButton):
            btn : _TransparentPushButton
            btn.setStyleSheet("font-weight:normal")
            if btn.text() == button_text:
                self.currentWidget = btn
                btn.setStyleSheet("font-weight:bold")
                self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.currentWidget:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 120, 215))

        x = int(self.currentWidget.x())
        y = int(self.currentWidget.y())
        h = int(self.currentWidget.height())
        w = int(self.currentWidget.width())
       
        painter.drawRoundedRect(x, y+h+2, w, 3, 1.5, 1.5)

        
    

