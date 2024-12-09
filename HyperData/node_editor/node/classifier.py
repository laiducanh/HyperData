from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from typing import Union
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import linear_model, svm, neighbors, ensemble, tree, gaussian_process
from sklearn.preprocessing import LabelBinarizer
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.base import ClassifierMixin
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,confusion_matrix,
                             top_k_accuracy_score,average_precision_score,roc_curve,auc,
                             precision_recall_curve,
                             brier_score_loss,f1_score,log_loss,precision_score,
                             recall_score,jaccard_score,roc_auc_score)
from sklearn.utils.multiclass import unique_labels
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (DropDownPrimaryPushButton, Toggle, ComboBox, _TransparentPushButton, 
                                    TransparentPushButton, SegmentedWidget, _PrimaryPushButton)
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.menu import Menu
from plot.canvas import Canvas
from node_editor.node.train_test_split import TrainTestSplitter
from node_editor.node.report import ConfusionMatrix, ROC
from config.settings import logger
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedLayout, QScrollArea, QHBoxLayout,
                             QApplication)
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtCore import Qt, pyqtSignal

class ClassifierBase (QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)   

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.estimator = None # ClassifierMixin
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
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
                  "Random Forest Classifier","Extra Trees Classifier"]:
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

def scoring(Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """

    if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
        return {"Accuracy":"--",
                "Balanced accuracy":"--",
                "Top K accuracy":"--",
                "Average precision":"--",
                "Brier score loss":"--",
                "F1 score":"--"}
    else:
        accuracy = np.array([])
        for ind, val in enumerate(Y):
            accuracy = np.append(accuracy, accuracy_score(Y[ind], Y_pred[ind]))

        return {"Accuracy":accuracy.mean(),
                }

class Report(Dialog):
    def __init__(self, Y, Y_pred, Y_pred_proba, parent=None):
        """ Y, Y_pred, and Y_pred_proba are nested lists """
        super().__init__(title="Scoring",parent=parent)

        self.score_function = "Accuracy"

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Confusion Matrix', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment_widget.addButton(text='ROC Curve', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment_widget.addButton(text='PR Curve', func=lambda: self.stackedlayout.setCurrentIndex(3))

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        metrics = self.metrics(Y, Y_pred)
        self.stackedlayout.addWidget(metrics)

        confusion_mat = ConfusionMatrix(Y, Y_pred)
        self.stackedlayout.addWidget(confusion_mat)

        roc = ROC(Y, Y_pred_proba)
        self.stackedlayout.addWidget(roc)

        # pr = self.precision_recall(Y, Y_pred)
        # self.stackedlayout.addWidget(pr)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")
    
    def change_metric(self, metric:str):
        self.score_function = metric

    def metrics(self, Y, Y_pred) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)

        metric_to_show = ComboBox(items=["Accuracy","Balanced accuracy","Top K accuracy",
                                         "Average precision","Brier score loss","F1 score",
                                         ], 
                                  text="Metric")
        metric_to_show.button.currentTextChanged.connect(lambda metric: self.change_metric(metric))
        layout.addWidget(metric_to_show)

        score = scoring(Y, Y_pred)
        for metric in score:
            _btn = TransparentPushButton(text=metric)
            _btn.button.setText(str(score[metric]))
            layout.addWidget(_btn)


        return widget

    def confustion_mat(self, Y, Y_pred) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)

        fold = 0

        _fold = ComboBox(items=[f"Fold {i+1}" for i in range(len(Y))],
                        text="Fold")
        _fold.button.setCurrentText(f"Fold {fold+1}")
        layout.addWidget(_fold)

        # Compute confusion matrix
        if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
            cm = np.array([[1,0],[0,1]])
        else: 
            cm = confusion_matrix(Y[fold], Y_pred[fold])
        
        canvas = Canvas()
        canvas.fig.set_edgecolor("black")
        canvas.fig.set_linewidth(2)
        for _ax in canvas.fig.axes: _ax.remove()
        ax = canvas.fig.add_subplot()
        im = ax.imshow(cm, cmap="Greens", aspect='auto')
        ax.figure.colorbar(im, ax=ax)

        # show appropriate ticks
        ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           title="Confusion matrix",
           ylabel='True label',
           xlabel='Predicted label')
        # Rotate the tick labels and set their alignment.
        ax.set_xticklabels(ax.get_xticks(), 
                           rotation=45, 
                           ha="right", 
                           rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations.
        fmt = 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        canvas.fig.set_tight_layout("rect")
        canvas.draw()
        layout.addWidget(canvas)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_layout.addWidget(BodyLabel("Confusion Matrix"))
        btn_layout.addWidget(BodyLabel(str(cm)))
        
        copy_btn = _PrimaryPushButton()
        copy_btn.setText("Copy to clipboard")
        copy_btn.released.connect(lambda: self.clipboard.setText(str(cm)))
        btn_layout.addWidget(copy_btn)

        return widget
        
    def roc(self, Y, Y_pred_proba) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)

        # calculate ROC metrics
        if len(Y) == 0 or len(Y_pred_proba) == 0: # check if Y or Y_pred is an empty list
            fpr, tpr = [0,0,1], [0,1,1]
            roc_auc = 1
        else:
            fpr, tpr, _ = roc_curve(Y, Y_pred_proba) 
            roc_auc = auc(fpr, tpr)

        canvas = Canvas()
        for _ax in canvas.fig.axes: _ax.remove()
        ax = canvas.fig.add_subplot()
        canvas.fig.set_edgecolor("black")
        canvas.fig.set_linewidth(2)
        ax.plot(fpr, tpr, marker='o', 
                label=f"ROC curve (area = {roc_auc:.2f})")
        ax.plot([0,1],[0,1],"k--",label="Random")
        ax.set_xlim([-0.05, 1.05])
        ax.set_ylim([-0.05, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curve')
        ax.legend()

        canvas.fig.set_tight_layout("rect")
        canvas.draw()
        layout.addWidget(canvas)

        btn_layout1 = QHBoxLayout()
        layout.addLayout(btn_layout1)

        btn_layout1.addWidget(BodyLabel("False Positive Rate (X Axis)"))
        btn_layout1.addWidget(BodyLabel(str(fpr)))
        
        copy_btn1 = _PrimaryPushButton()
        copy_btn1.setText("Copy to clipboard")
        copy_btn1.released.connect(lambda: self.clipboard.setText(str(fpr)))
        btn_layout1.addWidget(copy_btn1)

        btn_layout2 = QHBoxLayout()
        layout.addLayout(btn_layout2)

        btn_layout2.addWidget(BodyLabel("True Positive Rate (Y Axis)"))
        btn_layout2.addWidget(BodyLabel(str(tpr)))
        
        copy_btn2 = _PrimaryPushButton()
        copy_btn2.setText("Copy to clipboard")
        copy_btn2.released.connect(lambda: self.clipboard.setText(str(tpr)))
        btn_layout2.addWidget(copy_btn2)


        return widget

    def precision_recall(self, Y, Y_pred) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)

        # Calculate precision and recall
        if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
            precision, recall = [0,0,1], [0,1,1]
            pr_auc = 1
        else:
            precision, recall, _ = precision_recall_curve(Y, Y_pred)
            pr_auc = auc(recall, precision)

        canvas = Canvas()
        for _ax in canvas.fig.axes: _ax.remove()
        ax = canvas.fig.add_subplot()
        ax.plot(recall, precision, label=f"Precision-Recall curve (area = {pr_auc:.2f})")
        ax.set(xlabel="Recall",ylabel="Precision",
               title="Precision-Recall Curve")
        ax.legend()

        canvas.fig.set_tight_layout("rect")
        canvas.draw()
        layout.addWidget(canvas)

        btn_layout1 = QHBoxLayout()
        layout.addLayout(btn_layout1)

        btn_layout1.addWidget(BodyLabel("Recall (X Axis)"))
        btn_layout1.addWidget(BodyLabel(str(recall)))
        
        copy_btn1 = _PrimaryPushButton()
        copy_btn1.setText("Copy to clipboard")
        copy_btn1.released.connect(lambda: self.clipboard.setText(str(recall)))
        btn_layout1.addWidget(copy_btn1)

        btn_layout2 = QHBoxLayout()
        layout.addLayout(btn_layout2)

        btn_layout2.addWidget(BodyLabel("Precision (Y Axis)"))
        btn_layout2.addWidget(BodyLabel(str(precision)))
        
        copy_btn2 = _PrimaryPushButton()
        copy_btn2.setText("Copy to clipboard")
        copy_btn2.released.connect(lambda: self.clipboard.setText(str(precision)))
        btn_layout2.addWidget(copy_btn2)

        return widget
    
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

class GradientBoosting(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(loss="log_loss",learning_rate=0.1,
                                               n_estimators=100,subsample=1.0,criterion="friedman_mse",
                                               min_samples_split=2,min_samples_leaf=1,min_weight_fraction_leaf=0,
                                               max_depth=3,min_impurity_decrease=0,init=None,max_features=None,
                                               verbose=0,max_leaf_nodes=None,warm_start=False,validation_fraction=0.1,
                                               n_iter_no_change=None,tol=1e-4,ccp_alpha=0)
        else: self._config = config
        self.estimator = ensemble.GradientBoostingClassifier(**self._config)

        self.loss = ComboBox(items=["log_loss","exponential"], text="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.learning_rate = DoubleSpinBox(step=0.5, text="Learning Rate")
        self.learning_rate.button.setValue(self._config["learning_rate"])
        self.learning_rate.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.n_estimators = SpinBox(min=1, max=10000, step=100, text="Number of Boosting Stages")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.subsample = DoubleSpinBox(min=0.01, max=1, step=0.05, text="Fraction of samples")
        self.subsample.button.setValue(self._config["subsample"])
        self.subsample.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.subsample)

        self.criterion = ComboBox(items=["friedman_mse","squared_error"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.min_samples_split = SpinBox(min=2, max=1000, step=10, text="Minimum Number of Samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = SpinBox(min=1, max=1000, step=10, text="Minimum Number of Samples to A Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(max=0.5, step=0.05, text="Minimum Weighted Fraction to A Leaf")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_depth = SpinBox(min=1, max=1000, text="Maximum Depth of Estimators")
        self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity Decrease to Split ")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.max_features = ComboBox(items=["sqrt","log2","max"], text="Number of Features")
        if self._config["max_features"] == None:
            self.max_features.button.setCurrentText("max")
        else: self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum Number of Leafs in A Node")
        self.max_leaf_nodes.button.setDecimals(0)
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.validation_fraction = DoubleSpinBox(min=0.01, max=0.99, step=0.05, text="Validation Fraction")
        self.validation_fraction.button.setValue(self._config["validation_fraction"])
        self.validation_fraction.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.validation_fraction)

        self.n_iter_no_change = SpinBox(min=-1, text="Early Stopping")
        if self._config["n_iter_no_change"] == None:
            self.n_iter_no_change.button.setValue(-1)
        else: self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.tol = DoubleSpinBox(min=1e-5,max=1e-3,step=1e-4,text="Tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.ccp_alpha = DoubleSpinBox(text="Complexity Parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)
        
    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText()
        self._config["learning_rate"] = self.learning_rate.button.value()
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["subsample"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        if self.max_features.button.currentText() == "max":
            self._config["max_features"] = None
        else: self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() < 2:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        self._config["validation_fraction"] = self.validation_fraction.button.value()
        if self.n_iter_no_change.button.value() < 1:
            self._config["n_iter_no_change"] = None
        else: self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["tol"] = self.tol.button.value()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()
 
        self.estimator = ensemble.GradientBoostingClassifier(**self._config)

class HistGradientBoosting(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(loss="log_loss",learning_rate=0.1,max_iter=100,
                                               max_leaf_nodes=31,max_depth=None,
                                               min_samples_leaf=20,l2_regularization=0,
                                               max_features=1.0,max_bins=255,monotonic_cst=None,
                                               interaction_cst=None,warm_start=False,early_stopping="auto",
                                               scoring="loss",validation_fraction=0.1,n_iter_no_change=10,
                                               tol=1e-7,verbose=0,class_weight=None)
        else: self._config = config
        self.estimator = ensemble.HistGradientBoostingClassifier(**self._config)

        self.loss = ComboBox(items=["log_loss"], text="Loss Function")
        self.loss.button.setCurrentText(self._config["loss"])
        self.loss.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.loss)

        self.learning_rate = DoubleSpinBox(max=1,step=0.05,text="Learning Rate")
        self.learning_rate.button.setValue(self._config["learning_rate"])
        self.learning_rate.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.learning_rate)

        self.max_iter = SpinBox(max=10000, step=500, text="Maximum Number of Iterations")
        self.max_iter.button.setValue(self._config["max_iter"])
        self.max_iter.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_iter)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum nmber of Leaves")
        self.max_leaf_nodes.button.setDecimals(0)
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.max_depth = DoubleSpinBox(min=-1, text="Maximum Depth")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_leaf = SpinBox(text="Minimum Number of Samples per Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.l2_regularization = DoubleSpinBox(text="L2 Regularization")
        self.l2_regularization.button.setValue(self._config["l2_regularization"])
        self.l2_regularization.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.l2_regularization)

        self.max_features = DoubleSpinBox(text="Proportion of Randomly Features")
        self.max_features.button.setValue(self._config["max_features"])
        self.max_features.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_bins = SpinBox(max=255, text="Maximum Number of Bins")
        self.max_bins.button.setValue(self._config["max_bins"])
        self.max_bins.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_bins)

        self.interaction_cst = ComboBox(items=["pairwise","no_interactions"],
                                        text="Interaction Constraints")
        self.interaction_cst.button.setCurrentText(self._config["interaction_cst"])
        self.interaction_cst.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.interaction_cst)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.early_stopping = ComboBox(items=["auto","True","False"], text="Early Stopping")
        if self._config["early_stopping"] == True:
            self.early_stopping.button.setCurrentText("True")
        elif self._config["early_stopping"] == False:
            self.early_stopping.button.setCurrentText("False")
        else: self.early_stopping.button.setCurrentText(self._config["early_stopping"])
        self.early_stopping.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.early_stopping)

        self.validation_fraction = DoubleSpinBox(text="Proportion for Validation Data")
        self.validation_fraction.button.setValue(self._config["validation_fraction"])
        self.validation_fraction.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.validation_fraction)

        self.n_iter_no_change = SpinBox(text="Criterion for Early Stop")
        self.n_iter_no_change.button.setValue(self._config["n_iter_no_change"])
        self.n_iter_no_change.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_iter_no_change)

        self.tol = DoubleSpinBox(min=1e-8,max=1e-6,step=1e-7,text="Tolerance")
        self.tol.button.setValue(self._config["tol"])
        self.tol.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.tol)

        self.class_weight = ComboBox(items=["None","balanced"],text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)
        

    def set_estimator(self):
        self._config["loss"] = self.loss.button.currentText()
        self._config["learning_rate"] = self.learning_rate.button.value()
        self._config["max_iter"] = self.max_iter.button.value()
        if self.max_leaf_nodes.button.value() < 1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["l2_regularization"] = self.l2_regularization.button.value()
        self._config["max_features"] = self.max_features.button.value()
        self._config["max_bins"] = self.max_bins.button.value()
        self._config["interaction_cst"] = self.interaction_cst.button.currentText()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        if self.early_stopping.button.currentText() == "True":
            self._config["early_stopping"] = True
        elif self.early_stopping.button.currentText() == "False":
            self._config["early_stopping"] = False
        else: self._config["early_stopping"] = self.early_stopping.button.currentText()
        self._config["validation_fraction"] = self.validation_fraction.button.value()
        self._config["n_iter_no_change"] = self.n_iter_no_change.button.value()
        self._config["tol"] = self.tol.button.value()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self.estimator = ensemble.HistGradientBoostingClassifier(**self._config)

class RandomForest(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(n_estimators=100,criterion="gini",max_depth=None,
                                               min_samples_split=2,min_samples_leaf=1,
                                               min_weight_fraction_leaf=0,max_features="sqrt",
                                               max_leaf_nodes=None,min_impurity_decrease=0,
                                               bootstrap=True,oob_score=False,verbose=0,warm_start=False,
                                               class_weight=None,ccp_alpha=0,max_samples=None,monotonic_cst=None)
        else: self._config = config
        self.estimator = ensemble.RandomForestClassifier(**self._config)

        self.n_estimators = SpinBox(text="Number of Trees")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.max_depth = SpinBox(text="Maximum Depth")
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_split = DoubleSpinBox(text="Minimum Number of Samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = DoubleSpinBox(text="Minimum Number of Samples of A Leaf")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(text="Minimum Weighted Fraction of A Leaf")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_features = ComboBox(items=["sqrt","log2","None"],text="Number of Features to Split")
        self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = SpinBox(text="Maximum Leafs of A Node")
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity Decrease to Split")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.bootstrap = Toggle(text="Bootstrap")
        self.bootstrap.button.setChecked(self._config["bootstrap"])
        self.bootstrap.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.bootstrap)

        self.oob_score = Toggle(text="Out-Of-Bag Score")
        self.oob_score.button.setChecked(self._config["oob_score"])
        self.oob_score.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.oob_score)

        self.warm_start = Toggle(text="Warm Start")
        self.warm_start.button.setChecked(self._config["warm_start"])
        self.warm_start.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.warm_start)

        self.class_weight = ComboBox(items=["balanced","balanced_subsample","None"],
                                     text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.ccp_alpha = DoubleSpinBox(min=0, text="Complexity Parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)

        self.max_samples = DoubleSpinBox(text="Number of Samples to Train")
        if self._config["max_samples"] == None:
            self.max_samples.button.setValue(-1)
        else: self.max_samples.button.setValue(self._config["max_samples"])
        self.max_samples.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_samples)

    def set_estimator(self):
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        eles: self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() == -1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        self._config["bootstrap"] = self.bootstrap.button.isChecked()
        self._config["oob_score"] = self.oob_score.button.isChecked()
        self._config["warm_start"] = self.warm_start.button.isChecked()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()
        if self.max_samples.button.value() == -1:
            self._config["max_samples"] = None
        else: self._config["max_samples"] = self.max_samples.button.value()
 
        self.estimator = ensemble.RandomForestClassifier(**self._config)

class ExtraTrees(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(n_estimators=100,criterion="gini",max_depth=None,
                                               min_samples_split=2,min_samples_leaf=1,min_weight_fraction_leaf=0,
                                               max_features="sqrt",max_leaf_nodes=None,min_impurity_decrease=0,
                                               bootstrap=False,oob_score=False,verbose=0,warm_start=False,
                                               class_weight=None,ccp_alpha=0,max_samples=None)
        else: self._config = config
        self.estimator = ensemble.ExtraTreesClassifier(**self._config)

        self.n_estimators = SpinBox(max=1000,step=100,text="Number of Trees")
        self.n_estimators.button.setValue(self._config["n_estimators"])
        self.n_estimators.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_estimators)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"],text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.max_depth = DoubleSpinBox(min=-1, max=1000, step=10, text="Maximum Depth of Tree")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)


        
    def set_estimator(self):
        self._config["n_estimators"] = self.n_estimators.button.value()
        self._config["criterion"] = self.criterion.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        else: self._config["max_depth"] = int(self.max_depth.button.value())
        
        self.estimator = ensemble.ExtraTreesClassifier(**self._config)

class DecisionTree(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(criterion="gini",splitter="best",max_depth=None,
                                               min_samples_split=2,min_samples_leaf=1,
                                               min_weight_fraction_leaf=0,max_features=None,
                                               max_leaf_nodes=None,min_impurity_decrease=0,
                                               class_weight=None,ccp_alpha=0,monotonic_cst=None)
        else: self._config = config
        self.estimator = tree.DecisionTreeClassifier(**self._config)

        self.criterion = ComboBox(items=["gini","entropy","log_loss"], text="Criterion")
        self.criterion.button.setCurrentText(self._config["criterion"])
        self.criterion.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.criterion)

        self.splitter = ComboBox(items=["best","random"],text="Splitter")
        self.splitter.button.setCurrentText(self._config["splitter"])
        self.splitter.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.splitter)

        self.max_depth = DoubleSpinBox(min=-1, text="Maximum Depth")
        self.max_depth.button.setDecimals(0)
        if self._config["max_depth"] == None:
            self.max_depth.button.setValue(-1)
        else: self.max_depth.button.setValue(self._config["max_depth"])
        self.max_depth.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_depth)

        self.min_samples_split = SpinBox(text="Minimum samples to Split")
        self.min_samples_split.button.setValue(self._config["min_samples_split"])
        self.min_samples_split.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_split)

        self.min_samples_leaf = SpinBox(text="Minimum samples to a Node")
        self.min_samples_leaf.button.setValue(self._config["min_samples_leaf"])
        self.min_samples_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_samples_leaf)

        self.min_weight_fraction_leaf = DoubleSpinBox(step=0.1,max=1,
                                                      text="Minimum weighted fraction")
        self.min_weight_fraction_leaf.button.setValue(self._config["min_weight_fraction_leaf"])
        self.min_weight_fraction_leaf.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_weight_fraction_leaf)

        self.max_features = ComboBox(items=["sqrt","log2","max"], text="Max Features")
        if self._config["max_features"] == None:
            self.max_features.button.setCurrentText("max")
        else: self.max_features.button.setCurrentText(self._config["max_features"])
        self.max_features.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_features)

        self.max_leaf_nodes = DoubleSpinBox(min=-1, text="Maximum Nodes")
        if self._config["max_leaf_nodes"] == None:
            self.max_leaf_nodes.button.setValue(-1)
        else: self.max_leaf_nodes.button.setValue(self._config["max_leaf_nodes"])
        self.max_leaf_nodes.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.max_leaf_nodes)

        self.min_impurity_decrease = DoubleSpinBox(text="Impurity")
        self.min_impurity_decrease.button.setValue(self._config["min_impurity_decrease"])
        self.min_impurity_decrease.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.min_impurity_decrease)

        self.class_weight = ComboBox(items=["None","balanced"], text="Class Weight")
        if self._config["class_weight"] == None:
            self.class_weight.button.setCurrentText("None")
        else: self.class_weight.button.setCurrentText(self._config["class_weight"])
        self.class_weight.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.class_weight)

        self.ccp_alpha = DoubleSpinBox(text="Complexity parameter")
        self.ccp_alpha.button.setValue(self._config["ccp_alpha"])
        self.ccp_alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.ccp_alpha)

    def set_estimator(self):
        self._config["criterion"] = self.criterion.button.currentText()
        self._config["splitter"] = self.splitter.button.currentText()
        if self.max_depth.button.value() == -1:
            self._config["max_depth"] = None
        else: self._config["max_depth"] = self.max_depth.button.value()
        self._config["min_samples_split"] = self.min_samples_split.button.value()
        self._config["min_samples_leaf"] = self.min_samples_leaf.button.value()
        self._config["min_weight_fraction_leaf"] = self.min_weight_fraction_leaf.button.value()
        if self.max_features.button.currentText() == "max":
            self._config["max_features"] = None
        else: self._config["max_features"] = self.max_features.button.currentText()
        if self.max_leaf_nodes.button.value() == -1:
            self._config["max_leaf_nodes"] = None
        else: self._config["max_leaf_nodes"] = self.max_leaf_nodes.button.value()
        self._config["min_impurity_decrease"] = self.min_impurity_decrease.button.value()
        if self.class_weight.button.currentText() == "None":
            self._config["class_weight"] = None
        else: self._config["class_weight"] = self.class_weight.button.currentText()
        self._config["ccp_alpha"] = self.ccp_alpha.button.value()

        self.estimator = tree.DecisionTreeClassifier(**self._config)

class GaussianProcess(ClassifierBase):
    def __init__(self, config=None, parent=None):
        super().__init__(parent)

        self.set_config(config)        
    
    def set_config(self, config):

        self.clear_layout()

        if config == None: self._config = dict(kernel=None,optimizer="fmin_l_bfgs_b",
                                               n_restarts_optimizer=0,max_iter_predict=100,
                                               warm_start=False,multi_class="one_vs_rest")
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




class Classifier (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.parent = parent
        self.X, self.Y = list(), list()
        self.Y_test_score, self.Y_pred_score, self.Y_pred_proba_score = list(), list(), list()

        self.node.input_sockets[0].setTitle("Train/Test")
        self.node.output_sockets[0].setTitle("Model")
        self.node.output_sockets[1].setTitle("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.layout.insertWidget(2,self.score_btn)
        self.score_function = "Accuracy"
        
        self._config = dict(estimator="Logistic Regression",config=None)
        self.estimator_list = ["Ridge Classifier","Logistic Regression","SGD Classifier",
                               "Passive Aggressive Classifier", "SVC", "NuSVC", "Linear SVC",
                               "K Neighbors Classifier","Nearest Centroid", "Radius Neighbors Classifier",
                               "Gradient Boosting Classifier", "Histogram Gradient Boosting Classifier",
                               "Random Forest Classifier", "Extra Trees Classifier",
                               "Decision Tree Classifier","Gaussian Process Classifier"]
        self.estimator = linear_model.LogisticRegression()

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPrimaryPushButton(text="Algorithm")
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
        stackedlayout.addWidget(GradientBoosting())
        stackedlayout.addWidget(HistGradientBoosting())
        stackedlayout.addWidget(RandomForest())
        stackedlayout.addWidget(ExtraTrees())
        stackedlayout.addWidget(DecisionTree())
        stackedlayout.addWidget(GaussianProcess())
        stackedlayout.setCurrentIndex(self.estimator_list.index(algorithm.button.text()))
        stackedlayout.currentWidget().set_config(self._config["config"])
 
        if dialog.exec():
            self.estimator = stackedlayout.currentWidget().estimator
            self.estimator: linear_model.LogisticRegression
            self._config["estimator"] = algorithm.button.text()
            self._config["config"] = stackedlayout.currentWidget()._config
            self.exec()


    def func(self):
        self.eval()
        self.node.output_sockets[0].socket_data = self.estimator

        # try:
        if len(self.node.input_sockets[0].edges) == 1:
            if isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]
                
                self.data_to_view = self.node.input_sockets[0].socket_data[1].copy()
                n_classes = self.Y.shape[1]   
                n_samples = self.Y.shape[0]
                self.data_to_view[f"Label Encoder"] = str()
                for i in range(n_samples):
                    for j in range(n_classes):
                        self.data_to_view.iloc[i,-1] += str(self.Y.iloc[i,j])

                # convert self.X and self.Y into numpy arrays!
                self.X = self.X.to_numpy()
                self.Y = self.Y.to_numpy()
                
                for fold, (train_idx, test_idx) in enumerate(cv):

                    X_train, X_test = self.X[train_idx], self.X[test_idx]
                    Y_train, Y_test = self.Y[train_idx], self.Y[test_idx]
                    
                    model = OneVsRestClassifier(self.estimator)
                    model.fit(X_train, Y_train)
                    Y_pred = model.predict(X_test)
                    Y_pred_all = model.predict(self.X)
                    Y_pred_proba = model.predict_proba(X_test)

                    self.Y_test_score.append(Y_test)
                    self.Y_pred_score.append(Y_pred)
                    self.Y_pred_proba_score.append(Y_pred_proba)

                    n_classes = self.Y.shape[1]   
                    n_samples = self.Y.shape[0]
                    self.data_to_view[f"Fold{fold+1}_Prediction"] = str()
                    for i in range(n_samples):
                        for j in range(n_classes):
                            self.data_to_view.iloc[i,-1] += str(Y_pred_all[i,j])
                                
                score = scoring(self.Y_test_score, self.Y_pred_score)
                self.score_btn.setText(f"Score: {score[self.score_function]:.2f}")
                
                self.node.output_sockets[1].socket_data = None
                logger.info(f"{self.name} {self.node.id}::run successfully.")

        else:
            self.score_btn.setText(f"Score: --")
            logger.warning(f"{self.name} {self.node.id}::Did not define splitter.")
        
        # except Exception as e:
        #     self.score_btn.setText(f"Score: --")
        #     logger.error(f"{self.name} {self.node.id}::{repr(e)}.")
    
    def score_dialog(self):
        # dialog = Dialog("Scoring", self.parent.parent)
        dialog = Report(self.Y_test_score, self.Y_pred_score, self.Y_pred_proba_score)
        
        if dialog.exec():
            self.score_function = dialog.score_function
        pass
     
    def eval (self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None

        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
