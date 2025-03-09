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
            self.main_layout.addWidget(BodyLabel(f"Slope: {result.slope}"))
            self.main_layout.addWidget(BodyLabel(f"Intercept: {result.intercept}"))
            self.main_layout.addWidget(BodyLabel(f"Lower slope: {result.low_slope}"))
            self.main_layout.addWidget(BodyLabel(f"Higher slope: {result.high_slope}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Theil (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            method = "separate",
            alpha = 0.95
        )
        else: self._config = config

        self.method = ComboBox(items=["joint","separate"], text="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.vlayout.addWidget(self.method)

        self.alpha = DoubleSpinBox(max=1, step=0.05, text="Confidence")
        self.alpha.button.setValue(self._config["alpha"])
        self.vlayout.addWidget(self.alpha)

    def update_config(self):
        self._config.update(
            method = self.method.button.currentText(),
            alpha = self.alpha.button.value()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
