from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import neighbors

DEBUG = False

class KNeighbors (ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_neighbors=5, 
            weights="uniform",
            algorithm="auto",
            leaf_size=30, 
            p=2
        )
        else: self._config = config
        self.estimator = neighbors.KNeighborsClassifier(**self._config)

        self.n_neighbors = SpinBox(text="Number of neighbors")
        self.n_neighbors.button.setValue(self._config["n_neighbors"])
        self.n_neighbors.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_neighbors)

        self.weights = ComboBox(items=["uniform","distance"], text="Weight function")
        self.weights.button.setCurrentText(self._config["weights"])
        self.weights.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.weights)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf Size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = DoubleSpinBox(max=10, text="Power parameter")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)
        
    def set_estimator(self):
        self._config["n_neighbors"] = self.n_neighbors.button.value()
        self._config["weights"] = self.weights.button.currentText()
        self._config["algorithm"] = self.algorithm.button.currentText()
        self._config["leaf_size"] = self.leaf_size.button.value()
        self._config["p"] = self.p.button.value()
        
        self.estimator = neighbors.KNeighborsClassifier(**self._config)