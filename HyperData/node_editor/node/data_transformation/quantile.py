from node_editor.node.data_transformation.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import SpinBox

class Quantile(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_quantiles = 1000,
            output_distribution = "uniform",
            subsample = 10000,
        )
        else: self._config = config

        self.n_quantiles = SpinBox(max=100000, step=1000, text="Number of quantiles")
        self.n_quantiles.button.setValue(self._config["n_quantiles"])
        self.vlayout.addWidget(self.n_quantiles)

        self.output_dist = ComboBox(items=["uniform","normal"],text="Marginal distribution")
        self.output_dist.button.setCurrentText(self._config["output_distribution"])
        self.vlayout.addWidget(self.output_dist)

        self.subsample = SpinBox(max=100000, step=1000, text="Maximum of subsamples")
        self.subsample.button.setValue(self._config["subsample"])
        self.vlayout.addWidget(self.subsample)
        
    def update_config(self):
        self._config.update(
            n_quantiles = self.n_quantiles.button.value(),
            output_distribution = self.output_dist.button.currentText(),
            subsample = self.subsample.button.value(),
        )
