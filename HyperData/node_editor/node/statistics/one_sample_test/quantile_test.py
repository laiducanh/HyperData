from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.one_sample_test.base import TestBase

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
            self.main_layout.addWidget(BodyLabel(f"Statistic type: {result.statistic_type}"))
            self.main_layout.addWidget(BodyLabel(f"95% Confidence interval: {result.confidence_interval()}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))

class QuantileTest (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            q = 0.0,
            p = 0.5,
            alternative = "two-sided"
        )
        else: self._config = config
    
        self.q = DoubleSpinBox(text="Hypothesized value")
        self.q.button.setValue(self._config["q"])
        self.vlayout.addWidget(self.q)

        self.p = DoubleSpinBox(max=1, step=0.1, text="Probability of quantile")
        self.p.button.setValue(self._config["p"])
        self.vlayout.addWidget(self.p)

        self.alternative = ComboBox(items=["two-sided","less","greater"], text="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)
    
    def update_config(self):
        self._config.update(
            q = self.q.button.value(),
            p = self.p.button.value(),
            alternative = self.alternative.button.currentText()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
