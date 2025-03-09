from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import chi2

DEBUG = False

class Chi2 (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            df = 1
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.df = ComboBox(items=[str(i) for i in range(10)], text="Degrees of freedom")
        self.df.button.setCurrentText(str(self._config["df"]))
        self.vlayout.addWidget(self.df)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            df = int(self.df.button.currentText())
        )
        self.dist = chi2(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Chi-squared continuous distribution")
        dialog.exec()