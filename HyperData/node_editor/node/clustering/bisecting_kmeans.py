from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from sklearn import cluster

class BisectingKMeans(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 8,
            init = "k-means++",
            n_init=1,
            max_iter = 300,
            algorithm = "lloyd",
            bisecting_strategy = "biggest_inertia"
        )
        else: self._config = config
        self.method = cluster.BisectingKMeans(**self._config)

        self.n_clusters = HTransparentSpinBox(minimum=1,label="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)

        self.init = HTransparentComboBox(items=["k-means++","random"],label="Initialization")
        self.init.button.setCurrentText(self._config["init"])
        self.init.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.init)

        self.n_init = HTransparentSpinBox(
            label='Number of initializations',
            label2='Number of time the inner k-means algorithm will be run with different centroid seeds in each bisection',
            getter=lambda: self._config['n_init'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_iter = HTransparentSpinBox(minimum=1,maximum=10000,singleStep=100,label="Max of iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.algorithm = HTransparentComboBox(items=["lloyd","elkan"],label="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.bisecting_strategy = HTransparentComboBox(items=["biggest_inertia","largest_cluster"], label="Bisecting strategy")
        self.bisecting_strategy.button.setCurrentText(self._config["bisecting_strategy"])
        self.bisecting_strategy.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.bisecting_strategy)
        
    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            init = self.init.button.currentText(),
            n_int = self.n_init.button.value(),
            max_iter = self.max_iter.button.value(),
            algorithm = self.algorithm.button.currentText(),
            bisecting_strategy = self.bisecting_strategy.button.currentText()
        )
        self.method = cluster.BisectingKMeans(**self._config)
    