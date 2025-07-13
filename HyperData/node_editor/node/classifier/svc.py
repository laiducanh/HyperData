from ui.base_widgets.button import HToggle, HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from node_editor.node.classifier.base import ClassifierBase
from config.settings import logger, GLOBAL_DEBUG
from sklearn import svm

DEBUG = False

class SVC(ClassifierBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            C=1.0, 
            kernel="rbf", 
            degree=3, 
            gamma="scale", 
            coef0=0,
            shrinking=True, 
            probability=False, 
            tol=1e-3,
            class_weight=None, 
            verbose=False, 
            max_iter=-1,
            decision_function_shape="ovr",
            break_ties=False
        )
        else: self._config = config
        self.estimator = svm.SVC(**self._config)

        self.C = HTransparentDoubleSpinBox(minimum=0, maximum=10, singleStep=0.1, label="Regularization parameter")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.kernel = HTransparentComboBox(items=["linear","poly","rbf","sigmoid","precomputed"],label="Kernel")
        self.kernel.button.setCurrentText(self._config["kernel"])
        self.kernel.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.kernel)

        self.degree = HTransparentSpinBox(minimum=1, maximum=10, label="Degree")
        self.degree.button.setValue(self._config["degree"])
        self.degree.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.degree)

        self.gamma = HTransparentComboBox(items=["scale","auto"], label="Kernel coefficient")
        self.gamma.button.currentTextChanged.connect(self.set_estimator)
        self.gamma.button.setCurrentText(self._config["gamma"])
        self.vlayout.addWidget(self.gamma)

        self.coef0 = HTransparentDoubleSpinBox(label="Independent term")
        self.coef0.button.setValue(self._config["coef0"])
        self.coef0.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.coef0)

        self.shrinking = HToggle(label="Shrinking")
        self.shrinking.button.setChecked(self._config["shrinking"])
        self.shrinking.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shrinking)

        self.probability = HToggle(label="Probability")
        self.probability.button.setChecked(self._config["probability"])
        self.probability.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.probability)

        self.tol = HTransparentDoubleSpinBox(minimum=1e-4,maximum=1e-2,singleStep=1e-3,label="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.class_weight = HTransparentComboBox(items=["balanced", "None"])
        self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.verbose = HToggle(label="Verbose")
        self.verbose.button.setChecked(self._config["verbose"])
        self.verbose.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.verbose)

        self.max_iter = HTransparentDoubleSpinBox(minimum=-1,maximum=10000,singleStep=100,label="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.decision_function_shape = HTransparentComboBox(items=["ovo","ovr"])
        self.decision_function_shape.button.setCurrentText(self._config["decision_function_shape"])
        self.decision_function_shape.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.decision_function_shape)

        self.break_ties = HToggle(label="Break ties")
        self.break_ties.button.setChecked(self._config["break_ties"])
        self.break_ties.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.break_ties)
        
    def set_estimator(self):
        self._config.update(
            C=self.C.button.value(),
            kernel=self.kernel.button.currentText(), 
            degree=self.degree.button.value(), 
            gamma=self.gamma.button.currentText(), 
            coef0=self.coef0.button.value(),
            shrinking=self.shrinking.button.isChecked(), 
            probability=self.probability.button.isChecked(), 
            tol=self.tol.button.value(),
            class_weight=None if self.class_weight.button.currentText()=="None" else self.class_weight.button.currentText(), 
            verbose=self.verbose.button.isChecked(), 
            max_iter=self.max_iter.button.value(),
            decision_function_shape=self.decision_function_shape.button.currentText(),
            break_ties=self.break_ties.button.isChecked()
        )
        self.estimator = svm.SVC(**self._config)