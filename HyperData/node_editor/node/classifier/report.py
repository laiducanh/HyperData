import numpy as np
from sklearn import (linear_model, discriminant_analysis, svm, neighbors, gaussian_process,
                     naive_bayes, tree, ensemble, multiclass, dummy, metrics)
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.button import (HTransparentPushButton, SegmentedWidget, HTransparentComboBox)
from node_editor.node.report import ConfusionMatrix, ROC, PrecisionRecall, DET, DecisionBoundary
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QStackedLayout, QApplication)
from PySide6.QtCore import Qt

DEBUG = False

def scoring(Y=list(), Y_pred=list(), metric='Accuracy'):
    """ Y and Y_pred are nested lists """
    try:
        score = []
        for fold in range(len(Y)):
            y, y_pred = Y[fold], Y_pred[fold]
            if metric == 'Accuracy':
                score.append(metrics.accuracy_score(y, y_pred))
            elif metric == 'Balanced accuracy':
                score.append(metrics.balanced_accuracy_score(y, y_pred))
            elif metric == 'Micro Precision':
                score.append(metrics.precision_score(y, y_pred, average='micro'))
            elif metric == 'Macro Precision':
                score.append(metrics.precision_score(y, y_pred, average='macro'))
            elif metric == 'Weighted Precision':
                score.append(metrics.precision_score(y, y_pred, average='weighted'))
            elif metric == 'Micro Recall':
                score.append(metrics.recall_score(y, y_pred, average='micro'))
            elif metric == 'Macro Recall':
                score.append(metrics.recall_score(y, y_pred, average='macro'))
            elif metric == 'Weighted Recall':
                score.append(metrics.recall_score(y, y_pred, average='weighted'))
            elif metric == 'Micro F1 score':
                score.append(metrics.f1_score(y, y_pred, average='micro'))
            elif metric == 'Macro F1 score':
                score.append(metrics.f1_score(y, y_pred, average='macro'))
            elif metric == 'Weighted F1 score':
                score.append(metrics.f1_score(y, y_pred, average='weighted'))
            elif metric == 'Log loss':
                score.append(metrics.log_loss(y, y_pred))
            elif metric == 'Brier score loss':
                score.append(metrics.brier_score_loss(y, y_pred))
            elif metric == 'Zero-one loss':
                score.append(metrics.zero_one_loss(y, y_pred))

            return f"{np.array(score).mean():.2f} +/- {np.array(score).std():.2f}"
    
    except Exception as e:
        logger.exception(e)
        return '--'

def attributes(model):
    attrs = {
        "Number of features": model.n_features_in_,        
    }
    if isinstance(model, linear_model.RidgeClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Coefficient": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, linear_model.LogisticRegression):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Coefficient": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, discriminant_analysis.LinearDiscriminantAnalysis):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Weight vectors": model.coef_,
            "Intercept": model.intercept_,
        })
    elif isinstance(model, discriminant_analysis.QuadraticDiscriminantAnalysis):
        attrs.update({
            "Number of classes": len(model.classes_),
        })
    elif isinstance(model, svm.SVC):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Coefficient": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, svm.NuSVC):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Coefficient": model.coef_,
            "Intercept": model.intercept_,
            "Iterations run": model.n_iter_,
        })
    elif isinstance(model, neighbors.KNeighborsClassifier):
        attrs.update({
            "Number of samples": model.n_samples_fit_,
            "Number of classes": len(model.classes_),
        })
    elif isinstance(model, neighbors.RadiusNeighborsClassifier):
        attrs.update({
            "Number of samples": model.n_samples_fit_,
            "Number of classes": len(model.classes_),
            "Outlier label": model.outlier_label_
        })
    elif isinstance(model, neighbors.NeighborhoodComponentsAnalysis):
        attrs.update({
            "Iterations run": model.n_iter_
        })
    elif isinstance(model, gaussian_process.GaussianProcessClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
        })
    elif isinstance(model, naive_bayes.GaussianNB):
        attrs.update({
            "Number of training samples in each class": model.class_count_,
            "Number of classes": len(model.classes_),
            "Probability of each class": model.class_prior_,
            "Absolute additive value to variances": model.epsilon_,
            "Variance of each feature per class": model.var_,
            "Mean of each feature per class": model.theta_
        })
    elif isinstance(model, naive_bayes.MultinomialNB):
        attrs.update({
            "Number of training samples in each class": model.class_count_,
            "Number of classes": len(model.classes_),
            "Smoothed empirical log probability for each class": model.class_log_prior_,
        })
    elif isinstance(model, naive_bayes.ComplementNB):
        attrs.update({
            "Number of training samples in each class": model.class_count_,
            "Number of classes": len(model.classes_),
            "Smoothed empirical log probability for each class": model.class_log_prior_,
        })
    elif isinstance(model, naive_bayes.BernoulliNB):
        attrs.update({
            "Number of training samples in each class": model.class_count_,
            "Number of classes": len(model.classes_),
            "Smoothed empirical log probability for each class": model.class_log_prior_,
        })
    elif isinstance(model, naive_bayes.CategoricalNB):
        attrs.update({
            "Number of samples for each feature": model.category_count_,
            "Number of training samples in each class": model.class_count_,
            "Number of classes": len(model.classes_),
            "Smoothed empirical log probability for each class": model.class_log_prior_,
        })
    elif isinstance(model, tree.DecisionTreeClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Feature importance": model.feature_importances_,
            "Maximum features": model.max_features_,
            "Number of outputs": model.n_outputs_
        })
    elif isinstance(model, tree.ExtraTreeClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Feature importance": model.feature_importances_,
            "Maximum features": model.max_features_,
            "Number of outputs": model.n_outputs_
        })
    elif isinstance(model, ensemble.RandomForestClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Feature importance": model.feature_importances_,
            "Number of outputs": model.n_outputs_,
            "Out-of-bag score": model.oob_score_
        })
    elif isinstance(model, ensemble.ExtraTreesClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Feature importance": model.feature_importances_,
            "Number of outputs": model.n_outputs_,
            "Out-of-bag score": model.oob_score_
        })
    elif isinstance(model, ensemble.GradientBoostingClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Feature importance": model.feature_importances_,
            "Train score": model.train_score_,
            "Maximum features": model.max_features_
        })
    elif isinstance(model, ensemble.HistGradientBoostingClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Iterations run": model.n_iter_,
            "Early stopping": model.do_early_stopping_,
            "Train score": model.train_score_,
            "Validation score": model.validation_score_,
            "Number of tree": model.n_trees_per_iteration_
        })
    elif isinstance(model, ensemble.BaggingClassifier):
        attrs.update({
            "Estimator": model.estimator_.__class__.__name__,
            "Number of classes": len(model.classes_),
            "Out-of-bag score": model.oob_score_
        })
    elif isinstance(model, ensemble.VotingClassifier):
        attrs.update({
            "Estimators": model.named_estimators_,
            "Number of classes": len(model.classes_),
        })
    elif isinstance(model, ensemble.StackingClassifier):
        attrs.update({
            "Estimators": model.named_estimators_,
            "Number of classes": len(model.classes_),
        })
    elif isinstance(model, ensemble.AdaBoostClassifier):
        attrs.update({
            "Estimator": model.estimator_.__class__.__name__,
            "Number of classes": len(model.classes_),
            "Estimator weights": model.estimator_weights_,
            "Estimator errors": model.estimator_errors_,
            "Feature importance": model.feature_importances_
        })
    elif isinstance(model, dummy.DummyClassifier):
        attrs.update({
            "Number of classes": len(model.classes_),
            "Number of outputs": model.n_outputs_
        })
    return attrs

