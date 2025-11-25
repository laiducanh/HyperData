from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (HTransparentComboBox, HPrimaryComboBox, SegmentedWidget,  HTransparentPushButton)
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from config.settings import logger, GLOBAL_DEBUG, config
from plot.canvas import Canvas
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout
from sklearn import linear_model, metrics
from matplotlib.axes import Axes
from typing import Literal
import numpy as np
from node_editor.node.regressor.linear import LinearRegression

DEBUG = False

def scoring(metric='r2 score', Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """

    if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
        return '--'

    else:
        try:
            score = []
            for fold in range(len(Y)):
                y, y_pred = Y[fold], Y_pred[fold]
                if metric == 'r2 score':
                    score.append(metrics.r2_score(y, y_pred))
                elif metric == 'mean absolute error':
                    score.append(metrics.mean_absolute_error(y, y_pred))
                elif metric == 'mean squared error':
                    score.append(metrics.mean_squared_error(y, y_pred))
                elif metric == 'mean squared logarithmic error':
                    score.append(metrics.mean_squared_log_error(y, y_pred))
                elif metric == 'mean absolute percentage error':
                    score.append(metrics.mean_absolute_percentage_error(y, y_pred))
                elif metric == 'median absolute error':
                    score.append(metrics.median_absolute_error(y, y_pred))
                elif metric == 'maximum residual error':
                    score.append(metrics.max_error(y, y_pred))
                elif metric == 'root mean squared error':
                    score.append(metrics.root_mean_squared_error(y, y_pred))
                elif metric == 'root mean squared logarithmic error':
                    score.append(metrics.root_mean_squared_log_error(y, y_pred))
                elif metric == 'explained variance':
                    score.append(metrics.explained_variance_score(y, y_pred))
            
            return f"{np.array(score).mean():.2f} +/- {np.array(score).std():.2f}"
        except Exception as e:
            logger.exception(e)
            return '--'
    
class Report(Dialog):
    def __init__(self, model, Y, Y_pred, score_function, parent=None):
        """ Y and Y_pred are nested lists """
        super().__init__("Metrics and Scoring", parent)

        self.score_function = score_function
        self.model = model
        self.Y = Y
        self.Y_pred = Y_pred

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Plot', func=lambda: self.stackedlayout.setCurrentIndex(1))

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        metrics = self.metrics()
        self.stackedlayout.addWidget(metrics)

        plot = self.Plot()
        self.stackedlayout.addWidget(plot)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")
    
    def changeMetrics(self, metric:str):
        self.score_function = metric
        self.score.setText(f'Score: {scoring(self.score_function, self.Y, self.Y_pred)}')
    
    def metrics(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0,0,0,0)

        metricToShow = HTransparentComboBox(
            items=["r2 score","mean absolute error","mean squared error","mean squared logarithmic error",
                   "mean absolute percentage error","median absolute error","maximum residual error",
                   "root mean squared error","root mean squared logarithmic error","explained variance"],
            getter=lambda: self.score_function,
            setter=self.changeMetrics,
            label="Metrics",
            layout=layout
        )
        metricToShow.button.setMinimumWidth(250)
        layout.addWidget(SeparateHLine())

        self.score = BodyLabel(f'Score: {scoring(self.score_function, self.Y, self.Y_pred)}')
        layout.addWidget(self.score)

        if isinstance(self.model, linear_model.LinearRegression):
            attrs = LinearRegression.get_attributes(self.model)
            for key, value in attrs.items():
                layout.addWidget(SeparateHLine())
                layout.addWidget(BodyLabel(f'{key}: {value}'))
                

        return widget

    def Plot(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)   

        self.fold = HTransparentComboBox(
            items=[f"Fold {i+1}" for i in range(len(self.Y))],
            label='Fold',
            setter=self.draw,
            layout=layout
        ) 
        self.fold.button.setMinimumWidth(250)

        self.kind = HTransparentComboBox(
            items=['actual_vs_predicted','residual_vs_predicted'],
            label='Type',
            setter=self.draw,
            layout=layout
        )
        self.kind.button.setMinimumWidth(250)

        # init Canvas on widget
        self.canvas = Canvas()
        self.canvas.figure.clear()
        layout.addWidget(self.canvas)
        self.draw()

        return widget


    def draw(self):
        fold = int(self.fold.get_value().split()[-1])
        kind = self.kind.get_value()
        ax = self.canvas.figure.subplots()
        metrics.PredictionErrorDisplay.from_predictions(
            self.Y[fold-1], self.Y_pred[fold-1],
            kind = kind,
            scatter_kwargs={'c':config['themecolor']},
            ax = ax
        )
        self.canvas.draw_idle()