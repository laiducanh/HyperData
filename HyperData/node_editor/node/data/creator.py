from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import Toggle, TransparentComboBox
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import TransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel, BodyLabel
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
            fill_values = 0.0,
            structure = 'full',
            )
    
    def config(self):
        dialog = Dialog("Data Creator", self.parent)

        dialog.main_layout.addWidget(TitleLabel("Dimensions"))
        dialog.main_layout.addWidget(SeparateHLine())

        num_rows = TransparentSpinBox(max=1000000, text="Number of rows")
        num_rows.button.setValue(self._config["num_rows"])
        dialog.main_layout.addWidget(num_rows)

        num_cols = TransparentSpinBox(max=1000000, text="Number of columns")
        num_cols.button.setValue(self._config["num_cols"])
        dialog.main_layout.addWidget(num_cols)

        dialog.main_layout.addWidget(TitleLabel("Data structure"))
        dialog.main_layout.addWidget(SeparateHLine())

        structure = TransparentComboBox(items=["full","diagonal","triangular"],text="Structure")
        structure.button.setCurrentText(self._config["structure"])
        dialog.main_layout.addWidget(structure)

        fill_values = LineEdit(text="Fill values",text2="Values to fill to DataFrame")
        fill_values.button.setText(str(self._config["fill_values"]))
        dialog.main_layout.addWidget(fill_values)
        
        
        if dialog.exec():
            self._config.update(
                num_rows = num_rows.button.value(),
                num_cols = num_cols.button.value(),
                fill_values = fill_values.button.text(),
                structure = structure.button.currentText()
            )
            self.exec()
    
    def func(self):
        self.eval()

        try:
            fill_values = self._config["fill_values"]
            if self._config["fill_values"] != '':
                fill_values = eval(
                    self._config["fill_values"], 
                    {"numpy":np, "np": np, "math":math}
                )
                
            data = np.full(
                shape=(self._config["num_rows"], self._config["num_cols"]),
                fill_value=fill_values
            )
            if self._config["structure"] == 'triangular':
                data = np.tril(data)
            if self._config["structure"] == 'diagonal':
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
        self.resetNode()