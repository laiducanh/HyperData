from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, ShuffleSplit
from ui.base_widgets.window import Dialog
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.text import LineEdit, EditableComboBox, Completer
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from config.settings import logger
from PyQt6.QtWidgets import QFileDialog, QDialog, QWidget, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

DEBUG = True

class DataSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.output_sockets[0].setTitle("Splitter")
        self.label.hide()

        self.exec()

    def config(self):
        pass

    def exec(self):
        self.node.output_sockets[0].socket_data = ShuffleSplit()

class MLModeler (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Feature (X)")
        self.node.input_sockets[1].setTitle("Label (Y)")
        self.node.input_sockets[2].setTitle("Splitter")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Visualizer")

    def config(self):
        pass

    def exec(self):
        self.eval()
        estimator = LinearRegression()
        self.node.output_sockets[0].socket_data = estimator
        try:
            if isinstance(self.node.input_sockets[0].socket_data, pd.DataFrame) and isinstance(self.node.input_sockets[1].socket_data, pd.DataFrame):
                X = self.node.input_sockets[0].socket_data
                Y = self.node.input_sockets[1].socket_data
                cv = self.node.input_sockets[2].socket_data
                score = cross_validate(estimator, X, Y, cv=cv)
                print('abc', X, Y, score)
                self.node.output_sockets[1].socket_data = None
                logger.info("MLModeler run successfully.")
            else:
                logger.warning(f"Not enough input data.")
        except Exception as e:
            logger.error(f"{repr(e)}.")
        
        

        super().exec()
        
    
    def eval (self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None

        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[2].edges:
            self.node.input_sockets[2].socket_data = edge.start_socket.socket_data