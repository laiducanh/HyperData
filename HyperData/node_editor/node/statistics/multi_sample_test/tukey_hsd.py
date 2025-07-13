from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentPushButton
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        HTransparentPushButton(
            label='Statistic',
            label2='The computed statistic of the test for each comparison',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='The computed p-value of the test for each comparison',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='95% Confidence interval',
            getter=lambda: str(result.confidence_interval()),
            layout=self.vlayout
        )
            
class TukeyHSD(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()
