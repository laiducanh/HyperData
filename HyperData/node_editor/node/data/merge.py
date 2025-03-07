from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox
from config.settings import logger, GLOBAL_DEBUG
import pandas as pd

DEBUG = False

class DataMerge (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Left Data")
        self.node.input_sockets[1].setSocketLabel("Right Data")

        self._config = dict(
            how = "inner",
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        how = ComboBox(text="Type",items=["inner","outer","left","right","cross"])
        how.button.setCurrentText(self._config["how"])
        dialog.main_layout.addWidget(how)
        

        if dialog.exec():
            self._config["how"] = how.button.currentText()
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            self.node.input_sockets[0].socket_data = pd.DataFrame(
                {'lkey': ['foo', 'bar', 'baz', 'foo'],'value': [1, 2, 3, 5]}
            )
            self.node.input_sockets[1].socket_data = pd.DataFrame(
                {'rkey': ['foo', 'bar', 'baz', 'foo'],'value': [5, 6, 7, 8]}
            )
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            data_left = self.node.input_sockets[0].socket_data
            data_right = self.node.input_sockets[1].socket_data

            data = pd.merge(data_left, data_right, **self._config)

            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if not DEBUG and not GLOBAL_DEBUG:
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