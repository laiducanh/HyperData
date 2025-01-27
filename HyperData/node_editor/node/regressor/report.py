from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (PrimaryComboBox, SegmentedWidget,  TransparentPushButton)
from config.settings import logger, GLOBAL_DEBUG
from plot.canvas import Canvas
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout
from sklearn import metrics
from matplotlib.axes import Axes
from typing import Literal
import numpy as np

DEBUG = False

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
            "r2 score": f"{r2.mean():.2f} +/- {r2.std():.2f}",
            "mean absolute error": f"{mean_absolute_error.mean():.2f} +/- {mean_squared_error.std():.2f}",
            "mean squared error": f"{mean_squared_error.mean():.2f} +/- {mean_squared_error.std():.2f}",
            "mean squared logarithmic error": f"{mean_squared_log_error.mean():.2f} +/- {mean_squared_log_error.std():.2f}",
            "mean absolute percentage error": f"{mean_absolute_percentage_error.mean():.2f} +/- {mean_absolute_percentage_error.std():.2f}",
            "median absolute error": f"{median_absolute_error.mean():.2f} +/- {median_absolute_error.std():.2f}",
            "maximum residual error": f"{max_error.mean():.2f} +/- {max_error.std():.2f}",
            "explained variance": f"{explained_variance_score.mean():.2f} +/- {explained_variance_score.std():.2f}",
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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        metricToShow = PrimaryComboBox(
            items=["r2 score","mean absolute error","mean squared error","mean squared logarithmic error",
                   "mean absolute percentage error","median absolute error","maximum residual error",
                   "explained variance"],
            text="Metrics"
        )
        metricToShow.button.setMinimumWidth(250)
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