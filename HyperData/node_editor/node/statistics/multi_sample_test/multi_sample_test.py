from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import PrimaryComboBox, _TransparentPushButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QStackedLayout
import pandas as pd
from node_editor.node.statistics.multi_sample_test.base import TestBase
from node_editor.node.statistics.multi_sample_test.ttest_ind import TtestInd
from node_editor.node.statistics.multi_sample_test.welch import Welch
from node_editor.node.statistics.multi_sample_test.yuen import Yuen
from node_editor.node.statistics.multi_sample_test.mannwhitney import MannWhitney
from node_editor.node.statistics.multi_sample_test.bws import BWS
from node_editor.node.statistics.multi_sample_test.wilcoxon import RankSum
from node_editor.node.statistics.multi_sample_test.brunnermunzel import BrunnerMunzel
from node_editor.node.statistics.multi_sample_test.mood import Mood
from node_editor.node.statistics.multi_sample_test.ansari import Ansari
from node_editor.node.statistics.multi_sample_test.cramer import Cramer
from node_editor.node.statistics.multi_sample_test.es import ES
from node_editor.node.statistics.multi_sample_test.kolmogorov import Kolmogorov
from node_editor.node.statistics.multi_sample_test.f_oneway import FOneway
from node_editor.node.statistics.multi_sample_test.tukey_hsd import TukeyHSD
from node_editor.node.statistics.multi_sample_test.dunnett import Dunnett
from node_editor.node.statistics.multi_sample_test.kruskal import Kruskal
from node_editor.node.statistics.multi_sample_test.alexandergovern import AlexanderGovern
from node_editor.node.statistics.multi_sample_test.fligner import Fligner
from node_editor.node.statistics.multi_sample_test.levene import Levene
from node_editor.node.statistics.multi_sample_test.barlett import Barlett
from node_editor.node.statistics.multi_sample_test.median import MedianTest
from node_editor.node.statistics.multi_sample_test.friedman import Friedman
from scipy.stats import (ttest_ind, mannwhitneyu, bws_test, ranksums, brunnermunzel, mood, ansari,
                         cramervonmises_2samp, epps_singleton_2samp, ks_2samp, f_oneway, tukey_hsd,
                         dunnett, kruskal, alexandergovern, fligner, levene, bartlett, median_test,
                         friedmanchisquare)

DEBUG = True

class MultiSampleTest (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            test = "T-test",
            config = dict(alternative = "two-sided",equal_var = True)
        )
        self.test_list = ["T-test","Welch's T-test","Yuen's T-test","Mann-Whitney U rank test",
                          "Baumgartner-Weiss-Schindler test","Wilcoxon rank-sum","Brunner-Munzel test",
                          "Mood's test","Ansari-Bradley test","Cramer-von Mises test",
                          "Epps-Singleton test","Kolmogorov-Smirnov test","One-way ANOVA",
                          "Tukey's HSD test","Dunnett's test", "Kruskal-Wallis H-test",
                          "Alexander Govern test","Fliger-Killeen test","Levene test","Barlett's test",
                          "Mood's median test","Friedman test"]
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
        self.stackedlayout.addWidget(TtestInd())
        self.stackedlayout.addWidget(Welch())
        self.stackedlayout.addWidget(Yuen())
        self.stackedlayout.addWidget(MannWhitney())
        self.stackedlayout.addWidget(BWS())
        self.stackedlayout.addWidget(RankSum())
        self.stackedlayout.addWidget(BrunnerMunzel())
        self.stackedlayout.addWidget(Mood())
        self.stackedlayout.addWidget(Ansari())
        self.stackedlayout.addWidget(Cramer())
        self.stackedlayout.addWidget(ES())
        self.stackedlayout.addWidget(Kolmogorov())
        self.stackedlayout.addWidget(FOneway())
        self.stackedlayout.addWidget(TukeyHSD())
        self.stackedlayout.addWidget(Dunnett())
        self.stackedlayout.addWidget(Kruskal())
        self.stackedlayout.addWidget(AlexanderGovern())
        self.stackedlayout.addWidget(Fligner())
        self.stackedlayout.addWidget(Levene())
        self.stackedlayout.addWidget(Barlett())
        self.stackedlayout.addWidget(MedianTest())
        self.stackedlayout.addWidget(Friedman())

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
            self.node.input_sockets[0].socket_data = [df, df]
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data:list = self.node.input_sockets[0].socket_data
            test = self._config["test"]
            if test == "T-test":
                self.result = ttest_ind(data[0], data[1], **self._config["config"])
            elif test == "Welch's T-test":
                self.result = ttest_ind(data[0], data[1], **self._config["config"])
            elif test == "Yuen's T-test":
                self.result = ttest_ind(data[0], data[1], **self._config["config"])
            elif test == "Mann-Whitney U rank test":
                self.result = mannwhitneyu(data[0], data[1], **self._config["config"])
            elif test == "Baumgartner-Weiss-Schindler test":
                self.result = bws_test(data[0], data[1], **self._config["config"])
            elif test == "Wilcoxon rank-sum":
                self.result = ranksums(data[0], data[1], **self._config["config"])
            elif test == "Brunner-Munzel test":
                self.result = brunnermunzel(data[0], data[1], **self._config["config"])
            elif test == "Mood's test":
                self.result = mood(data[0], data[1], **self._config["config"])
            elif test == "Ansari-Bradley test":
                self.result = ansari(data[0], data[1], **self._config["config"])
            elif test == "Cramer-von Mises test":
                self.result = cramervonmises_2samp(data[0], data[1], **self._config["config"])
            elif test == "Epps-Singleton test":
                self.result = epps_singleton_2samp(data[0], data[1], **self._config["config"])
            elif test == "Kolmogorov-Smirnov test":
                self.result = ks_2samp(data[0], data[1], **self._config["config"])
            elif test == "One-way ANOVA":
                self.result = f_oneway(*data, **self._config["config"])
            elif test == "Tukey's HSD test":
                self.result = tukey_hsd(*data, **self._config["config"])
            elif test == "Dunnett's test":
                self.result = dunnett(*data, **self._config["config"])
            elif test == "Kruskal-Wallis H-test":
                self.result = kruskal(*data, **self._config["config"])
            elif test == "Alexander Govern test":
                self.result = alexandergovern(*data, **self._config["config"])
            elif test == "Fligner-Killeen test":
                self.result = fligner(*data, **self._config["config"])
            elif test == "Levene test":
                self.result = levene(*data, **self._config["config"])
            elif test == "Barlett's test":
                self.result = bartlett(*data, **self._config["config"])
            elif test == "Mood's median test":
                self.result = median_test(*data, **self._config["config"])
            elif test == "Friedman test":
                self.result = friedmanchisquare(*data, **self._config["config"])
            
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
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data.append(edge.start_socket.socket_data)