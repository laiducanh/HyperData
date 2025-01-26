from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import gaussian_process

DEBUG = False

class GaussianProcess(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            kernel=None,
            optimizer="fmin_l_bfgs_b",
            n_restarts_optimizer=0,
            max_iter_predict=100,
            warm_start=False,
            multi_class="one_vs_rest"
        )
        else: self._config = config
        self.estimator = gaussian_process.GaussianProcessClassifier(**self._config)
        
        self.optimizer = ComboBox(items=["fmin_l_bfgs_b"],text="Optimizer")
        self.optimizer.button.setCurrentText(self._config["optimizer"])
        self.optimizer.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.optimizer)

        self.n_restarts_optimizer =SpinBox(text="Number of restarts")
        self.n_restarts_optimizer.button.setValue(self._config["n_restarts_optimizer"])
        self.n_restarts_optimizer.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_restarts_optimizer)

        self.max_iter_predict = SpinBox(max=10000, step=100, text="Maximum iterations")
        self.max_iter_predict.button.setValue(self._config["max_iter_predict"])
        self.max_iter_predict.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter_predict)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.multi_class = ComboBox(items=["one_vs_rest","one_vs_one"],text="Multi-class")
        self.multi_class.button.setCurrentText(self._config["multi_class"])
        self.multi_class.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.multi_class)

    def set_estimator(self):
        self._config["optimizer"] = self.optimizer.button.currentText()
        self._config["n_restarts_optimizer"] = self.n_restarts_optimizer.button.value()
        self._config["max_iter_predict"] = self.max_iter_predict.button.value()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        self._config["multi_class"] = self.multi_class.button.currentText()
        self.estimator = gaussian_process.GaussianProcessClassifier(**self._config)