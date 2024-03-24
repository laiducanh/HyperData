from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
from typing import Union
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import linear_model
from sklearn.base import ClassifierMixin
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import DropDownPushButton, Toggle, ComboBox
from ui.base_widgets.text import LineEdit, EditableComboBox, Completer
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.menu import Menu
from node_editor.node.train_test_split import TrainTestSplitter
from config.settings import logger
from PyQt6.QtWidgets import QFileDialog, QDialog, QWidget, QVBoxLayout, QStackedLayout
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
        for i in ["SVC", "NuSCV","Linear SVC"]:
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

class Classifier (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Data out")
        
        self._config = dict(estimator="Logistic Regression",config=None)
        self.estimator_list = ["Ridge Classifier","Logistic Regression","SGD Classifier",
                               "Passive Aggressive Classifier"]

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        dialog.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMaximumSize)
        dialog.widget.setMinimumWidth(400)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"].title())
        algorithm.button.setMenu(menu)
        algorithm.button.released.connect(lambda: menu.exec(QCursor().pos()))
        dialog.textLayout.addWidget(algorithm)
        dialog.textLayout.addWidget(SeparateHLine())
        stackedlayout = QStackedLayout()
        dialog.textLayout.addLayout(stackedlayout)
        stackedlayout.addWidget(RidgeClassifier())
        stackedlayout.addWidget(LogisticRegression())
        stackedlayout.addWidget(SGDClassifier())
        stackedlayout.addWidget(PassiveAgressiveClassifier())
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
