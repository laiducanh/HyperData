from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer
from sklearn.preprocessing import LabelEncoder as sk_LabelEncoder
from sklearn.preprocessing import OrdinalEncoder as sk_OrdinalEncoder
from ui.base_widgets.window import Dialog
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.text import LineEdit, EditableComboBox, Completer
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from PyQt6.QtWidgets import QFileDialog, QDialog, QWidget, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

DEBUG = True

class LabelEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def config(self):
        pass

    def exec(self):
        encoder = sk_LabelEncoder()
        self.node.data_out = encoder.fit_transform(self.node.data_in)

        super().exec()
        if DEBUG: print("LabelEncoder run successfully")
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.data_in = pd.DataFrame()
        else:
            self.node.data_in = self.node.input_sockets[0].edges[0].start_socket.node.data_out

class OrdinalEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def config(self):
        pass

    def exec(self):
        encoder = sk_OrdinalEncoder()
        self.node.data_out = encoder.fit_transform(self.node.data_in)

        super().exec()
        if DEBUG: print("LabelEncoder run successfully")
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.data_in = pd.DataFrame()
        else:
            self.node.data_in = self.node.input_sockets[0].edges[0].start_socket.node.data_out

