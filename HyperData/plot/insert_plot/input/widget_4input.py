from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from data_processing.data_window import DataSelection
from ui.base_widgets.button import _ToolButton, _DropDownPushButton
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.line_edit import _LineEdit, BodyLabel, _CompleterLineEdit
from node_editor.node_node import Node

class Widget3D_4input (QWidget):
    sig = Signal()
    def __init__(self,node:Node,input:list=[str(),str(),str(),str()],parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = "3d"

        from plot.insert_plot.utilis import icon_open

        self.input1 = _CompleterLineEdit()
        self.input1.setCurrentText(self.input[0])
        self.input1.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_1 = _ToolButton()
        self.choose_data_1.setIcon(icon_open)
        self.choose_data_1.clicked.connect(lambda: self.open_data('input 1'))

        self.input2 = _CompleterLineEdit()
        self.input2.setCurrentText(self.input[1])
        self.input2.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(icon_open)
        self.choose_data_2.clicked.connect(lambda: self.open_data('input 2'))

        self.input3 = _CompleterLineEdit()
        self.input3.setCurrentText(self.input[2])
        self.input3.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_3 = _ToolButton()
        self.choose_data_3.setIcon(icon_open)
        self.choose_data_3.clicked.connect(lambda: self.open_data('input 3'))

        self.input4 = _CompleterLineEdit()
        self.input4.setCurrentText(self.input[3])
        self.input4.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_4 = _ToolButton()
        self.choose_data_4.setIcon(icon_open)
        self.choose_data_4.clicked.connect(lambda: self.open_data('input 4'))

        

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)
        layout1.addWidget(QLabel('X Axis'))
        layout1.addWidget(self.input1)
        layout1.addWidget(self.choose_data_1)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        layout2.addWidget(QLabel('Y Axis'))
        layout2.addWidget(self.input2)
        layout2.addWidget(self.choose_data_2)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)
        layout3.addWidget(QLabel('Z Axis'))
        layout3.addWidget(self.input3)
        layout3.addWidget(self.choose_data_3)

        layout4 = QHBoxLayout()
        layout.addLayout(layout4)
        layout4.addWidget(QLabel('Other'))
        layout4.addWidget(self.input4)
        layout4.addWidget(self.choose_data_4)


    def input_func(self):
        
        _input1 = self.input1.currentText()
        _input2 = self.input2.currentText()
        _input3 = self.input3.currentText()
        _input4 = self.input4.currentText()
        self.input = [_input1, _input2,_input3, _input4]
        if _input1 and _input2 and _input3 and _input4:       
            self.sig.emit()

    def open_data (self, which_input):
        self.dataview = DataSelection(self.node.input_sockets[0].socket_data)
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.show()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """
        if which_input == "input 1": self.input1.setCurrentText(text)
        elif which_input == "input 2": self.input2.setCurrentText(text)
        elif which_input == "input 3": self.input3.setCurrentText(text)
        elif which_input == "input 4": self.input4.setCurrentText(text)

        self.input_func()
        self.dataview.close()