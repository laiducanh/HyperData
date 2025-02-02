from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from sklearn.preprocessing import normalize
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox

DEBUG = False

class DataNormalizer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            norm = "l2",
            axis = 1,
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        norm = ComboBox(text="Norm",items=["l1","l2","max"])
        norm.button.setCurrentText(self._config["norm"])
        dialog.main_layout.addWidget(norm)
        axis = ComboBox(items=["row","column"],text="Axis")
        dialog.main_layout.addWidget(axis)
        axis.button.setCurrentText("row" if self._config["axis"] else "column")

        if dialog.exec():
            self._config["norm"] = norm.button.currentText()
            self._config["axis"] = 1 if axis.button.currentText() == "row" else 2
            self.exec()
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            columns = self.node.input_sockets[0].socket_data.columns
            X = self.node.input_sockets[0].socket_data.to_numpy()
            data = pd.DataFrame(normalize(X,**self._config), columns=columns)
           
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: normalized data successfully.")
           
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
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data