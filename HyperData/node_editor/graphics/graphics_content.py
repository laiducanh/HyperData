from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction
import pandas as pd
from data_processing.data_window import DataView
from ui.base_widgets.menu import Menu
from ui.base_widgets.line_edit import TextEdit
from ui.base_widgets.button import TransparentPushButton, TransparentToolButton
from ui.base_widgets.window import ProgressBar

class NodeComment (TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("Comment")

class GraphicsContent(QWidget):
    sig = Signal()
    def __init__(self, parent=None): # parent is an instance of "NodeGraphicsView"
        super().__init__()

        self.view = DataView(pd.DataFrame(),parent)
        self.menu = Menu()
        self.comment = NodeComment() 
        self.comment.hide()

        self.initUI()
        self.initMenu()

        self.data_to_view = pd.DataFrame()

    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.hlayout = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout)

        
        self.exec_btn = TransparentToolButton()
        self.exec_btn.setIcon("play.png")
        self.exec_btn.setToolTip("Execute")
        self.exec_btn.clicked.connect(self.exec)
        self.hlayout.addWidget(self.exec_btn)
        self.config_btn = TransparentToolButton()
        self.config_btn.setIcon("settings.png")
        self.config_btn.setToolTip("Configuration")
        self.config_btn.clicked.connect(self.config)
        self.hlayout.addWidget(self.config_btn)
        comment = TransparentToolButton()
        comment.setIcon("comment.png")
        comment.setToolTip("Comment")
        comment.clicked.connect(lambda: self.comment.hide() if self.comment.isVisible() else self.comment.show())
        self.hlayout.addWidget(comment)

        self.label = TransparentPushButton()
        self.label.clicked.connect(self.viewData)
        #self.label.setContentsMargins(5,0,5,3)
        self.vlayout.addWidget(self.label)
        #self.setFixedHeight(46)
        
        self.vlayout.addWidget(self.comment)
        self.progress = ProgressBar()
        self.vlayout.addWidget(self.progress)
    
    def initMenu(self):
        action = QAction("Execute Card",self.menu)
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = QAction("View Output",self.menu)
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        action = QAction("Configuration",self.menu)
        action.triggered.connect(self.config)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Show Comment",self.menu)
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = QAction("Hide Comment",self.menu)
        action.triggered.connect(self.comment.hide)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Change Color", self.menu)
        action.triggered.connect(self.showColorDialog)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Save Data", self.menu)
        action.triggered.connect(self.saveData)
        self.menu.addAction(action)
        action = QAction("Delete Card",self.menu)
        action.triggered.connect(lambda: self.parent.deleteSelected())
        self.menu.addAction(action)

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        pass
    
    def exec (self, *args, **kwargs):
        pass

    def func(self, *args, **kwargs):
        """ main function of the node """
        pass
    
    def exec_done(self):
        pass

    def pipeline (self):
        pass
    
    def pipeline_signal (self):
        pass

    def eval (self):
        """ use to process data_in """
        pass

    def viewData (self):
        self.view.update_data(self.data_to_view)
        self.view.show()
    
    def saveData(self):
        self.view.tableview.save_data()
    
    def showColorDialog(self):
        pass

    def resetNode(self):
        pass
        
    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass
