from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn.experimental import enable_iterative_imputer # is required to load sklear.impute
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.line_edit import CompleterLineEdit
from config.settings import logger, GLOBAL_DEBUG

DEBUG = False

class NAEliminator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            axis='index',
            thresh='any',
            ignore_index=False
        )

    def config(self):
        dialog = Dialog("Configuration", self.parent)

        axis = ComboBox(items=["index","columns"], text="drop")
        axis.button.setCurrentText(self._config["axis"])
        dialog.main_layout.addWidget(axis)

        thresh = CompleterLineEdit(text='thresh', items=["any","all"])
        thresh.button.setCurrentText(self._config['thresh'])
        dialog.main_layout.addWidget(thresh)

        ignore_index = Toggle(text='ignore index')
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.main_layout.addWidget(ignore_index)

        if dialog.exec():
            self._config["axis"] = axis.button.currentText()
            self._config["thresh"] = thresh.button.currentText()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            # randomly introduce some missing values
            df = df.mask(np.random.random(df.shape) < 0.2)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            if self._config["thresh"].isdigit():
                data: pd.DataFrame = self.node.input_sockets[0].socket_data.dropna(
                    axis=self._config["axis"],
                    thresh=int(self._config["thresh"]),
                    ignore_index=self._config["ignore_index"]
                )
            
            elif self._config["thresh"] in ["any","all"]:
                data = self.node.input_sockets[0].socket_data.dropna(
                    axis=self._config["axis"],
                    how=self._config["thresh"],
                    ignore_index=self._config["ignore_index"]
                )
            else:
                data = self.node.input_sockets[0].socket_data.dropna(
                    axis=self._config["axis"],
                    how="any",
                    ignore_index=self._config["ignore_index"]
                )
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: eliminated NaNs successfully.")
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