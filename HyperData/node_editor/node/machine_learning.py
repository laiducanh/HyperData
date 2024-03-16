from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.linear_model import *
from sklearn.model_selection import *
from sklearn.metrics import *
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

class TrainTestSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Feature (X)")
        self.node.input_sockets[1].setTitle("Label (Y)")
        self.node.output_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[1].setTitle("Data")
        self.data_to_view = pd.DataFrame()
        self.exec()


    def config(self):
        pass

    def exec(self):
        self.eval()
        splitter = ShuffleSplit()
        result = list()

        try:
            if isinstance(self.node.input_sockets[0].socket_data, pd.DataFrame) and isinstance(self.node.input_sockets[1].socket_data, pd.DataFrame):
                X = self.node.input_sockets[0].socket_data
                Y = self.node.input_sockets[1].socket_data
                self.data_to_view = pd.concat([X,Y],axis=1)

                for fold, (train_idx, test_idx) in enumerate(splitter.split(X, Y)):

                    self.data_to_view.loc[train_idx.tolist(),f"Fold{fold+1}"] = "Train"
                    self.data_to_view.loc[test_idx.tolist(),f"Fold{fold+1}"] = "Test"     
                    result.append((train_idx, test_idx))                       

                logger.info("TrainTestSplitter run successfully.")
            else:
                X, Y = pd.DataFrame(), pd.DataFrame()
                self.data_to_view = pd.DataFrame()
                logger.warning(f"Not enough input data, return an empty DataFrame.")

        except Exception as e:
            X, Y = pd.DataFrame(), pd.DataFrame()
            self.data_to_view = pd.DataFrame()
            logger.error(f"{repr(e)}, return an empty DataFrame.")

        super().exec()
       
        self.node.output_sockets[0].socket_data = [result, X, Y]
        self.node.output_sockets[1].socket_data = self.data_to_view
     
    def eval(self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data

class Modeler (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Visualizer")

    def config(self):
        pass

    def exec(self):
        self.eval()
        estimator = LinearRegression()
        self.node.output_sockets[0].socket_data = estimator

        
            
        try:
            if len(self.node.input_sockets[0].edges) == 1:
                if isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                    cv = self.node.input_sockets[0].socket_data[0]
                    X = self.node.input_sockets[0].socket_data[1]
                    Y = self.node.input_sockets[0].socket_data[2]
                        
                    self.data_to_view = pd.concat([X,Y],axis=1)

                    for fold, (train_idx, test_idx) in enumerate(cv):
                        X_train, X_test = X.loc[train_idx], X.loc[test_idx]
                        Y_train, Y_test = Y.loc[train_idx], Y.loc[test_idx]
                        estimator.fit(X_train, Y_train)
                        Y_pred = estimator.predict(X).round(5)
                        score = mean_absolute_error(Y, Y_pred)
                    
                        self.data_to_view = pd.concat([self.data_to_view, pd.DataFrame(Y_pred, columns=[f"Fold{fold+1}_Prediction"])],axis=1)
                    
                    self.node.output_sockets[1].socket_data = None
                    logger.info("MLModeler run successfully.")

            else:
                logger.warning(f"Did not define splitter.")
        
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
        