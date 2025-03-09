from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import PrimaryComboBox, _TransparentPushButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QStackedLayout
import pandas as pd
from node_editor.node.statistics.correlation_test.base import TestBase
from node_editor.node.statistics.correlation_test.pearson import Pearson
from node_editor.node.statistics.correlation_test.spearman import Spearman
from node_editor.node.statistics.correlation_test.pointbiserial import Pointbiserial
from node_editor.node.statistics.correlation_test.kendall import Kendall
from node_editor.node.statistics.correlation_test.somersd import SomersD
from node_editor.node.statistics.correlation_test.siegelslopes import Siegel
from node_editor.node.statistics.correlation_test.theil import Theil
from node_editor.node.statistics.correlation_test.mgc import MGC
from scipy.stats import (pearsonr, spearmanr, pointbiserialr, kendalltau, somersd, siegelslopes,
                         theilslopes, multiscale_graphcorr)

DEBUG = True

class CorrelationTest (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("X")
        self.node.input_sockets[1].setSocketLabel("Y")

        self._config = dict(
            test = "Pearson correlation coefficient",
            config = dict(popmean = 0,alternative = "two-sided")
        )
        self.test_list = ["Pearson correlation coefficient","Spearman correlation coefficient",
                          "Point biserial correlation coefficient","Kendall's tau","Somers' D",
                          "Siegel's slope","Theil-Sen's slope","Multiscale graph correlation"]
        self.result = None

        self.label.hide()

        self.result_btn = _TransparentPushButton()
        self.result_btn.setText("Result")
        self.result_btn.released.connect(self.result_dialog)
        self.vlayout.insertWidget(2,self.result_btn)

        self.initDialog()
    
    def initDialog(self):
        self.dialog = Dialog(title="Configuration", parent=self.parent)

        self.test = PrimaryComboBox(items=self.test_list, text="Test")
        self.test.button.setCurrentText(self._config["test"])
        self.test.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.test_list.index(s)))
        self.dialog.main_layout.addWidget(self.test)

        self.dialog.main_layout.addWidget(SeparateHLine())
        self.stackedlayout = QStackedLayout()
        self.dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(Pearson())
        self.stackedlayout.addWidget(Spearman())
        self.stackedlayout.addWidget(Pointbiserial())
        self.stackedlayout.addWidget(Kendall())
        self.stackedlayout.addWidget(SomersD())
        self.stackedlayout.addWidget(Siegel())
        self.stackedlayout.addWidget(Theil())
        self.stackedlayout.addWidget(MGC())
        
        self.stackedlayout.setCurrentIndex(self.test_list.index(self.test.button.currentText()))
        self.currentWidget().set_config(self._config["config"])
    
    def currentWidget(self) -> TestBase:
        return self.stackedlayout.currentWidget()
    
    def config(self):
        if self.dialog.exec():
            self.currentWidget().update_config()
            self._config.update(
                test = self.test.button.currentText(),
                config = self.currentWidget()._config
            )
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from scipy.stats import norm
            df = pd.DataFrame({
                    "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                    "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]})
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = norm()
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            X = self.node.input_sockets[0].socket_data.copy()
            Y = self.node.input_sockets[1].socket_data.copy()
            test = self._config["test"]
            if test == "Pearson correlation coefficient":
                self.result = pearsonr(X, Y, **self._config["config"])
            elif test == "Spearman correlation coefficient":
                self.result = spearmanr(X, Y, **self._config["config"])
            elif test == "Point biserial correlation coefficient":
                self.result = pointbiserialr(X, Y, **self._config["config"])
            elif test == "Kendall's tau":
                self.result = kendalltau(X, Y, **self._config["config"])
            elif test == "Somers' D":
                self.result = somersd(X, Y, **self._config["config"])
            elif test == "Siegel's slope":
                self.result = siegelslopes(X, Y, **self._config["config"])
            elif test == "Theil-Sen's slope":
                self.result = theilslopes(X, Y, **self._config["config"])
            elif test == "Multiscale graph correlation":
                self.result = multiscale_graphcorr(X, Y, **self._config["config"])
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {test} run successfully.")

        except Exception as e:
            self.result = None
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)
    
    def result_dialog(self):
        self.currentWidget().result_dialog(self.result)
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data