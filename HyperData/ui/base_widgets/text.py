from PyQt6.QtCore import QObject, pyqtSignal, Qt, QStringListModel
from PyQt6.QtGui import QFocusEvent, QFont, QColor, QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QCompleter, QHBoxLayout, QTreeWidget
import os, qfluentwidgets
from ui.base_widgets.menu import Menu

class BodyLabel (qfluentwidgets.BodyLabel):
    def __init__(self, text:str=None):
        super().__init__(text)

class StrongBodyLabel (qfluentwidgets.StrongBodyLabel):
    def __init__(self, text:str):
        super().__init__(text)

class TitleLabel (qfluentwidgets.TitleLabel):
    def __init__(self, text:str):
        super().__init__(text)

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


class _LineEdit (qfluentwidgets.LineEdit):
    def __init__(self, tooltip=None, completer_source=None, parent=None):
        super().__init__(parent=parent)
        self.completer_source = completer_source

        if self.completer_source != None:
            self.completer_ = Completer(completer_source)
            self.setCompleter(self.completer_)
        if tooltip != None:
            self.setToolTip(tooltip)
            self.installEventFilter(qfluentwidgets.ToolTipFilter(self, 0, qfluentwidgets.ToolTipPosition.TOP_LEFT))
        
    def focusInEvent(self, e):
        self.clearButton.setVisible(True)  
        if self.completer_source != None: 
            self.completer_.updateModel(self.completer_source)
        return super().focusInEvent(e)
    

    
class LineEdit (QWidget):
    def __init__(self, text=None):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        if text != None:
            self.layout.addWidget(BodyLabel(text.title()))

        self.button = _LineEdit()
        self.layout.addWidget(self.button)    



class _EditableComboBox (qfluentwidgets.EditableComboBox):
    def __init__(self, tooltip=None, completer_source=None, parent=None):
        super().__init__(parent=parent)
        self.completer_source = completer_source
        
        if self.completer_source != None: 
            self.addItems(self.completer_source)
            self.completer_ = Completer(completer_source)
            self.setCompleter(self._completer)

        if tooltip != None:
            self.setToolTip(tooltip)
            self.installEventFilter(qfluentwidgets.ToolTipFilter(self, 0, qfluentwidgets.ToolTipPosition.TOP_LEFT))

        self.setCurrentIndex(-1)
        self.dropButton.clicked.connect(self.update)
        
    def focusInEvent(self, e):
        self.clearButton.setVisible(True)
        self.update()
        
        return super().focusInEvent(e)

    def focusOutEvent(self, e):
        
        return super().focusOutEvent(e)

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        return super().mouseMoveEvent(a0)


    def update(self):
        if self.completer_source != None: 
            _completer = self.completer_source
            
            if not _completer in [None]:
                if not self.text() in _completer and self.text() != '':
                    _completer.append(self.text())
                for i, item in enumerate(self.items):
                    if item.text in _completer:
                        _completer.remove(item.text)
                self.addItems(_completer)
                self.completer_.updateModel(_completer)
                self.completer_source = [a.text for a in self.items]

class EditableComboBox(QWidget):
    def __init__(self, text=None, tooltip=None, completer_source=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        if text != None:
            layout.addWidget(BodyLabel(text.title()))

        self.button = _EditableComboBox(tooltip, completer_source, parent)
        layout.addWidget(self.button)

    
class _TextEdit (qfluentwidgets.TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

class TextEdit (QWidget):
    def __init__(self, text=None, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)


        if text != None:
            self.layout.addWidget(BodyLabel(text.title()))

        self.button = _TextEdit()
        self.layout.addWidget(self.button)
    


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
        
        

class _Search_Box (qfluentwidgets.SearchLineEdit):
    def __init__(self, treeview: QTreeWidget=None, parent=None):
        super().__init__(parent)

        self.treeview = treeview
        self.textChanged.connect(self.search_func)
    
    def set_TreeView (self, treeview:QTreeWidget):
        self.treeview = treeview
    
    def search_func (self, s:str):
        for i in range(self.treeview.topLevelItemCount()):
            self.treeview.topLevelItem(i).setHidden(True)
       
        for i in range(self.treeview.topLevelItemCount()):
            if s.lower() in self.treeview.topLevelItem(i).text(0).lower():
                self.treeview.topLevelItem(i).setHidden(False)
                for j in range(self.treeview.topLevelItem(i).childCount()):
                    self.treeview.topLevelItem(i).child(j).setHidden(False)
            else:
                for j in range(self.treeview.topLevelItem(i).childCount()):
                    if s.lower() in self.treeview.topLevelItem(i).child(j).text(0).lower():
                        self.treeview.topLevelItem(i).setHidden(False)
                        self.treeview.topLevelItem(i).child(j).setHidden(False)
                    else:
                        self.treeview.topLevelItem(i).child(j).setHidden(True)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.clear()
        return super().keyPressEvent(a0)