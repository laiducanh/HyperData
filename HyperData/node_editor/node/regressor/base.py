from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from ui.base_widgets.button import HButton

DEBUG = False
       
class RegressorBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.estimator = None # ClassifierMixin

        self.set_config(config=None)
        
    def clear_layout(self):
        for i in reversed(range(self.vlayout.count())):
            item = self.vlayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, HButton):
                self.vlayout.removeWidget(widget)
                widget.deleteLater()
    
    def set_config(self, config=None):
        self.clear_layout()
