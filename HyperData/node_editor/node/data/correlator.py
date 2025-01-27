from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.window import Dialog

DEBUG = False

class DataCorrelator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._config = dict(
            type="correlation",
            method="pearson",
            numeric_only=True
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        method = ComboBox(text="Type",items=["correlation","covariance"])
        method.button.setCurrentText(self._config["type"])
        dialog.main_layout.addWidget(method)
        function = ComboBox(items=["pearson","kendall","spearman"],text="Method")
        dialog.main_layout.addWidget(function)
        function.button.setCurrentText(self._config["method"])
        overwrite = Toggle(text="Numeric only")
        dialog.main_layout.addWidget(overwrite)
        overwrite.button.setChecked(self._config["numeric_only"])

        if dialog.exec():
            self._config["method"] = function.button.currentText()
            self._config["numeric_only"] = overwrite.button.isChecked()
            self._config["type"] = method.button.currentText()
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df.copy()
            print('data in', self.node.input_sockets[0].socket_data)

        data = pd.DataFrame()
        try:
            if self._config["type"] == "correlation":
                data = self.node.input_sockets[0].socket_data.corr(
                    method=self._config["method"],
                    numeric_only=self._config["numeric_only"],
                )   
            else:
                data = self.node.input_sockets[0].socket_data.cov(
                    numeric_only=self._config["numeric_only"]
                )
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")

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
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data.copy()