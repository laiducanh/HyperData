from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import linear_model

DEBUG = False

class RidgeClassifier(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            alpha=1.0,
            fit_intercept=True,
            tol=1e-4,
            solver="auto",
            positive=False
        )
        else: self._config = config
        self.estimator = linear_model.RidgeClassifier(**self._config)
        
        self.alpha = DoubleSpinBox(min=0, max=1000, step=1, text="regularization strength")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)
        
        self.fit_intercept = Toggle(text="intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.tol = DoubleSpinBox(min=1e-8,max=1e-3,step=1e-6,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.solver = ComboBox(items=["auto","svd","cholesky","lsqr","sparse_cg","sag","saga","lbfgs"],
                               text="solver")
        self.solver.button.setCurrentText(self._config["solver"])
        self.solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.solver)

        self.positive = Toggle(text="positive coefficients")
        self.positive.button.setChecked(self._config["positive"])
        self.positive.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.positive)
    
    def set_estimator(self):
        self._config["alpha"] = self.alpha.button.value()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["tol"] = self.tol.button.value()
        self._config["solver"] = self.solver.button.currentText()
        self._config["positive"] = self.positive.button.isChecked()
        self.estimator = linear_model.RidgeClassifier(**self._config)