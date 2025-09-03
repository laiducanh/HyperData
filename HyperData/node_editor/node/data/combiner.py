from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel, BodyLabel, InfoLabel
from ui.base_widgets.frame import SeparateHLine, VFrame

DEBUG = False

class DataCombiner(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            func="minimum",
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.setMinimumSize(600, 200)
        dialog.main_layout.addWidget(TitleLabel("Combine by function"))
        dialog.main_layout.addWidget(BodyLabel("Combines two DataFrames using a function"))
        dialog.main_layout.addWidget(SeparateHLine())
        fr = VFrame(dialog.main_layout)

        self.label  = BodyLabel(text="Function")
        self.label2 = InfoLabel(text="Function to merge DataFrames column by columns", wordWrap=False)
        fr.vlayout.addWidget(self.label)
        fr.vlayout.addWidget(self.label2)
        function = TransparentComboBox(
            items=["addition", "subtraction", "multiplication", "dot product",
                   "floating division", "integer division","modulo", 
                   "take smaller","take bigger","minimum","maximum","mean"],
            getter=lambda: self._config["func"],
            layout=fr.vlayout
        )

        if dialog.exec():
            self._config["func"] = function.get_value()
            self.exec()
    
    def func(self):
        if self._config["func"] == "addition":
            func = lambda s1, s2: s1 + s2
        elif self._config["func"] == "subtraction":
            func = lambda s1, s2: s1 - s2
        elif self._config["func"] == "multiplication":
            func = lambda s1, s2: s1 * s2
        elif self._config["func"] == "dot product":
            func = lambda s1, s2: s1 @ s2
        elif self._config["func"] == "floating division":
            func = lambda s1, s2: s1 / s2
        elif self._config["func"] == "integer division":
            func = lambda s1, s2: s1 // s2
        elif self._config["func"] == "floating division":
            func = lambda s1, s2: s1 % s2
        elif self._config["func"] == "take smaller":
            func = lambda s1, s2: s1 if s1.sum() < s2.sum() else s2
        elif self._config["func"] == "take bigger":
            func = lambda s1, s2: s1 if s1.sum() > s2.sum() else s2
        elif self._config["func"] == "minimum":
            func = np.minimum
        elif self._config["func"] == "maximum":
            func = np.maximum
        elif self._config["func"] == "mean":
            func = np.mean

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        data = pd.DataFrame()
        try:
            data = self.node.input_sockets[0].socket_data
            other = self.node.input_sockets[1].socket_data
            data = data.combine(other, func)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            node1 = self.node.input_sockets[0].edges[0].start_socket.node
            node2 = self.node.input_sockets[1].edges[0].start_socket.node
            logger.info(f"{self.name} {self.node.id}: combined data from {node2} {node2.id} and {node1} {node1.id} successfully.")
        
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
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data