from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import DoubleSpinBox
from ui.base_widgets.button import ComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import f

DEBUG = False

class F (DistBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loc = 0,
            scale = 1,
            dfn = 1,
            dfd = 1
        )
        else: self._config = config
    
        self.loc = DoubleSpinBox(min=-100000, max=100000, text="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = DoubleSpinBox(min=-100000, max=100000, text="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.dfn = ComboBox(items=[str(i) for i in range(10)], text="Degrees of freedom in numerator")
        self.dfn.button.setCurrentText(str(self._config["dfn"]))
        self.vlayout.addWidget(self.dfn)

        self.dfd = ComboBox(items=[str(i) for i in range(10)], text="Degrees of freedom in denominator")
        self.dfd.button.setCurrentText(str(self._config["dfd"]))
        self.vlayout.addWidget(self.dfd)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            dfn = int(self.dfn.button.currentText()),
            dfd = int(self.dfd.button.currentText())
        )
        self.dist = f(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "F continuous distribution")
        dialog.exec()