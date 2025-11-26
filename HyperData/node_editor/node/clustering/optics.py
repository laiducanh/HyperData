from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox
from sklearn import cluster

class OPTICS(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            min_samples = 5,
            metric = "minkowski",
            cluster_method = "xi",
            xi = 0.05,
            predecessor_correction = True,
            algorithm = "auto",
            leaf_size = 30
        )
        else: self._config = config
        self.method = cluster.OPTICS(**self._config)

        self.min_samples = HTransparentSpinBox(label="Minimum number of samples")
        self.min_samples.button.setValue(self._config["min_samples"])
        self.min_samples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples)

        self.metric_ = HTransparentComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan",
                                      "braycurtis","canberra","chebyshev","correlation","dice",
                                      "hamming","jaccard","kulsinski","mahalanobis","minkowski","rogerstanimoto",
                                      "russellrao","seuclidean","sokalmichener","sokalsneath","sqeuclidean",
                                      "yule"], label="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)

        self.cluster_method = HTransparentComboBox(items=["xi","dbscan"], label="Method")
        self.cluster_method.button.setCurrentText(self._config["cluster_method"])
        self.cluster_method.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.cluster_method)

        self.xi = HTransparentDoubleSpinBox(minimum=0, maximum=1, singleStep=0.05, label="Minimum steepness")
        self.xi.button.setValue(self._config["xi"])
        self.xi.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.xi)

        self.predecessor_correction = HToggle(label="Predecessor correction")
        self.predecessor_correction.button.setChecked(self._config["predecessor_correction"])
        self.predecessor_correction.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.predecessor_correction)

        self.algorithm = HTransparentComboBox(items=["auto","ball_tree","kd_tree","brute"], label="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = HTransparentSpinBox(label="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)
        
    def set_estimator(self):
        self._config.update(
            min_samples = self.min_samples.button.value(),
            metric = self.metric_.button.currentText(),
            cluster_method = self.cluster_method.button.currentText(),
            xi = self.xi.button.value(),
            predecessor_correction = self.predecessor_correction.button.isChecked(),
            algorithm = self.algorithm.button.currentText(),
            leaf_size = self.leaf_size.button.value(),
        )
        self.method = cluster.OPTICS(**self._config)
    