from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from sklearn import decomposition

class TruncatedSVD(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            algorithm = "randomized",
            n_iter = 5,
            n_oversamples = 10,
            power_iteration_normalizer = "auto"
        )
        else: self._config = config
        self.method = decomposition.TruncatedSVD(**self._config)

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.algorithm = ComboBox(items=["arpack","randomized"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.n_iter = SpinBox(text="Number of iterations")
        self.n_iter.button.setValue(self._config["n_iter"])
        self.n_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter)

        self.n_oversamples = SpinBox(text="Number of oversamples")
        self.n_oversamples.button.setValue(self._config["n_oversamples"])
        self.n_oversamples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_oversamples)

        self.power_iteration_normalizer = ComboBox(items=["auto","QR","LU","none"],text="Power iteration normalizer")
        self.power_iteration_normalizer.button.setCurrentText(self._config["power_iteration_normalizer"])
        self.power_iteration_normalizer.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.power_iteration_normalizer)
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            algorithm = self.algorithm.button.currentText(),
            n_iter = self.n_iter.button.value(),
            n_oversamples = self.n_oversamples.button.value(),
            power_iteration_normalizer = self.power_iteration_normalizer.button.currentText(),
        )
        self.method = decomposition.TruncatedSVD(**self._config)