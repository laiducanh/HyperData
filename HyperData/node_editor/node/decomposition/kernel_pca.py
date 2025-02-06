from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from sklearn import decomposition

class KernelPCA(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_components = None,
            kernel = "linear",
            eigen_solver = "auto"
        )
        else: self._config = config
        self.method = decomposition.KernelPCA(**self._config)

        self.n_components = SpinBox(text="Number of components")
        self.n_components.button.setValue(self._config["n_components"])
        self.n_components.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_components)

        self.kernel = ComboBox(items=["linear","poly","rbf","sigmoid","cosine"], text="Kernel")
        self.kernel.button.setCurrentText(self._config["kernel"])
        self.kernel.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.kernel)

        self.eigen_solver = ComboBox(items=["auto","dense","arpack","randomized"], text="Solver")
        self.eigen_solver.button.setCurrentText(self._config["eigen_solver"])
        self.eigen_solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.eigen_solver)
        
    def set_estimator(self):
        self._config.update(
            n_components = self.n_components.button.value(),
            kernel = self.kernel.button.currentText(),
            eigen_solver = self.eigen_solver.button.currentText()
        )
        self.method = decomposition.KernelPCA(**self._config)