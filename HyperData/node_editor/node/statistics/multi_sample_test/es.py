from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentPushButton
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        TransparentPushButton(
            text='Statistic',
            text2='The Epps-Singleton (ES) test statistic',
            getter=lambda: str(result.statistic[0]),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='p-value',
            text2='Probability of observing this result (or more extreme) if null hypothesis is true',
            getter=lambda: str(result.pvalue[0]),
            layout=self.main_layout
        )
            
class ES(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()

