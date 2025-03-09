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
            self.main_layout.addWidget(BodyLabel(f"Median: {result.median}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class MedianTest (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            ties = "below"
        )
        else: self._config = config

        self.ties = ComboBox(items=["below","above","ignore"], text="Ties")
        self.ties.button.setCurrentText(self._config["ties"])
        self.vlayout.addWidget(self.ties)
    
    def update_config(self):
        self._config.update(
            ties = self.ties.button.currentText()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
