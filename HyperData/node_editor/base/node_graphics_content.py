from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import pyqtSignal, Qt, QThreadPool
from PyQt6.QtGui import QFont, QAction, QPaintEvent
import qfluentwidgets, pandas
from data_processing.data_window import DataView
from ui.base_widgets.menu import Menu
from ui.base_widgets.text import _TextEdit
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.threadpool import Worker
from config.settings import logger


class NodeComment (_TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFontItalic(True)
        self.setPlaceholderText("Comment")

class NodeContentWidget(QWidget):
    sig = pyqtSignal()
    def __init__(self, node: NodeGraphicsNode,parent=None): # parent is an instance of "NodeGraphicsSence"
        super().__init__()
        self.setStyleSheet('background-color:transparent')
        self.node = node
        self.parent = parent
        self.threadpool = parent.threadpool
        self.threadpool: QThreadPool
        self.view = DataView(pandas.DataFrame())
        self.menu = Menu()
        self.comment = NodeComment() 
        self.comment.hide()
        self.name = type(self).__name__

        self.initUI()
        self.initMenu()

        self.data_to_view = pandas.DataFrame()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        font = QFont('Monospace', 8)
        self.exec_btn = qfluentwidgets.PillPushButton('Execute')
        self.exec_btn.setFont(font)
        self.exec_btn.setCheckable(False)
        self.exec_btn.pressed.connect(self.exec)
        self.layout.addWidget(self.exec_btn)
        self.label = qfluentwidgets.TransparentPushButton(f'Shape: (0, 0)')
        self.label.setFont(font)
        self.label.pressed.connect(self.viewData)
        #self.label.setContentsMargins(5,0,5,3)
        self.layout.addWidget(self.label)
        #self.setFixedHeight(46)
        self.config_btn = qfluentwidgets.TransparentPushButton("Configuration")
        self.config_btn.clicked.connect(self.config)
        self.config_btn.setFont(font)
        self.layout.addWidget(self.config_btn)
        self.layout.addWidget(self.comment)
        self.progress = qfluentwidgets.ProgressBar()
        self.layout.addWidget(self.progress)
    
    def initMenu(self):
        action = QAction("Execute Card")
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = QAction("View Output")
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        action = QAction("Configuration")
        action.triggered.connect(self.config)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Show Comment")
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = QAction("Hide Comment")
        action.triggered.connect(self.comment.hide)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Delete Card")
        action.triggered.connect(lambda: self.parent.removeNode(self.node))
        self.menu.addAction(action)

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        """ use for threadpool run """
        self.progress.setVal(0)
        self.progress.setValue(0)
        worker = Worker(self.func, *args, **kwargs)
        worker.signals.finished.connect(self.exec_done)
        self.threadpool.start(worker)
    
    def exec (self):
        """ use to process data_out
         this function will be called when pressing execute button """
        
        self.run_threadpool()

    def func(self, *args, **kwargs):
        """ main function of the node """
        pass
    
    def exec_done(self):
        self.label.setText(f"Shape: {self.data_to_view.shape}")    
        
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e: print(e)

        self.pipeline()
        self.progress.setValue(100)

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.exec()

    def eval (self):
        """ use to process data_in """
        pass

    def viewData (self):
        self.view.update_data(self.data_to_view)
        self.view.showMaximized()
        
    def serialize(self):
        return dict()

    def deserialize(self, data, hashmap={}):
        pass





    