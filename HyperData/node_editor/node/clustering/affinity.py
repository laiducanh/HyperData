from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from sklearn import cluster

class AffinityPropagation(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            damping = 0.5,
            max_iter = 200,
            convergence_iter = 15,
            affinity = "euclidean"
        )
        else: self._config = config
        self.method = cluster.AffinityPropagation(**self._config)

        self.damping = DoubleSpinBox(min=0.5, max=1, step=0.05, text="Damping factor")
        self.damping.button.setValue(self._config["damping"])
        self.damping.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.damping)

        self.max_iter = SpinBox(min=1,max=10000,step=100,text="Max of iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.convergence_iter = SpinBox(min=1, text="Early convergence")
        self.convergence_iter.button.setValue(self._config["convergence_iter"])
        self.convergence_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.convergence_iter)

        self.affinity = ComboBox(items=["euclidean","precomputed"], text="Affinity")
        self.affinity.button.setCurrentText(self._config["affinity"])
        self.affinity.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.affinity)
        
    def set_estimator(self):
        self._config.update(
            damping = self.damping.button.value(),
            max_iter = self.max_iter.button.value(),
            convergence_iter = self.convergence_iter.button.value(),
            affinity = self.affinity.button.currentText()
        )
        self.method = cluster.AffinityPropagation(**self._config)