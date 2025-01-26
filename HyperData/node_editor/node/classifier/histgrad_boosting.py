from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble

DEBUG = False

class HistGradientBoosting(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loss="log_loss",
            learning_rate=0.1,
            max_iter=100,
            max_leaf_nodes=31,
            max_depth=None,
            min_samples_leaf=20,
            l2_regularization=0,
            max_features=1.0,
            max_bins=255,
            monotonic_cst=None,
            interaction_cst=None,
            warm_start=False,
            early_stopping="auto",
            scoring="loss",
            validation_fraction=0.1,
            n_iter_no_change=10,
            tol=1e-7,
            verbose=0,
            class_weight=None
        )
        else: self._config = config
        self.estimator = ensemble.HistGradientBoostingClassifier(**self._config)

        self.loss = ComboBox(items=["log_loss"], text="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.learning_rate = DoubleSpinBox(max=1,step=0.05,text="Learning Rate")
        self.learning_rate.button.setValue(self._config["learning_rate"])
        self.learning_rate.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.max_iter = SpinBox(max=10000, step=500, text="Maximum Number of Iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum nmber of Leaves")
        self.max_leaf_nodes.button.setDecimals(0)
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.max_depth = DoubleSpinBox(min=-1, text="Maximum Depth")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_leaf = SpinBox(text="Minimum Number of Samples per Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.l2_regularization = DoubleSpinBox(text="L2 Regularization")
        self.l2_regularization.button.setValue(self._config["l2_regularization"])
        self.l2_regularization.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.l2_regularization)

        self.max_features = DoubleSpinBox(text="Proportion of Randomly Features")
        self.max_features.button.setValue(self._config["max_features"])
        self.max_features.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_bins = SpinBox(max=255, text="Maximum Number of Bins")
        self.max_bins.button.setValue(self._config["max_bins"])
        self.max_bins.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_bins)

        self.interaction_cst = ComboBox(items=["pairwise","no_interactions"],
                                        text="Interaction Constraints")
        self.interaction_cst.button.setCurrentText(self._config["interaction_cst"])
        self.interaction_cst.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.interaction_cst)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.early_stopping = ComboBox(items=["auto","True","False"], text="Early Stopping")
        if self._config["early_stopping"] == True:
            self.early_stopping.button.setCurrentText("True")
        elif self._config["early_stopping"] == False:
            self.early_stopping.button.setCurrentText("False")
        else: self.early_stopping.button.setCurrentText(self._config["early_stopping"])
        self.early_stopping.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.early_stopping)

        self.validation_fraction = DoubleSpinBox(text="Proportion for Validation Data")
        self.validation_fraction.button.setValue(self._config["validation_fraction"])
        self.validation_fraction.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.validation_fraction)

        self.n_iter_no_change = SpinBox(text="Criterion for Early Stop")
        self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.tol = DoubleSpinBox(min=1e-8,max=1e-6,step=1e-7,text="Tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.class_weight = ComboBox(items=["None","balanced"],text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)
        

    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText()
        self._config["learning_rate"] = self.learning_rate.button.value()
        self._config["max_iter"] = self.max_iter.button.value()
        if self.max_leaf_nodes.button.value() < 1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["l2_regularization"] = self.l2_regularization.button.value()
        self._config["max_features"] = self.max_features.button.value()
        self._config["max_bins"] = self.max_bins.button.value()
        self._config["interaction_cst"] = self.interaction_cst.button.currentText()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        if self.early_stopping.button.currentText() == "True":
            self._config["early_stopping"] = True
        elif self.early_stopping.button.currentText() == "False":
            self._config["early_stopping"] = False
        else: self._config["early_stopping"] = self.early_stopping.button.currentText()
        self._config["validation_fraction"] = self.validation_fraction.button.value()
        self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["tol"] = self.tol.button.value()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self.estimator = ensemble.HistGradientBoostingClassifier(**self._config)