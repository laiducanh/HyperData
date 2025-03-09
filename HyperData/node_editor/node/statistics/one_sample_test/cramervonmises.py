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
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class CramervonMises (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict()
        else: self._config = config
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
