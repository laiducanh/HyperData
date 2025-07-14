from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import kappa4

DEBUG = False

class Kappa4 (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            h = 0,
            k = 0
        )
        else: self._config = config
    
        self.loc = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.h = HTransparentDoubleSpinBox(label="h")
        self.h.button.setValue(self._config["h"])
        self.vlayout.addWidget(self.h)

        self.k = HTransparentDoubleSpinBox(label='k')
        self.k.button.setValue(self._config["k"])
        self.vlayout.addWidget(self.k)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            h = self.h.button.value(),
            k = self.k.button.value()
        )
        self.dist = kappa4(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Kappa 4 parameter distribution")
        dialog.exec()