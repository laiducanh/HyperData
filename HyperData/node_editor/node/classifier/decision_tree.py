from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import tree

DEBUG = False

class DecisionTree(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            criterion="gini",
            splitter="best",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0,
            max_features=None,
            max_leaf_nodes=None,
            min_impurity_decrease=0,
            class_weight=None,
            ccp_alpha=0,
            monotonic_cst=None
        )
        else: self._config = config
        self.estimator = tree.DecisionTreeClassifier(**self._config)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.splitter = ComboBox(items=["best","random"],text="Splitter")
        self.splitter.button.setCurrentText(self._config["splitter"])
        self.splitter.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.splitter)

        self.max_depth = DoubleSpinBox(min=-1, text="Maximum Depth")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_split = SpinBox(text="Minimum samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = SpinBox(text="Minimum samples to a Node")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(step=0.1,max=1,
                                                      text="Minimum weighted fraction")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_features = ComboBox(items=["sqrt","log2","max"], text="Max Features")
        if self._config["max_features"] == None:
            self.max_features.button.setCurrentText("max")
        else: self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum Nodes")
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.class_weight = ComboBox(items=["None","balanced"], text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.ccp_alpha = DoubleSpinBox(text="Complexity parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)

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

        self.estimator = tree.DecisionTreeClassifier(**self._config)