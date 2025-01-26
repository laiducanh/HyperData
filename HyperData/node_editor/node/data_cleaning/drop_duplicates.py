from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from config.settings import logger, GLOBAL_DEBUG

DEBUG = False

class DropDuplicate (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            keep='first',
            ignore_index=False
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        keep = ComboBox(items=["first","last","none"], text='keep')
        keep.button.setCurrentText(self._config["keep"])
        dialog.main_layout.addWidget(keep)

        ignore_index = Toggle(text='ignore index')
        ignore_index.button.setChecked(self._config["ignore_index"])
        dialog.main_layout.addWidget(ignore_index)

        if dialog.exec():
            self._config["keep"] = keep.button.currentText()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()
    
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            # Randomly select rows to duplicate
            duplicate_indices = np.random.choice(df.index, 10, replace=False)
            # Append the duplicated rows to the original dataframe
            df = pd.concat([df, df.loc[duplicate_indices]])
            # randomly introduce some duplicates
            # shuffle the dataframe to randomize the order of duplicates
            df = df.sample(frac=1).reset_index(drop=True)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        if self._config["keep"] == 'none': keep = False
        else: keep = self._config["keep"]

        try:
            data = self.node.input_sockets[0].socket_data.drop_duplicates(
                keep=keep,
                ignore_index=self._config["ignore_index"]
            )
            # change progressbar's color
            self.progress.changeColor('success')       
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: dropped duplicated values successfully.")
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
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
    