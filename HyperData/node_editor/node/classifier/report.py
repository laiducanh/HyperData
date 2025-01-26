import numpy as np
from sklearn import metrics
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (PrimaryComboBox, TransparentPushButton, SegmentedWidget, _PrimaryPushButton)
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas
from node_editor.node.report import ConfusionMatrix, ROC
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout, QApplication)

DEBUG = False

def scoring(Y=list(), Y_pred=list()):
    """ Y and Y_pred are nested lists """

    if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
        return {
            "Accuracy": "--",
        }
    
    else:
        accuracy = np.array([])

        for idx in range(len(Y)):
            accuracy = np.append(
                accuracy,
                metrics.accuracy_score(Y[idx], Y_pred[idx])
            )

        return {
            "Accuracy": accuracy.mean(),
        }

class Report(Dialog):
    def __init__(self, model, X, Y, Y_pred, parent=None):
        """ X, Y, and Y_pred are nested lists """
        super().__init__(title="Metrics and Scoring",parent=parent)

        self.score_function = "Accuracy"

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.clipboard = QApplication.clipboard()

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

        # roc = self.roc(model, X, Y)
        # self.stackedlayout.addWidget(roc)

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

        metric_to_show = PrimaryComboBox(
            items=["Accuracy","Balanced accuracy","Average precision",
                   "Brier score loss","F1 score",], 
            text="Metric"
        )
        metric_to_show.button.currentTextChanged.connect(self.change_metric)
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

        _fold = PrimaryComboBox(
            items=[f"Fold {i+1}" for i in range(len(Y))],
            text="Fold"
        )
        _fold.button.setCurrentText(f"Fold {fold+1}")
        layout.addWidget(_fold)

        # Compute confusion matrix
        if len(Y) == 0 or len(Y_pred) == 0: # check if Y or Y_pred is an empty list
            cm = np.array([[1,0],[0,1]])
        else: 
            cm = metrics.confusion_matrix(Y[fold], Y_pred[fold])
        
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
        
    def roc(self, estimator, X, Y) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        widget.setLayout(layout)

        canvas = Canvas()
        for _ax in canvas.fig.axes: _ax.remove()
        ax = canvas.fig.add_subplot()
        canvas.fig.set_edgecolor("black")
        canvas.fig.set_linewidth(2)

        # calculate ROC metrics
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        for fold in range(len(X)):
        # if len(X) and len(Y): # check if X or Y is an empty list
            viz = metrics.RocCurveDisplay.from_estimator(
                estimator, 
                X[fold], 
                Y[fold],
                name=f"ROC fold {fold}",
                alpha=0.3,
                lw=1,
                ax=ax,
                plot_chance_level=(fold==0), # only plot 1 chance line
            )
            interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
            interp_tpr[0] = 0.0
            tprs.append(interp_tpr)
            aucs.append(viz.roc_auc)
        
        if fold > 0:
            mean_tpr = np.mean(tprs, axis=0)
            mean_tpr[-1] = 1.0
            mean_auc = metrics.auc(mean_fpr, mean_tpr)
            std_auc = np.std(aucs)
            ax.plot(
                mean_fpr,
                mean_tpr,
                color="b",
                label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
                lw=2,
                alpha=0.8,
            )
            std_tpr = np.std(tprs, axis=0)
            tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
            tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
            ax.fill_between(
                mean_fpr,
                tprs_lower,
                tprs_upper,
                color="grey",
                alpha=0.2,
                label=r"$\pm$ 1 std. dev.",
            )
        # else:
        #     fpr, tpr = [0,0,1], [0,1,1]
        #     roc_auc = 1
        
        
        # ax.plot(fpr, tpr, marker='o', 
        #         label=f"ROC curve (area = {roc_auc:.2f})")
        # ax.plot([0,1],[0,1],"k--",label="Random")
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

        # btn_layout1.addWidget(BodyLabel("False Positive Rate (X Axis)"))
        # btn_layout1.addWidget(BodyLabel(str(fpr)))
        
        # copy_btn1 = _PrimaryPushButton()
        # copy_btn1.setText("Copy to clipboard")
        # copy_btn1.released.connect(lambda: self.clipboard.setText(str(fpr)))
        # btn_layout1.addWidget(copy_btn1)

        # btn_layout2 = QHBoxLayout()
        # layout.addLayout(btn_layout2)

        # btn_layout2.addWidget(BodyLabel("True Positive Rate (Y Axis)"))
        # btn_layout2.addWidget(BodyLabel(str(tpr)))
        
        # copy_btn2 = _PrimaryPushButton()
        # copy_btn2.setText("Copy to clipboard")
        # copy_btn2.released.connect(lambda: self.clipboard.setText(str(tpr)))
        # btn_layout2.addWidget(copy_btn2)


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
            precision, recall, _ = metrics.precision_recall_curve(Y, Y_pred)
            pr_auc = metrics.auc(recall, precision)

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
    