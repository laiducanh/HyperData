from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from data_processing.data_window import DataSelection
from ui.base_widgets.button import TransparentToolButton
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.line_edit import CompleterLineEdit
from ui.base_widgets.text import BodyLabel
from node_editor.base.node_graphics_node import NodeGraphicsNode

class Widget2D_4input (QWidget):
    sig = Signal()
    def __init__(self,node:NodeGraphicsNode,input:list[str], axes:list[str], parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = ['','']
        self.axes[0] = 'axis top' if 'axis top' in axes else 'axis bottom'
        self.axes[1] = 'axis right' if 'axis right' in axes else 'axis left'


        from plot.insert_plot.utilis import (icon_axisbot, icon_axisleft, 
                                             icon_axisright, icon_axistop, icon_open)

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        self.x_axis = Menu(parent=self)
        self.axis_bottom = Action(icon=icon_axisbot,text='Bottom Axis', parent=self)
        self.axis_bottom.triggered.connect(self.choose_axis_bottom)
        self.axis_top = Action(icon=icon_axistop,text='Top Axis', parent=self)
        self.axis_top.triggered.connect(self.choose_axis_top)
        self.x_axis.addActions([self.axis_bottom, self.axis_top])

        self.choose_axis1 = TransparentToolButton(
            icon=icon_axisbot if 'axis bottom' in self.axes else icon_axistop,
            menu=self.x_axis,
            layout=layout1
        )
                
        self.input1 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            setter=self.input_func,
            getter=lambda: self.input[0],
            layout=layout1
        )
        self.input1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_1 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 1'),
            layout=layout1
        )

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        self.y_axis = Menu(parent=self)
        self.axis_left = Action(icon=icon_axisleft,text='Left Axis', parent=self)
        self.axis_left.triggered.connect(self.choose_axis_left)
        self.axis_right = Action(icon=icon_axisright,text='Right Axis', parent=self)
        self.axis_right.triggered.connect(self.choose_axis_right)
        self.y_axis.addActions([self.axis_left,self.axis_right])
        
        self.choose_axis2 = TransparentToolButton(
            icon=icon_axisleft if 'axis left' in self.axes else icon_axisright,
            menu=self.y_axis,
            layout=layout2
        )
        
        self.input2 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            getter=lambda: self.input[1],
            setter=self.input_func,
            layout=layout2
        )
        self.input2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_2 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 2'),
            layout=layout2
        )        

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        layout3.addWidget(BodyLabel("Other"))
        self.input3 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            setter=self.input_func,
            getter=lambda: self.input[2],
            layout=layout3
        )
        self.input3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_3 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 3'),
            layout=layout3
        )

        layout4 = QHBoxLayout()
        layout.addLayout(layout4)

        self.input4 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            getter=lambda: self.input[3],
            setter=self.input_func,
            layout=layout4
        ) 
        self.input4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_4 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 4'),
            layout=layout4
        )
        
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
        _input3 = self.input3.currentText()
        _input4 = self.input4.currentText()
        self.input = [_input1, _input2,_input3, _input4]
        if _input1 and _input2:       
            self.sig.emit()

    def open_data (self, which_input):

        self.dataview = DataSelection(self.node.input_sockets[0].socket_data, self.parent())
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.exec()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """
        if which_input == "input 1": self.input1.setCurrentText(text)
        elif which_input == "input 2": self.input2.setCurrentText(text)
        elif which_input == "input 3": self.input3.setCurrentText(text)
        elif which_input == "input 4": self.input4.setCurrentText(text)

        self.input_func()
        self.dataview.close()


class Widget3D_4input (QWidget):
    sig = Signal()
    def __init__(self,node:NodeGraphicsNode, input:list[str], axes:list[str], parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = '3d'

        from plot.insert_plot.utilis import icon_open

        layout1 = QHBoxLayout()
        layout.addLayout(layout1)

        layout1.addWidget(BodyLabel('X Axis'))
                
        self.input1 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            setter=self.input_func,
            getter=lambda: self.input[0],
            layout=layout1
        )
        self.input1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_1 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 1'),
            layout=layout1
        )

        layout2 = QHBoxLayout()
        layout.addLayout(layout2)

        layout2.addWidget(BodyLabel('Y Axis'))
        
        self.input2 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            getter=lambda: self.input[1],
            setter=self.input_func,
            layout=layout2
        )
        self.input2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_2 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 2'),
            layout=layout2
        )        

        layout3 = QHBoxLayout()
        layout.addLayout(layout3)

        layout3.addWidget(BodyLabel('Z Axis'))

        layout3.addWidget(BodyLabel("Other"))
        self.input3 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            setter=self.input_func,
            getter=lambda: self.input[2],
            layout=layout3
        )
        self.input3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_3 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 3'),
            layout=layout3
        )

        layout4 = QHBoxLayout()
        layout.addLayout(layout4)

        layout4.addWidget(BodyLabel('Other'))

        self.input4 = CompleterLineEdit(
            items=node.content.data_to_view.columns.tolist(),
            getter=lambda: self.input[3],
            setter=self.input_func,
            layout=layout4
        ) 
        self.input4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.choose_data_4 = TransparentToolButton(
            icon=icon_open,
            setter=lambda: self.open_data('input 4'),
            layout=layout4
        )

    def input_func(self):
        
        _input1 = self.input1.currentText()
        _input2 = self.input2.currentText()
        _input3 = self.input3.currentText()
        _input4 = self.input4.currentText()
        self.input = [_input1, _input2,_input3, _input4]
        if _input1 and _input2 and _input3 and _input4:       
            self.sig.emit()

    def open_data (self, which_input):
        self.dataview = DataSelection(self.node.input_sockets[0].socket_data, self.parent())
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.exec()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """
        if which_input == "input 1": self.input1.setCurrentText(text)
        elif which_input == "input 2": self.input2.setCurrentText(text)
        elif which_input == "input 3": self.input3.setCurrentText(text)
        elif which_input == "input 4": self.input4.setCurrentText(text)

        self.input_func()
        self.dataview.close()

class Bubble3D(Widget3D_4input):
    ''' '''
class Errorbar (Widget2D_4input):
    ''' '''