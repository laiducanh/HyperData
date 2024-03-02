from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
import qfluentwidgets

class NodeContentWidget(QWidget):
    sig = pyqtSignal()
    def __init__(self, node=None):
        super().__init__()
        self.setStyleSheet('background-color:transparent')
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        font = QFont('Monospace', 10)
        self.exec_btn = qfluentwidgets.PillPushButton('Execute',parent=self)
        self.exec_btn.setFont(font)
        self.exec_btn.setCheckable(False)
        self.layout.addWidget(self.exec_btn)
        self.label = qfluentwidgets.CaptionLabel(f'Shape: (0, 0)')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setContentsMargins(5,0,5,0)
        self.layout.addWidget(self.label)
        self.setFixedHeight(46)

    
    def exec (self):
        """ use to process data_out """
        pass
    def eval (self):
        """ use to process data_in """
        pass
        
    def serialize(self):
        return dict()

    def deserialize(self, data, hashmap={}):
        pass


    
    



    