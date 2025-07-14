from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt
from ui.base_widgets.button import HButton

class MethodBase(QWidget):
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

        self.set_config(config=None)
        
    def clear_layout (self):
        # Remove all child widgets from the layout
        while self.vlayout.count():
            item = self.vlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
    
    def set_config(self, config=None):
        self.clear_layout()
    
    def update_config(self):
        pass