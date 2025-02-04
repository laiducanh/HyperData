from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from sklearn import cluster

class Birch(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            threshold = 0.5,
            branching_factor = 50,
            n_clusters = 3,
        )
        else: self._config = config
        self.method = cluster.Birch(**self._config)

        self.threshold = DoubleSpinBox(text="Threshold")
        self.threshold.button.setValue(self._config["threshold"])
        self.threshold.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.threshold)

        self.branching_factor = SpinBox(text="Branching factor")
        self.branching_factor.button.setValue(self._config["branching_factor"])
        self.branching_factor.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.branching_factor)

        self.n_clusters = SpinBox(text="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)
        
    def set_estimator(self):
        self._config.update(
            threshold = self.threshold.button.value(),
            branching_factor = self.branching_factor.button.value(),
            n_clusters = self.n_clusters.button.value(),
        )
        self.method = cluster.Birch(**self._config)