from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox, TransparentPushButton, Toggle
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        TransparentPushButton(
            text='Statistic',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='p-value',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
            
class Friedman(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()