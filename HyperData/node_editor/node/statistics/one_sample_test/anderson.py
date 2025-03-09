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
            self.main_layout.addWidget(BodyLabel(f"Critical values: {result.critical_values}"))
            self.main_layout.addWidget(BodyLabel(f"Significant levels: {result.significane_level}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))

class Anderson (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            dist = "norm"
        )
        else: self._config = config
    
        self.dist = ComboBox(items=["norm","expon","logistic","gumbel","gumbel_l","gumbel_r",
                                    "extreme1","weibull_min"], text="Type of distribution")
        self.dist.button.setCurrentText(self._config["dist"])
        self.vlayout.addWidget(self.dist)
    
    def update_config(self):
        self._config.update(
            dist = self.dist.button.currentText()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
