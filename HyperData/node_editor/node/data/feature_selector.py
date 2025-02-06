from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import feature_selection, linear_model
from sklearn.feature_selection import (f_classif, mutual_info_classif, chi2, f_regression,
                                       mutual_info_regression)
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle, PrimaryComboBox, ComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import SpinBox, DoubleSpinBox
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

DEBUG = False

class MethodBase(QWidget):
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
        self.method = None

        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()

class VarianceThreshold (MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            threshold = 0.0
        )
        else: self._config = config
        self.method = feature_selection.VarianceThreshold(**self._config)
        
        self.threshold = DoubleSpinBox(text="Threshold")
        self.threshold.button.setValue(self._config["threshold"])
        self.threshold.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.threshold)   
    
    def set_estimator(self):
        self._config.update(
            threshold = self.threshold.button.value()
        )
        self.method = feature_selection.VarianceThreshold(**self._config)

class SelectKBest(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            score_func = f_classif,
            k = 10
        )
        else: self._config = config
        self.method = feature_selection.SelectKBest(**self._config)
        
        self.score_func = ComboBox(items=["ANOVA F-value", "Mutual information classification",
                                          "Chi-squared", "F-value","Mutual information regression"], 
                                   text="Scoring function")
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)
        self.score_func.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.score_func)

        self.k = SpinBox(text="Number of features")
        self.k.button.setValue(self._config["k"])
        self.k.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.k)
    
    def set_estimator(self):
        match self.score_func.button.currentText():
            case "ANOVA F-value": score_func = f_classif
            case "Mutual information classification": score_func = mutual_info_classif
            case "Chi-squared": score_func = chi2
            case "F-value": score_func = f_regression
            case "Mutual information regression": score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            k = self.k.button.value()
        )
        self.method = feature_selection.SelectKBest(**self._config)

class SelectFpr(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            score_func = f_classif,
            alpha = 0.05
        )
        else: self._config = config
        self.method = feature_selection.SelectFpr(**self._config)
        
        self.score_func = ComboBox(items=["ANOVA F-value", "Mutual information classification",
                                          "Chi-squared", "F-value","Mutual information regression"], 
                                   text="Scoring function")
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)
        self.score_func.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.score_func)

        self.alpha = DoubleSpinBox(text="P-values")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)
    
    def set_estimator(self):
        match self.score_func.button.currentText():
            case "ANOVA F-value": score_func = f_classif
            case "Mutual information classification": score_func = mutual_info_classif
            case "Chi-squared": score_func = chi2
            case "F-value": score_func = f_regression
            case "Mutual information regression": score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            alpha = self.alpha.button.value()
        )
        self.method = feature_selection.SelectFpr(**self._config)

class SelectFdr(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            score_func = f_classif,
            alpha = 0.05
        )
        else: self._config = config
        self.method = feature_selection.SelectFdr(**self._config)
        
        self.score_func = ComboBox(items=["ANOVA F-value", "Mutual information classification",
                                          "Chi-squared", "F-value","Mutual information regression"], 
                                   text="Scoring function")
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)
        self.score_func.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.score_func)

        self.alpha = DoubleSpinBox(text="P-values")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)
    
    def set_estimator(self):
        match self.score_func.button.currentText():
            case "ANOVA F-value": score_func = f_classif
            case "Mutual information classification": score_func = mutual_info_classif
            case "Chi-squared": score_func = chi2
            case "F-value": score_func = f_regression
            case "Mutual information regression": score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            alpha = self.alpha.button.value()
        )
        self.method = feature_selection.SelectFdr(**self._config)

