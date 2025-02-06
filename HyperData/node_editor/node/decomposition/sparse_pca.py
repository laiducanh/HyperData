from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from sklearn import decomposition

class SparsePCA(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            alpha = 1.0,
            max_iter = 1000,
            tol = 1e-8,
            method = "lars"
        )
        else: self._config = config
        self.method = decomposition.SparsePCA(**self._config)

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.alpha = DoubleSpinBox(text="Sparsity")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

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
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            alpha = self.alpha.button.value(),
            max_iter = self.max_iter.button.value(),
            tol = 10**(-self.tol.button.value()),
            method = self.method.button.currentText()
        )
        self.method = decomposition.SparsePCA(**self._config)