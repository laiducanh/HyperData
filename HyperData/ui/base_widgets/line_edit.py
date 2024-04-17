from PyQt6.QtCore import pyqtSignal, Qt, QStringListModel, QSize
from PyQt6.QtGui import QContextMenuEvent, QFocusEvent, QFont, QKeyEvent
from PyQt6.QtWidgets import (QTextEdit, QVBoxLayout, QWidget, QCompleter, QHBoxLayout,
                             QTreeWidget, QLineEdit)
from ui.base_widgets.menu import Menu, LineEdit_Menu
from ui.base_widgets.button import _TransparentPushButton, _ComboBox
from ui.base_widgets.text import BodyLabel

class _LineEdit (QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent) 
        
    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self)
        menu.exec(a0.globalPos())

class _TextEdit (QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self)
        menu.exec(a0.globalPos())

class _SearchBox (_LineEdit):
    def __init__(self, data_lookup: QTreeWidget=None, parent=None):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        self.searchButton = _TransparentPushButton(parent=parent)
        self.searchButton.setIcon("search.png")
        self.searchButton.setIconSize(QSize(12,12))
        self.searchButton.setFixedSize(29, 25)
        self.hBoxLayout.addWidget(self.searchButton, 0, Qt.AlignmentFlag.AlignRight)

        self.setTextMargins(0, 0, 59, 0)

        self.lookup = data_lookup
        self.textChanged.connect(self.search_func)
    
    def set_TreeView (self, data_lookup:QTreeWidget):
        self.lookup = data_lookup
    
    def search_func (self, s:str):
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

class _CompleterLineEdit (_ComboBox):
    def __init__(self, items:list=None, parent=None):
        super().__init__(items=items, parent=parent)    

        if items: self.items = items
        else: self.items = list()

        self.lineedit = QLineEdit(parent=parent)
        self.setLineEdit(self.lineedit)
        
        self.completer().setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer().setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer().setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)        
    
    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        menu = LineEdit_Menu(parent=self.lineedit)
        menu.exec(a0.globalPos())
    
    def _addItems (self, items:list):
        self.items += items
        self.items = list(set(self.items)) # remove duplicates
        self.clear()
        self.addItems(self.items)
        self.setCompleter(Completer(string_list=self.items))
    
    def _addItem(self, item:str):
        self.items.append(item)
        self.items = list(set(self.items)) # remove duplicates
        self.clear()
        self.addItems(self.items)
        self.setCompleter(Completer(string_list=self.items))
    
    def focusOutEvent(self, e: QFocusEvent) -> None:
        # add current text in lineedit when focus out
        self._addItem(self.currentText())
        return super().focusOutEvent(e)
    
class LineEdit (QWidget):
    def __init__(self, text=None, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        if text != None:
            self.layout.addWidget(BodyLabel(text))

        self.button = _LineEdit(parent=parent)
        self.layout.addWidget(self.button)   

class TextEdit (QWidget):
    def __init__(self, text=None, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        if text != None:
            self.layout.addWidget(BodyLabel(text))

        self.button = _TextEdit(parent=parent)
        self.layout.addWidget(self.button) 

class CompleterLineEdit(QWidget):
    def __init__(self, text=None, items=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text))

        self.button = _CompleterLineEdit(items=items, parent=parent)
        layout.addWidget(self.button)


















class Completer (QCompleter):
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




    


class TextEditBase (_TextEdit):
    sig_focusOut = pyqtSignal()
    def __init__(self, text=None, font=QFont('Arial',13), parent=None):
        super().__init__(parent=parent)

        self.append(text)
        self.setFont(font)

        #self.setStyleSheet('background-color:white')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.setContentsMargins(0,0,0,0)
        
        
         
    def focusOutEvent(self, e):
        # Do something with the event here
        self.sig_focusOut.emit()
        #self.deleteLater()
        super(TextEditBase, self).focusOutEvent(e) # Do the default action on the parent class QLineEdit
    

    
class TextEdit_Menu (Menu): 
    def __init__(self, text=None, font=QFont('Arial',13), parent=None):
        super().__init__(parent=parent)
        
        _layout = QVBoxLayout()
        self.text = TextEditBase(text=text,font=font,parent=self)
        #self.view.hide()
        self.hBoxLayout.addChildWidget(self.text)
        #elf.setLayout(_layout)
        _layout.setContentsMargins(0,0,0,0)
        self.text.textChanged.connect(self.adjustBox)
        self.setStyleSheet('background-color:transparent; border:none')

        self.adjustBox()
       
    def adjustBox (self):
        self.text.setFocus()
        margins = self.layout().contentsMargins()
        _height = int(self.text.document().size().height() + margins.top() + margins.bottom())
        _width = int(self.text.document().size().width() + margins.left() + margins.right())
        
        #self.setFixedSize(_width,_height)
        self.text.setFixedSize(_width,_height)
        

        