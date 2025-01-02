from node_editor.base.node_graphics_content import NodeContentWidget
from ui.base_widgets.window import Dialog
from ui.base_widgets.menu import Menu
from ui.base_widgets.button import (DropDownPrimaryPushButton, PrimaryComboBox, SegmentedWidget,
                                    _TransparentPushButton, TransparentPushButton)
from ui.base_widgets.frame import SeparateHLine
from config.settings import logger, GLOBAL_DEBUG
from node_editor.node.train_test_split import TrainTestSplitter
from plot.canvas import Canvas
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PySide6.QtGui import QAction
from sklearn import linear_model, svm, neighbors, gaussian_process
from sklearn import metrics
from matplotlib.axes import Axes
from typing import Literal
import pandas as pd
import numpy as np

DEBUG = False

class AlgorithmMenu(Menu):
    sig = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        linear_model = Menu("Linear Model", self)
        for i in ["Linear Regression","Ridge Regression","Lasso","ElasticNet",
                  "Least Angle Regression","LARS Lasso","Orthogonal Matching Pursuit",
                  "Bayesian Ridge Regression","Automatic Relevance Determination",
                  "Stochastic Gradient Descent","Passive Aggressive Regression",
                  "Random Sample Consensus","Theil-Sen Regression","Huber Regression",
                  "Quantile Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            linear_model.addAction(action)
        self.addMenu(linear_model)

        generalizedlinear_model = Menu("Generalized Linear Model", self)
        for i in ["Tweedie Regression","Poisson Regression","Gamma Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            generalizedlinear_model.addAction(action)
        self.addMenu(generalizedlinear_model)

        svm = Menu("Support Vector Machines", self)
        for i in ["SVR","NuSVR","Linear SVR"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            svm.addAction(action)
        self.addMenu(svm)

        neighbors = Menu("Nearest Neighbors", self)
        for i in ["K Neighbors Regression","Radius Neighbors Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            neighbors.addAction(action)
        self.addMenu(neighbors)

        gaussian = Menu("Gaussian Process", self)
        for i in ["Gaussian Process Regression"]:
            action = QAction(i, self)
            action.triggered.connect(lambda _, s=i: self.sig.emit(s))
            gaussian.addAction(action)
        self.addMenu(gaussian)

def scoring(Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """

    if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
        return {
            "r2 score": "--",
            "mean absolute error": "--",
            "mean squared error": "--",
            "mean squared logarithmic error": "--",
            "mean absolute percentage error": "--",
            "median absolute error": "--",
            "maximum residual error": "--",
            "explained variance": "--",
        }
    
    else:
        r2 = np.array([])
        mean_absolute_error = np.array([])
        mean_squared_error = np.array([])
        mean_squared_log_error = np.array([])
        mean_absolute_percentage_error = np.array([])
        median_absolute_error = np.array([])
        max_error = np.array([])
        explained_variance_score = np.array([])
        
        for idx in range(len(Y)): # idx is fold index in cross validation.
            r2 = np.append(
                r2, 
                metrics.r2_score(Y[idx], Y_pred[idx])
            )
            mean_absolute_error = np.append(
                mean_absolute_error,
                metrics.mean_absolute_error(Y[idx], Y_pred[idx])
            )
            mean_squared_error = np.append(
                mean_squared_error,
                metrics.mean_squared_error(Y[idx], Y_pred[idx])
            )
            mean_squared_log_error = np.append(
                mean_squared_log_error,
                metrics.mean_squared_log_error(Y[idx], Y_pred[idx])
            )
            mean_absolute_percentage_error = np.append(
                mean_absolute_percentage_error,
                metrics.mean_absolute_percentage_error(Y[idx], Y_pred[idx])
            )
            median_absolute_error = np.append(
                median_absolute_error,
                metrics.median_absolute_error(Y[idx], Y_pred[idx])
            )
            max_error = np.append(
                max_error,
                metrics.max_error(Y[idx], Y_pred[idx])
            )
            explained_variance_score = np.append(
                explained_variance_score,
                metrics.explained_variance_score(Y[idx], Y_pred[idx])
            )
            

        return {
            "r2 score": r2.mean(),
            "mean absolute error": mean_absolute_error.mean(),
            "mean squared error": mean_squared_error.mean(),
            "mean squared logarithmic error": mean_squared_log_error.mean(),
            "mean absolute percentage error": mean_absolute_percentage_error.mean(),
            "median absolute error": median_absolute_error.mean(),
            "maximum residual error": max_error.mean(),
            "explained variance": explained_variance_score.mean(),
        }
    
class Report(Dialog):
    metricChange = Signal(str)
    def __init__(self, Y, Y_pred, parent=None):
        """ Y and Y_pred are nested lists """
        super().__init__("Metrics and Scoring", parent)

        self.score_function = "r2 score"
        self.Y = Y
        self.Y_pred = Y_pred

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Actual vs. Predicted', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment_widget.addButton(text='Residuals vs. Predicted', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        metrics = self.metrics()
        self.stackedlayout.addWidget(metrics)

        applot = self.APplot()
        self.stackedlayout.addWidget(applot)

        rpplot = self.RPplot()
        self.stackedlayout.addWidget(rpplot)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")
    
    def changeMetrics(self, metric:str):
        self.score_function = metric
        self.metricChange.emit(metric)
    
    def metrics(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)

        metricToShow = PrimaryComboBox(
            items=["r2 score","mean absolute error","mean squared error","mean squared logarithmic error",
                   "mean absolute percentage error","median absolute error","maximum residual error",
                   "explained variance"],
            text="Metrics"
        )
        metricToShow.setMinimumWidth(250)
        metricToShow.button.setCurrentText(self.score_function)
        metricToShow.button.currentTextChanged.connect(self.changeMetrics)
        layout.addWidget(metricToShow)
        
        score = scoring(self.Y, self.Y_pred)
        for metric in score:
            _btn = TransparentPushButton(text=metric.title())
            _btn.button.setText(str(score[metric]))
            layout.addWidget(_btn)
        
        return widget

    def APplot(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)            

        _fold = PrimaryComboBox(
            items=[f"Fold {i+1}" for i in range(len(self.Y))],
            text="Fold"
        )
        _fold.button.setCurrentText(f"Fold 1")
        _fold.button.currentTextChanged.connect(lambda s: self.plot(canvas,ax,'actual_vs_predicted',s.split()[-1]))
        layout.addWidget(_fold)

        # init Canvas on widget
        canvas = Canvas()
        canvas.fig.clear()
        ax = canvas.fig.subplots()
        layout.addWidget(canvas)
        
        self.plot(canvas, ax, 'actual_vs_predicted')

        return widget

    def RPplot(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)            

        _fold = PrimaryComboBox(
            items=[f"Fold {i+1}" for i in range(len(self.Y))],
            text="Fold"
        )
        _fold.button.setCurrentText(f"Fold 1")
        _fold.button.currentTextChanged.connect(lambda s: self.plot(canvas,ax,'residual_vs_predicted',s.split()[-1]))
        layout.addWidget(_fold)

        # init Canvas on widget
        canvas = Canvas()
        canvas.fig.clear()
        ax = canvas.fig.subplots()
        layout.addWidget(canvas)
        
        self.plot(canvas, ax, 'residual_vs_predicted')

        return widget


    def plot(self, canvas:Canvas, ax:Axes, 
             kind:Literal["actual_vs_predicted","residual_vs_predicted"], 
             fold = 1):
        fold = int(fold)
        ax.clear()
        metrics.PredictionErrorDisplay.from_predictions(
            self.Y[fold-1], self.Y_pred[fold-1],
            kind = kind,
            ax = ax
        )
        canvas.draw_idle()


        
        

class RegressorBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._config = dict()
        self.estimator = None
        self.initUI()
        self.setConfig()
        self.setEstimator()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.scroll_area = QScrollArea(self.parent())
        layout.addWidget(self.scroll_area)

        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)
    
    def clearLayout(self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def setConfig(self):
        pass

    def setEstimator(self):
        pass

class LinearRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setEstimator(self):
        self.estimator = linear_model.LinearRegression(**self._config)

class RidgeRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.Ridge(**self._config)

class Lasso(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.Lasso(**self._config)

class ElasticNet(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.ElasticNet(**self._config)

class LeastAngleRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.Lars(**self._config)

class LarsLasso(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.LassoLars(**self._config)

class OrthogonalMatchingPursuit(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.OrthogonalMatchingPursuit(**self._config)

class BayesianRidgeRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.BayesianRidge(**self._config)

class ARD(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.ARDRegression(**self._config)

class TweedieRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.TweedieRegressor(**self._config)

class PoissonRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.PoissonRegressor(**self._config)

class GammaRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.GammaRegressor(**self._config)

class StochasticGradientDescent(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.SGDRegressor(**self._config)

class PassiveAggressiveRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setEstimator(self):
        self.estimator = linear_model.PassiveAggressiveRegressor(**self._config)

class RANSAC(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setEstimator(self):
        self.estimator = linear_model.RANSACRegressor(**self._config)

class HuberRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.HuberRegressor(**self._config)

class TheilSenRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.TheilSenRegressor(**self._config)

class QuantileRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = linear_model.QuantileRegressor(**self._config)

class SVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = svm.SVR(**self._config)

class NuSVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = svm.NuSVR(**self._config)

class LinearSVR(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = svm.LinearSVR(**self._config)

class KNeighborsRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = neighbors.KNeighborsRegressor(**self._config)

class RadiusNeighborsRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = neighbors.RadiusNeighborsRegressor(**self._config)

class GaussianProcessRegression(RegressorBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def setEstimator(self):
        self.estimator = gaussian_process.GaussianProcessRegressor(**self._config)


class Regressor(NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)

        self.X, self.Y = list(), list()
        self.Y_test_score, self.Y_pred_score = list(), list()

        self.node.input_sockets[0].setSocketLabel("Train/Test")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "r2 score"

        self._config = dict(
            estimator = "Linear Regression",
            config = dict(),
        )

        self.estimator_list = ["Linear Regression","Ridge Regression","Lasso","ElasticNet",
                               "Least Angle Regression","LARS Lasso","Orthogonal Matching Pursuit",
                               "Bayesian Ridge Regression","Automatic Relevance Determination",
                               "Tweedie Regression","Poisson Regression","Gamma Regression",
                               "Stochastic Gradient Descent","Passive Aggressive Regression",
                               "Randon Sample Consensus","Huber Regression","Theil-Sen Regression",
                               "Quantile Regression","SVR","NuSVR","Linear SVR","K Neighbors Regression",
                               "Radius Neighbors Regression","Gaussian Process Regression"]

        self.estimator = linear_model.LinearRegression(**self._config["config"])

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        menu = AlgorithmMenu()
        menu.sig.connect(lambda string: algorithm.button.setText(string))
        menu.sig.connect(lambda string: stackedlayout.setCurrentIndex(self.estimator_list.index(string)))
        algorithm = DropDownPrimaryPushButton(text="Algorithm")
        algorithm.button.setText(self._config["estimator"])
        algorithm.button.setMenu(menu)
        dialog.main_layout.addWidget(algorithm)
        dialog.main_layout.addWidget(SeparateHLine())
        stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(stackedlayout)
        stackedlayout.addWidget(LinearRegression())
        stackedlayout.addWidget(RidgeRegression())
        stackedlayout.addWidget(Lasso())
        stackedlayout.addWidget(ElasticNet())
        stackedlayout.addWidget(LeastAngleRegression())
        stackedlayout.addWidget(LarsLasso())
        stackedlayout.addWidget(OrthogonalMatchingPursuit())
        stackedlayout.addWidget(BayesianRidgeRegression())
        stackedlayout.addWidget(ARD())
        stackedlayout.addWidget(TweedieRegression())
        stackedlayout.addWidget(PoissonRegression())
        stackedlayout.addWidget(GammaRegression())
        stackedlayout.addWidget(StochasticGradientDescent())
        stackedlayout.addWidget(PassiveAggressiveRegression())
        stackedlayout.addWidget(RANSAC())
        stackedlayout.addWidget(HuberRegression())
        stackedlayout.addWidget(TheilSenRegression())
        stackedlayout.addWidget(QuantileRegression())
        stackedlayout.addWidget(SVR())
        stackedlayout.addWidget(NuSVR())
        stackedlayout.addWidget(LinearSVR())
        stackedlayout.addWidget(KNeighborsRegression())
        stackedlayout.addWidget(RadiusNeighborsRegression())
        stackedlayout.addWidget(GaussianProcessRegression())

        if dialog.exec():
            self.estimator = stackedlayout.currentWidget().estimator
            self.exec()
        
    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            X = df.iloc[:,:4]
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
            split = model_selection.ShuffleSplit(n_splits=2, test_size=0.2).split(X, Y)
            result = list()
            for fold, (train_idx, test_idx) in enumerate(split):
                result.append((train_idx, test_idx))
            self.node.input_sockets[0].socket_data = [result, X, Y]
            print('data in', self.node.input_sockets[0].socket_data)
        
        try:
            if DEBUG or isinstance(self.node.input_sockets[0].edges[0].start_socket.node.content, TrainTestSplitter):
                # cv is an array of indexes corresponding to (train, test)
                cv = self.node.input_sockets[0].socket_data[0]
                self.X = self.node.input_sockets[0].socket_data[1]
                self.Y = self.node.input_sockets[0].socket_data[2]

                data = pd.concat([self.X, self.Y], axis=1)

                # convert self.X and self.Y into numpy arrays!
                self.X = self.X.to_numpy()
                self.Y = self.Y.to_numpy()
            
                for fold, (train_idx, test_idx) in enumerate(cv):
                    X_train, X_test = self.X[train_idx], self.X[test_idx]
                    Y_train, Y_test = self.Y[train_idx], self.Y[test_idx]

                    model = self.estimator
                    model.fit(X_train, Y_train)
                    
                    Y_pred = model.predict(X_test)
                    Y_pred_all = model.predict(self.X)

                    self.Y_test_score.append(Y_test)
                    self.Y_pred_score.append(Y_pred)

                    data[f"Fold{fold+1}_Prediction"] = Y_pred_all

                score = scoring(self.Y_test_score, self.Y_pred_score)
                self.score_btn.setText(f"Score: {score[self.score_function]:.2f}")
                # change progressbar's color   
                self.progress.changeColor('success')
                # write log
                if DEBUG or GLOBAL_DEBUG: print('data out', data)
                logger.info(f"{self.name} {self.node.id}: {self.estimator} run successfully.")
            else:
                data = pd.DataFrame()
                self.score_btn.setText(f"Score: --")
                # change progressbar's color   
                self.progress.changeColor('fail')
                # write log
                logger.warning(f"{self.name} {self.node.id}: not a valid splitter, return an empty Dataframe.")
        
        except Exception as e:
            data = pd.DataFrame()
            self.score_btn.setText(f"Score: --")
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)


        
        
        self.node.output_sockets[0].socket_data = self.estimator
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def score_dialog(self):
        dialog = Report(self.Y_test_score, self.Y_pred_score)
        score = scoring(self.Y_test_score, self.Y_pred_score)
        dialog.metricChange.connect(lambda s: self.score_btn.setText(f"Score {score[s]:.2f}"))
        if dialog.exec():
            self.score_function = dialog.score_function
    
    def eval(self):
        # reset input sockets
        for socket in self.node.input_sockets:
            socket.socket_data = None
        # reset socket data
        self.node.input_sockets[0].socket_data = [[],pd.DataFrame(), pd.DataFrame()]
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data