from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox, Toggle
from ui.base_widgets.spinbox import TransparentSpinBox
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
        method = TransparentComboBox(text="Type", items=["correlation","covariance"])
        method.button.setCurrentText(self._config["type"])
        dialog.main_layout.addWidget(method)
        function = TransparentComboBox(
            items=["pearson","kendall","spearman"],
            text="Method",
            text2="Method of correlation: Pearson (standard) correlation coefficient, " \
            "Kendall Tau correlation coefficient, Spearman rank correlation")
        dialog.main_layout.addWidget(function)
        function.button.setCurrentText(self._config["method"])
        min_periods = TransparentSpinBox(
            min=1,
            text="Minimum observations",
            text2="Minimum number of observations required per pair of columns to have a valid result. " \
            "Currently only available for Pearson, Spearman correlation, and covariance analyses."
        )
        min_periods.button.setValue(self._config["min_periods"])
        dialog.main_layout.addWidget(min_periods)
        ddof = TransparentSpinBox(
            min=1,
            text="Delta degrees of freedom",
            text2="To determine the divisor used in calculations. This option is applicable only " \
            "when no missing data is in the DataFrame"
        )
        ddof.button.setValue(self._config["ddof"])
        dialog.main_layout.addWidget(ddof)
        overwrite = Toggle(text="Numeric only", text2="Include only float, int or boolean data")
        dialog.main_layout.addWidget(overwrite)
        overwrite.button.setChecked(self._config["numeric_only"])

        if dialog.exec():
            self._config["method"] = function.button.currentText()
            self._config["numeric_only"] = overwrite.button.isChecked()
            self._config["type"] = method.button.currentText()
            self._config["min_periods"]=min_periods.button.value()
            self._config["ddof"]=ddof.button.value()
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
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data.copy()