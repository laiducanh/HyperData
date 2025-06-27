from PySide6.QtCore import QObject, Qt, Signal, QEvent, QPoint, QRectF, QTimer
from PySide6.QtWidgets import (QHBoxLayout, QMenu, QWidget, QComboBox, QPushButton, QFrame, QSizePolicy,
                             QSizePolicy, QGridLayout, QToolButton, QScrollArea, QVBoxLayout, QLayout)
from PySide6.QtGui import QCursor, QPainter, QColor, QIcon
from PySide6.QtSvg import QSvgRenderer
from typing import Iterable, Union
from ui.base_widgets.text import BodyLabel, InfoLabel, TitleLabel
from ui.base_widgets.menu import Menu
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.utils import icon as Icon
from ui.utils import isDark
from config.settings import config
from typing import Callable, Union

class _PushButton (QPushButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, 
                 getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.icon_path = None
        self._menu = menu
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

class _TransparentPushButton (_PushButton):
    """ PushButton with no border and background color """

class _PrimaryPushButton (_PushButton):
    """ PushButton with highlight color """

class _DropDownPushButton (_PushButton):
    """ PushButton with dropdown arrow """

class _DropDownTransparentPushButton (_DropDownPushButton):
    """ DropDownPushButton with no border and background color """

class _DropDownPrimaryPushButton (_DropDownPushButton):
     """ DropDownPushButton with highlight color """

class _TogglePushButton (_PushButton):
    """ checkable PushButton """
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, 
                 getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(icon=icon, menu=menu, getter=getter, setter=setter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)

class _CheckBox(_TransparentPushButton):
    """ checkable button, the same as _TogglePushButton,
    but behaves as transparent button when uncheck """
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None, 
                 getter:Callable=None, setter:Callable=None, 
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(icon=icon, menu=menu, getter=getter, setter=setter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)
    
class _ToolButton (QToolButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.icon_path = None
        self._menu = menu
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

    # def mousePressEvent(self, a0):
    #     self.clearFocus()
    #     self.pressed.emit()
    #     self.clicked.emit()

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

class _TransparentToolButton (_ToolButton):
    """ ToolButton with no border and background color """
    
class _PrimaryToolButton (_ToolButton):
    """ PushButton with highlight color """

class _ToggleToolButton (_ToolButton):
    """ checkable ToolButton """
    def __init__(self, icon:Union[str, QIcon]=None, setter:Callable=None, getter:Callable=None,
                 layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(icon=icon, setter=setter, getter=getter, layout=layout, parent=parent, *args, **kwargs)

        self.setCheckable(True)

class _ComboBox (QComboBox):
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
        self.view().window().setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        if items: self.addItems(items)
        if getter: self.setCurrentText(getter())
        if setter: self.currentTextChanged.connect(setter)
        if layout: layout.addWidget(self)
    
    def addItems(self, texts:list[str]):
        self.items = texts
        return super().addItems(texts)

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

class _TransparentComboBox (_ComboBox):
    """ """

class _PrimaryComboBox (_ComboBox):
    """ """

class _Toggle(QFrame):
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

class _RadioButton (QFrame):
    checkChanged = Signal()
    def __init__(self, items:dict=dict(), parent=None):
        super().__init__(parent=parent)
    
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 2, 0, 2)

        self.buttons = list()
        for key in items:
            btn = _TogglePushButton(parent)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            main_label = BodyLabel(key)
            sub_label = InfoLabel(items[key])
            sub_label.setWordWrap(True)

            inner_layout = QVBoxLayout()
            inner_layout.setContentsMargins(5, 5, 5, 5)
            inner_layout.addWidget(main_label)
            inner_layout.addWidget(sub_label)

            btn.setLayout(inner_layout)
            btn.setObjectName(key)
            
            layout.addWidget(btn)
            btn.pressed.connect(lambda key=key: self.setCurrentWidget(key))
            self.buttons.append(key)
        
        self.setCurrentWidget(self.buttons[0])
        self.currentWidget.setChecked(True)

    def setCurrentWidget (self, button_text:str):
        for btn in self.findChildren(_TogglePushButton):
            btn : _TogglePushButton
            if btn.objectName() == button_text: 
                self.currentWidget = btn
            else: btn.setChecked(False)
            self.checkChanged.emit()
            self.update()


class VButton(Frame):
    """" Button Widget in vertical layout """
    def __init__(self, text:str=None, text2:str=None, 
                 parent:QWidget=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.text = text
        self.text2 = text2

        self.label  = BodyLabel(parent, text=text)
        self.label2 = InfoLabel(parent, text=text2, wordWrap=True)
        if not text2: self.label2.hide()

        layout = QVBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

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
    
    def get_value(self):
        return self.button.get_value()

    def set_value(self, value):
        self.button.set_value(value)
    
class HButton(Frame): 
    """" Button Widget in horizontal layout """
    def __init__(self, text:str=None, text2:str=None, layout:QLayout=None,
                 parent:QWidget=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.text = text
        self.text2 = text2

        self.label  = BodyLabel(parent, text=text)
        self.label2 = InfoLabel(parent, text=text2, wordWrap=True)
        if not text2: self.label2.hide()

        hlayout = QHBoxLayout(self)
        #layout.setContentsMargins(0,0,0,0)

        self.text_layout = QVBoxLayout()
        hlayout.addLayout(self.text_layout)
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.label2)

        self.butn_layout = QVBoxLayout()
        hlayout.addLayout(self.butn_layout)

        if layout: layout.addWidget(self)

    def setText(self, value:str):
        self.label.setText(value)
        self.text = value
    
    def setText2(self, value:str):
        self.label2.setText(value)
        self.text2 = value
    
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
    
    def enterEvent(self, event):
        #self.label2.show()
        return super().enterEvent(event)

    def leaveEvent(self, a0):
        #self.label2.hide()
        return super().leaveEvent(a0)

class PushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _PushButton(icon=icon, menu=menu, setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)
           
class TransparentPushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)
        
        self.button = _TransparentPushButton(icon=icon, menu=menu, setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)
        
class PrimaryPushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)
        
        self.button = _PrimaryPushButton(icon=icon, menu=menu, setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownPushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _DropDownPushButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownTransparentPushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _DropDownTransparentPushButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class DropDownPrimaryPushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _DropDownPrimaryPushButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class TogglePushButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _TogglePushButton(icon=icon, menu=menu, setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)

class ToolButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _ToolButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class TransparentToolButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _TransparentToolButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class PrimaryToolButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, menu:QMenu=None,
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _PrimaryToolButton(icon=icon, menu=menu, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)

class ToggleToolButton (HButton):
    def __init__(self, icon:Union[str, QIcon]=None, 
                 setter:Callable=None, getter:Callable=None,
                 text:str=None, text2:str=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _ToggleToolButton(icon=icon, setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)

class ComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None, 
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _ComboBox(items=items, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)

class TransparentComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None,  
                 getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)
        
        self.button = _TransparentComboBox(items=items, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)

class PrimaryComboBox (HButton):
    def __init__(self, items:Iterable[str]=None, text:str=None, text2:str=None, 
                 setter:Callable=None, getter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)

        self.button = _PrimaryComboBox(items=items, getter=getter, setter=setter, parent=parent)
        self.butn_layout.addWidget(self.button)
        self.button.setFixedWidth(150)
    
class Toggle (HButton):
    def __init__(self, text:str=None, text2:str=None, setter:Callable=None, 
                 getter:Callable=None, layout:QLayout=None, parent=None):
        super().__init__(text=text, text2=text2, layout=layout, parent=parent)
        
        self.button = _Toggle(setter=setter, getter=getter, parent=parent)
        self.butn_layout.addWidget(self.button)

class RadioButton (VButton):
    def __init__(self, text = None, text2 = None, items = dict(), parent = None, *args, **kwargs):
        super().__init__(text, text2, parent, *args, **kwargs)

        self.button = _RadioButton(items, parent)
        self.butn_layout.addWidget(self.button)

class SegmentedWidget (Frame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        # self._layout.setContentsMargins(0,0,0,5)
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
        for idx, btn in enumerate(self.findChildren(_TransparentPushButton)):
            btn : _TransparentPushButton
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

    def paintEvent(self, e):
        super().paintEvent(e)

        # painter = QPainter(self)
        # painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        # painter.setPen(Qt.PenStyle.NoPen)
        # painter.setBrush(QColor(0, 120, 215))

        # x = int(self.currentWidget.x())
        # y = int(self.currentWidget.y())
        # h = int(self.currentWidget.height())
        # w = int(self.currentWidget.width())
       
        # painter.drawRoundedRect(x, y+h+2, w, 3, 1.5, 1.5)

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
        for btn in self.findChildren(_CheckBox):
            self.btn_layout.removeWidget(btn)
            btn.deleteLater()
        
        for idx, btn in enumerate(list_btn):
            btn = _CheckBox(text=btn)
            btn.pressed.connect(lambda i=idx, b=btn: self.changeState(i, b.isChecked()))
            btn.setChecked(self.states[idx])
            self.btn_layout.addWidget(btn)
    
    def changeState(self, idx:int, state:bool):
        self.states[idx] = not state
       
    

