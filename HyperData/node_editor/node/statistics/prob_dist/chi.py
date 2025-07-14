from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.button import HTransparentComboBox
from node_editor.node.statistics.prob_dist.base import DistBase, ResultDialog
from scipy.stats._continuous_distns import chi

DEBUG = False

class Chi (DistBase):
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
    
        self.loc = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Mean")
        self.loc.button.setValue(self._config["loc"])
        self.vlayout.addWidget(self.loc)

        self.scale = HTransparentDoubleSpinBox(minimum=-100000, maximum=100000, label="Standard deviation")
        self.scale.button.setValue(self._config["scale"])
        self.vlayout.addWidget(self.scale)

        self.df = HTransparentComboBox(items=[str(i) for i in range(10)], label="Degrees of freedom")
        self.df.button.setCurrentText(str(self._config["df"]))
        self.vlayout.addWidget(self.df)

    def update_config(self):
        self._config.update(
            loc = self.loc.button.value(),
            scale = self.scale.button.value(),
            df = int(self.df.button.currentText())
        )
        self.dist = chi(**self._config)
               
    def result_dialog(self):
        dialog = ResultDialog(self.dist, "Chi continuous distribution")
        dialog.exec()