from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import os
from data_processing.data_window import DataSelection
from ui.base_widgets.button import _DropDownToolButton, _ToolButton
from ui.base_widgets.menu import Menu
from ui.base_widgets.text import _LineEdit, BodyLabel, _EditableComboBox
from ui.base_widgets.icons import Icon, Action
from node_editor.node_node import Node

class Widget2D_3input (QWidget):
    sig = pyqtSignal()
    sig_choose_axes = pyqtSignal()
    def __init__(self,node:Node,input:list=[str(),str(),str()],parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = ["axis bottom", "axis left"]

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
        self.input1.setText(self.input[0])
        self.input1.returnPressed.connect(self.input1_func)
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
        self.input2.setText(self.input[1])
        self.input2.returnPressed.connect(self.input2_func)
        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_2.clicked.connect(lambda: self.open_data('input 2'))
        

        self.text3 = BodyLabel("Other")
        self.input3 = _EditableComboBox()
        self.input3.setText(self.input[2])
        self.input3.returnPressed.connect(self.input3_func)
        self.choose_data_3 = _ToolButton()
        self.choose_data_3.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_3.clicked.connect(lambda: self.open_data('input 3'))

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

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)
        layout3.addWidget(self.text3)
        layout3.addWidget(self.input3)
        layout3.addWidget(self.choose_data_3)
    
    def choose_axis_bottom(self):
        
        self.choose_axis1.setIcon(Icon(os.path.join("axis-bottom.png")))
        self.axes[0] = "axis bottom"

        self.y_axis.clear()
        self.y_axis.addActions([self.axis_left,self.axis_right])
        self.sig.emit()


    def choose_axis_top(self):

        self.choose_axis1.setIcon(Icon(os.path.join("axis-top.png")))
        self.axes[0] = "axis top"

        self.y_axis.clear()
        self.y_axis.addAction(self.axis_left)
        self.sig.emit()


    def choose_axis_left(self):
        
        self.choose_axis2.setIcon(Icon(os.path.join("axis-left.png")))
        self.axes[1] = "axis left"

        self.x_axis.clear()
        self.x_axis.addActions([self.axis_bottom,self.axis_top])
        self.sig.emit()

    def choose_axis_right(self):

        self.choose_axis2.setIcon(Icon(os.path.join("axis-right.png")))
        self.axes[1] = "axis right"

        self.x_axis.clear()
        self.x_axis.addAction(self.axis_bottom)
        self.sig.emit()
        
    def input1_func(self):
        
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        self.input = [_input1, _input2,_input3]
        if _input1 != '' and _input2 != '' and _input3 != '':       
            self.sig.emit()
    
    def input2_func(self):
        
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        self.input = [_input1, _input2,_input3]
        if _input1 != '' and _input2 != '' and _input3 != '':   
            self.sig.emit()

    def input3_func(self):
        
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        self.input = [_input1, _input2,_input3]
        if _input1 != '' and _input2 != '' and _input3 != '':
            self.sig.emit()

    def open_data (self, which_input):

        self.dataview = DataSelection(self.node.input_sockets[0].socket_data)
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.show()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """

        if which_input == 'input 1':
            self.input1.setText(text)
        elif which_input == 'input 2':
            self.input2.setText(text)

        self.input = [self.input1.text(), self.input2.text()]
        
        if self.input1.text() != '' and self.input2.text() != '':
            self.sig.emit()
        
        self.dataview.close()

class Widget3D (QWidget):
    sig = pyqtSignal()
    def __init__(self,num_plot,figure):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.num_plot = num_plot
        self.figure = figure
        self.source = f'figure {self.figure}/plot/graph {self.num_plot}/general'

        self.input1 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        if settings.value(f'{self.source}/data')[0] in [[],'']:
            self.input1.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input1.setText(settings.value(f'{self.source}/data')[0])
        self.input1.editingFinished.connect(self.input1_func)

        self.choose_data_1 = _ToolButton()
        self.choose_data_1.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_1.clicked.connect(lambda: self.open_data('input 1'))

        self.input2 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        self.input2.editingFinished.connect(self.input2_func)
        if settings.value(f'{self.source}/data')[1] in [[],'']:
            self.input2.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input2.setText(settings.value(f'{self.source}/data')[1])

        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_2.clicked.connect(lambda: self.open_data('input 2'))

        self.input3 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        self.input3.editingFinished.connect(self.input3_func)
        if settings.value(f'{self.source}/data')[2] in [[],'']:
            self.input3.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input3.setText(settings.value(f'{self.source}/data')[2])

        self.choose_data_3 = _ToolButton()
        self.choose_data_3.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_3.clicked.connect(lambda: self.open_data('input 3'))

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


    def input1_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        if _input1 != '' and _input2 != '' and _input3 != '':    
            self.sig.emit()
    
    def input2_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        if _input1 != '' and _input2 != '' and _input3 != '':     
            self.sig.emit()

    def input3_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        if _input1 != '' and _input2 != '' and _input3 != '':     
            self.sig.emit()

    def open_data (self, which_input):
        self.data_window = DataSelection()
        self.data_window.show()
        self.data_window.sig.connect(lambda s: self.assign_data(which_input,s))

    def assign_data (self, which_input, text):
        if which_input == 'input 1':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [_input, None, None])
            self.input1.setText(text)
            self.input1_done = True
        elif which_input == 'input 2':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [None, _input, None])
            self.input2.setText(text)
            self.input2_done = True
        elif which_input == 'input 3':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [None, None, _input])
            self.input3.setText(text)
            self.input3_done = True
        if self.input1_done and self.input2_done and self.input3_done:
            self.sig.emit()

class WidgetHist2d (QWidget):
    sig = pyqtSignal()
    def __init__(self,num_plot,figure):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.num_plot = num_plot
        self.figure = figure
        self.source = f'figure {self.figure}/plot/graph {self.num_plot}/general'

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)
        layout1.addWidget(BodyLabel('X'))
        self.input1 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        if settings.value(f'{self.source}/data')[0] in [[],'']:
            self.input1.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input1.setText(settings.value(f'{self.source}/data')[0])
        self.input1.editingFinished.connect(self.input1_func)
        layout1.addWidget(self.input1)
        self.choose_data_1 = _ToolButton()
        self.choose_data_1.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_1.clicked.connect(lambda: self.open_data('input 1'))
        layout1.addWidget(self.choose_data_1)

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)
        layout2.addWidget(BodyLabel('Y'))
        self.input2 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        if settings.value(f'{self.source}/data')[1] in [[],'']:
            self.input2.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input2.setText(settings.value(f'{self.source}/data')[1])
        self.input2.editingFinished.connect(self.input2_func)
        layout2.addWidget(self.input2)
        self.choose_data_2 = _ToolButton()
        self.choose_data_2.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_2.clicked.connect(lambda: self.open_data('input 2'))
        layout2.addWidget(self.choose_data_2)

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)
        layout3.addWidget(QLabel('Weights'))
        self.input3 = _EditableComboBox(completer_source=f'figure {self.figure}/data/completer')
        if settings.value(f'{self.source}/data')[2] in [[],'']:
            self.input3.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input3.setText(settings.value(f'{self.source}/data')[2])
        self.input3.editingFinished.connect(self.input3_func)
        layout3.addWidget(self.input3)
        self.choose_data_3 = _ToolButton()
        self.choose_data_3.setIcon(Icon(os.path.join('open.png')))
        self.choose_data_3.clicked.connect(lambda: self.open_data('input 3'))
        layout3.addWidget(self.choose_data_3)


    def input1_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        if _input1 != '' and _input2 != '':
            self.sig.emit()
    
    def input2_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        if _input1 != '' and _input2 != '':
            self.sig.emit()

    def input3_func(self):
        #_input1 = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        #_input2 = split_input(self.input2.text(),current_plot=f"graph {self.num_plot}")
        #_input3 = split_input(self.input3.text(),current_plot=f"graph {self.num_plot}")
        _input1 = self.input1.text()
        _input2 = self.input2.text()
        _input3 = self.input3.text()
        settings.setValue(f'{self.source}/data',[_input1, _input2,_input3])
        self.sig.emit()

    def open_data (self, which_input):
        self.data_window = DataSelection()
        self.data_window.show()
        self.data_window.sig.connect(lambda s: self.assign_data(which_input,s))

    def assign_data (self, which_input, text):
        if which_input == 'input 1':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [_input, None, None])
            self.input1.setText(text)
            self.input1_done = True
        elif which_input == 'input 2':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [None, _input, None])
            self.input2.setText(text)
            self.input2_done = True
        elif which_input == 'input 3':
            #_input = split_input(text,current_plot=f"graph {self.num_plot}")
            _input = text
            settings.setValue(f'{self.source}/data', [None, None, _input])
            self.input3.setText(text)
            self.input3_done = True
        if self.input1_done and self.input2_done and self.input3_done:
            self.sig.emit()