from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication)
from ui.base_widgets.button import ComboBox, _PrimaryPushButton
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, det_curve
from sklearn.preprocessing import LabelBinarizer
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier

class ConfusionMatrix (QWidget):
    def __init__(self, Y, Y_pred, parent=None):
        """ Y, and Y_pred are nested lists """
        super().__init__(parent=parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.fold = 0
        self.Y = Y
        self.Y_pred = Y_pred
        self.clipboard = QApplication.clipboard()   

        _fold = ComboBox(items=[f"Fold {i+1}" for i in range(len(Y))],
                        text="Fold")
        _fold.button.setCurrentText(f"Fold {self.fold+1}")
        _fold.button.currentTextChanged.connect(self.setFold)
        layout.addWidget(_fold)

        self.canvas = Canvas()
        for _ax in self.canvas.fig.axes: _ax.remove()
        layout.addWidget(self.canvas)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        btn_layout.addWidget(BodyLabel("Confusion Matrix"))
        self.cm = BodyLabel()
        btn_layout.addWidget(self.cm)
        
        copy_btn = _PrimaryPushButton()
        copy_btn.setText("Copy to clipboard")
        copy_btn.released.connect(lambda: self.clipboard.setText(self.cm.text()))
        btn_layout.addWidget(copy_btn)

        self.draw_plot()
    
    def setFold(self, fold:str):
        """ fold has the form of 'Fold 1' """
        self.fold = int(fold.split()[-1]) - 1
        self.draw_plot()
    
    def compute_matrix(self):
        if len(self.Y) == 0 or len(self.Y_pred) == 0: # check if Y or Y_pred is an empty list
            cm = np.array([[1,0],[0,1]])
        else: 
            cm = confusion_matrix(self.Y[self.fold], self.Y_pred[self.fold])

        self.cm.setText(str(cm))

        return cm

    def draw_plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        # Compute confusion matrix
        cm = self.compute_matrix()

        # drawing
        im = self.ax.imshow(cm, cmap="Greens", aspect='auto')
        self.ax.figure.colorbar(im, ax=self.ax)

        # show appropriate ticks
        self.ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           title="Confusion matrix",
           ylabel='True label',
           xlabel='Predicted label')
        # Rotate the tick labels and set their alignment.
        self.ax.set_xticklabels(self.ax.get_xticks(), 
                           rotation=45, 
                           ha="right", 
                           rotation_mode="anchor")
        
        # Loop over data dimensions and create text annotations.
        fmt = 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                self.ax.text(j, i, format(cm[i, j], fmt),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        self.canvas.fig.set_tight_layout("rect")
        self.canvas.draw_idle()


class ROC(QWidget):
    def __init__(self, model:OneVsOneClassifier|OneVsRestClassifier, 
                 X_test, Y_test, parent=None):
        """ X_test, and Y_test are nested lists """
        super().__init__(parent=parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.fold = 0
        self.model = model
        self.X_test = X_test
        self.Y_test = Y_test
        self.classes = model.classes_
        self.method = 0
        self.clipboard = QApplication.clipboard()   

        btn_layout2 = QHBoxLayout()
        layout.addLayout(btn_layout2)

        method = ComboBox(text="Method", items=["By Class","Micro-averaged OvR",
                                                "Macro-averaged OvR","Macro-averaged OvO"])
        method.button.currentTextChanged.connect(self.methodChange)
        btn_layout2.addWidget(method)

        self.class_ = ComboBox(text="Class", items=[f"{s} vs Rest" for s in self.classes])
        self.class_.button.currentTextChanged.connect(self.classChange)
        btn_layout2.addWidget(self.class_)

        self.canvas = Canvas()
        for _ax in self.canvas.fig.axes: _ax.remove()
        layout.addWidget(self.canvas)

        btn_layout1 = QHBoxLayout()
        layout.addLayout(btn_layout1)

        btn_layout1.addWidget(BodyLabel("False Positive Rate (X Axis)"))
        self.fpr = BodyLabel()
        btn_layout1.addWidget(self.fpr)
        
        copy_btn1 = _PrimaryPushButton()
        copy_btn1.setText("Copy to clipboard")
        copy_btn1.released.connect(lambda: self.clipboard.setText(self.fpr.text()))
        btn_layout1.addWidget(copy_btn1)

        btn_layout2 = QHBoxLayout()
        layout.addLayout(btn_layout2)

        btn_layout2.addWidget(BodyLabel("True Positive Rate (Y Axis)"))
        self.tpr = BodyLabel()
        btn_layout2.addWidget(self.tpr)
        
        copy_btn2 = _PrimaryPushButton()
        copy_btn2.setText("Copy to clipboard")
        copy_btn2.released.connect(lambda: self.clipboard.setText(self.tpr.text()))
        btn_layout2.addWidget(copy_btn2)

        self.draw_plot()
    
    def methodChange(self, method:str):
        
        match method:
            case "By Class": 
                self.class_.button.clear()
                self.class_.button.addItems([f"{s} vs Rest" for s in self.classes])
            case "Micro-averaged OvR":
                self.method = method
                self.class_.button.clear()
            case "Macro-averaged OvR":
                self.method = method
                self.class_.button.clear()
            case "Macro-averaged OvO":
                self.class_.button.clear()
                self.class_.button.addItems([str(s) for s in list(itertools.combinations(self.classes, 2))])

        self.draw_plot()

    def classChange(self, class_:str):
       
        if "vs Rest" in class_: 
            self.method = [f"{s} vs Rest" for s in self.classes].index(class_)
        if "," in class_:
            self.method = list(itertools.combinations(self.classes, 2))[[str(s) for s in list(itertools.combinations(self.classes, 2))].index(class_)]
            
        self.draw_plot()

    def compute_metrics(self):

        tprs = [0] * len(self.X_test)
        aucs = [0] * len(self.X_test)
        
        for fold in range(len(self.X_test)):
            try:
                Y_pred = self.model.predict_proba(self.X_test[fold])
            except:
                Y_pred = self.model.decision_function(self.X_test[fold])
            Y_true = LabelBinarizer().fit(self.classes).transform(self.Y_test[fold])
            
            if self.method == "Micro-averaged OvR":
                fpr, tpr, _ = self._compute(
                    Y_true.ravel(),
                    Y_pred.ravel(),
                )
                tprs[fold] = np.interp(np.linspace(0,1,100), fpr, tpr)
                aucs[fold] = self._computeAUC(fpr, tpr)

            elif self.method == "Macro-averaged OvR":
                fpr, tpr, roc_auc = dict(), dict(), dict()
                for i in range(self.model.n_classes_):
                    fpr[i], tpr[i], _ = self._compute(Y_true[:, i], Y_pred[:, i])
                    roc_auc[i] = self._computeAUC(fpr[i], tpr[i])
                fpr_grid = np.linspace(0, 1, 100)
                mean_tpr = np.zeros_like(fpr_grid)
                for i in range(self.model.n_classes_):
                    mean_tpr += np.interp(fpr_grid, fpr[i], tpr[i])
                mean_tpr /= self.model.n_classes_
                tprs[fold] = mean_tpr
                aucs[fold] = self._computeAUC(fpr_grid, mean_tpr)

            elif isinstance(self.method, int):
                fpr, tpr, _ = self._compute(
                    Y_true[:, self.method],
                    Y_pred[:, self.method],
                )
                fpr_grid = np.linspace(0, 1, 100)
                interp_tpr = np.interp(fpr_grid, fpr, tpr)
                interp_tpr[0] = 0.0
                tprs[fold] = interp_tpr
                aucs[fold] = self._computeAUC(fpr_grid, tprs[fold])
            
            elif isinstance(self.method, tuple):
                label_a, label_b = self.method
              
                a_mask = self.Y_test[fold] == label_a
                b_mask = self.Y_test[fold] == label_b
                ab_mask = np.logical_or(a_mask, b_mask)
               
                a_true = a_mask[ab_mask]
                b_true = b_mask[ab_mask]
                
                idx_a = np.flatnonzero(self.model.classes_ == label_a)[0]
                idx_b = np.flatnonzero(self.model.classes_ == label_b)[0]
              
                fpr_a, tpr_a, _ = self._compute(a_true, Y_pred[ab_mask.ravel(), idx_a])
                fpr_b, tpr_b, _ = self._compute(b_true, Y_pred[ab_mask.ravel(), idx_b])

                fpr_grid = np.linspace(0, 1, 100)
                mean_tpr = np.zeros_like(fpr_grid)
                mean_tpr += np.interp(fpr_grid, fpr_a, tpr_a)
                mean_tpr += np.interp(fpr_grid, fpr_b, tpr_b)
                mean_tpr /= 2
                tprs[fold] = mean_tpr
                aucs[fold] = self._computeAUC(fpr_grid, mean_tpr)

        return tprs, aucs

    def _compute(self, y_true, y_score):
        return roc_curve(y_true, y_score)
    
    def _computeAUC(self, x, y):
        return auc(x, y)
    
    def draw_plot(self): 

        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        # compute metrics
        tprs, aucs = self.compute_metrics()
        
        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_tpr[0] = 0.0
        mean_fpr = np.linspace(0, 1, len(mean_tpr))
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)

        # for fold, tpr in enumerate(tprs):
        #     self.ax.plot(
        #         mean_fpr,
        #         tpr,
        #         label=f"ROC fold {fold}",
        #         alpha=0.3,
        #         lw=1
        #     )
    
        self.ax.plot(
            mean_fpr,
            mean_tpr,
            color="b",
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
            lw=2,
            alpha=0.8,
        )

        if len(self.X_test) > 1:
            std_tpr = np.std(tprs, axis=0)
            tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
            tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
            self.ax.fill_between(
                mean_fpr,
                tprs_lower,
                tprs_upper,
                color="grey",
                alpha=0.2,
                label=r"$\pm$ 1 std. dev.",
            )

        self.ax.plot([0,1],[0,1],"k--",label="Random")
        self.ax.set_xlim([-0.05, 1.05])
        self.ax.set_ylim([-0.05, 1.05])
        self.ax.set_xlabel('False Positive Rate')
        self.ax.set_ylabel('True Positive Rate')
        self.ax.set_title('Receiver Operating Characteristic (ROC) Curve')
        self.ax.legend()

        # self.canvas.fig.set_tight_layout("rect")
        self.canvas.draw_idle()

class PrecisionRecall(ROC):
    def __init__(self, model:OneVsOneClassifier|OneVsRestClassifier,
                 X_test, Y_test, parent=None):
        super().__init__(model, X_test, Y_test, parent)

    def _compute(self, y_true, y_score):
        return precision_recall_curve(y_true, y_score)
    
    def draw_plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        # compute metrics
        precs, aucs = self.compute_metrics()
        
        mean_prec = np.mean(precs, axis=0)
        mean_prec[0] = 1.0
        mean_recall = np.linspace(0, 1, len(mean_prec))
        mean_auc = auc(mean_recall, mean_prec)
        std_auc = np.std(aucs)

        # for fold, prec in enumerate(precs):
        #     self.ax.plot(
        #         mean_fpr,
        #         prec,
        #         label=f"PR fold {fold}",
        #         alpha=0.3,
        #         lw=1
        #     )
    
        self.ax.plot(
            mean_recall,
            mean_prec,
            color="b",
            label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
            lw=2,
            alpha=0.8,
        )

        if len(self.X_test) > 1:
            std_prec = np.std(precs, axis=0)
            precs_upper = np.minimum(mean_prec + std_prec, 1)
            precs_lower = np.maximum(mean_prec - std_prec, 0)
            self.ax.fill_between(
                mean_recall,
                precs_lower,
                precs_upper,
                color="grey",
                alpha=0.2,
                label=r"$\pm$ 1 std. dev.",
            )

        self.ax.set_xlim([-0.05, 1.05])
        self.ax.set_ylim([-0.05, 1.05])
        self.ax.set_xlabel('Recall')
        self.ax.set_ylabel('Precision')
        self.ax.set_title('Precision Recall (PR) Curve')
        self.ax.legend()

        # self.canvas.fig.set_tight_layout("rect")
        self.canvas.draw_idle()

class DET(ROC):
    def __init__(self, model:OneVsOneClassifier|OneVsRestClassifier,
                 X_test, Y_test, parent=None):
        super().__init__(model, X_test, Y_test, parent)

    def _compute(self, y_true, y_score):
        return det_curve(y_true, y_score)
    
    def _computeAUC(self, x, y):
        return

    def draw_plot(self): 

        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        # compute metrics
        tnrs, _ = self.compute_metrics()
        
        mean_tnr = np.mean(tnrs, axis=0)
        mean_fpr = np.linspace(0, 1, len(mean_tnr))

        # for fold, tnr in enumerate(tnrs):
        #     self.ax.plot(
        #         mean_fpr,
        #         tnr,
        #         label=f"DET fold {fold}",
        #         alpha=0.3,
        #         lw=1
        #     )
    
        self.ax.plot(
            mean_fpr,
            mean_tnr,
            color="b",
            label="Mean DET",
            lw=2,
            alpha=0.8,
        )

        if len(self.X_test) > 1:
            std_tnr = np.std(tnrs, axis=0)
            tnrs_upper = np.minimum(mean_tnr + std_tnr, 1)
            tnrs_lower = np.maximum(mean_tnr - std_tnr, 0)
            self.ax.fill_between(
                mean_fpr,
                tnrs_lower,
                tnrs_upper,
                color="grey",
                alpha=0.2,
                label=r"$\pm$ 1 std. dev.",
            )

        self.ax.set_xlim([-0.05, 1.05])
        self.ax.set_ylim([-0.05, 1.05])
        self.ax.set_xlabel('False Positive Rate')
        self.ax.set_ylabel('False Negative Rate')
        self.ax.set_title("Detection Error Tradeoff (DET) Curve")
        self.ax.legend()

        # self.canvas.fig.set_tight_layout("rect")
        self.canvas.draw_idle()

