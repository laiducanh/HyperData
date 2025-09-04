from node_editor.node.data_transformation.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.frame import VFrame

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

        fr = VFrame(self.vlayout)

        self.n_quantiles = HTransparentSpinBox(
            maximum=100000, 
            singleStep=1000, 
            label="Number of quantiles",
            getter=lambda: self._config["n_quantiles"],
            layout=fr.vlayout
        )

        self.output_dist = HTransparentComboBox(
            items=["uniform","normal"],
            label="Marginal distribution",
            getter=lambda: self._config["output_distribution"],
            layout=fr.vlayout
        )

        self.subsample = HTransparentSpinBox(
            maximum=100000, 
            singleStep=1000, 
            label="Maximum of subsamples",
            getter=lambda: self._config["subsample"],
            layout=fr.vlayout
        )
        
    def update_config(self):
        self._config.update(
            n_quantiles = self.n_quantiles.button.value(),
            output_distribution = self.output_dist.button.currentText(),
            subsample = self.subsample.button.value(),
        )
