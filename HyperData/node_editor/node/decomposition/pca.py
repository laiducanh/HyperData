from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from sklearn import decomposition

class PCA(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            whiten = False,
            svd_solver = "auto",
            iterated_power = 1000,
            n_oversamples = 10,
            power_iteration_normalizer = "auto",
        )
        else: self._config = config
        self.method = decomposition.PCA(**self._config)

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.whiten = Toggle(text="Whitening")
        self.whiten.button.setChecked(self._config["whiten"])
        self.whiten.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.whiten)

        self.svd_solver = ComboBox(items=["auto","full","covariance_eigh","arpack","randomized"],
                                   text="Solver")
        self.svd_solver.button.setCurrentText(self._config["svd_solver"])
        self.svd_solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.svd_solver)

        self.iterated_power = SpinBox(text="Number of iterations")
        self.iterated_power.button.setValue(self._config["iterated_power"])
        self.iterated_power.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.iterated_power)

        self.n_oversamples = SpinBox(text="Oversamples")
        self.n_oversamples.button.setValue(self._config["n_oversamples"])
        self.n_oversamples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_oversamples)

        self.power_iteration_normalizer = ComboBox(items=["auto","QR","LU","none"])
        self.power_iteration_normalizer.button.setCurrentText(self._config["power_iteration_normalizer"])
        self.power_iteration_normalizer.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.power_iteration_normalizer)
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            whiten = self.whiten.button.isChecked(),
            svd_solver = self.svd_solver.button.currentText(),
            iterated_power = self.iterated_power.button.value(),
            n_oversamples = self.n_oversamples.button.value(),
            power_iteration_normalizer = self.power_iteration_normalizer.button.currentText(),
        )
        self.method = decomposition.PCA(**self._config)