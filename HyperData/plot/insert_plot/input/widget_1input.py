from PyQt6.QtCore import pyqtSignal, Qt, QSettings, QStandardPaths, QDir
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon
import os
from DATA_PROCESSING.utlis import split_input
from DATA_PROCESSING.data_window import DataSelection
from config.settings import settings
from ui.base_widgets.text import LineEdit, _EditableComboBox
from ui.base_widgets.button import ToolButton
from ui.base_widgets.icons import Icon

class WidgetPie (QWidget):
    sig = pyqtSignal()
    def __init__(self,num_plot,figure):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.num_plot = num_plot
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)
        self.figure = figure

        self.input1 = _EditableComboBox(tooltip='1D array-like',completer_source=f'figure {self.figure}/data/completer')
        if settings.value(f'figure {self.figure}/plot/graph {self.num_plot}/general/data')[0] in [[],'']:
            self.input1.setPlaceholderText('Input data (e.g., A.1:a.4|B:b)')
        else:
            self.input1.setText(settings.value(f'figure {self.figure}/plot/graph {self.num_plot}/general/data')[0])
        self.input1.editingFinished.connect(self.input_func)
        layout.addWidget(self.input1)

        self.choose_data = ToolButton()
        self.choose_data.button.setIcon(Icon(os.path.join('open.png')))
        self.choose_data.button.clicked.connect(self.open_data)
        layout.addWidget(self.choose_data)

        

    def input_func(self):
        #_input = split_input(self.input1.text(),current_plot=f"graph {self.num_plot}")
        _input = self.input1.text()
        settings.setValue(f'figure {self.figure}/plot/graph {self.num_plot}/general/data', [_input])
        
        self.sig.emit()
    
    def open_data (self):
        self.data_window = DataSelection()
        self.data_window.show()
        self.data_window.sig.connect(lambda s: self.assign_data(s))

    def assign_data (self, text):
        #_input = split_input(text,current_plot=f"graph {self.num_plot}")
        _input = self.input1.text()
        settings.setValue(f'figure {self.figure}/plot/graph {self.num_plot}/general/data', [_input])
        self.input1.setText(text)

        self.sig.emit()