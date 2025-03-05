from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import Toggle
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.window import Dialog
import pandas as pd
import numpy as np
import math

DEBUG = False

class DataCreator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            num_rows = 0,
            num_cols = 0,
            fill_values = None,
            diagonal = False,
            tri = False,
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        num_rows = SpinBox(max=1000000, text="Number of rows")
        num_rows.button.setValue(self._config["num_rows"])
        dialog.main_layout.addWidget(num_rows)

        num_cols = SpinBox(max=1000000, text="Number of columns")
        num_cols.button.setValue(self._config["num_cols"])
        dialog.main_layout.addWidget(num_cols)

        fill_values = LineEdit(text="Fill values")
        fill_values.button.setText(self._config["fill_values"])
        dialog.main_layout.addWidget(fill_values)

        diagonal = Toggle(text="Diagonal matrix")
        diagonal.button.setChecked(self._config["diagonal"])
        dialog.main_layout.addWidget(diagonal)

        tri = Toggle(text="Triangluar matrix")
        tri.button.setChecked(self._config["tri"])
        dialog.main_layout.addWidget(tri)
        
        if dialog.exec():
            self._config.update(
                num_rows = num_rows.button.value(),
                num_cols = num_cols.button.value(),
                fill_values = fill_values.button.text(),
                diagonal = diagonal.button.isChecked(),
                tri = tri.button.isChecked(),
            )
            self.exec()
    
    def func(self):
        self.eval()

        try:
            fill_values = 0.0
            if self._config["fill_values"] != '':
                fill_values = eval(
                    self._config["fill_values"], 
                    {"numpy":np, "np": np, "math":math}
                )
                
            data = np.full(
                shape=(self._config["num_rows"], self._config["num_cols"]),
                fill_value=fill_values
            )
            if self._config["tri"]:
                data = np.tril(data)
            if self._config["diagonal"]:
                diag = np.diag(data)
                data = np.zeros_like(data)
                np.fill_diagonal(data, diag)
            data = pd.DataFrame(data)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: created data successfully.")
        
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