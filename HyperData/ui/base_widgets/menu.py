from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QCursor, QIcon
from ui.utils import icon as Icon
from typing import Union

class Menu (QMenu):
    def __init__(self, text:str=None, parent=None):
        super().__init__(title=text, parent=parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.Popup | 
                            Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.icon_path = None
    
    def setIcon(self, icon: Union[str, QIcon]) -> None:
        if isinstance(icon, str):
            self.icon_path = icon
            super().setIcon(Icon(self.icon_path))
        elif isinstance(icon, QIcon):
            self.icon_path = icon.path
            super().setIcon(icon)

    def update(self):
        if self.icon_path: super().setIcon(Icon(self.icon_path))
        for action in self.actions():
            if isinstance(action, Action): action.update()
        super().update()
    

class Action (QAction):
    """ 
    this class is an alternative of QAction 
    in cases we need to change the action's icon according to the theme change 
    
    """
    def __init__(self, icon:str=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if icon: self.setIcon(icon)

    def setIcon(self, icon: Union[str, QIcon]) -> None:
        if isinstance(icon, str):
            self.icon_path = icon
            super().setIcon(Icon(self.icon_path))
        elif isinstance(icon, QIcon):
            self.icon_path = icon.path
            super().setIcon(icon)

    def update(self):
        if self.icon_path: super().setIcon(Icon(self.icon_path))

class LineEdit_Menu (Menu):
    def __init__(self, text: str = None, parent=None):
        super().__init__(text, parent)

        self.undoAct = QAction(text="Undo", shortcut=QKeySequence("Ctrl+Z"), parent=parent)
        self.undoAct.triggered.connect(parent.undo)
        self.addAction(self.undoAct)

        self.redoAct = QAction(text="Redo", shortcut=QKeySequence("Ctrl+Y"), parent=parent)
        self.redoAct.triggered.connect(parent.redo)
        self.addAction(self.redoAct)

        self.addSeparator()

        self.cutAct = Action(text="Cut", shortcut=QKeySequence("Ctrl+X"), parent=parent)
        self.cutAct.triggered.connect(parent.cut)
        self.addAction(self.cutAct)

        self.copyAct = QAction(text="Copy", shortcut=QKeySequence("Ctrl+C"), parent=parent)
        self.copyAct.triggered.connect(parent.copy)
        self.addAction(self.copyAct)

        self.pasteAct = QAction(text="Paste", shortcut=QKeySequence("Ctrl+V"), parent=parent)
        self.pasteAct.triggered.connect(parent.paste)
        self.addAction(self.pasteAct)

        self.deleteAct = QAction(text="Delete", shortcut=QKeySequence("Del"), parent=parent)
        self.deleteAct.triggered.connect(parent.del_)
        self.addAction(self.deleteAct)

        self.addSeparator()

        self.selectAllAct = QAction(text="Select All", shortcut=QKeySequence("Ctrl+A"), parent=parent)
        self.selectAllAct.triggered.connect(parent.selectAll)
        self.addAction(self.selectAllAct)

        



        