from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import neighbors

DEBUG = False

class RadiusNeighbors(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            radius=1.0, 
            weights="uniform", 
            algorithm="auto",
            leaf_size=30,
            p=2, 
            outlier_label=None
        )
        else: self._config = config
        self.estimator = neighbors.RadiusNeighborsClassifier(**self._config)

        self.radius = HTransparentDoubleSpinBox(label="Range of parameter space")
        self.radius.button.setValue(self._config["radius"])
        self.radius.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.radius)

        self.weights = HTransparentComboBox(items=["uniform","distance"], label="Weight Function")
        self.weights.button.setCurrentText(self._config["weights"])
        self.weights.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.weights)

        self.algorithm = HTransparentComboBox(items=["auto","ball_tree","kd_tree","brute"], label="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = HTransparentSpinBox(label="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = HTransparentDoubleSpinBox(label="Power parameter")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)

        self.outlier_label = HTransparentComboBox(items=["manual label","most_frequent","None"], label="Label for outliers")
        self.outlier_label.button.setCurrentText(self._config["outlier_label"])
        self.outlier_label.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.outlier_label)
        
    def set_estimator(self):
        self._config["radius"] = self.radius.button.value()
        self._config["weights"] = self.weights.button.currentText()
        self._config["algorithm"] = self.algorithm.button.currentText()
        self._config["leaf_size"] = self.leaf_size.button.value()
        self._config["p"] = self.p.button.value()
        self._config["outlier_label"] = self.outlier_label.button.currentText()
 
        self.estimator = neighbors.RadiusNeighborsClassifier(**self._config)