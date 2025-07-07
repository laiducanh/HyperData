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
        TransparentPushButton(
            text='Median',
            text2='The grand median',
            getter=lambda: str(result.median),
            layout=self.main_layout
        )
            
class MedianTest(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            ties = "below",
            correction = True,
            lambda_ = "pearson"

        )
        else: self._config = config

        self.ties = TransparentComboBox(
            items=["below","above","ignore"], 
            text="Ties",
            text2='Determines how values equal to the grand median are classified in the contingency table',
            getter=lambda: self._config["ties"],
            layout=self.vlayout
        )

        self.correction = Toggle(
            text='Correction',
            text2="Apply Yate's correction for continuity",
            getter=lambda: self._config["correction"],
            layout=self.vlayout
        )

        self.lambda_ = TransparentComboBox(
            items=['pearson','log-likelihood','freeman-tukey','mod-log-likelihood','neyman','cressie-read'],
            text='Power divergence',
            text2='The power in the power divergence statistic',
            getter=lambda: self._config["lambda_"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            ties = self.ties.button.get_value(),
            correction = self.correction.get_value(),
            lambda_ = self.lambda_.get_value()
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()
