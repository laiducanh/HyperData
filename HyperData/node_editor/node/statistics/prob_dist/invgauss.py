from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import invgauss

DEBUG = False

class Invgauss (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            mu = 0
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.mu = DoubleSpinBox(text="mu")
        self.mu.button.setValue(self._config["mu"])
        self.vlayout.addWidget(self.mu)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            mu = self.mu.button.value()
        )
        self.dist = invgauss(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Inverse Gaussian continuous distribution")
        dialog.exec()