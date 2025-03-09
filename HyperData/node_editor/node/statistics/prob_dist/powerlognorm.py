from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import powerlognorm

DEBUG = False

class Powerlognorm (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            c = 0,
            s = 0
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.c = DoubleSpinBox(text="c")
        self.c.button.setValue(self._config["c"])
        self.vlayout.addWidget(self.c)

        self.s = DoubleSpinBox(text='s')
        self.s.button.setValue(self._config["s"])
        self.vlayout.addWidget(self.s)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            c = self.c.button.value(),
            s = self.s.button.value()
        )
        self.dist = powerlognorm(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Power log-normal continuous distribution")
        dialog.exec()