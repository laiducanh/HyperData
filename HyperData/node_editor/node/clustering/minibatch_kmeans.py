from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from sklearn import cluster

class MiniBatchKMeans(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 8,
            init = "k-means++",
            max_iter = 100,
            batch_size = 1024,
            tol = 1e-4,
            max_no_improvement = 10,
            reassignment_ratio = 0.01
        )
        else: self._config = config
        self.method = cluster.MiniBatchKMeans(**self._config)

        self.n_clusters = SpinBox(min=1,text="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)

        self.init = ComboBox(items=["k-means++","random"],text="Initialization")
        self.init.button.setCurrentText(self._config["init"])
        self.init.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.init)

        self.max_iter = SpinBox(min=1,max=10000,step=100,text="Max of iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.batch_size = SpinBox(min=1, step=10, text="Batch size")
        self.batch_size.button.setValue(self._config["batch_size"])
        self.batch_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.batch_size)

        self.tol = SpinBox(min=1, text="Tolerance")
        self.tol.button.setValue(int(1/self._config["tol"]))
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.max_no_improvement = SpinBox(text="Early convergence")
        self.max_no_improvement.button.setValue(self._config["max_no_improvement"])
        self.max_no_improvement.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_no_improvement)

        self.reassignment_ratio = DoubleSpinBox(text="Reassignment ratio")
        self.reassignment_ratio.button.setValue(self._config["reassignment_ratio"])
        self.reassignment_ratio.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.reassignment_ratio)
        
    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            init = self.init.button.currentText(),
            max_iter = self.max_iter.button.value(),
            batch_size = self.batch_size.button.value(),
            tol = 1/(10**(-self.tol)),
            max_no_improvement = self.max_no_improvement.button.value(),
            reassignment_ratio = self.reassignment_ratio.button.value()
        )
        self.method = cluster.MiniBatchKMeans(**self._config)