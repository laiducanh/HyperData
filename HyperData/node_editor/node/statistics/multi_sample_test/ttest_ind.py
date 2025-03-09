from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.multi_sample_test.base import TestBase
from scipy.stats._result_classes import TtestResult

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result:TtestResult, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
            self.main_layout.addWidget(BodyLabel(f"Number of degrees of freedom: {result.df}"))
            self.main_layout.addWidget(BodyLabel(f"95% Confidence interval: {result.confidence_interval()}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class TtestInd (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            equal_var = True
        )
        else: self._config = config

        self.alternative = ComboBox(items=["two-sided","less","greater"], text="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)
    
    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText()
        )
       
    def result_dialog(self, result:TtestResult):
        dialog = ResultDialog(result)
        dialog.exec()
