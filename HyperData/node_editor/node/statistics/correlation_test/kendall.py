from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.multi_sample_test.base import TestBase

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Kendall (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            method = "auto",
            variant = "b"
        )
        else: self._config = config

        self.alternative = HTransparentComboBox(items=["two-sided","less","greater"], label="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)

        self.method = HTransparentComboBox(items=["auto","asymptotic","exact"], label="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.vlayout.addWidget(self.method)

        self.variant = HTransparentComboBox(items=["b","c"], label="Variant")
        self.variant.button.setCurrentText(self._config["variant"])
        self.vlayout.addWidget(self.variant)

    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
            method = self.method.button.currentText(),
            variant = self.variant.button.currentText()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
