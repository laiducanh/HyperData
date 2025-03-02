from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import layers
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from config.settings import logger, GLOBAL_DEBUG

DEBUG = True

class DenseLayer (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            units = 16
        )
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            pass

        try:
            input_layer = self.node.input_sockets[0].socket_data[2]
            output_layer = layers.Dense(**self._config)(input_layer)
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

        X = self.node.input_sockets[0].socket_data[0]
        Y = self.node.input_sockets[0].socket_data[1]
        self.node.output_sockets[0].socket_data = [X, Y, input_layer, output_layer]

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = [None, None, None]
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data