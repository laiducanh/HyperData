from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

DEBUG = False
       
class RegressorBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._config = dict()
        self.estimator = None
        self.initUI()
        self.setConfig()
        self.setEstimator()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.scroll_area = QScrollArea(self.parent())
        layout.addWidget(self.scroll_area)

        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
    
    def clearLayout(self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def setConfig(self):
        pass

    def setEstimator(self):
        pass