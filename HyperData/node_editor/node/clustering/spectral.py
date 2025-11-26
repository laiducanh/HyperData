from node_editor.node.clustering.base import MethodBase
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox, HTransparentDoubleSpinBox
from sklearn import cluster

class SpectralClustering(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_clusters = 8,
            gamma=1.0,
            affinity = "rbf",
            n_neighbors=10,
            assign_labels = "kmeans",
            degree=3,
            coef0=1,
        )
        else: self._config = config
        self.method = cluster.SpectralClustering(**self._config)

        self.n_clusters = HTransparentSpinBox(minimum=1,label="Number of clusters")
        self.n_clusters.button.setValue(self._config["n_clusters"])
        self.n_clusters.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_clusters)

        self.gamma = HTransparentDoubleSpinBox(
            label='Kernel coefficient',
            label2='Used for rbf, poly, sigmoid, laplacian, and chi2 kernel',
            getter=lambda: self._config['gamma'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.affinity = HTransparentComboBox(
            items=["nearest_neighbors","rbf","precomputed","precomputed_nearest_neighbors",
                   'additive_chi2','chi2','linear','polynomial','poly','rbf',
                   'laplacian','sigmoid','cosine'],
            label='Affinity',
            label2='Method to construct the affinity matrix',
            getter=lambda: self._config['affinity'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.n_neighbors = HTransparentSpinBox(
            label='Number of neighbors',
            label2='Using with the nearest neighbors method',
            getter=lambda: self._config['n_neighbors'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.assign_labels = HTransparentComboBox(items=["kmeans","discretize","cluster_qr"], label="Assigning label strategy")
        self.assign_labels.button.setCurrentText(self._config["assign_labels"])
        self.assign_labels.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.assign_labels)

        self.degree = HTransparentSpinBox(
            label='Degree',
            label2='Degree of the polynomial kernel',
            getter=lambda: self._config['degree'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.coef0 = HTransparentDoubleSpinBox(
            label='Zero coefficient',
            label2='Used for polynomial and sigmoid kernels',
            getter=lambda: self._config['coef0'],
            setter=self.set_estimator,
            layout=self.vlayout
        )

    def set_estimator(self):
        self._config.update(
            n_clusters = self.n_clusters.button.value(),
            gamma = self.gamma.get_value(),
            affinity = self.affinity.button.currentText(),
            n_neighbors = self.n_neighbors.get_value(),
            assign_labels = self.assign_labels.button.currentText(),
            degree = self.degree.get_value(),
            coef0 = self.coef0.get_value()
        )
        self.method = cluster.SpectralClustering(**self._config)