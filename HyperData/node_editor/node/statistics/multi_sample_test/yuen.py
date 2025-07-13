from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox, HTransparentPushButton
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.statistics.multi_sample_test.base import TestBase, ResultDialogBase

DEBUG = False

class ResultDialog(ResultDialogBase):
    def __init__(self, title, samples, result, parent=None):
        super().__init__(title, samples, result, parent)
        
    def initStats(self, result):
        HTransparentPushButton(
            label='The t-statistic',
            label2='The difference between the arithmetic means of the two samples',
            getter=lambda: str(result.statistic[0]),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            label2='Probability of observing this result (or more extreme) if null hypothesis is true',
            getter=lambda: str(result.pvalue[0]),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='Degrees of freedom',
            label2='The number of degrees of freedom used in the calculation of the t-statistic',
            getter=lambda: str(result.df[0]),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='95% Confidence interval',
            label2='The confidence interval around the difference in population means',
            getter=lambda: f"[{result.confidence_interval().low[0]}, {result.confidence_interval().high[0]}]",
            layout=self.main_layout
        )
            
class Yuen(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alternative = "two-sided",
            equal_var = True,
            trim = 0
        )
        else: self._config = config

        self.alternative = HTransparentComboBox(
            items=["two-sided","less","greater"], 
            label="Alternative hypothesis",
            getter=lambda: self._config["alternative"],
            layout=self.vlayout
        )

        self.trim = HTransparentDoubleSpinBox(
            maximum=0.49, singleStep=0.01, label="Trim value",
            getter=lambda: self._config["trim"],
            layout=self.vlayout
        )
    
    def update_config(self):
        self._config.update(
            alternative = self.alternative.button.currentText(),
            trim = self.trim.button.value()
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()

