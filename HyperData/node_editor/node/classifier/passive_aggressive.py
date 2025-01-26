from ui.base_widgets.button import Toggle
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import linear_model

DEBUG = False

class PassiveAggressiveClassifier(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            fit_intercept=True,
            max_iter=100,
            tol=1e-3,
            n_iter_no_change=5,
            shuffle=True,
            average=False,
            C=1.0,
            early_stopping=False
        )
        else: self._config = config
        self.estimator = linear_model.PassiveAggressiveClassifier(**self._config)

        self.C = DoubleSpinBox(min=0, max=10, step=0.1, text="maximum step size")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.fit_intercept = Toggle(text="intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.max_iter = SpinBox(min=1,max=10000,step=100,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.tol = DoubleSpinBox(min=1e-4,max=1e-2,step=1e-3,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.early_stopping = Toggle(text="early stopping")
        self.early_stopping.button.setChecked(self._config["early_stopping"])
        self.early_stopping.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.early_stopping)

        self.n_iter_no_change = SpinBox(min=1, max=self.max_iter.max, step=1, text="iters before stopping fitting")
        self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.shuffle = Toggle(text="shuffle")
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.shuffle.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shuffle)

        self.average = Toggle(text="average SGD weights")
        self.average.button.setChecked(self._config["average"])
        self.average.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.average)
    
    def set_estimator(self):
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["C"] = self.C.button.value()
        self._config["tol"] = self.tol.button.value()
        self._config["early_stopping"] = self.early_stopping.button.isChecked()
        self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self._config["average"] = self.average.button.isChecked()
        self.estimator = linear_model.PassiveAggressiveClassifier(**self._config)