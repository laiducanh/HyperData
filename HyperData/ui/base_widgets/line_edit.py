from PySide6.QtCore import Qt, QStringListModel, QSize
from PySide6.QtGui import QContextMenuEvent, QKeyEvent
from PySide6.QtWidgets import (QTextEdit, QLayout, QCompleter, QHBoxLayout, QTreeWidget, QLineEdit, QSizePolicy)
from ui.base_widgets.menu import LineEdit_Menu
from ui.base_widgets.button import TransparentPushButton, TransparentComboBox, HButton, VButton
from typing import Callable

class LineEdit(QLineEdit):
    def __init__(self, getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs) 

        self.default_width = 150
        self.setFixedWidth(self.default_width)
        self.setMouseTracking(True)

        self.getter = getter
        self.setter = setter

        if getter: self.setText(getter())
        if setter: self.returnPressed.connect(lambda: setter(self.text()))
        if layout: layout.addWidget(self)
    
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
        
    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self)
        menu.exec(a0.globalPos())
    
    def set_width(self, value:float):
        self.default_width = value
        self.setFixedWidth(self.default_width)

    def enterEvent(self, event):
        self.setMaximumWidth(3*self.default_width)
        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Minimum
        )
        return super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setFixedWidth(self.default_width)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum
        )
        return super().leaveEvent(event)
    
class TextEdit(QTextEdit):
    def __init__(self, getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.getter = getter
        self.setter = setter

        if getter: self.setText(getter())
        if setter: self.textChanged.connect(setter)
        if layout: layout.addWidget(self)
    
    def set_value(self, value:str):
        self.setText(value)
    
    def get_value(self) -> str:
        return self.toPlainText()

    def set_setter(self, setter:Callable):
        self.setter = setter
    
    def get_setter(self) -> Callable:
        return self.setter
    
    def set_getter(self, getter:Callable):
        self.getter = getter

    def get_getter(self) -> Callable:
        return self.getter

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self)
        menu.exec(a0.globalPos())

class SearchBox(LineEdit):
    def __init__(self, data_lookup: QTreeWidget=None, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.setMaximumWidth(100000) # Expand as much as possible
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.searchButton = TransparentPushButton(parent=parent)
        self.searchButton.setIcon("search.png")
        self.searchButton.setIconSize(QSize(12,12))
        self.searchButton.setFixedWidth(29)
        self.searchButton.clicked.connect(self.search_func)
        self.hBoxLayout.addWidget(self.searchButton, 0, Qt.AlignmentFlag.AlignRight)

        self.setTextMargins(0, 0, 59, 0)

        self.lookup = data_lookup
        self.textChanged.connect(self.search_func)
    
    def set_TreeView (self, data_lookup:QTreeWidget):
        self.lookup = data_lookup
    
    def search_func (self):
        if self.lookup:
            s = self.text()
            for i in range(self.lookup.topLevelItemCount()):
                self.lookup.topLevelItem(i).setHidden(True)
        
            for i in range(self.lookup.topLevelItemCount()):
                if s.lower() in self.lookup.topLevelItem(i).text(0).lower():
                    self.lookup.topLevelItem(i).setHidden(False)
                    for j in range(self.lookup.topLevelItem(i).childCount()):
                        self.lookup.topLevelItem(i).child(j).setHidden(False)
                else:
                    for j in range(self.lookup.topLevelItem(i).childCount()):
                        if s.lower() in self.lookup.topLevelItem(i).child(j).text(0).lower():
                            self.lookup.topLevelItem(i).setHidden(False)
                            self.lookup.topLevelItem(i).child(j).setHidden(False)
                        else:
                            self.lookup.topLevelItem(i).child(j).setHidden(True)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.clear()
        return super().keyPressEvent(a0)

    def enterEvent(self, event):
        return QLineEdit().enterEvent(event)
    
    def leaveEvent(self, event):
        return QLineEdit().leaveEvent(event)

class CompleterLineEdit(TransparentComboBox):
    def __init__(self, items:list[str]=[], getter:Callable=None, setter:Callable=None, layout:QLayout=None, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)   

        self.items = items
        self.getter = getter
        self.setter = setter 

        self.lineedit = QLineEdit(parent=parent)
        self.setLineEdit(self.lineedit)
        
        self.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer().setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)        

        if layout: layout.addWidget(self)
        if items: self._addItems(items)
        if setter: self.lineedit.editingFinished.connect(setter)
        if getter: self.lineedit.setText(getter())

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self.lineedit)
        menu.exec(a0.globalPos())
    
    def _addItems (self, items:list):
        _text = self.lineedit.text()
        self.items = items
        self.clear()
        self.addItems(items)
        self.setCompleter(Completer(string_list=self.items))
        self.setCurrentText(_text)
        self.update()
    
    def _addItem(self, item:str):
        _text = self.lineedit.text()
        if item not in self.items: self.items.append(item)
        self.clear()
        self.addItems(self.items)
        self.setCompleter(Completer(string_list=self.items))
        self.setCurrentText(_text)
        self.update()

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

class Completer(QCompleter):
    def __init__(self, string_list:list):
        super().__init__()

        self._model = QStringListModel()
        self.updateModel(string_list)
        self.setModel(self._model)
        self.setMaxVisibleItems(5)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

    def updateModel (self, string_list):
        self._model.setStringList(string_list)
