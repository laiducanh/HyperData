from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox, TransparentPushButton
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        TransparentPushButton(
            text='Statistic',
            text2='The computed statistic of the test for each comparison',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='p-value',
            text2='The computed p-value of the test for each comparison',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='95% Confidence interval',
            getter=lambda: str(result.confidence_interval()),
            layout=self.vlayout
        )
            
class Dunnett(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
        )
        else: self._config = config

        self.alternative = TransparentComboBox(items=["two-sided","less","greater"], text="Alternative hypothesis")
        self.alternative.button.setCurrentText(self._config["alternative"])
        self.vlayout.addWidget(self.alternative)

    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()
