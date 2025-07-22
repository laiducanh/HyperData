from PySide6.QtCore import QObject, Qt, Signal, QEvent, QPoint, QRectF, QTimer
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QWidget, QComboBox, QPushButton, QFrame, QSizePolicy, QCheckBox,
                             QSizePolicy, QGridLayout, QToolButton, QScrollArea, QVBoxLayout, QLayout, QRadioButton,
                             QGroupBox)
from PySide6.QtGui import QCursor, QPainter, QColor, QIcon
from PySide6.QtSvg import QSvgRenderer
from typing import Iterable, Union
from ui.base_widgets.text import BodyLabel, InfoLabel, TitleLabel
from ui.base_widgets.menu import Menu
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.utils import icon as Icon
from ui.utils import isDark
from config.settings import config
from typing import Callable, Union, overload

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
        super().__init__(icon=icon, menu=menu, getter=getter, setter=setter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)

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

class VButton(Frame):
    """" Button Widget in vertical layout """
    def __init__(self, label:str=None, label2:str=None, layout:QLayout=None, parent:QWidget=None):
        super().__init__(parent)

        self.label  = BodyLabel(parent=parent, text=label)
        self.label2 = InfoLabel(parent=parent, text=label2, wordWrap=True)
        if not label2: self.label2.hide()

        vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        vlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        vlayout.addLayout(self.butn_layout)

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
    
class HButton(Frame): 
    """" Button Widget in horizontal layout """
    def __init__(self, label:str=None, label2:str=None, layout:QLayout=None, parent:QWidget=None):
        super().__init__(parent)

        self.label  = BodyLabel(parent=parent, text=label)
        self.label2 = InfoLabel(parent=parent, text=label2, wordWrap=True)
        if not label2: self.label2.hide()

        hlayout = QHBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        hlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QHBoxLayout()
        hlayout.addLayout(self.butn_layout)

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

class VGroupRadioButton(Frame):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 setter:Callable=None, getter:Callable=None, layout:QLayout=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=True)
        if not label2: self.label2.hide()

        vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        vlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        vlayout.addLayout(self.butn_layout)

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
    
class HGroupRadioButton(Frame):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=True)
        if not label2: self.label2.hide()

        vlayout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        vlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QHBoxLayout()
        vlayout.addLayout(self.butn_layout)

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

class GridGroupRadioButton(Frame):
    checkChanged = Signal(str)
    def __init__(self, label:str=None, label2:str=None, items:Iterable[str]=None,
                 grid:tuple[float,float]=(0,0), layout:QLayout=None, 
                 setter:Callable=None, getter:Callable=None, parent = None):
        super().__init__(parent)

        self.items = items
        self.setter = setter
        self.getter = getter

        self.label  = BodyLabel(parent, text=label)
        self.label2 = InfoLabel(parent, text=label2, wordWrap=True)
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

class SegmentedWidget(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        # self._layout.setContentsMargins(0,0,0,5)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.buttons = list()
        self.funcs = list()
    
    def addButton (self, text:str, func):
        button = TransparentPushButton()
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
       
    

