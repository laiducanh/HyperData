from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import crystalball

DEBUG = False

class Crystalball (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            beta = 1,
            m = 1
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.beta = DoubleSpinBox(text="Beta")
        self.beta.button.setValue(self._config["beta"])
        self.vlayout.addWidget(self.beta)

        self.m = DoubleSpinBox(text="m")
        self.m.button.setValue(self._config["m"])
        self.vlayout.addWidget(self.m)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            beta = self.beta.button.value(),
            m = self.m.button.value()
        )
        self.dist = crystalball(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Crystalball continuous distribution")
        dialog.exec()