from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import linear_model

DEBUG = False

class SGDClassifier(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            loss="hinge",
            penalty="l2",
            alpha=0.0001,
            fit_intercept=True,
            max_iter=1000,
            shuffle=True,
            learning_rate="optimal",
            eta0=0,
            power_t=0.5,
            early_stopping=False,
            tol=1e-3,
            average=False,
            n_iter_no_change=5
        )
        else: self._config = config
        self.estimator = linear_model.SGDClassifier(**self._config)

        self.loss = HTransparentComboBox(items=["hinge","log_loss","modified_huber","squared_hinge",
                                    "perceptron","squared_error","huber","epsilon_insensitive",
                                    "squared_epsilon_insensitive"], label="loss function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)

        self.penalty = HTransparentComboBox(items=["l1", "l2", "elasticnet", "none"], label="Penalty")
        self.penalty.button.setCurrentText(self._config["penalty"])
        self.penalty.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.penalty)

        self.alpha = HTransparentDoubleSpinBox(minimum=0, maximum=10, singleStep=0.0001, label="regularization strength")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

        self.fit_intercept = HToggle(label="intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.max_iter = HTransparentSpinBox(minimum=1,maximum=10000,singleStep=1000,label="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.tol = HTransparentDoubleSpinBox(minimum=1e-4,maximum=1e-2,singleStep=1e-3,label="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.shuffle = HToggle(label="shuffle")
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.shuffle.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shuffle)

        self.learning_rate = HTransparentComboBox(items=["constant","optimal","invscaling","adaptive"], 
                                      label="learning rate")
        self.learning_rate.button.setCurrentText(self._config["learning_rate"])
        self.learning_rate.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.eta0 = HTransparentDoubleSpinBox(minimum=0,maximum=10000,singleStep=1,label="initial learning rate")
        self.eta0.button.setValue(self._config["eta0"])
        self.eta0.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.eta0)

        self.power_t = HTransparentDoubleSpinBox(minimum=-10000,maximum=10000,singleStep=1,label="exponent for learning rate")
        self.power_t.button.setValue(self._config["power_t"])
        self.power_t.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.power_t)

        self.early_stopping = HToggle(label="early stopping")
        self.early_stopping.button.setChecked(self._config["early_stopping"])
        self.early_stopping.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.early_stopping)

        self.n_iter_no_change = HTransparentSpinBox(minimum=1, maximum=10000, singleStep=1, label="iters before stopping fitting")
        self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.average = HToggle(label="average SGD weights")
        self.average.button.setChecked(self._config["average"])
        self.average.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.average)
    
    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText()
        self._config["penalty"] = self.penalty.button.currentText()
        self._config["alpha"] = self.alpha.button.value()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["tol"] = self.tol.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self._config["learning_rate"] = self.learning_rate.button.currentText()
        self._config["eta0"] = self.eta0.button.value()
        self._config["power_t"] = self.power_t.button.value()
        self._config["early_stopping"] = self.early_stopping.button.isChecked()
        self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["average"] = self.average.button.isChecked()
        self.estimator = linear_model.SGDClassifier(**self._config)
