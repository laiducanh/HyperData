from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from data_processing.data_window import DataSelection
from ui.base_widgets.line_edit import LineEdit, _CompleterLineEdit
from ui.base_widgets.button import _ToolButton
from node_editor.node_node import Node

class WidgetPie (QWidget):
    sig = pyqtSignal()
    def __init__(self, node:Node,input:list=[str()],parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = "pie"

        from plot.insert_plot.utilis import icon_open

        self.input1 = _CompleterLineEdit()
        self.input1.setCurrentText(self.input[0])
        self.input1.lineedit.returnPressed.connect(self.input_func)
        layout.addWidget(self.input1)

        self.choose_data = _ToolButton()
        self.choose_data.setIcon(icon_open)
        self.choose_data.clicked.connect(self.open_data)
        layout.addWidget(self.choose_data)

        
    def input_func(self):

        self.input = [self.input1.currentText()]        
        self.sig.emit()
    
    def open_data (self):
        self.data_window = DataSelection(self.node.input_sockets[0].socket_data)
        self.data_window.update_data(self.node.input_sockets[0].socket_data)
        self.data_window.show()
        self.data_window.sig.connect(lambda s: self.assign_data(s))

    def assign_data (self, text):
        self.input1.setCurrentText(text)
        self.input = [self.input1.currentText()] 
        self.sig.emit()