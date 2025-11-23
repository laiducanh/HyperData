from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble, tree

DEBUG = False

class ExtraTrees(ClassifierBase):
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
            bootstrap=False,
            oob_score=False,
            verbose=0,
            warm_start=False,
            class_weight=None,
            ccp_alpha=0,
            max_samples=None
        )
        else: self._config = config
        self.estimator = ensemble.ExtraTreesClassifier(**self._config)

        self.n_estimators = HTransparentSpinBox(maximum=1000,singleStep=100,label="Number of Trees")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.criterion = HTransparentComboBox(items=["gini","entropy","log_loss"],label="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.max_depth = HTransparentDoubleSpinBox(minimum=-1, maximum=1000, singleStep=10, label="Maximum Depth of Tree")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)


        
    def set_estimator(self):
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        else: self._config["max_depth"] = int(self.max_depth.button.value())
        
        self.estimator = ensemble.ExtraTreesClassifier(**self._config)

class ExtraTree(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            criterion='gini',
            splitter='random',
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_features='sqrt',
            max_leaf_nodes=None,
            min_impurity_decrease=0,
            class_weight=None,
            ccp_alpha=0,
        )
        else: self._config = config
        self.estimator = tree.ExtraTreeClassifier(**self._config)

        self.criterion = HTransparentComboBox(
            items=["gini","entropy","log_loss"], 
            label="Criterion",
            label2='The function to measure the quality of a split',
            getter=lambda: self._config["criterion"],
            setter=self.set_estimator,
            layout=self.vlayout
        )   

        self.splitter = HTransparentComboBox(
            items=["best","random"],
            label="Splitter",
            label2='The strategy used to choose the split at each node',
            getter=lambda: self._config["splitter"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_depth = HTransparentSpinBox(
            minimum=-1, singleStep=1,
            label="Maximum Depth",
            label2='The maximum depth of the tree',
            getter=lambda: -1 if not self._config["max_depth"] else self._config["max_depth"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_samples_split = HTransparentSpinBox(
            label="Minimum samples to split",
            getter=lambda: self._config["min_samples_split"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_samples_leaf = HTransparentSpinBox(
            label="Minimum samples to a node",
            getter=lambda: self._config["min_samples_leaf"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_weight_fraction_leaf = HTransparentDoubleSpinBox(
            singleStep=0.1,maximum=1,minimum=0,
            label="Minimum weighted fraction",
            getter=lambda: self._config["min_weight_fraction_leaf"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_features = HTransparentComboBox(
            items=["sqrt","log2","max"], 
            label="Max Features",
            getter=lambda: "max" if not self._config["max_features"] else self._config["max_features"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_leaf_nodes = HTransparentSpinBox(
            minimum=-1, 
            label="Maximum Nodes",
            getter=lambda: -1 if not self._config["max_leaf_nodes"] else self._config["max_leaf_nodes"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_impurity_decrease = HTransparentDoubleSpinBox(
            label="Impurity",
            getter=lambda: self._config["min_impurity_decrease"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.class_weight = HTransparentComboBox(
            items=["None","balanced"], 
            label="Class Weight",
            getter=lambda: 'None' if not self._config["class_weight"] else self._config["class_weight"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.ccp_alpha = HTransparentDoubleSpinBox(
            label="Complexity parameter",
            getter=lambda: self._config["ccp_alpha"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
        
    def set_estimator(self):
        self._config["criterion"] = self.criterion.button.currentText()
        self._config["splitter"] = self.splitter.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        else: self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        if self.max_features.button.currentText() == "max":
            self._config["max_features"] = None
        else: self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() == -1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()
        self.estimator = tree.ExtraTreeClassifier(**self._config)