class SelectFwe(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            score_func = f_classif,
            alpha = 0.05
        )
        else: self._config = config
        self.method = feature_selection.SelectFwe(**self._config)
        
        self.score_func = ComboBox(items=["ANOVA F-value", "Mutual information classification",
                                          "Chi-squared", "F-value","Mutual information regression"], 
                                   text="Scoring function")
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)
        self.score_func.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.score_func)

        self.alpha = DoubleSpinBox(text="P-values")
        self.alpha.button.setValue(self._config["alpha"])
        self.alpha.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.alpha)
    
    def set_estimator(self):
        match self.score_func.button.currentText():
            case "ANOVA F-value": score_func = f_classif
            case "Mutual information classification": score_func = mutual_info_classif
            case "Chi-squared": score_func = chi2
            case "F-value": score_func = f_regression
            case "Mutual information regression": score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            alpha = self.alpha.button.value()
        )
        self.method = feature_selection.SelectFwe(**self._config)

class RFE(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_features_to_select = 10,
            step = 1,
        )
        else: self._config = config
        
        self.n_features_to_select = SpinBox(text="Number of features")
        self.n_features_to_select.button.setValue(self._config["n_features_to_select"])
        self.n_features_to_select.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_features_to_select)

        self.step = SpinBox(text="Features remove each iteration")
        self.step.button.setValue(self._config["step"])
        self.step.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.step)
    
    def set_estimator(self):
        self._config.update(
            n_features_to_select = self.n_features_to_select.button.value(),
            step = self.step.button.value(),
        )

class SelectFromModel(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        
class SequentialFeatureSelector(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

        

class FeatureSelector (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Estimator")
        self.node.input_sockets[1].setSocketLabel("Features (X)")
        self.node.input_sockets[2].setSocketLabel("Labels (Y)")
        self.node.output_sockets[0].setSocketLabel("Data out")

        self._config = dict(
            model = "Variance Threshold",
            config = dict(),
        )
        
        self.method_list = ["Variance Threshold","Select K best","Select for False Positive",
                            "Select for False Discovery","Select for Family-wise Error",
                            "Recursive Feature Elimination","Select From Estimator",
                            "Sequential Feature Selection"]
        
        self.model = feature_selection.VarianceThreshold(**self._config["config"])
    
    def currentWidget(self) -> MethodBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        method = PrimaryComboBox(items=self.method_list,text="Scaler")
        method.button.setMinimumWidth(250)
        method.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.method_list.index(s)))
        dialog.main_layout.addWidget(method)
        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(VarianceThreshold())
        self.stackedlayout.addWidget(SelectKBest())
        self.stackedlayout.addWidget(SelectFpr())
        self.stackedlayout.addWidget(SelectFdr())
        self.stackedlayout.addWidget(SelectFwe())
        self.stackedlayout.addWidget(RFE())
        self.stackedlayout.addWidget(SelectFromModel())
        self.stackedlayout.addWidget(SequentialFeatureSelector())
        self.stackedlayout.setCurrentIndex(self.method_list.index(method.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                method = method.button.currentText()
            )
            self.model = self.currentWidget().method
            print("abc", self.model)
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = linear_model.LogisticRegression()
            self.node.input_sockets[1].socket_data = df
            self.node.input_sockets[2].socket_data = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            print('data in', self.node.input_sockets[0].socket_data, 
                  self.node.input_sockets[1].socket_data,
                  self.node.input_sockets[2].socket_data)

        try:
            estimator = self.node.input_sockets[0].socket_data
            X = self.node.input_sockets[1].socket_data
            Y = self.node.input_sockets[2].socket_data

            if self._config["model"] == "Select From Estimator":
                self.model = feature_selection.SelectFromModel(estimator, **self._config["config"])
            elif self._config["model"] == "Sequential Feature Selection":
                self.model = feature_selection.SequentialFeatureSelector(estimator, **self._config["config"])
            elif self._config["model"] == "Recursive Feature Elimination":
                self.model = feature_selection.RFE(estimator, **self._config["config"])

            data = self.model.fit_transform(X, Y)
            data = pd.DataFrame(data)
            
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.model} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
     
    def eval (self):
        self.resetStatus()
        # reset socket data
        self.node.input_sockets[0].socket_data = None
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        self.node.input_sockets[2].socket_data = None
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[2].edges:
            self.node.input_sockets[2].socket_data = edge.start_socket.socket_data