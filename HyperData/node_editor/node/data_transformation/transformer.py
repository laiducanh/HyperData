from PySide6.QtWidgets import QStackedLayout
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from node_editor.node.data_transformation.base import MethodBase
from node_editor.node.data_transformation.quantile import Quantile
from node_editor.node.data_transformation.power import Power
from sklearn import preprocessing
import pandas as pd

DEBUG = False

class DataTransformer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            method = "Quantile Transformation",
            config = dict(n_quantiles = 1000, output_distribution = "uniform",subsample = 10000)
        )
        self.method_list = ["Quantile Transformation","Power Transformation"]
    
    def config(self):
        dialog = Dialog(title="configuration", parent=self.parent)
        
        method = ComboBox(items=self.method_list, text="Transformer")
        method.button.setCurrentText(self._config["method"])
        dialog.main_layout.addWidget(method)
        dialog.main_layout.addWidget(SeparateHLine())
        method.button.currentIndexChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(s))

        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(Quantile())
        self.stackedlayout.addWidget(Power())
        
        self.stackedlayout.setCurrentIndex(self.method_list.index(method.button.currentText()))
        self.currentWidget().set_config(self._config["config"])

        if dialog.exec():
            self.currentWidget().update_config()
            self._config.update(
                method = method.button.currentText(),
                config = self.currentWidget()._config
            )
            self.exec()

    def currentWidget(self) -> MethodBase:
        return self.stackedlayout.currentWidget()
    
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            X = self.node.input_sockets[0].socket_data.copy(deep=True)
            columns = X.columns
            if self._config["method"] == "Quantile Transformation":
                X_transformed = preprocessing.quantile_transform(X, **self._config["config"])
            elif self._config["method"] == "Power Transformation":
                X_transformed = preprocessing.power_transform(X, **self._config["config"])

            data = pd.DataFrame(X_transformed, columns=columns)
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: transformed data successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
       