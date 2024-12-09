from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer
from sklearn.preprocessing import LabelBinarizer as sk_LabelEncoder
from sklearn.preprocessing import OrdinalEncoder as sk_OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder as sk_OneHotEncoder

from config.settings import logger


# TODO: only encode categorical data

class LabelEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def config(self):
        pass

    def func(self):

        encoder = sk_LabelEncoder() # LabelBinarizer
        transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
        columns=self.node.input_sockets[0].socket_data.columns
        self.node.output_sockets[0].socket_data = pd.DataFrame(data=transform, 
                                                               columns=encoder.classes_)
        
        # self.node.output_sockets[0].socket_data = pd.DataFrame(columns=columns, dtype=object)
        
        # for ind, val in enumerate(transform):
        #     self.node.output_sockets[0].socket_data.loc[ind, "variety"] = str(val)
        
        # try:
        #     encoder = sk_LabelEncoder() # LabelBinarizer
        #     transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
        #     self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.copy()
        #     columns = self.node.input_sockets[0].socket_data.columns
        #     self.node.output_sockets[0].socket_data[columns].astype(object)
        #     for ind, val in enumerate(transform):
        #         self.node.output_sockets[0].socket_data.loc[ind, columns] = val
            
        #     logger.info(f"{self.name} {self.node.id}::run successfully.")
        # except Exception as e:
        #     self.node.output_sockets[0].socket_data = pd.DataFrame()
        #     logger.error(f"{self.name} {self.node.id}::{repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = pd.DataFrame(columns=columns)    
        n_classes = self.node.output_sockets[0].socket_data.shape[1]   
        n_samples = self.node.output_sockets[0].socket_data.shape[0]
        for i in range(n_samples):
            self.data_to_view.loc[i] = str()
            for j in range(n_classes):
                self.data_to_view.loc[i] += str(self.node.output_sockets[0].socket_data.iloc[i,j])
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data

class OrdinalEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def config(self):
        pass

    def func(self):
        try:
            encoder = sk_OrdinalEncoder()
            columns = self.node.input_sockets[0].socket_data.columns
            self.node.output_sockets[0].socket_data = encoder.fit_transform(self.node.input_sockets[0].socket_data)
            self.node.output_sockets[0].socket_data = pd.DataFrame(self.node.output_sockets[0].socket_data, columns=columns)
            logger.info(f"{self.name} {self.node.id}::run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {self.node.id}::{repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data

class OneHotEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def config(self):
        pass

    def func(self):
        try:
            self.node.output_sockets[0].socket_data = pd.get_dummies(self.node.input_sockets[0].socket_data)
            logger.info(f"{self.name} {self.node.id}::run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {self.node.id}::{repr(e)}, return an empty DataFrame.")

        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
