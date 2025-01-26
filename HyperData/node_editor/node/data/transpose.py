from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG

DEBUG = False

class DataTranspose (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try: 
            data = self.node.input_sockets[0].socket_data.transpose()
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else:
                connect_to_edge = self.node.input_sockets[0].edges[0]
                connect_to_node = connect_to_edge.start_socket.node
                logger.info(f"{self.name} {self.node.id}: transposed data from {connect_to_node.content.name} {connect_to_node.id} successfully.")
        except Exception as e: 
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()  
        
    def eval (self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data