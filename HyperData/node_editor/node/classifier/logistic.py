from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import linear_model

DEBUG = False

class LogisticRegression(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            penalty="l2",
            fit_intercept=True,
            max_iter=100,
            C=1.0,
            multi_class="auto",
            tol=1e-4,
            solver="lbfgs"
        )
        else: self._config = config
        self.estimator = linear_model.LogisticRegression(**self._config)
    
        self.penalty = ComboBox(items=["l1", "l2", "elasticnet", "none"], text="Penalty")
        self.penalty.button.setCurrentText(self._config["penalty"])
        self.penalty.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.penalty)

        self.fit_intercept = Toggle(text="intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.max_iter = SpinBox(min=1,max=10000,step=100,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.C = DoubleSpinBox(min=0, max=10, step=0.1, text="inverse of regularization strength")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.multi_class = ComboBox(items=["auto","ovr","multinomial"], text="Multiple classes")
        self.multi_class.button.setCurrentText(self._config["multi_class"])
        self.multi_class.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.multi_class)

        self.tol = DoubleSpinBox(min=1e-8,max=1e-3,step=1e-6,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.solver = ComboBox(items=["lbfgs","liblinear","newton-cg","newton-cholesky","sag","saga"],
                               text="solver")
        self.solver.button.setCurrentText(self._config["solver"])
        self.solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.solver)
    
    def set_estimator(self):
        self._config["penalty"] = self.penalty.button.currentText()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["C"] = self.C.button.value()
        self._config["multi_class"] = self.multi_class.button.currentText()
        self._config["tol"] = self.tol.button.value()
        self._config["solver"] = self.solver.button.currentText()
        self.estimator = linear_model.LogisticRegression(**self._config)