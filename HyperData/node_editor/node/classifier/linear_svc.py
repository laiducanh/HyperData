from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
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

        self.penalty = HTransparentComboBox(items=["l1","l2"], label="Penalization")
        self.penalty.button.setCurrentText(self._config["penalty"])
        self.penalty.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.penalty)

        self.loss = HTransparentComboBox(items=["hinge","squared_hinged"], label="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.dual = HTransparentComboBox(items=["auto","True","False"], label="Optimization problem")
        self.dual.button.setCurrentText(self._config["dual"])
        self.dual.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.dual)

        self.tol = HTransparentDoubleSpinBox(minimum=1e-5,maximum=1e-2,singleStep=1e-5,label="Tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.C = HTransparentDoubleSpinBox(minimum=0, maximum=10, singleStep=0.1, label="Regularization parameter")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.multi_class = HTransparentComboBox(items=["ovr","crammer_singer"], label="Multi-class")
        self.multi_class.button.setCurrentText(self._config["multi_class"])
        self.multi_class.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.multi_class)

        self.fit_intercept = HToggle(label="Fit intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.intercept_scaling = HTransparentDoubleSpinBox(minimum=1, maximum=10, singleStep=1, label="Intercept scaling")
        self.intercept_scaling.button.setValue(self._config["intercept_scaling"])
        self.intercept_scaling.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.intercept_scaling)

        self.class_weight = HTransparentComboBox(items=["balanced", "None"])
        self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.verbose = HTransparentSpinBox(label="Verbose")
        self.verbose.button.setValue(self._config["verbose"])
        self.verbose.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.verbose)

        self.max_iter = HTransparentDoubleSpinBox(minimum=1000,maximum=50000,singleStep=1000,label="maximum iterations")
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