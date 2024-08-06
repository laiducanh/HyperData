from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from typing import Union
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import linear_model, svm, neighbors
from sklearn.base import ClassifierMixin
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import DropDownPushButton, Toggle, ComboBox
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.menu import Menu
from node_editor.node.train_test_split import TrainTestSplitter
from config.settings import logger
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

class ClassifierBase (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.vlayout)
        self._config = dict()
        self.estimator = None # ClassifierMixin
        
    def clear_layout (self):
        for widget in self.findChildren(QWidget):
            self.vlayout.removeWidget(widget)

class AlgorithmMenu(Menu):
    sig = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        linear_model = Menu("Linear Model", self)
        for i in ["Ridge Classifier","Logistic Regression","SGD Classifier",
                  "Passive Aggressive Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type))
            linear_model.addAction(action)
        self.addMenu(linear_model)
        
        svm = Menu("Support Vector Machines", self)
        for i in ["SVC", "NuSVC","Linear SVC"]:
            action = QAction(i, self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors Classifier","Nearest Centroid", "Radius Neighbors Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        ensembles = Menu("Ensembles", self)
        for i in ["Gradient Boosting Classifier","Histogram Gradient Boosting Classifier",
                  "Random Forest Classifier","Extra Trees Classifier","Bagging Classifier",
                  "Voting Classifier","Stacking Classifier","AdaBoost Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type))
            ensembles.addAction(action)
        self.addMenu(ensembles)

        others = Menu("Others", self)
        for i in ["Decision Tree Classifier", "Gaussian Process Classifier"]:
            action = QAction(i, self)
            action.triggered.connect(lambda checked, type=i: self.sig.emit(type))
            others.addAction(action)
        self.addMenu(others)


class RidgeClassifier(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(alpha=1.0,fit_intercept=True,
                                               tol=1e-4,solver="auto",positive=False)
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
        self.solver.button.setCurrentText(self._config["solver"].title())
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
        self._config["solver"] = self.solver.button.currentText().lower()
        self._config["positive"] = self.positive.button.isChecked()
        self.estimator = linear_model.RidgeClassifier(**self._config)

class LogisticRegression(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(penalty="l2",fit_intercept=True,max_iter=100,
                                               C=1.0,multi_class="auto",tol=1e-4,solver="lbfgs")
        else: self._config = config
        self.estimator = linear_model.LogisticRegression(**self._config)
    
        self.penalty = ComboBox(items=["l1", "l2", "elasticnet", "none"], text="Penalty")
        self.penalty.button.setCurrentText(self._config["penalty"].title())
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
        self.solver.button.setCurrentText(self._config["solver"].title())
        self.solver.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.solver)
    
    def set_estimator(self):
        self._config["penalty"] = self.penalty.button.currentText().lower()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["C"] = self.C.button.value()
        self._config["multi_class"] = self.multi_class.button.currentText().lower()
        self._config["tol"] = self.tol.button.value()
        self._config["solver"] = self.solver.button.currentText().lower()
        self.estimator = linear_model.LogisticRegression(**self._config)

class SGDClassifier(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(loss="hinge",penalty="l2",alpha=0.0001,
                                               fit_intercept=True,max_iter=1000,shuffle=True,
                                               learning_rate="optimal",eta0=0,power_t=0.5,
                                               early_stopping=False,tol=1e-3,average=False,
                                               n_iter_no_change=5)
        else: self._config = config
        self.estimator = linear_model.SGDClassifier(**self._config)

        self.loss = ComboBox(items=["hinge","log_loss","modified_huber","squared_hinge",
                                    "perceptron","squared_error","huber","epsilon_insensitive",
                                    "squared_epsilon_insensitive"], text="loss function")
        self.loss.button.setCurrentText(self._config["loss"].title())
        self.loss.button.currentTextChanged.connect(self.set_estimator)

        self.penalty = ComboBox(items=["l1", "l2", "elasticnet", "none"], text="Penalty")
        self.penalty.button.setCurrentText(self._config["penalty"].title())
        self.penalty.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.penalty)

        self.alpha = DoubleSpinBox(min=0, max=10, step=0.0001, text="regularization strength")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)

        self.fit_intercept = Toggle(text="intercept")
        self.fit_intercept.button.setChecked(self._config["fit_intercept"])
        self.fit_intercept.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.fit_intercept)

        self.max_iter = SpinBox(min=1,max=10000,step=1000,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.tol = DoubleSpinBox(min=1e-4,max=1e-2,step=1e-3,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.shuffle = Toggle(text="shuffle")
        self.shuffle.button.setChecked(self._config["shuffle"])
        self.shuffle.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shuffle)

        self.learning_rate = ComboBox(items=["constant","optimal","invscaling","adaptive"], 
                                      text="learning rate")
        self.learning_rate.button.setCurrentText(self._config["learning_rate"])
        self.learning_rate.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.eta0 = DoubleSpinBox(min=0,max=10000,step=1,text="initial learning rate")
        self.eta0.button.setValue(self._config["eta0"])
        self.eta0.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.eta0)

        self.power_t = DoubleSpinBox(min=-10000,max=10000,step=1,text="exponent for learning rate")
        self.power_t.button.setValue(self._config["power_t"])
        self.power_t.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.power_t)

        self.early_stopping = Toggle(text="early stopping")
        self.early_stopping.button.setChecked(self._config["early_stopping"])
        self.early_stopping.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.early_stopping)

        self.n_iter_no_change = SpinBox(min=1, max=self.max_iter.max, step=1, text="iters before stopping fitting")
        self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.average = Toggle(text="average SGD weights")
        self.average.button.setChecked(self._config["average"])
        self.average.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.average)
    
    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText().lower()
        self._config["penalty"] = self.penalty.button.currentText().lower()
        self._config["alpha"] = self.alpha.button.value()
        self._config["fit_intercept"] = self.fit_intercept.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["tol"] = self.tol.button.value()
        self._config["shuffle"] = self.shuffle.button.isChecked()
        self._config["learning_rate"] = self.learning_rate.button.currentText().lower()
        self._config["eta0"] = self.eta0.button.value()
        self._config["power_t"] = self.power_t.button.value()
        self._config["early_stopping"] = self.early_stopping.button.isChecked()
        self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["average"] = self.average.button.isChecked()
        self.estimator = linear_model.SGDClassifier(**self._config)

