from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from sklearn import cluster

class BisectingKMeans(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 8,
            init = "k-means++",
            max_iter = 300,
            tol = 1e-4,
            algorithm = "lloyd",
            bisecting_strategy = "biggest_inertia"
        )
        else: self._config = config
        self.method = cluster.BisectingKMeans(**self._config)

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

        self.tol = SpinBox(min=1, text="Tolerance")
        self.tol.button.setValue(int(1/self._config["tol"]))
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.algorithm = ComboBox(items=["lloyd","elkan"],text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.bisecting_strategy = ComboBox(items=["biggest_inertia","largest_cluster"], text="Bisecting strategy")
        self.bisecting_strategy.button.setCurrentText(self._config["bisecting_strategy"])
        self.bisecting_strategy.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.bisecting_strategy)
        
    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            init = self.init.button.currentText(),
            max_iter = self.max_iter.button.value(),
            tol = 1/(10**(-self.tol)),
            algorithm = self.algorithm.button.currentText(),
            bisecting_strategy = self.bisecting_strategy.button.currentText()
        )
        self.method = cluster.BisectingKMeans(**self._config)