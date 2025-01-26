from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.window import Dialog

DEBUG = False

class DataCombiner (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = list()
        self._config = dict(
            func="minimum",
            overwrite=True
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        function = ComboBox(items=["take smaller","minimum"],text="Function")
        dialog.main_layout.addWidget(function)
        function.button.setCurrentText(self._config["func"])
        overwrite = Toggle(text="Overwrite")
        dialog.main_layout.addWidget(overwrite)
        overwrite.button.setChecked(self._config["overwrite"])

        if dialog.exec():
            self._config["func"] = function.button.currentText()
            self._config["overwrite"] = overwrite.button.isChecked()
            self.exec()
    
    def func(self):
        if self._config["func"] == "take smaller":
            func = lambda s1, s2: s1 if s1.sum() < s2.sum() else s2
        else:
            func = np.minimum
        overwrite = self._config["overwrite"]

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data.append(df)
            self.node.input_sockets[0].socket_data.append(df)
            print('data in', self.node.input_sockets[0].socket_data)

        data = pd.DataFrame()
        try:
            for input_data in self.node.input_sockets[0].socket_data:
                data = data.combine(input_data, func=func, overwrite=overwrite)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else:
                connectedEdges = self.node.input_sockets[0].edges
                connectedNodes = [edge.start_socket.node for edge in connectedEdges]
                logger.info(f"{self.name} {self.node.id}: combined data from {connectedNodes} {[node.id for node in connectedNodes]} successfully.")
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
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data.append(edge.start_socket.socket_data)