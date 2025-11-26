from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (HTransparentComboBox, HPrimaryComboBox, SegmentedWidget,  HTransparentPushButton)
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from config.settings import logger, GLOBAL_DEBUG, config
from plot.canvas import Canvas
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout
from sklearn import (linear_model, kernel_ridge, svm, neighbors, tree, ensemble,
                     gaussian_process, cross_decomposition, dummy, metrics)
from matplotlib.axes import Axes
from typing import Literal
import numpy as np

DEBUG = False

def scoring(metric='r2 score', Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """
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

def attributes(model):
    attrs = {
        "Number of features": model.n_features_in_,        
    }
    if isinstance(model, linear_model.LinearRegression):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Rank": model.rank_,
            "Singular": model.singular_,
            
        })
    elif isinstance(model, linear_model.Ridge):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.Lasso):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.MultiTaskLasso):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
            "Tolerance": model.eps_
        })
    elif isinstance(model, linear_model.ElasticNet):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.MultiTaskElasticNet):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
            "Tolerance": model.eps_
        })
    elif isinstance(model, linear_model.Lars):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.LassoLars):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.OrthogonalMatchingPursuit):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, linear_model.BayesianRidge):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
            "Estimated precision of the noise": model.alpha_,
            "Estimated precision of the weights": model.lambda_,
            "Scores": model.scores_,
        })
    elif isinstance(model, linear_model.ARDRegression):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Estimated precision of the noise": model.alpha_,
            "Estimated precision of the weights": model.lambda_,
            "Scores": model.scores_,
        })
    elif isinstance(model, linear_model.TweedieRegressor):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, linear_model.HuberRegressor):
        attrs.update({
             "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
            "Scale": model.scale_
        })
    elif isinstance(model, linear_model.TheilSenRegressor):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
            "Approximated breakdown point": model.breakdown_,
            "Number of subpopulations": model.n_subpopulation_
        })
    elif isinstance(model, linear_model.QuantileRegressor):
        attrs.update({
            "Coefficients": model.coef_,
            "Intercept": model.intercept_,
        })
    elif isinstance(model, kernel_ridge.KernelRidge):
        pass
    elif isinstance(model, svm.SVR):
        attrs.update({
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, svm.NuSVR):
        attrs.update({
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, neighbors.KNeighborsRegressor):
        pass
    elif isinstance(model, neighbors.RadiusNeighborsRegressor):
        pass
    elif isinstance(model, gaussian_process.GaussianProcessRegressor):
        pass
    elif isinstance(model, cross_decomposition.PLSCanonical):
        attrs.update({
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, tree.DecisionTreeRegressor):
        attrs.update({
            "Feature importance": model.feature_importances_,
            "Maximum features": model.max_features_,
            "Number of outputs": model.n_outputs_
        })
    elif isinstance(model, tree.ExtraTreeRegressor):
        attrs.update({
            "Feature importance": model.feature_importances_,
            "Maximum features": model.max_features_,
            "Number of outputs": model.n_outputs_
        })
    elif isinstance(model, ensemble.RandomForestRegressor):
        attrs.update({
            "Feature importance": model.feature_importances_,
            "Number of outputs": model.n_outputs_,
            "Out-of-bag score": model.oob_score_,
        })
    elif isinstance(model, ensemble.ExtraTreesRegressor):
        attrs.update({
            "Feature importance": model.feature_importances_,
            "Number of outputs": model.n_outputs_,
            "Out-of-bag score": model.oob_score_,
        })
    elif isinstance(model, ensemble.GradientBoostingRegressor):
        pass
    elif isinstance(model, ensemble.HistGradientBoostingRegressor):
        attrs.update({
            "Early stopping": model.do_early_stopping_,
            "Iterations run": model.n_iter_,
            "Number of tree": model.n_trees_per_iteration_,
            "Train scores": model.train_score_,
            "Validation score": model.validation_score_
        })
    elif isinstance(model, ensemble.BaggingRegressor):
        attrs.update({
            "Estimator": model.estimator_.__class__.__name__,
            "Out-of-bag score": model.oob_score_,
            "Out-of-bag prediction": model.oob_prediction_
        })
    elif isinstance(model, ensemble.VotingRegressor):
        attrs.update({
            "Estimators": model.named_estimators_,
        })
    elif isinstance(model, ensemble.StackingRegressor):
        attrs.update({
            "Estimators": model.named_estimators_,
        })
    elif isinstance(model, ensemble.AdaBoostRegressor):
        attrs.update({
            "Estimator": model.estimator_.__class__.__name__,
            "Feature importance": model.feature_importances_,
            "Estimator weights": model.estimator_weights_,
            "Estimator errors": model.estimator_errors_,
        })
    elif isinstance(model, dummy.DummyRegressor):
        attrs.update({
            "Number of outputs": model.n_outputs_
        })

    return attrs
    
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

        for key, value in attributes(self.model).items():
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