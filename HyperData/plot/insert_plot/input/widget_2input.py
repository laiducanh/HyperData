from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import os, pandas
from ui.base_widgets.button import _ToolButton, _DropDownToolButton
from ui.base_widgets.menu import Menu
from ui.base_widgets.text import _LineEdit, _EditableComboBox
from ui.base_widgets.icons import Icon, Action
from data_processing.data_window import DataSelection

class Widget2D_2input (QWidget):
    sig = pyqtSignal()
    def __init__(self, node):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = list()
        self.node = node
        self.axes = list()

        self.choose_axis1 = _DropDownToolButton()
        self.choose_axis1.setIcon(Icon(os.path.join("axis-bottom.png")))
        self.x_axis = Menu(self)
        self.axis_bottom = Action(Icon(os.path.join("axis-bottom.png")),'Bottom Axis', self)
        self.axis_bottom.triggered.connect(self.choose_axis_bottom)
        self.axis_top = Action(Icon(os.path.join("axis-top.png")),'Top Axis', self)
        self.axis_top.triggered.connect(self.choose_axis_top)
        self.x_axis.addAction(self.axis_bottom)
        self.x_axis.addAction(self.axis_top)
        self.choose_axis1.setMenu(self.x_axis)
        
        self.input1 = _EditableComboBox()
        self.input1.textChanged.connect(self.input1_func)
        self.choose_data_1 = _ToolButton()
        self.choose_data_1.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_1.clicked.connect(lambda: self.open_data('input 1'))
        
        self.choose_axis2 = _DropDownToolButton()
        self.choose_axis2.setIcon(Icon(os.path.join("axis-left.png")))
        self.y_axis = Menu(self)
        self.axis_left = Action(Icon(os.path.join("axis-left.png")),'Left Axis', self)
        self.axis_left.triggered.connect(self.choose_axis_left)
        self.axis_right = Action(Icon(os.path.join("axis-right.png")),'Right Axis', self)
        self.axis_right.triggered.connect(self.choose_axis_right)
        self.y_axis.addActions([self.axis_left,self.axis_right])
        self.choose_axis2.setMenu(self.y_axis)

        self.input2 = _EditableComboBox()
        self.input2.textChanged.connect(self.input2_func)
        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(Icon(os.path.join('open.png')))
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
        
        self.choose_axis1.setIcon(Icon(os.path.join("axis-bottom.png")))
        self.axes[0] = 'axis bottom'

        self.y_axis.clear()
        self.y_axis.addActions([self.axis_left,self.axis_right])


    def choose_axis_top(self):

        self.choose_axis1.setIcon(Icon(os.path.join("axis-top.png")))
        self.axes[0] = 'axis top'

        self.y_axis.clear()
        self.y_axis.addAction(self.axis_left)


    def choose_axis_left(self):
        
        self.choose_axis2.setIcon(Icon(os.path.join("axis-left.png")))
        self.axes[1] = 'axis left'

        self.x_axis.clear()
        self.x_axis.addActions([self.axis_bottom,self.axis_top])

    def choose_axis_right(self):

        self.choose_axis2.setIcon(Icon(os.path.join("axis-right.png")))
        self.axes[1] = 'axis right'

        self.x_axis.clear()
        self.x_axis.addAction(self.axis_bottom)

        
    def input1_func(self):
       
        _input1 = self.input1.text()
        _input2 = self.input2.text()

        self.input = [_input1, _input2]
                        
        if _input1 != '' and _input2 != '':
            self.sig.emit()

    def input2_func(self):
       
        _input1 = self.input1.text()
        _input2 = self.input2.text()

        self.input = [_input1, _input2]
        if _input1 != '' and _input2 != '':
            self.sig.emit()
    
    def open_data (self, which_input):

        self.dataview = DataSelection(self.node.data_out)
        self.dataview.update_data(self.node.data_out)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.show()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """

        if which_input == 'input 1':

            self.input1.setText(text)
            self.input1_done = True

        elif which_input == 'input 2':
            
            self.input2.setText(text)
            self.input2_done = True

        if self.input1.text() != '' and self.input2.text() != '':
            self.sig.emit()
        
        self.dataview.close()