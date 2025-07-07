from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from ui.base_widgets.button import HButton

DEBUG = False

class SplitterBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._config = dict()
        self.splitter = None # Union[model_selection.BaseCrossValidator, model_selection.BaseShuffleSplit]
        self.initUI()

        self.set_config(config=None)
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
    def clear_layout (self):
        for i in reversed(range(self.vlayout.count())):
            item = self.vlayout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, HButton):
                self.vlayout.removeWidget(widget)
                widget.deleteLater()
    
    def set_config(self, config):
        self.clear_layout()