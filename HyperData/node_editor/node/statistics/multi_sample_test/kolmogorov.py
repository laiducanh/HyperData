from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.multi_sample_test.base import TestBase

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
            self.main_layout.addWidget(BodyLabel(f"Statistic location: {result.statistic_location}"))
            self.main_layout.addWidget(BodyLabel(f"Statistic sign: {result.statistic_sign}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Kolmogorov (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            distribution = "t"
        )
        else: self._config = config

        self.alternative = ComboBox(items=["two-sided","less","greater"], text="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)

        self.distribution = ComboBox(items=["t","normal"], text="Distribution")
        self.distribution.button.setCurrentText(self._config["distribution"])
        self.vlayout.addWidget(self.distribution)
    
    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
            distribution = self.distribution.button.currentText()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