class Report(Dialog):
    def __init__(self, model, estimator, X, Y, X_test, Y_test, Y_pred, score_function, parent=None):
        """ X, Y, and Y_pred are nested lists """
        super().__init__(title="Metrics and Scoring",parent=parent)

        self.model = model
        self.estimator = estimator
        self.score_function = score_function
        self.X = X
        self.Y = Y
        self.X_test = X_test
        self.Y_test = Y_test
        self.Y_pred = Y_pred

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.clipboard = QApplication.clipboard()

        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Confusion Matrix', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment_widget.addButton(text='Decision Boundary', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment_widget.addButton(text='ROC Curve', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment_widget.addButton(text='PR Curve', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.segment_widget.addButton(text='DET Curve', func=lambda: self.stackedlayout.setCurrentIndex(5))

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        metrics = self.metrics(Y_test, Y_pred)
        self.stackedlayout.addWidget(metrics)

        confusion_mat = ConfusionMatrix(Y_test, Y_pred)
        self.stackedlayout.addWidget(confusion_mat)

        decision_boundary = DecisionBoundary(estimator, X, Y)
        self.stackedlayout.addWidget(decision_boundary)

        roc = ROC(model, X_test, Y_test)
        self.stackedlayout.addWidget(roc)

        pr = PrecisionRecall(model, X_test, Y_test)
        self.stackedlayout.addWidget(pr)

        det = DET(model, X_test, Y_test)
        self.stackedlayout.addWidget(det)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")
    
    def change_metric(self, metric:str):
        self.score_function = metric
        self.score.setText(f'Score: {scoring(self.score_function, self.Y, self.Y_pred)}')

    def metrics(self, Y, Y_pred) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)

        metric_to_show = HTransparentComboBox(
            items=["Accuracy","Balanced accuracy",
                   "Micro Precision","Macro Precision","Weighted Precision",
                   "Micro Recall","Macro Recall","Weighted Recall",
                   "Micro F1 score","Macro F1 score","Weighted F1 score",
                   "Log loss","Brier score loss","Zero-one loss"], 
            label="Metric",
            setter=self.change_metric,
            layout=layout
        )
        metric_to_show.button.setMinimumWidth(250)
        layout.addWidget(SeparateHLine())

        self.score = BodyLabel(f'Score: {scoring(Y, Y_pred, self.score_function)}')
        layout.addWidget(self.score)

        if isinstance(self.model, (multiclass.OneVsOneClassifier, multiclass.OneVsRestClassifier)):
            model = self.model.estimators_[0]
        else:
            model = self.model
        for key, value in attributes(model).items():
            layout.addWidget(SeparateHLine())
            layout.addWidget(BodyLabel(f'{key}: {value}'))

        return widget
