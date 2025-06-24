from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout
from data_processing.data_window import DataSelection
from ui.base_widgets.line_edit import _CompleterLineEdit
from ui.base_widgets.button import _TransparentToolButton
from node_editor.base.node_graphics_node import NodeGraphicsNode

class WidgetPie (QWidget):
    sig = Signal()
    def __init__(self, node:NodeGraphicsNode,input:list=[str()],parent=None):
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

        self.choose_data = _TransparentToolButton(
            icon=icon_open,
            setter=self.open_data,
            layout=layout
        )
        
    def input_func(self):

        self.input = [self.input1.currentText()]        
        self.sig.emit()
    
    def open_data (self):
        self.data_window = DataSelection(self.node.input_sockets[0].socket_data, self.parent())
        self.data_window.update_data(self.node.input_sockets[0].socket_data)
        self.data_window.exec()
        self.data_window.sig.connect(lambda s: self.assign_data(s))

    def assign_data (self, text):
        self.input1.setCurrentText(text)
        self.input = [self.input1.currentText()] 
        self.sig.emit()

class Pie(WidgetPie):
    ''' '''
class Coxcomb(WidgetPie):
    ''' '''
class Doughnut(WidgetPie):
    ''' '''
class MultilevelDoughnut(WidgetPie):
    ''' '''
class SemicircleDoughnut(WidgetPie):
    ''' '''
class Histogram(WidgetPie):
    ''' '''
class StackedHistogram(WidgetPie):
    ''' '''
class Boxplot(WidgetPie):
    ''' '''
class Violinplot(WidgetPie):
    ''' '''
class Eventplot(WidgetPie):
    ''' '''
class Treemap(WidgetPie):
    ''' '''
class Marimekko(WidgetPie):
    ''' '''
class Heatmap(WidgetPie):
    ''' '''
class Contour(WidgetPie):
    ''' '''