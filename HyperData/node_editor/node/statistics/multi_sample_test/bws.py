from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HTransparentPushButton
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        HTransparentPushButton(
            label='Statistic',
            getter=lambda: str(result.statistic[0]),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='Probability of observing this result (or more extreme) if null hypothesis is true',
            getter=lambda: str(result.pvalue[0]),
            layout=self.main_layout
        )
            
class BWS(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
        )
        else: self._config = config

        self.alternative = HTransparentComboBox(items=["two-sided","less","greater"], label="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)
    
    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()

