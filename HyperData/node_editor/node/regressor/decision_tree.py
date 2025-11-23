from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.regressor.base import RegressorBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import tree

DEBUG = False

class DecisionTree(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            criterion="squared_error",
            splitter="best",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0,
            max_features=None,
            max_leaf_nodes=None,
            min_impurity_decrease=0,
            ccp_alpha=0,
            monotonic_cst=None
        )
        else: self._config = config
        self.estimator = tree.DecisionTreeRegressor(**self._config)

        self.criterion = HTransparentComboBox(
            items=['squared_error','friedman_mse','absolute_error','poisson'], 
            label="Criterion",
            getter=lambda: self._config["criterion"],
            setter=self.set_estimator,
            layout=self.vlayout
        )   

        self.splitter = HTransparentComboBox(
            items=["best","random"],
            label="Splitter",
            getter=lambda: self._config["splitter"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max_depth = HTransparentDoubleSpinBox(
            minimum=-1, 
            label="Maximum Depth",
            decimals=0,
            getter=lambda: -1 if not self._config["max_depth"] else self._config["max_depth"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_samples_split = HTransparentSpinBox(
            label="Minimum samples to Split",
            getter=lambda: self._config["min_samples_split"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_samples_leaf = HTransparentSpinBox(
            label="Minimum samples to a Node",
            getter=lambda: self._config["min_samples_leaf"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.min_weight_fraction_leaf = HTransparentDoubleSpinBox(
            singleStep=0.1,maximum=1,
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

        self.max_leaf_nodes = HTransparentDoubleSpinBox(
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
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()

        self.estimator = tree.DecisionTreeRegressor(**self._config)