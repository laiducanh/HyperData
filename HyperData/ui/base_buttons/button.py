from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (QMenu, QComboBox, QPushButton, QFrame, QSizePolicy, QCheckBox,
                             QSizePolicy, QGridLayout, QToolButton, QLayout, QRadioButton,)
from PySide6.QtGui import QCursor, QIcon
from typing import Union
from ui.utils import icon as Icon
from config.settings import config
from typing import Callable, Union

class PushButton(QPushButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(text, parent, *args, **kwargs)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.icon_path = None
        self._menu = None
        self.getter = getter
        self.setter = setter

        if icon: self.setIcon(icon)
        if menu: self.setMenu(menu)
        if layout: layout.addWidget(self)
        if getter: self.setText(getter())
        if setter: self.clicked.connect(setter)
    
    def set_value(self, value:str):
        self.setText(value)

    def get_value(self) -> str:
        return self.text()

    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter

    def setMenu(self, menu: QMenu):
        self._menu = menu
        return super().setMenu(menu)
    
    def mousePressEvent(self, e):
        if self._menu:
            pos = self.mapToGlobal(self.rect().bottomLeft())
            self._menu.setMinimumWidth(self.width())
            QTimer.singleShot(0, lambda: self._menu.popup(pos))
            self.clearFocus()
        else:
            super().mousePressEvent(e)
    
    def setIcon(self, icon: Union[str, QIcon]) -> None:
        if isinstance(icon, str):
            self.icon_path = icon
            super().setIcon(Icon(self.icon_path))
        elif isinstance(icon, QIcon):
            self.icon_path = icon.path
            super().setIcon(icon)
            
    def _update(self):
        # This function serves as an updater for buttons when toggling dark/light mode
        if self.icon_path: super().setIcon(Icon(self.icon_path))
        super().update()

class TransparentPushButton(PushButton):
    """ PushButton with no border and background color """

class PrimaryPushButton(PushButton):
    """ PushButton with highlight color """

class DropDownPushButton(PushButton):
    """ PushButton with dropdown arrow """

class DropDownTransparentPushButton(DropDownPushButton):
    """ DropDownPushButton with no border and background color """

class DropDownPrimaryPushButton(DropDownPushButton):
     """ DropDownPushButton with highlight color """
    
class TogglePushButton(PushButton):
    def __init__(self, text:str='', icon:Union[str, QIcon]=None, menu:QMenu=None, getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(text=text, icon=icon, menu=menu, getter=getter, setter=setter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)

class CheckBox(QCheckBox):
    def __init__(self, text:str='', getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(text, parent, *args, **kwargs)

        self.getter = getter
        self.setter = setter

        if layout: layout.addWidget(self)
        if getter: self.setChecked(getter())
        if setter: self.toggled.connect(setter)
    
    def set_value(self, value:bool):
        self.setChecked(value)

    def get_value(self) -> bool:
        return self.isChecked()

    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter
    
class ToolButton(QToolButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.icon_path = None
        self._menu = None
        self.setter = setter
        self.getter = getter
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    
        if layout: layout.addWidget(self)
        if menu: self.setMenu(menu)
        if getter: self.setIcon(getter())
        if setter: self.clicked.connect(setter)
        if icon: self.setIcon(icon)
    
    def get_value(self) -> str:
        return self.icon_path
    
    def set_value(self, value:str):
        self.setIcon(value)
    
    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter
    
    def setMenu(self, menu: QMenu) -> None:
        self.setProperty("hasMenu", True)
        self._menu = menu
        return super().setMenu(menu)

    def setIcon(self, icon: Union[str, QIcon]) -> None:
        if isinstance(icon, str):
            self.icon_path = icon
            super().setIcon(Icon(self.icon_path))
        elif isinstance(icon, QIcon):
            self.icon_path = icon.path
            super().setIcon(icon)
    
    def _update(self):
        # This function serves as an updater for buttons when toggling dark/light mode
        if self.icon_path: super().setIcon(Icon(self.icon_path))
        super().update()

class TransparentToolButton(ToolButton):
    """ ToolButton with no border and background color """
    
class PrimaryToolButton(ToolButton):
    """ PushButton with highlight color """

class ToggleToolButton(ToolButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, setter:Callable=None, getter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(icon=icon, menu=menu, setter=setter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)
        if getter: self.setChecked(getter())

class ComboBox(QComboBox):
    def __init__(self, items:list[str]=[], getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.items = items
        self.setter = setter
        self.getter = getter

        # Cursor
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.view().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Rounded popup
        # self.view().window().setWindowFlags(
        #     Qt.WindowType.Popup | 
        #     Qt.WindowType.FramelessWindowHint |
        #     Qt.WindowType.NoDropShadowWindowHint
        # )
        # self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        if items: self.addItems(items)
        if getter: self.setCurrentText(getter())
        if setter: self.currentTextChanged.connect(setter)
        if layout: layout.addWidget(self)
    
    def wheelEvent(self, e):
        e.ignore()
    
    def _addItems(self, texts:list[str]):
        self.items = texts
        return super().addItems(texts)
    
    def _addItem(self, text:str):
        self.items.append(text)
        return super().addItem(text)

    def get_value(self) -> str:
        return self.currentText()
    
    def set_value(self, value:str):
        self.setCurrentText(value)
    
    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter

class TransparentComboBox (ComboBox):
    """ """

class PrimaryComboBox (ComboBox):
    """ """

class Toggle(QFrame):
    checkedChanged = Signal(bool)
    def __init__(self, setter:Callable=None, getter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(parent)

        self.width = 60
        self.height = 40
        if self.width < self.height * 2 - 20:
            self.width = self.height * 2 - 20
        self.setFixedSize(self.width, self.height)
        self.toggle_on = False
        self.setter = setter
        self.getter = getter

        self.initUI()
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        if getter: self.setChecked(getter())
        if setter: self.checkedChanged.connect(setter)
        if layout: layout.addWidget(self)

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
        
        if self.toggle_on:
            self.button_1.setStyleSheet(f"border-radius : {(self.height - 20)//2}; border : none; background-color: {config['themecolor']}")
            self.button_2.setVisible(False)
            self.button_3.setVisible(True)
        else:
            self.button_1.setStyleSheet(f"border-radius : {(self.height - 20)//2}; border : 1px solid black; background-color: white")
            self.button_2.setVisible(True)
            self.button_3.setVisible(False)
        
        self.checkedChanged.emit(self.toggle_on)

    def isChecked(self):
        return self.toggle_on
    
    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value:bool):
        self.setChecked(value)
    
    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter

class RadioButton(QRadioButton):
    def __init__(self, text:str='', layout:QLayout=None, parent=None):
        super().__init__(text, parent)

        if layout: layout.addWidget(self)
    
    def get_value(self) -> bool:
        return self.isChecked()

    def set_value(self, value:bool):
        self.setChecked(value)