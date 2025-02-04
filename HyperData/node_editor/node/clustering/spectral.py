from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from sklearn import cluster

class SpectralClustering(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 8,
            eigen_solver = "arpack",
            affinity = "rbf",
            assign_labels = "kmeans",
        )
        else: self._config = config
        self.method = cluster.SpectralClustering(**self._config)

        self.n_clusters = SpinBox(min=1,text="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)

        self.eigen_solver = ComboBox(items=["arpack","lobpcg","amg"],text="Decomposition strategy")
        self.eigen_solver.button.setCurrentText(self._config["eigen_solver"])
        self.eigen_solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.eigen_solver)

        self.affinity = ComboBox(items=["nearest_neighbors","rbf","precomputed","precomputed_nearest_neighbors"])
        self.affinity.button.setCurrentText(self._config["affinity"])
        self.affinity.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.affinity)

        self.assign_labels = ComboBox(items=["kmeans","discretize","cluster_qr"], text="Assigning label strategy")
        self.assign_labels.button.setCurrentText(self._config["assign_labels"])
        self.assign_labels.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.assign_labels)

    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            eigen_solver = self.eigen_solver.button.currentText(),
            affinity = self.affinity.button.currentText(),
            assign_labels = self.assign_labels.button.currentText(),
        )
        self.method = cluster.SpectralClustering(**self._config)