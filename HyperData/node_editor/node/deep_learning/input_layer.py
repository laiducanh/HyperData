from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import Input
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from config.settings import logger, GLOBAL_DEBUG

DEBUG = True

class InputLayer (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("X")
        self.node.input_sockets[1].setSocketLabel("Y")

        self._config = dict(
            shape = (32,)
        )
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            pass

        try:
            layer = Input(**self._config)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)

        X = self.node.input_sockets[0].socket_data
        Y = self.node.input_sockets[1].socket_data
        self.node.output_sockets[0].socket_data = [X, Y, layer]

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        self.node.input_sockets[1].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data