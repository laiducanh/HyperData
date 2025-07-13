from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel, BodyLabel

DEBUG = False

class DataCorrelator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._config = dict(
            type="correlation",
            method="pearson",
            min_periods=1,
            ddof=1,
            numeric_only=False
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.main_layout.addWidget(TitleLabel("Correlation and Covariance"))
        dialog.main_layout.addWidget(SeparateHLine())
        method = HTransparentComboBox(
            label="Type", 
            items=["correlation","covariance"],
            getter=lambda: self._config['type'],
            layout=dialog.main_layout
        )
        function = HTransparentComboBox(
            items=["pearson","kendall","spearman"],
            label="Method",
            label2="Method of correlation: Pearson (standard) correlation coefficient, " \
            "Kendall Tau correlation coefficient, Spearman rank correlation",
            getter=lambda: self._config['method'],
            layout=dialog.main_layout
        )
        min_periods = HTransparentSpinBox(
            minimum=1,
            label="Minimum observations",
            label2="Minimum number of observations required per pair of columns to have a valid result. " \
            "Currently only available for Pearson, Spearman correlation, and covariance analyses.",
            getter=lambda: self._config["min_periods"],
            layout=dialog.main_layout
        )
        ddof = HTransparentSpinBox(
            minimum=1,
            label="Delta degrees of freedom",
            label2="To determine the divisor used in calculations. This option is applicable only " \
            "when no missing data is in the DataFrame",
            getter=lambda: self._config["ddof"],
            layout=dialog.main_layout
        )
        overwrite = HToggle(
            label="Include only float, int or boolean data",
            getter=lambda: self._config["numeric_only"],
            layout=dialog.main_layout
        )

        if dialog.exec():
            self._config["method"] = function.get_value()
            self._config["numeric_only"] = overwrite.get_value()
            self._config["type"] = method.get_value()
            self._config["min_periods"]=min_periods.get_value()
            self._config["ddof"]=ddof.get_value()
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
                    min_periods=self._config["min_periods"],
                    numeric_only=self._config["numeric_only"],
                )   
            else:
                data = self.node.input_sockets[0].socket_data.cov(
                    min_periods=self._config["min_periods"],
                    ddof=self._config["ddof"],
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
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data.copy()