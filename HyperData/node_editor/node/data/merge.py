from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG

DEBUG = False

class DataMerge (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            data_left = self.node.input_sockets[0].socket_data
            data_right = self.node.input_sockets[1].socket_data
            data = data_left.merge(data_right)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else:
                node1 = self.node.input_sockets[0].edges[0].start_socket.node
                node2 = self.node.input_sockets[1].edges[0].start_socket.node
                logger.info(f"{self.name} {self.node.id}: merged data from {node1} {node1.id} and {node2} {node2.id} successfully.")
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()      
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data