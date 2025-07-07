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
            text2='The KS test statistic',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='p-value',
            text2='Probability of observing that large a difference if null is true',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Statistic location',
            text2='The distance between the empirical distribution functions is measured at this observation',
            getter=lambda: str(result.statistic_location),
            layout=self.main_layout
        )
        TransparentPushButton(
            text='Statistic sign',
            getter=lambda: 'positive' if result.statistic_sign == 1 else 'negative',
            layout=self.main_layout
        )
            
class Kolmogorov(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            distribution = "t"
        )
        else: self._config = config

        self.alternative = TransparentComboBox(
            items=["two-sided","less","greater"], 
            text="Alternative hypothesis",
            text2='Define the null and alternative hypotheses',
            getter=lambda: self._config["alternative"],
            layout=self.vlayout
        )

        self.distribution = TransparentComboBox(
            items=["t","normal"], 
            text="Distribution",
            text2='The method used for calculating the p-value',
            getter=lambda: self._config["distribution"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
            distribution = self.distribution.button.currentText()
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()

