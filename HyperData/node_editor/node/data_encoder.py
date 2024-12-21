from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer
from sklearn.preprocessing import LabelBinarizer as sk_LabelBinarizer
from sklearn.preprocessing import LabelEncoder as sk_LabelEncoder
from sklearn.preprocessing import OrdinalEncoder as sk_OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder as sk_OneHotEncoder

from config.settings import logger


# TODO: only encode categorical data
class LabelBinarizer(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)

    def func(self):
        try:
            encoder = sk_LabelBinarizer()
            transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
            self.node.output_sockets[0].socket_data = pd.DataFrame(data=transform, 
                                                                columns=encoder.classes_)
            # write log
            logger.info(f"{self.name} {self.node.id}: binarized target labels successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.warning(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.data_to_view = self.node.output_sockets[0].socket_data 
    
    def eval (self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()   
        
class LabelEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def func(self):
        try:
            encoder = sk_LabelEncoder()
            transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
            columns=self.node.input_sockets[0].socket_data.columns
            self.node.output_sockets[0].socket_data = pd.DataFrame(data=transform, 
                                                                columns=columns)
            # write log
            logger.info(f"{self.name} {self.node.id}: encoded target labels successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.warning(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.data_to_view = self.node.output_sockets[0].socket_data 
    
    def eval (self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()            

class OrdinalEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def func(self):
        try:
            encoder = sk_OrdinalEncoder()
            columns = self.node.input_sockets[0].socket_data.columns
            self.node.output_sockets[0].socket_data = encoder.fit_transform(self.node.input_sockets[0].socket_data)
            self.node.output_sockets[0].socket_data = pd.DataFrame(self.node.output_sockets[0].socket_data, columns=columns)
            # write log
            logger.info(f"{self.name} {self.node.id}: encoded categorical features successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval (self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()            

class OneHotEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def func(self):
        try:
            self.node.output_sockets[0].socket_data = pd.get_dummies(self.node.input_sockets[0].socket_data)
            # write log
            logger.info(f"{self.name} {self.node.id}: one-hot encoded categorical features successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)

        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval (self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
            
