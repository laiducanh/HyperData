import os
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence

class Menu (QMenu):
    def __init__(self, text:str=None, parent=None):
        super().__init__(title=text, parent=parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.Popup | 
                            Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

class LineEdit_Menu (Menu):
    def __init__(self, text: str = None, parent=None):
        super().__init__(text, parent)
        icon_path = os.path.join("ui","icons","black")
        self.cutAct = QAction(text="Cut", icon=QIcon(os.path.join(icon_path, "Cut_black.svg")),
                              shortcut=QKeySequence("Ctrl+X"), parent=parent)
        self.cutAct.triggered.connect(parent.cut)
        self.addAction(self.cutAct)

        self.copyAct = QAction(text="Copy", icon=QIcon(os.path.join(icon_path, "Copy_black.svg")),
                              shortcut=QKeySequence("Ctrl+C"), parent=parent)
        self.copyAct.triggered.connect(parent.copy)
        self.addAction(self.copyAct)

        self.pasteAct = QAction(text="Paste", icon=QIcon(os.path.join(icon_path, "Paste_black.svg")),
                                shortcut=QKeySequence("Ctrl+V"), parent=parent)
        self.pasteAct.triggered.connect(parent.paste)
        self.addAction(self.pasteAct)

        self.selectAllAct = QAction(text="Select All",
                                    shortcut=QKeySequence("Ctrl+A"), parent=parent)
        self.selectAllAct.triggered.connect(parent.selectAll)
        self.addAction(self.selectAllAct)

        self.addSeparator()

        self.undoAct = QAction(text="Undo", icon=QIcon(os.path.join(icon_path, "Undo_black.svg")),
                               shortcut=QKeySequence("Ctrl+Z"), parent=parent)
        self.undoAct.triggered.connect(parent.undo)
        self.addAction(self.undoAct)

        self.redoAct = QAction(text="Redo",
                               shortcut=QKeySequence("Ctrl+Y"), parent=parent)
        self.redoAct.triggered.connect(parent.redo)
        self.addAction(self.redoAct)