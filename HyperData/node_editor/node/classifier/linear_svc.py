from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import svm

DEBUG = False

class Linear_SVC (ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            penalty="l2", 
            loss="squared_hinge", 
            dual="auto", 
            tol=1e-4, 
            C=1.0, 
            multi_class="ovr", 
            fit_intercept=True,
            intercept_scaling=1.0, 
            class_weight=None, 
            verbose=0, 
            max_iter=1000
        )
        else: self._config = config
        self.estimator = svm.LinearSVC(**self._config)

        self.penalty = ComboBox(items=["l1","l2"], text="Penalization")
        self.penalty.button.setCurrentText(self._config["penalty"])
        self.penalty.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.penalty)

        self.loss = ComboBox(items=["hinge","squared_hinged"], text="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.dual = ComboBox(items=["auto","True","False"], text="Optimization problem")
        self.dual.button.setCurrentText(self._config["dual"])
        self.dual.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.dual)

        self.tol = DoubleSpinBox(min=1e-5,max=1e-2,step=1e-5,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.C = DoubleSpinBox(min=0, max=10, step=0.1, text="Regularization parameter")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.multi_class = ComboBox(items=["ovr","crammer_singer"], text="Multi-class")
        self.multi_class.button.setCurrentText(self._config["multi_class"])
        self.multi_class.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.multi_class)

        self.fit_intercept = Toggle(text="Fit intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.intercept_scaling = DoubleSpinBox(min=1, max=10, step=1, text="Intercept scaling")
        self.intercept_scaling.button.setValue(self._config["intercept_scaling"])
        self.intercept_scaling.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.intercept_scaling)

        self.class_weight = ComboBox(items=["balanced", "None"])
        self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.verbose = SpinBox(text="Verbose")
        self.verbose.button.setValue(self._config["verbose"])
        self.verbose.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.verbose)

        self.max_iter = DoubleSpinBox(min=1000,max=50000,step=1000,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        
    def set_estimator(self):
        self._config["penalty"] = self.penalty.button.currentText()
        self._config["loss"] = self.loss.button.currentText()
        if self.dual.button.currentText() == "True":
            self._config["dual"] = True
        elif self.dual.button.currentText() == "False":
            self._config["dual"] = False
        else: 
            self._config["dual"] = "auto"
        self._config["tol"] = self.tol.button.value()
        self._config["C"] = self.C.button.value()
        self._config["multi_class"] = self.multi_class.button.currentText()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["intercept_scaling"] = self.intercept_scaling.button.value()
        self._config["class_weight"] = None if self.class_weight.button.currentText()=="None" else self.class_weight.button.currentText()
        self._config["verbose"] = self.verbose.button.value()
        self._config["max_iter"] = self.max_iter.button.value()
        
        self.estimator = svm.LinearSVC(**self._config)