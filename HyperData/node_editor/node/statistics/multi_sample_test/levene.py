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
            label='Statistic',
            getter=lambda: str(result.statistic),
            layout=self.main_layout
        )
        HTransparentPushButton(
            label='p-value',
            getter=lambda: str(result.pvalue),
            layout=self.main_layout
        )
            
class Levene(TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            center = "median",
            proportiontocut = 0.05
        )
        else: self._config = config

        self.center = HTransparentComboBox(items=["mean","median","trimmed"], label="Center")
        self.center.button.setCurrentText(self._config["center"])
        self.vlayout.addWidget(self.center)

        self.proprotiontocut = HTransparentDoubleSpinBox(singleStep=0.01, label="Proportion to cut")
        self.proprotiontocut.button.setValue(self._config["proportiontocut"])
        self.vlayout.addWidget(self.proprotiontocut)
    
    def update_config(self):
        self._config.update(
            center = self.center.button.currentText(),
            proportiontocut = self.proprotiontocut.button.value()
        )
       
    def result_dialog(self, title, samples, result):
        dialog = ResultDialog(title, samples, result)
        dialog.exec()