class PassiveAgressiveClassifier(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(fit_intercept=True,max_iter=100,tol=1e-3,n_iter_no_change=5,
                                               shuffle=True,average=False,C=1.0,early_stopping=False)
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

class SVC(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(C=1.0, kernel="rbf", degree=3, gamma="scale", coef0=0,
                                               shrinking=True, probability=False, tol=1e-3,
                                               class_weight=None, verbose=False, max_iter=-1,
                                               decision_function_shape="ovr",break_ties=False)
        else: self._config = config
        self.estimator = svm.SVC(**self._config)

        self.C = DoubleSpinBox(min=0, max=10, step=0.1, text="Regularization parameter")
        self.C.button.setValue(self._config["C"])
        self.C.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.C)

        self.kernel = ComboBox(items=["linear","poly","rbf","sigmoid","precomputed"],text="Kernel")
        self.kernel.button.setCurrentText(self._config["kernel"])
        self.kernel.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.kernel)

        self.degree = SpinBox(min=1, max=10, text="Degree")
        self.degree.button.setValue(self._config["degree"])
        self.degree.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.degree)

        self.gamma = ComboBox(items=["scale","auto"], text="Kernel coefficient")
        self.gamma.button.currentTextChanged.connect(self.set_estimator)
        self.gamma.button.setCurrentText(self._config["gamma"])
        self.vlayout.addWidget(self.gamma)

        self.coef0 = DoubleSpinBox(text="Independent term")
        self.coef0.button.setValue(self._config["coef0"])
        self.coef0.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.coef0)

        self.shrinking = Toggle(text="Shrinking")
        self.shrinking.button.setChecked(self._config["shrinking"])
        self.shrinking.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shrinking)

        self.probability = Toggle(text="Probability")
        self.probability.button.setChecked(self._config["probability"])
        self.probability.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.probability)

        self.tol = DoubleSpinBox(min=1e-4,max=1e-2,step=1e-3,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.class_weight = ComboBox(items=["balanced", "None"])
        self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.verbose = Toggle(text="Verbose")
        self.verbose.button.setChecked(self._config["verbose"])
        self.verbose.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.verbose)

        self.max_iter = DoubleSpinBox(min=-1,max=10000,step=100,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.decision_function_shape = ComboBox(items=["ovo","ovr"])
        self.decision_function_shape.button.setCurrentText(self._config["decision_function_shape"])
        self.decision_function_shape.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.decision_function_shape)

        self.break_ties = Toggle(text="Break ties")
        self.break_ties.button.setChecked(self._config["break_ties"])
        self.break_ties.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.break_ties)
        
    def set_estimator(self):
        self._config["C"] = self.C.button.value()
        self._config["kernel"] = self.kernel.button.currentText()
        self._config["degree"] = self.degree.button.value()
        self._config["gamma"] = self.gamma.button.currentText()
        self._config["coef0"] = self.coef0.button.value()
        self._config["shrinking"] = self.shrinking.button.isChecked()
        self._config["probability"] = self.probability.button.isChecked()
        self._config["tol"] = self.tol.button.value()
        self._config["class_weight"] = None if self.class_weight.button.currentText()=="None" else self.class_weight.button.currentText()
        self._config["verbose"] = self.verbose.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["decision_function_shape"] = self.decision_function_shape.button.currentText()
        self._config["break_ties"] = self.break_ties.button.isChecked()

        self.estimator = svm.SVC(**self._config)

