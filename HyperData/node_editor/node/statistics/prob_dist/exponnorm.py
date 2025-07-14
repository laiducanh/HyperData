from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import exponnorm

DEBUG = False

class Exponnorm (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            K = 0
        )
        else: self._config = config
    
        self.loc = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.K = HTransparentDoubleSpinBox(label="K")
        self.K.button.setValue(self._config["K"])
        self.vlayout.addWidget(self.K)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            K = self.K.button.value()
        )
        self.dist = exponnorm(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Exponentially modified Normal continuous distribution")
        dialog.exec()