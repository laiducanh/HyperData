from node_editor.node.clustering.base import MethodBase
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from sklearn import cluster

class AgglomerativeClustering(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 2,
            metric = "euclidean",
            linkage = "ward",
            compute_distances = False
        )
        else: self._config = config
        self.method = cluster.AgglomerativeClustering(**self._config)

        self.n_clusters = SpinBox(min=1,text="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)

        self.metric_ = ComboBox(items=["euclidean","l1","l2","manhattan","cosine"],text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)

        self.linkage = ComboBox(items=["ward","complete","average","single"], text="Linkage criterion")
        self.linkage.button.setCurrentText(self._config["linkage"])
        self.linkage.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.linkage)
        
    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            metric = self.metric_.button.currentText(),
            linkage = self.linkage.button.currentText(),
        )
        self.method = cluster.AgglomerativeClustering(**self._config)