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
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='Critical values',
            label2='The critical values for significance levels 25%, 10%, 5%, 2.5%, 1%, 0.5%, 0.1%',
            getter=lambda: str(result.critical_values),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
            
class Anderson(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            midrank = True

        )
        else: self._config = config

        self.midrank = Toggle(
            text='Midrank',
            text2='Type of ANderson-Darling test',
            getter=lambda: self._config['midrank'],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            midrank = self.midrank.get_value()
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()