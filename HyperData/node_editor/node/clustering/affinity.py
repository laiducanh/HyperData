from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
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

        self.damping = HTransparentDoubleSpinBox(minimum=0.5, maximum=1, singleStep=0.05, label="Damping factor")
        self.damping.button.setValue(self._config["damping"])
        self.damping.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.damping)

        self.max_iter = HTransparentSpinBox(minimum=1,maximum=10000,singleStep=100,label="Max of iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.convergence_iter = HTransparentSpinBox(minimum=1, label="Early convergence")
        self.convergence_iter.button.setValue(self._config["convergence_iter"])
        self.convergence_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.convergence_iter)

        self.affinity = HTransparentComboBox(items=["euclidean","precomputed"], label="Affinity")
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