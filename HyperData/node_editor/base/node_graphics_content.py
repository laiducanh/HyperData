from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QAction, QPaintEvent
import qfluentwidgets
from data_processing.data_window import DataView
from ui.base_widgets.menu import Menu
from ui.base_widgets.text import _TextEdit
from node_editor.base.node_graphics_node import NodeGraphicsNode


class NodeComment (_TextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFontItalic(True)
        self.setPlaceholderText("Comment")

class NodeContentWidget(QWidget):
    sig = pyqtSignal()
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__()
        self.setStyleSheet('background-color:transparent')
        self.node = node
        self.parent = parent
        self.view = DataView(self.node.data_out)
        self.menu = Menu()
        self.comment = NodeComment() 
        self.comment.hide()

        self.initUI()
        self.initMenu()

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

    def config(self):
        pass
    
    def exec (self):
        """ use to process data_out """
        self.label.setText(f'Shape: {str(self.node.data_out.shape)}')

        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e: print(e)

        self.pipeline()
        

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.exec()

    def eval (self):
        """ use to process data_in """
        pass

    def viewData (self):
        self.view.update_data(self.node.data_out)
        self.view.showMaximized()
        
    def serialize(self):
        return dict()

    def deserialize(self, data, hashmap={}):
        pass





    