class NuSVC(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(nu=0.5, kernel="rbf", degree=3, gamma="scale", coef0=0,
                                               shrinking=True, probability=False, tol=1e-3,
                                               class_weight=None, verbose=False, max_iter=-1,
                                               decision_function_shape="ovr",break_ties=False)
        else: self._config = config
        self.estimator = svm.NuSVC(**self._config)

        self.nu = DoubleSpinBox(min=0, max=10, step=0.1, text="Nu")
        self.nu.button.setValue(self._config["nu"])
        self.nu.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.nu)

        self.kernel = ComboBox(items=["linear","poly","rbf","sigmoid","precomputed"],text="Kernel")
        self.kernel.button.setCurrentText(self._config["kernel"])
        self.kernel.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.kernel)

        self.degree = SpinBox(min=1, max=10, text="Degree")
        self.degree.button.setValue(self._config["degree"])
        self.degree.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.degree)

        self.gamma = ComboBox(items=["scale","auto"], text="Kernel coefficient")
        self.gamma.button.setCurrentText(self._config["gamma"])
        self.gamma.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.gamma)

        self.coef0 = DoubleSpinBox(text="Independent term")
        self.coef0.button.setValue(self._config["coef0"])
        self.coef0.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.coef0)

        self.shrinking = Toggle(text="Shrinking")
        self.shrinking.button.setChecked(self._config["shrinking"])
        self.shrinking.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.shrinking)

        self.probability = Toggle(text="Probability")
        self.probability.button.setChecked(self._config["probability"])
        self.probability.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.probability)

        self.tol = DoubleSpinBox(min=1e-4,max=1e-2,step=1e-3,text="tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.class_weight = ComboBox(items=["balanced", "None"])
        self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.verbose = Toggle(text="Verbose")
        self.verbose.button.setChecked(self._config["verbose"])
        self.verbose.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.verbose)

        self.max_iter = SpinBox(min=-1,max=10000,step=100,text="maximum iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.decision_function_shape = ComboBox(items=["ovo","ovr"])
        self.decision_function_shape.button.setCurrentText(self._config["decision_function_shape"])
        self.decision_function_shape.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.decision_function_shape)

        self.break_ties = Toggle(text="Break ties")
        self.break_ties.button.setChecked(self._config["break_ties"])
        self.break_ties.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.break_ties)
        
        
    def set_estimator(self):
        self._config["nu"] = self.nu.button.value()
        self._config["kernel"] = self.kernel.button.currentText()
        self._config["degree"] = self.degree.button.value()
        self._config["gamma"] = self.gamma.button.currentText()
        self._config["coef0"] = self.coef0.button.value()
        self._config["shrinking"] = self.shrinking.button.isChecked()
        self._config["probability"] = self.probability.button.isChecked()
        self._config["tol"] = self.tol.button.value()
        self._config["class_weight"] = None if self.class_weight.button.currentText()=="None" else self.class_weight.button.currentText()
        self._config["verbose"] = self.verbose.button.isChecked()
        self._config["max_iter"] = self.max_iter.button.value()
        self._config["decision_function_shape"] = self.decision_function_shape.button.currentText()
        self._config["break_ties"] = self.break_ties.button.isChecked()

        self.estimator = svm.NuSVC(**self._config)

