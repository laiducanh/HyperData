from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer
from sklearn import preprocessing
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox
import pandas as pd

DEBUG = False

class LabelEncoder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            method = "Ordinal Encoder"
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        method = ComboBox(items=["Ordinal Encoder","Binarizer"], text="Type")
        method.button.setCurrentText(self._config["method"])
        dialog.main_layout.addWidget(method)

        if dialog.exec():
            self._config.update(method = method.button.currentText())
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = pd.DataFrame(df.iloc[:,4])
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            if self._config["method"] == "Ordinal Encoder":
                encoder = preprocessing.LabelEncoder()
                transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
                columns = self.node.input_sockets[0].socket_data.columns
                data = pd.DataFrame(data=transform, columns=columns)
            elif self._config["method"] == "Binarizer":
                encoder = preprocessing.LabelBinarizer()
                transform = encoder.fit_transform(self.node.input_sockets[0].socket_data)
                data = pd.DataFrame(data=transform, columns=encoder.classes_)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: encoded target labels successfully.")
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.warning(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval (self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame() 
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data   