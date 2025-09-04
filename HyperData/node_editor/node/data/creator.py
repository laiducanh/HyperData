from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine, VFrame
from ui.base_widgets.text import TitleLabel
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
        dialog.setMinimumSize(600, 400)
        dialog.main_layout.addWidget(TitleLabel("Dimensions"))
        dialog.main_layout.addWidget(SeparateHLine())

        fr = VFrame(dialog.main_layout)
        num_rows = HTransparentSpinBox(
            maximum=1000000, 
            label="Number of rows",
            getter=lambda: self._config["num_rows"],
            layout=fr.vlayout
        )
        num_cols = HTransparentSpinBox(
            maximum=1000000, 
            label="Number of columns",
            getter=lambda: self._config["num_cols"],
            layout=fr.vlayout
        )

        dialog.main_layout.addWidget(TitleLabel("Data structure"))
        dialog.main_layout.addWidget(SeparateHLine())

        fr = VFrame(dialog.main_layout)
        structure = HTransparentComboBox(
            items=["full","diagonal","triangular"],
            label="Structure",
            getter=lambda: self._config["structure"],
            layout=fr.vlayout
        )
        fill_values = HLineEdit(
            label="Fill values",
            label2="Values to fill to DataFrame",
            getter=lambda: str(self._config["fill_values"]),
            layout=fr.vlayout
        )        
        
        if dialog.exec():
            self._config.update(
                num_rows = num_rows.get_value(),
                num_cols = num_cols.get_value(),
                fill_values = fill_values.get_value(),
                structure = structure.get_value()
            )
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
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
            logger.info(f"{self.name} {self.node.id}: create data successfully.")
        
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return an empty DataFrame.")
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy() 

    def eval(self):
        self.resetNode()