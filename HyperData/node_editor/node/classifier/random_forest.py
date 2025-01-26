from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble

DEBUG = False

class RandomForest(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_estimators=100,
            criterion="gini",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0,
            max_features="sqrt",
            max_leaf_nodes=None,
            min_impurity_decrease=0,
            bootstrap=True,
            oob_score=False,
            verbose=0,
            warm_start=False,
            class_weight=None,
            ccp_alpha=0,
            max_samples=None,
            monotonic_cst=None
        )
        else: self._config = config
        self.estimator = ensemble.RandomForestClassifier(**self._config)

        self.n_estimators = SpinBox(text="Number of Trees")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.max_depth = SpinBox(text="Maximum Depth")
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_split = DoubleSpinBox(text="Minimum Number of Samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = DoubleSpinBox(text="Minimum Number of Samples of A Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(text="Minimum Weighted Fraction of A Leaf")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_features = ComboBox(items=["sqrt","log2","None"],text="Number of Features to Split")
        self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = SpinBox(text="Maximum Leafs of A Node")
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity Decrease to Split")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.bootstrap = Toggle(text="Bootstrap")
        self.bootstrap.button.setChecked(self._config["bootstrap"])
        self.bootstrap.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.bootstrap)

        self.oob_score = Toggle(text="Out-Of-Bag Score")
        self.oob_score.button.setChecked(self._config["oob_score"])
        self.oob_score.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.oob_score)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.class_weight = ComboBox(items=["balanced","balanced_subsample","None"],
                                     text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.ccp_alpha = DoubleSpinBox(min=0, text="Complexity Parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)

        self.max_samples = DoubleSpinBox(text="Number of Samples to Train")
        if self._config["max_samples"] == None:
            self.max_samples.button.setValue(-1)
        else: self.max_samples.button.setValue(self._config["max_samples"])
        self.max_samples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_samples)

    def set_estimator(self):
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        else: self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() == -1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        self._config["bootstrap"] = self.bootstrap.button.isChecked()
        self._config["oob_score"] = self.oob_score.button.isChecked()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()
        if self.max_samples.button.value() == -1:
            self._config["max_samples"] = None
        else: self._config["max_samples"] = self.max_samples.button.value()
 
        self.estimator = ensemble.RandomForestClassifier(**self._config)