class Linear_SVC (ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(penalty="l2", loss="squared_hinge", dual="auto", 
                                               tol=1e-4, C=1.0, multi_class="ovr", fit_intercept=True,
                                               intercept_scaling=1.0, class_weight=None, 
                                               verbose=0, max_iter=1000)
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

class KNeighbors (ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(n_neighbors=5, weights="uniform",algorithm="auto",
                                               leaf_size=30, p=2)
        else: self._config = config
        self.estimator = neighbors.KNeighborsClassifier(**self._config)

        self.n_neighbors = SpinBox(text="Number of neighbors")
        self.n_neighbors.button.setValue(self._config["n_neighbors"])
        self.n_neighbors.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_neighbors)

        self.weights = ComboBox(items=["uniform","distance"], text="Weight function")
        self.weights.button.setCurrentText(self._config["weights"])
        self.weights.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.weights)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf Size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = DoubleSpinBox(max=10, text="Power parameter")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)
        
    def set_estimator(self):
        self._config["n_neighbors"] = self.n_neighbors.button.value()
        self._config["weights"] = self.weights.button.currentText()
        self._config["algorithm"] = self.algorithm.button.currentText()
        self._config["leaf_size"] = self.leaf_size.button.value()
        self._config["p"] = self.p.button.value()
        
        self.estimator = neighbors.KNeighborsClassifier(**self._config)

class NearestCentroid(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(metric="euclidean")
        else: self._config = config
        self.estimator = neighbors.NearestCentroid(**self._config)

        self.metric_ = ComboBox(items=["euclidean","manhattan"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
        
    def set_estimator(self):
        self._config["metric"] = self.metric_.button.currentText()
        
        self.estimator = neighbors.NearestCentroid(**self._config)

class RadiusNeighbors(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(radius=1.0, weights="uniform", algorithm="auto",leaf_size=30,
                                               p=2, outlier_label=None)
        else: self._config = config
        self.estimator = neighbors.RadiusNeighborsClassifier(**self._config)

        self.radius = DoubleSpinBox(text="Range of parameter space")
        self.radius.button.setValue(self._config["radius"])
        self.radius.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.radius)

        self.weights = ComboBox(items=["uniform","distance"], text="Weight Function")
        self.weights.button.setCurrentText(self._config["weights"])
        self.weights.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.weights)

        self.algorithm = ComboBox(items=["auto","ball_tree","kd_tree","brute"], text="Algorithm")
        self.algorithm.button.setCurrentText(self._config["algorithm"])
        self.algorithm.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.algorithm)

        self.leaf_size = SpinBox(text="Leaf size")
        self.leaf_size.button.setValue(self._config["leaf_size"])
        self.leaf_size.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.leaf_size)

        self.p = DoubleSpinBox(text="Power parameter")
        self.p.button.setValue(self._config["p"])
        self.p.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.p)

        self.outlier_label = ComboBox(items=["manual label","most_frequent","None"], text="Label for outliers")
        self.outlier_label.button.setCurrentText(self._config["outlier_label"])
        self.outlier_label.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.outlier_label)
        
    def set_estimator(self):
        self._config["radius"] = self.radius.button.value()
        self._config["weights"] = self.weights.button.currentText()
        self._config["algorithm"] = self.algorithm.button.currentText()
        self._config["leaf_size"] = self.leaf_size.button.value()
        self._config["p"] = self.p.button.value()
        self._config["outlier_label"] = self.outlier_label.button.currentText()
 
        self.estimator = neighbors.RadiusNeighborsClassifier(**self._config)


