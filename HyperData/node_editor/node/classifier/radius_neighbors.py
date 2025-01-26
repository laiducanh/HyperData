from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
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

        self.radius = DoubleSpinBox(text="Range of parameter space")
        self.radius.button.setValue(self._config["radius"])
        self.radius.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.radius)

        self.weights = ComboBox(items=["uniform","distance"], text="Weight Function")
        self.weights.button.setCurrentText(self._config["weights"])
        self.weights.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.weights)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = DoubleSpinBox(text="Power parameter")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)

        self.outlier_label = ComboBox(items=["manual label","most_frequent","None"], text="Label for outliers")
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