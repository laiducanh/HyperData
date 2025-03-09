from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.text import BodyLabel
from node_editor.node.statistics.multi_sample_test.base import TestBase

DEBUG = False

class ResultDialog(Dialog):
    def __init__(self, result, parent=None):
        super().__init__(parent)
        if result:
            self.main_layout.addWidget(BodyLabel(f"Statistic: {result.statistic}"))
            self.main_layout.addWidget(BodyLabel(f"p-value: {result.pvalue}"))
        else:
            self.main_layout.addWidget(BodyLabel("Failed to run hypothesis test."))
            
class Fligner (TestBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            center = "median",
            proportiontocut = 0.05
        )
        else: self._config = config

        self.center = ComboBox(items=["mean","median","trimmed"], text="Center")
        self.center.button.setCurrentText(self._config["center"])
        self.vlayout.addWidget(self.center)

        self.proprotiontocut = DoubleSpinBox(step=0.01, text="Proportion to cut")
        self.proprotiontocut.button.setValue(self._config["proportiontocut"])
        self.vlayout.addWidget(self.proprotiontocut)
    
    def update_config(self):
        self._config.update(
            center = self.center.button.currentText(),
            proportiontocut = self.proprotiontocut.button.value()
        )
       
    def result_dialog(self, result):
        dialog = ResultDialog(result)
        dialog.exec()
