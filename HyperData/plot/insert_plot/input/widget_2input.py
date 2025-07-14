from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from ui.base_widgets.button import TransparentToolButton
from ui.base_widgets.menu import Menu, Action
from ui.base_widgets.line_edit import CompleterLineEdit
from ui.base_widgets.text import BodyLabel
from data_processing.data_window import DataSelection
from node_editor.base.node_graphics_node import NodeGraphicsNode

class Widget2D_2input (QWidget):
    sig = Signal()
    def __init__(self, node:NodeGraphicsNode, input:list[str], axes:list[str], parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = ['','']
        self.axes[0] = 'axis top' if 'axis top' in axes else 'axis bottom'
        self.axes[1] = 'axis right' if 'axis right' in axes else 'axis left'

        from plot.insert_plot.utilis import (icon_axisbot, icon_axisleft, 
                                             icon_axisright, icon_axistop, icon_open)
        layout1 = QHBoxLayout()
        self.vlayout.addLayout(layout1)

        self.x_axis = Menu(parent=self)
        self.axis_bottom = Action(icon=icon_axisbot,text='Bottom Axis')
        self.axis_bottom.triggered.connect(self.choose_axis_bottom)
        self.axis_top = Action(icon=icon_axistop,text='Top Axis')
        self.axis_top.triggered.connect(self.choose_axis_top)
        self.x_axis.addActions([self.axis_bottom, self.axis_top])

        self.choose_axis1 = TransparentToolButton(
            icon=icon_axisbot if 'axis bottom' in self.axes else icon_axistop,
            layout=layout1
        )
        self.choose_axis1.setMenu(self.x_axis)
                
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
        self.vlayout.addLayout(layout2)

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

        self.dataview = DataSelection(self.node.input_sockets[0].socket_data, self.parent())
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.exec()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """

        if which_input == 'input 1':
            self.input1.setCurrentText(text)
        elif which_input == 'input 2':
            self.input2.setCurrentText(text)

        self.input_func()
        self.dataview.close()

class Line2D(Widget2D_2input):
    ''' '''
class Step2D(Widget2D_2input):
    ''' '''
class Stem2D(Widget2D_2input):
    ''' '''
class Spline2D(Widget2D_2input):
    ''' '''
class Area2D(Widget2D_2input):
    ''' '''
class StackedArea(Widget2D_2input):
    ''' '''
class StackedArea100(Widget2D_2input):
    ''' '''
class Column2D(Widget2D_2input):
    ''' '''
class Dot2D(Widget2D_2input):
    ''' '''
class ClusteredColumn2D(Widget2D_2input):
    ''' '''
class ClusteredDot(Widget2D_2input):
    ''' '''
class StackedColumn2D(Widget2D_2input):
    ''' '''
class StackedDot(Widget2D_2input):
    ''' '''
class StackedColumn2D100(Widget2D_2input):
    ''' '''
class Waterfall(Widget2D_2input):
    ''' '''
class Scatter2D(Widget2D_2input):
    ''' '''
class Hist2D(Widget2D_2input):
    ''' '''
class Pareto(QWidget):
    sig = Signal()
    def __init__(self, node:NodeGraphicsNode, input:list[str], axes:list[str], parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vlayout.setContentsMargins(0,0,0,0)

        self.input = input
        self.node = node
        self.axes = ['axis bottom','axis left']
    
        from plot.insert_plot.utilis import (icon_open)

        layout1 = QHBoxLayout()
        self.vlayout.addLayout(layout1)
        
        layout1.addWidget(BodyLabel("X"))
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
        self.vlayout.addLayout(layout2)

        layout2.addWidget(BodyLabel("Y"))        
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
        
    def input_func(self):
       
        _input1 = self.input1.currentText()
        _input2 = self.input2.currentText()

        self.input = [_input1, _input2]
                        
        if _input1 and _input2:
            self.sig.emit()

    def open_data (self, which_input):

        self.dataview = DataSelection(self.node.input_sockets[0].socket_data, self.parent())
        self.dataview.update_data(self.node.input_sockets[0].socket_data)
        self.dataview.sig.connect(lambda s: self.assign_data(which_input,s))
        self.dataview.exec()

    def assign_data (self, which_input, text):
        """ this function is called when choose data from Data Selection Window """

        if which_input == 'input 1':
            self.input1.setCurrentText(text)
        elif which_input == 'input 2':
            self.input2.setCurrentText(text)

        self.input_func()
        self.dataview.close()

class Andrews(Line2D):
    ''' '''

class CovEllipse(Line2D):
    ''' '''