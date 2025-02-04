from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from sklearn import cluster

class DBSCAN(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            eps = 0.5,
            min_samples = 5,
            metric = "euclidean",
            algorithm = "auto",
            leaf_size = 30,
            p = 2.0,
        )
        else: self._config = config
        self.method = cluster.DBSCAN(**self._config)

        self.eps = DoubleSpinBox(text="Maximum distance")
        self.eps.button.setValue(self._config["eps"])
        self.eps.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.eps)

        self.min_samples = SpinBox(text="Minimum number of samples")
        self.min_samples.button.setValue(self._config["min_samples"])
        self.min_samples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples)

        self.metric_ = ComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan",
                                      "braycurtis","canberra","chebyshev","correlation","dice",
                                      "hamming","jaccard","kulsinski","mahalanobis","rogerstanimoto",
                                      "russellrao","seuclidean","sokalmichener","sokalsneath","sqeuclidean",
                                      "yule"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = DoubleSpinBox(text="Minkowski metric")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)
        
    def set_estimator(self):
        self._config.update(
            eps = self.eps.button.value(),
            min_samples = self.min_samples.button.value(),
            metric = self.metric_.button.currentText(),
            algorithm = self.algorithm.button.currentText(),
            leaf_size = self.leaf_size.button.value(),
            p = self.p.button.value(),
        )
        self.method = cluster.DBSCAN(**self._config)