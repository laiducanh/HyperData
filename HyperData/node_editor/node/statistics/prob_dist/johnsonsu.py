from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import johnsonsu

DEBUG = False

class JohnsonSU (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            a = 0,
            b = 0
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.a = DoubleSpinBox(text="a")
        self.a.button.setValue(self._config["a"])
        self.vlayout.addWidget(self.a)

        self.b = DoubleSpinBox(text='b')
        self.b.button.setValue(self._config["b"])
        self.vlayout.addWidget(self.b)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            a = self.a.button.value(),
            b = self.b.button.value()
        )
        self.dist = johnsonsu(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Johnson SU continuous distribution")
        dialog.exec()