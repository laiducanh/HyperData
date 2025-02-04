from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from sklearn import cluster

class HDBSCAN(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            min_cluster_size = 5,
            cluster_selection_epsilon = 0.0,
            metric = "euclidean",
            alpha = 1.0,
            algorithm = "auto",
            leaf_size = 40,
            cluster_selection_method = "eom",
            allow_single_cluster = False
        )
        else: self._config = config
        self.method = cluster.HDBSCAN(**self._config)

        self.min_cluster_size = SpinBox(text="Minimum number of samples")
        self.min_cluster_size.button.setValue(self._config["min_cluster_size"])
        self.min_cluster_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_cluster_size)

        self.cluster_selection_epsilon = DoubleSpinBox(text="Distance threshold")
        self.cluster_selection_epsilon.button.setValue(self._config["cluster_selection_epsilon"])
        self.cluster_selection_epsilon.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.cluster_selection_epsilon)

        self.metric_ = ComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan",
                                      "braycurtis","canberra","chebyshev","correlation","dice",
                                      "hamming","jaccard","kulsinski","mahalanobis","rogerstanimoto",
                                      "russellrao","seuclidean","sokalmichener","sokalsneath","sqeuclidean",
                                      "yule"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)

        self.alpha = DoubleSpinBox(text="Scaling parameter")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.cluster_selection_method = ComboBox(items=["eom","leaf"], text="Method")
        self.cluster_selection_method.button.setCurrentText(self._config["cluster_selection_method"])
        self.cluster_selection_method.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.cluster_selection_method)

        self.allow_single_cluster = Toggle(text="Single cluster")
        self.allow_single_cluster.button.setChecked(self._config["allow_single_cluster"])
        self.allow_single_cluster.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.allow_single_cluster)
        
    def set_estimator(self):
        self._config.update(
            min_cluster_size = self.min_cluster_size.button.value(),
            cluster_selection_epsilon = self.cluster_selection_epsilon.button.value(),
            metric = self.metric_.button.currentText(),
            alpha = self.alpha.button.value(),
            algorithm = self.algorithm.button.currentText(),
            leaf_size = self.leaf_size.button.value(),
            cluster_selection_method = self.cluster_selection_method.button.currentText(),
            allow_single_cluster = self.allow_single_cluster.button.isChecked()
        )
        self.method = cluster.HDBSCAN(**self._config)