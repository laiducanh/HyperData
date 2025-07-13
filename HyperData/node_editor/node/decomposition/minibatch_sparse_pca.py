from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox
from sklearn import decomposition

class MiniBatchSparsePCA(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            alpha = 1,
            ridge_alpha = 0.01,
            max_iter = 1000,
            tol = 1e-3,
            method = "lars",
            batch_size = 3,
            shuffle = True,
            max_no_improvement = 10
        )
        else: self._config = config
        self.method = decomposition.MiniBatchSparsePCA(**self._config)

        self.n_components = HTransparentSpinBox(label="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.alpha = HTransparentSpinBox(label="Sparsity")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

        self.ridge_alpha = HTransparentDoubleSpinBox(singleStep=0.01, label="Ridge shrinkage")
        self.ridge_alpha.button.setValue(self._config["ridge_alpha"])
        self.ridge_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ridge_alpha)

        self.max_iter = HTransparentSpinBox(maximum=10000, singleStep=1000, label="Maximum iteration")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.tol = HTransparentSpinBox(label="Tolerance")
        self.tol.button.setValue(int(1/self._config["tol"]))
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.method = HTransparentComboBox(items=["lars","cd"],label="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.method.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.method)

        self.batch_size = HTransparentSpinBox(label="Batch size")
        self.batch_size.button.setValue(self._config["batch_size"])
        self.batch_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.batch_size)

        self.shuffle = HToggle(label="Shuffle data")
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.shuffle.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shuffle)

        self.max_no_improvement = HTransparentSpinBox(label="Early convergence")
        self.max_no_improvement.button.setValue(self._config["max_no_improvement"])
        self.max_no_improvement.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_no_improvement)
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            alpha = self.alpha.button.value(),
            ridge_alpha = self.ridge_alpha.button.value(),
            max_iter = self.max_iter.button.value(),
            tol = 10**(-self.tol.button.value()),
            method = self.method.button.currentText(),
            batch_size = self.batch_size.button.value(),
            shuffle = self.shuffle.button.isChecked(),
            max_no_improvement = self.max_no_improvement.button.value()
        )
        self.method = decomposition.MiniBatchSparsePCA(**self._config)