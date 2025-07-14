from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import nct

DEBUG = False

class NCT (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            df = 0,
            nc = 0,
        )
        else: self._config = config
    
        self.loc = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.df = HTransparentDoubleSpinBox(label="Degrees of freedom")
        self.df.button.setValue(self._config["df"])
        self.vlayout.addWidget(self.df)

        self.nc = HTransparentDoubleSpinBox(label="k")
        self.nc.button.setValue(self._config["nc"])
        self.vlayout.addWidget(self.nc)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            df = self.df.button.value(),
            nc = self.nc.button.value()
        )
        self.dist = nct(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Non-central Student's t continuous distribution")
        dialog.exec()