from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble

DEBUG = False

class GradientBoosting(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loss="log_loss",
            learning_rate=0.1,
            n_estimators=100,
            subsample=1.0,
            criterion="friedman_mse",
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0,
            max_depth=3,
            min_impurity_decrease=0,
            init=None,
            max_features=None,
            verbose=0,
            max_leaf_nodes=None,
            warm_start=False,
            validation_fraction=0.1,
            n_iter_no_change=None,
            tol=1e-4,
            ccp_alpha=0
        )
        else: self._config = config
        self.estimator = ensemble.GradientBoostingClassifier(**self._config)

        self.loss = ComboBox(items=["log_loss","exponential"], text="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.learning_rate = DoubleSpinBox(step=0.5, text="Learning Rate")
        self.learning_rate.button.setValue(self._config["learning_rate"])
        self.learning_rate.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.n_estimators = SpinBox(min=1, max=10000, step=100, text="Number of Boosting Stages")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.subsample = DoubleSpinBox(min=0.01, max=1, step=0.05, text="Fraction of samples")
        self.subsample.button.setValue(self._config["subsample"])
        self.subsample.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.subsample)

        self.criterion = ComboBox(items=["friedman_mse","squared_error"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.min_samples_split = SpinBox(min=2, max=1000, step=10, text="Minimum Number of Samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = SpinBox(min=1, max=1000, step=10, text="Minimum Number of Samples to A Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(max=0.5, step=0.05, text="Minimum Weighted Fraction to A Leaf")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_depth = SpinBox(min=1, max=1000, text="Maximum Depth of Estimators")
        self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity Decrease to Split ")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.max_features = ComboBox(items=["sqrt","log2","max"], text="Number of Features")
        if self._config["max_features"] == None:
            self.max_features.button.setCurrentText("max")
        else: self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum Number of Leafs in A Node")
        self.max_leaf_nodes.button.setDecimals(0)
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.validation_fraction = DoubleSpinBox(min=0.01, max=0.99, step=0.05, text="Validation Fraction")
        self.validation_fraction.button.setValue(self._config["validation_fraction"])
        self.validation_fraction.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.validation_fraction)

        self.n_iter_no_change = SpinBox(min=-1, text="Early Stopping")
        if self._config["n_iter_no_change"] == None:
            self.n_iter_no_change.button.setValue(-1)
        else: self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.tol = DoubleSpinBox(min=1e-5,max=1e-3,step=1e-4,text="Tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.ccp_alpha = DoubleSpinBox(text="Complexity Parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)
        
    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText()
        self._config["learning_rate"] = self.learning_rate.button.value()
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["subsample"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        if self.max_features.button.currentText() == "max":
            self._config["max_features"] = None
        else: self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() < 2:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        self._config["validation_fraction"] = self.validation_fraction.button.value()
        if self.n_iter_no_change.button.value() < 1:
            self._config["n_iter_no_change"] = None
        else: self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["tol"] = self.tol.button.value()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()
 
        self.estimator = ensemble.GradientBoostingClassifier(**self._config)