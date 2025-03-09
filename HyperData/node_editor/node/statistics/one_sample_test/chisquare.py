from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.one_sample_test.base import TestBase

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Chisquare (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            ddof = 0
        )
        else: self._config = config

        self.ddof = SpinBox(text="Delta degrees of freedom")
        self.ddof.button.setValue(self._config["ddof"])
        self.vlayout.addWidget(self.ddof)
    
    def update_config(self):
        self._config.update(
            ddof = self.ddof.button.value()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()