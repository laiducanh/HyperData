from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
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

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.alpha = SpinBox(text="Sparsity")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

        self.ridge_alpha = DoubleSpinBox(step=0.01, text="Ridge shrinkage")
        self.ridge_alpha.button.setValue(self._config["ridge_alpha"])
        self.ridge_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ridge_alpha)

        self.max_iter = SpinBox(max=10000, step=1000, text="Maximum iteration")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.tol = SpinBox(text="Tolerance")
        self.tol.button.setValue(int(1/self._config["tol"]))
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.method = ComboBox(items=["lars","cd"],text="Method")
        self.method.button.setCurrentText(self._config["method"])
        self.method.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.method)

        self.batch_size = SpinBox(text="Batch size")
        self.batch_size.button.setValue(self._config["batch_size"])
        self.batch_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.batch_size)

        self.shuffle = Toggle(text="Shuffle data")
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.shuffle.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shuffle)

        self.max_no_improvement = SpinBox(text="Early convergence")
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