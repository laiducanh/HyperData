from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import feature_selection, linear_model
from sklearn.feature_selection import (f_classif, mutual_info_classif, chi2, 
                                       r_regression, f_regression, mutual_info_regression)
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import PrimaryComboBox, TransparentComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import TransparentSpinBox, TransparentDoubleSpinBox
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

        self.set_config(config=None)
        
    def clear_layout (self):
        # Remove all child widgets from the layout
        while self.vlayout.count():
            item = self.vlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
    
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
        
        self.threshold = TransparentDoubleSpinBox(
            text="Threshold",
            getter=lambda: self._config["threshold"],
            setter=self.set_estimator,
            layout=self.vlayout
        ) 
    
    def set_estimator(self):
        self._config.update(
            threshold = self.threshold.button.value()
        )

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
        
        self.score_func = TransparentComboBox(
            items=["ANOVA F-value", "Mutual information classification","Chi-squared", 
                   "Pearson's r", "F-value","Mutual information regression"], 
            text="Scoring function",
            setter=self.set_estimator,
            layout=self.vlayout
        )
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == r_regression: s = "Pearson's r"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)

        self.k = TransparentSpinBox(
            text="Number of features",
            getter=lambda: self._config["k"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        if self.score_func.button.currentText() == "ANOVA F-value": 
            score_func = f_classif
        elif self.score_func.button.currentText() == "Mutual information classification": 
            score_func = mutual_info_classif
        elif self.score_func.button.currentText() == "Chi-squared": 
            score_func = chi2
        elif self.score_func.button.currentText() == "Pearson's r":
            score_func = r_regression
        elif self.score_func.button.currentText() == "F-value": 
            score_func = f_regression
        elif self.score_func.button.currentText() == "Mutual information regression": 
            score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            k = self.k.button.value()
        )

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
        
        self.score_func = TransparentComboBox(
            items=["ANOVA F-value", "Mutual information classification","Chi-squared", 
                   "F-value","Mutual information regression"], 
            text="Scoring function",
            setter=self.set_estimator,
            layout=self.vlayout
        )
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == r_regression: s = "Pearson's r"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)

        self.alpha = TransparentDoubleSpinBox(
            text="P-values",
            getter=lambda: self._config["alpha"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        if self.score_func.button.currentText() == "ANOVA F-value": 
            score_func = f_classif
        elif self.score_func.button.currentText() == "Mutual information classification": 
            score_func = mutual_info_classif
        elif self.score_func.button.currentText() == "Chi-squared": 
            score_func = chi2
        elif self.score_func.button.currentText() == "Pearson's r":
            score_func = r_regression
        elif self.score_func.button.currentText() == "F-value": 
            score_func = f_regression
        elif self.score_func.button.currentText() == "Mutual information regression": 
            score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            alpha = self.alpha.button.value()
        )

class SelectFdr(SelectFpr):
    """ """
class SelectFwe(SelectFpr):
    """ """
class SelectPercentile(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            score_func = f_classif,
            percentile = 10
        )
        else: self._config = config
        
        self.score_func = TransparentComboBox(
            items=["ANOVA F-value", "Mutual information classification","Chi-squared", 
                   "F-value","Mutual information regression"], 
            text="Scoring function",
            setter=self.set_estimator,
            layout=self.vlayout
        )
        if self._config["score_func"] == f_classif: s = "ANOVA F-value"
        elif self._config["score_func"] == mutual_info_classif: s = "Mutual information classification"
        elif self._config["score_func"] == chi2: s = "Chi2"
        elif self._config["score_func"] == r_regression: s = "Pearson's r"
        elif self._config["score_func"] == f_regression: s = "F-value"
        elif self._config["score_func"] == mutual_info_regression: s = "Mutual information regression"
        self.score_func.button.setCurrentText(s)

        self.percentile = TransparentSpinBox(
            text="Percentile",
            text2="Percent of features to keep",
            getter=lambda: self._config["percentile"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        if self.score_func.button.currentText() == "ANOVA F-value": 
            score_func = f_classif
        elif self.score_func.button.currentText() == "Mutual information classification": 
            score_func = mutual_info_classif
        elif self.score_func.button.currentText() == "Chi-squared": 
            score_func = chi2
        elif self.score_func.button.currentText() == "Pearson's r":
            score_func = r_regression
        elif self.score_func.button.currentText() == "F-value": 
            score_func = f_regression
        elif self.score_func.button.currentText() == "Mutual information regression": 
            score_func = mutual_info_regression

        self._config.update(
            score_func = score_func,
            percentile = self.percentile.button.value()
        )

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
        
        self.n_features_to_select = TransparentSpinBox(
            text="Number of features",
            getter=lambda: self._config["n_features_to_select"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.step = TransparentSpinBox(
            text="Features remove each iteration",
            getter=lambda: self._config["step"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
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

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            direction = "forward"
        )
        else: self._config = config
        
        self.direction = TransparentComboBox(
            items=["forward","backward"],
            text="Direction",
            text2="Whether to perform forward selection or backward selection",
            setter=self.set_estimator,
            getter=lambda: self._config["direction"],
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config.update(
            direction = self.direction.button.currentText()
        )

class FeatureSelector (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Estimator")
        self.node.input_sockets[1].setSocketLabel("Features (X)")
        self.node.input_sockets[2].setSocketLabel("Labels (Y)")
        self.node.output_sockets[0].setSocketLabel("Data out")

        self._config = dict(
            method = "Variance Threshold",
            config = dict(),
        )
        
        self.method_list = ["Variance Threshold","Select K best","Select for False Positive",
                            "Select for False Discovery","Select for Family-wise Error",
                            "Select by Percentile","Recursive Feature Elimination",
                            "Select From Estimator","Sequential Feature Selection"]
            
    def currentWidget(self) -> MethodBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Feature Selection", self.parent)
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
        self.stackedlayout.addWidget(SelectPercentile())
        self.stackedlayout.addWidget(RFE())
        self.stackedlayout.addWidget(SelectFromModel())
        self.stackedlayout.addWidget(SequentialFeatureSelector())
        self.stackedlayout.setCurrentIndex(self.method_list.index(method.button.currentText()))
        self.currentWidget().set_config(self._config["config"])

        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                method = method.button.currentText()
            )
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
            elif self._config["model"] == "Variance Threshold":
                self.model = feature_selection.VarianceThreshold(**self._config["config"])
            elif self._config["'model"] == "Select K best":
                self.model = feature_selection.SelectKBest(**self._config["config"])
            elif self._config["model"] == "Select for False Positive":
                self.model = feature_selection.SelectFpr(**self._config["'config"])
            elif self._config["model"] == "Select for False Discovery":
                self.model = feature_selection.SelectFdr(**self._config["config"])
            elif self._config["model"] == "Select for Family-wise Error":
                self.model = feature_selection.SelectFwe(**self._config["config"])
            elif self._config["model"] == "Select by Percentile":
                self.model = feature_selection.SelectPercentile(**self._config["config"])

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