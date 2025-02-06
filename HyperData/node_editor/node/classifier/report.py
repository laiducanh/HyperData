import numpy as np
from sklearn import metrics, preprocessing
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (PrimaryComboBox, TransparentPushButton, SegmentedWidget, _PrimaryPushButton)
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas
from node_editor.node.report import ConfusionMatrix, ROC, PrecisionRecall, DET, DecisionBoundary
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout, QApplication)
from PySide6.QtCore import Qt

DEBUG = False

def scoring(Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """

    if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
        return {
            "Accuracy": "--",
            "Balanced accuracy": "--",
            "Micro Precision": "--",
            "Macro Precision": "--",
            "Weighted Precision": "--",
            "Micro Recall": "--",
            "Macro Recall": "--",
            "Weighted Recall": "--",
            "Micro F1 score": "--",
            "Macro F1 score": "--",
            "Weighted F1 score": "--",
            "Log loss": "--",
            "Brier score loss":"--",
            "Zero-one loss": "--",
        }
    
    else:
        accuracy = np.array([])
        balanced_accuracy = np.array([])
        micro_precision = np.array([])
        macro_precision = np.array([])
        weighted_precision = np.array([])
        micro_recall = np.array([])
        macro_recall = np.array([])
        weighted_recall = np.array([])
        micro_f1_score = np.array([])
        macro_f1_score = np.array([])
        weighted_f1_score = np.array([])
        log_loss = np.array([])
        brier_loss = np.array([])
        zero_one_loss = np.array([])

        for idx in range(len(Y)):
            accuracy = np.append(
                accuracy,
                metrics.accuracy_score(Y[idx], Y_pred[idx])
            )
            balanced_accuracy = np.append(
                balanced_accuracy,
                metrics.balanced_accuracy_score(Y[idx], Y_pred[idx])
            )
            micro_precision = np.append(
                micro_precision,
                metrics.precision_score(Y[idx], Y_pred[idx], average="micro"),
            )
            macro_precision = np.append(
                macro_precision,
                metrics.precision_score(Y[idx], Y_pred[idx], average="macro")
            )
            weighted_precision = np.append(
                weighted_precision,
                metrics.precision_score(Y[idx], Y_pred[idx], average="weighted")
            )
            micro_recall = np.append(
                micro_recall,
                metrics.recall_score(Y[idx], Y_pred[idx], average="micro")
            )
            macro_recall = np.append(
                macro_recall,
                metrics.recall_score(Y[idx], Y_pred[idx], average="macro")
            )
            weighted_recall = np.append(
                weighted_recall,
                metrics.recall_score(Y[idx], Y_pred[idx], average="weighted")
            )
            micro_f1_score = np.append(
                micro_f1_score,
                metrics.f1_score(Y[idx], Y_pred[idx], average="micro")
            )
            macro_f1_score = np.append(
                macro_f1_score,
                metrics.f1_score(Y[idx], Y_pred[idx], average="macro")
            )
            weighted_f1_score = np.append(
                weighted_f1_score,
                metrics.f1_score(Y[idx], Y_pred[idx], average="weighted")
            )
            try:
                log_loss = np.append(
                    log_loss,
                    metrics.log_loss(Y[idx], Y_pred[idx])
                )
                brier_loss = np.append(
                    brier_loss,
                    metrics.brier_score_loss(Y[idx], Y_pred[idx])
                )
            except: pass
            zero_one_loss = np.append(
                zero_one_loss,
                metrics.zero_one_loss(Y[idx], Y_pred[idx])
            )

        return {
            "Accuracy": f"{accuracy.mean():.2f} +/- {accuracy.std():.2f}",
            "Balanced accuracy": f"{balanced_accuracy.mean():.2f} +/- {balanced_accuracy.std():.2f}",
            "Micro Precision": f"{micro_precision.mean():.2f} +/- {micro_precision.std():.2f}",
            "Macro Precision": f"{macro_precision.mean():.2f} +/- {macro_precision.std():.2f}",
            "Weighted Precision": f"{weighted_precision.mean():.2f} +/- {weighted_precision.std():.2f}",
            "Micro Recall": f"{micro_recall.mean():.2f} +/- {micro_recall.std():.2f}",
            "Macro Recall": f"{macro_recall.mean():.2f} +/- {macro_recall.std():.2f}",
            "Weighted Recall": f"{weighted_recall.mean():.2f} +/- {weighted_precision.std():.2f}",
            "Micro F1 score": f"{micro_f1_score.mean():.2f} +/- {micro_f1_score.std():.2f}",
            "Macro F1 score": f"{macro_f1_score.mean():.2f} +/- {macro_f1_score.std():.2f}",
            "Weighted F1 score": f"{weighted_f1_score.mean():.2f} +/- {weighted_f1_score.std():.2f}",
            "Log loss": f"{log_loss.mean():.2f} +/- {log_loss.std():.2f}",
            "Brier score loss": f"{brier_loss.mean():.2f} +/- {brier_loss.std():.2f}",
            "Zero-one loss": f"{zero_one_loss.mean():.2f} +/- {zero_one_loss.std():.2f}"
        }

class Report(Dialog):
    def __init__(self, model, estimator, X, Y, X_test, Y_test, Y_pred, parent=None):
        """ X, Y, and Y_pred are nested lists """
        super().__init__(title="Metrics and Scoring",parent=parent)

        self.score_function = "Accuracy"

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

    def metrics(self, Y, Y_pred) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget.setLayout(layout)

        metric_to_show = PrimaryComboBox(
            items=["Accuracy","Balanced accuracy",
                   "Micro Precision","Macro Precision","Weighted Precision",
                   "Micro Recall","Macro Recall","Weighted Recall",
                   "Micro F1 score","Macro F1 score","Weighted F1 score",
                   "Log loss","Brier score loss","Zero-one loss"], 
            text="Metric"
        )
        metric_to_show.button.setMinimumWidth(250)
        metric_to_show.button.currentTextChanged.connect(self.change_metric)
        layout.addWidget(metric_to_show)

        score = scoring(Y, Y_pred)
        for metric in score:
            _btn = TransparentPushButton(text=metric)
            _btn.button.setText(str(score[metric]))
            layout.addWidget(_btn)


        return widget
