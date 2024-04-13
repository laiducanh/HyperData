from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt, QThreadPool, QTimer
from PyQt6.QtGui import QAction
import pandas
from data_processing.data_window import DataView
from ui.base_widgets.menu import Menu
from ui.base_widgets.line_edit import _TextEdit
from ui.base_widgets.button import _TransparentPushButton, _TransparentToolButton
from ui.base_widgets.window import ProgressBar
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.threadpool import Worker
from config.settings import logger


class NodeComment (_TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("Comment")

class NodeContentWidget(QWidget):
    sig = pyqtSignal()
    def __init__(self, node: NodeGraphicsNode,parent=None): # parent is an instance of "NodeGraphicsView"
        super().__init__()
        
        self.node = node
        self.parent = parent
        self.threadpool = parent.threadpool
        self.threadpool: QThreadPool
        self.num_signal_pipeline = 0
        self.view = DataView(pandas.DataFrame())
        self.menu = Menu()
        self.comment = NodeComment() 
        self.comment.hide()
        self.name = type(self).__name__
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerStop)

        self.initUI()
        self.initMenu()

        self.data_to_view = pandas.DataFrame()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.hboxlayout = QHBoxLayout()
        self.layout.addLayout(self.hboxlayout)

        
        self.exec_btn = _TransparentToolButton()
        self.exec_btn.setIcon("play.png")
        self.exec_btn.setToolTip("Execute")
        self.exec_btn.pressed.connect(self.exec)
        self.hboxlayout.addWidget(self.exec_btn)
        self.config_btn = _TransparentToolButton()
        self.config_btn.setIcon("settings.png")
        self.config_btn.setToolTip("Configuration")
        self.config_btn.clicked.connect(self.config)
        self.hboxlayout.addWidget(self.config_btn)
        comment = _TransparentToolButton()
        comment.setIcon("comment.png")
        comment.setToolTip("Comment")
        comment.clicked.connect(lambda: self.comment.hide() if self.comment.isVisible() else self.comment.show())
        self.hboxlayout.addWidget(comment)

        self.label = _TransparentPushButton()
        self.label.setText(f'Shape: (0, 0)')
        self.label.pressed.connect(self.viewData)
        #self.label.setContentsMargins(5,0,5,3)
        self.layout.addWidget(self.label)
        #self.setFixedHeight(46)
        
        self.layout.addWidget(self.comment)
        self.progress = ProgressBar()
        self.layout.addWidget(self.progress)
    
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
        action = QAction("Delete Card",self.menu)
        action.triggered.connect(lambda: self.parent.deleteSelected())
        self.menu.addAction(action)

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        """ use for threadpool run """
        self.progress.setValue(0)
        self.progress._setValue(0)
        worker = Worker(self.func, *args, **kwargs)
        worker.signals.finished.connect(self.exec_done)
        self.threadpool.start(worker)
        self.timerStart()
        self.progress.setValue(30)
    
    def timerStart (self):
        self.timer.start(5000)
    
    def timerStop (self, step:int=10):
        if self.progress.value() < 100-step:
            self.progress.setValue(self.progress.value()+step)
        self.timerStart()
    
    def exec (self):
        """ use to process data_out
         this function will be called when pressing execute button """
        self.num_signal_pipeline = 0 # reset number of pipeline signal
        self.run_threadpool()

    def func(self, *args, **kwargs):
        """ main function of the node """
        pass
    
    def exec_done(self):
        
        self.timer.stop()
        self.label.setText(f"Shape: {self.data_to_view.shape}")    
        
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e: print(e)

        self.pipeline()
        self.progress.setValue(100)

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.pipeline_signal()
    
    def pipeline_signal (self):
        self.num_signal_pipeline += 1
        if self.num_signal_pipeline >= len(self.node.socket_pipeline_in.edges):
            self.exec()

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





    