class Classifier (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Data out")
        
        self._config = dict(estimator="Logistic Regression",config=None)
        self.estimator_list = ["Ridge Classifier","Logistic Regression","SGD Classifier",
                               "Passive Aggressive Classifier", "SVC", "NuSVC", "Linear SVC",
                               "K Neighbors Classifier","Nearest Centroid", "Radius Neighbors Classifier",
                               ]

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"].title())
        algorithm.button.setMenu(menu)
        algorithm.button.released.connect(lambda: menu.exec(QCursor().pos()))
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(stackedlayout)
        stackedlayout.addWidget(RidgeClassifier())
        stackedlayout.addWidget(LogisticRegression())
        stackedlayout.addWidget(SGDClassifier())
        stackedlayout.addWidget(PassiveAgressiveClassifier())
        stackedlayout.addWidget(SVC())
        stackedlayout.addWidget(NuSVC())
        stackedlayout.addWidget(Linear_SVC())
        stackedlayout.addWidget(KNeighbors())
        stackedlayout.addWidget(NearestCentroid())
        stackedlayout.addWidget(RadiusNeighbors())
        stackedlayout.setCurrentIndex(self.estimator_list.index(algorithm.button.text()))
        stackedlayout.currentWidget().set_config(self._config["config"])
 
        if dialog.exec():
            self.estimator = stackedlayout.currentWidget().estimator
            self.estimator: ClassifierMixin
            self._config["estimator"] = algorithm.button.text()
            self._config["config"] = stackedlayout.currentWidget()._config
            self.exec()


    def func(self):
        self.eval()
        self.node.output_sockets[0].socket_data = self.estimator

        try:
            if len(self.node.input_sockets[0].edges) == 1:
                if isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                    cv = self.node.input_sockets[0].socket_data[0]
                    X = self.node.input_sockets[0].socket_data[1]
                    Y = self.node.input_sockets[0].socket_data[2]
                        
                    self.data_to_view = pd.concat([X,Y],axis=1)

                    for fold, (train_idx, test_idx) in enumerate(cv):
                        X_train, X_test = X.loc[train_idx], X.loc[test_idx]
                        Y_train, Y_test = Y.loc[train_idx], Y.loc[test_idx]
                        self.estimator.fit(X_train, Y_train)
                        Y_pred = self.estimator.predict(X).round(5)
                        #score = mean_absolute_error(Y, Y_pred)
                    
                        self.data_to_view = pd.concat([self.data_to_view, pd.DataFrame(Y_pred, columns=[f"Fold{fold+1}_Prediction"])],axis=1)
                    
                    self.node.output_sockets[1].socket_data = None
                    logger.info(f"{self.name} run successfully.")

            else:
                logger.warning(f"{self.name} Did not define splitter.")
        
        except Exception as e:
            logger.error(f"{self.name} {repr(e)}.")
        
        

        super().exec()
     
    def eval (self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None

        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
