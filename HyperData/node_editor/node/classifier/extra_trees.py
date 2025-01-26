from ui.base_widgets.button import ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import ensemble

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

        self.n_estimators = SpinBox(max=1000,step=100,text="Number of Trees")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"],text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.max_depth = DoubleSpinBox(min=-1, max=1000, step=10, text="Maximum Depth of Tree")
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