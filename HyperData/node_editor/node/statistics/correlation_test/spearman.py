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
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Spearman (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
        )
        else: self._config = config

        self.alternative = ComboBox(items=["two-sided","less","greater"], text="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)

    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
