from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import ncf

DEBUG = False

class NCF (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            df1 = 0,
            df2 = 0,
            nc = 0,
        )
        else: self._config = config
    
        self.loc = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.df1 = HTransparentDoubleSpinBox(label="Degrees of freedom in numerator")
        self.df1.button.setValue(self._config["df1"])
        self.vlayout.addWidget(self.df1)

        self.df2 = HTransparentDoubleSpinBox(label="Degrees of freedom in denominator")
        self.df2.button.setValue(self._config["df2"])
        self.vlayout.addWidget(self.df2)

        self.nc = HTransparentDoubleSpinBox(label="Lambda")
        self.nc.button.setValue(self._config["nc"])
        self.vlayout.addWidget(self.nc)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            df1 = self.df1.button.value(),
            df2 = self.df2.button.value(),
            nc = self.nc.button.value()
        )
        self.dist = ncf(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Non-central F continuous distribution")
        dialog.exec()