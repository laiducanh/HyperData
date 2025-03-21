from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from ui.base_widgets.button import _ToolButton
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.line_edit import _LineEdit, _CompleterLineEdit
from data_processing.data_window import DataSelection
from node_editor.node_node import Node

class Widget2D_2input (QWidget):
    sig = Signal()
    def __init__(self, node:Node, input:list=[str(),str()], parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = ["axis bottom", "axis left"]

        from plot.insert_plot.utilis import (icon_axisbot, icon_axisleft, 
                                             icon_axisright, icon_axistop, icon_open)

        self.choose_axis1 = _ToolButton()
        self.choose_axis1.setIcon(icon_axisbot)
        self.x_axis = Menu(parent=self)
        self.axis_bottom = Action(icon=icon_axisbot,text='Bottom Axis', parent=self)
        self.axis_bottom.triggered.connect(self.choose_axis_bottom)
        self.axis_top = Action(icon=icon_axistop,text='Top Axis', parent=self)
        self.axis_top.triggered.connect(self.choose_axis_top)
        self.x_axis.addAction(self.axis_bottom)
        self.x_axis.addAction(self.axis_top)
        self.choose_axis1.setMenu(self.x_axis)
        
        self.input1 = _CompleterLineEdit()
        self.input1.setCurrentText(self.input[0])
        self.input1.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_1 = _ToolButton()
        self.choose_data_1.setIcon(icon_open)
        self.choose_data_1.clicked.connect(lambda: self.open_data('input 1'))
        
        self.choose_axis2 = _ToolButton()
        self.choose_axis2.setIcon(icon_axisleft)
        self.y_axis = Menu(parent=self)
        self.axis_left = Action(icon=icon_axisleft,text='Left Axis', parent=self)
        self.axis_left.triggered.connect(self.choose_axis_left)
        self.axis_right = Action(icon=icon_axisright,text='Right Axis', parent=self)
        self.axis_right.triggered.connect(self.choose_axis_right)
        self.y_axis.addActions([self.axis_left,self.axis_right])
        self.choose_axis2.setMenu(self.y_axis)

        self.input2 = _CompleterLineEdit()
        self.input2.setCurrentText(self.input[1])
        self.input2.lineedit.returnPressed.connect(self.input_func)
        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(icon_open)
        self.choose_data_2.clicked.connect(lambda: self.open_data('input 2'))

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)
        layout1.addWidget(self.choose_axis1)
        layout1.addWidget(self.input1)
        layout1.addWidget(self.choose_data_1)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        layout2.addWidget(self.choose_axis2)
        layout2.addWidget(self.input2)
        layout2.addWidget(self.choose_data_2)
        
    
    def choose_axis_bottom(self):
        
        self.choose_axis1.setIcon("axis-bottom.png")
        self.axes[0] = "axis bottom"

        self.y_axis.clear()
        self.y_axis.addActions([self.axis_left,self.axis_right])
        self.sig.emit()


    def choose_axis_top(self):

        self.choose_axis1.setIcon("axis-top.png")
        self.axes[0] = "axis top"

        self.y_axis.clear()
        self.y_axis.addAction(self.axis_left)
        self.sig.emit()


    def choose_axis_left(self):
        
        self.choose_axis2.setIcon("axis-left.png")
        self.axes[1] = "axis left"

        self.x_axis.clear()
        self.x_axis.addActions([self.axis_bottom,self.axis_top])
        self.sig.emit()

    def choose_axis_right(self):

        self.choose_axis2.setIcon("axis-right.png")
        self.axes[1] = "axis right"

        self.x_axis.clear()
        self.x_axis.addAction(self.axis_bottom)
        self.sig.emit()

        
    def input_func(self):
       
        _input1 = self.input1.currentText()
        _input2 = self.input2.currentText()

        self.input = [_input1, _input2]
                        
        if _input1 and _input2:
            self.sig.emit()

    def open_data (self, which_input):

        self.dataview = DataSelection(self.node.input_sockets[0].socket_data)
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.show()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """

        if which_input == 'input 1':
            self.input1.setCurrentText(text)
        elif which_input == 'input 2':
            self.input2.setCurrentText(text)

        self.input_func()
        self.dataview.close()