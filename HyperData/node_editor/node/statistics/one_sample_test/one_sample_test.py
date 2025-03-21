from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import PrimaryComboBox, _TransparentPushButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QStackedLayout
import pandas as pd
from scipy.stats import (ttest_1samp, quantile_test, skewtest, kurtosistest, jarque_bera, shapiro,
                         anderson, cramervonmises, ks_1samp, chisquare)
from node_editor.node.statistics.one_sample_test.ttest_1samp import Ttest1samp
from node_editor.node.statistics.one_sample_test.quantile_test import QuantileTest
from node_editor.node.statistics.one_sample_test.jarque_bera import JarqueBera
from node_editor.node.statistics.one_sample_test.shapiro import Shapiro
from node_editor.node.statistics.one_sample_test.anderson import Anderson
from node_editor.node.statistics.one_sample_test.cramervonmises import CramervonMises
from node_editor.node.statistics.one_sample_test.kolmogorov import Kolmogorov
from node_editor.node.statistics.one_sample_test.chisquare import Chisquare
from node_editor.node.statistics.one_sample_test.base import TestBase

DEBUG = True

class OneSampleTest (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Samples (X)")
        self.node.input_sockets[1].setSocketLabel("Distribution")

        self._config = dict(
            test = "T-test",
            config = dict(popmean = 0,alternative = "two-sided")
        )
        self.test_list = ["T-test","Quantile test","Jarque-Bera test","Shapiro-Wilk test",
                          "Anderson-Darling test","Cramer-von Mises test","Kolmogorov-Smirnov test",
                          "Chi-square test"]
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
        self.stackedlayout.addWidget(Ttest1samp())
        self.stackedlayout.addWidget(QuantileTest())
        self.stackedlayout.addWidget(JarqueBera())
        self.stackedlayout.addWidget(Shapiro())
        self.stackedlayout.addWidget(Anderson())
        self.stackedlayout.addWidget(CramervonMises())
        self.stackedlayout.addWidget(Kolmogorov())
        self.stackedlayout.addWidget(Chisquare())

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
            data = self.node.input_sockets[0].socket_data.copy()
            dist = self.node.input_sockets[1].socket_data
            test = self._config["test"]
            if test == "T-test":
                self.result = ttest_1samp(data, **self._config["config"])
            elif test == "Binomial test":
                self.result = quantile_test(data, **self._config["config"])
            elif test == "Jarque-Bera test":
                self.result = jarque_bera(data, **self._config["config"])
            elif test == "Shapiro-Wilk test":
                self.result = shapiro(data, **self._config["config"])
            elif test == "Anderson-Darling test":
                self.result = anderson(data, **self._config["config"])
            elif test == "Cramer-von Mises test":
                self.result = cramervonmises(data, dist.cdf, **self._config["config"])
            elif test == "Kolmogorov-Smirnov test":
                self.result = ks_1samp(data, dist.cdf, **self._config["config"])
            elif test == "Chi-square test":
                self.result = chisquare(data, **self._config["config"])
            
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
        self.node.input_sockets[0].socket_data = None
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data