from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QApplication)
from ui.base_widgets.button import ComboBox, _PrimaryPushButton
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc

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
        self.canvas.fig.set_edgecolor("black")
        self.canvas.fig.set_linewidth(2)
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
        self.canvas.draw()


class ROC(QWidget):
    def __init__(self, Y, Y_pred_proba, parent=None):
        """ Y, and Y_pred are nested lists """
        super().__init__(parent=parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)

        self.fold = 0
        self.Y = Y
        self.Y_pred_proba = Y_pred_proba
        self.clipboard = QApplication.clipboard()   

        _fold = ComboBox(items=[f"Fold {i+1}" for i in range(len(Y))],
                        text="Fold")
        _fold.button.setCurrentText(f"Fold {self.fold+1}")
        _fold.button.currentTextChanged.connect(self.setFold)
        layout.addWidget(_fold)

        self.canvas = Canvas()
        self.canvas.fig.set_edgecolor("black")
        self.canvas.fig.set_linewidth(2)
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

    
    def setFold(self, fold:str):
        """ fold has the form of 'Fold 1' """
        self.fold = int(fold.split()[-1]) - 1
        self.draw_plot()
    
    def compute_roc(self):
        if len(self.Y) == 0 or len(self.Y_pred_proba) == 0: # check if Y or Y_pred is an empty list
            fpr, tpr = [[0,0,1]], [[0,1,1]]
            roc_auc = [1]
        else:
            print(self.Y[self.fold])
            n_classes = 3
            print(n_classes)
            fpr = [0] * n_classes
            tpr = [0] * n_classes
            roc_auc = [0] * n_classes

            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(self.Y[self.fold][:,i], 
                                              self.Y_pred_proba[self.fold][:,1]) 
                roc_auc[i] = auc(fpr[i], tpr[i])

        self.fpr.setText(str(fpr))
        self.tpr.setText(str(tpr))

        return fpr, tpr, roc_auc
    
    def draw_plot(self): 

        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        # Compute ROC metrics
        _fpr, _tpr, _roc_auc = self.compute_roc()   
        index = 0
        for fpr, tpr, roc_auc in zip(_fpr, _tpr, _roc_auc):
            self.ax.plot(fpr, tpr, marker='o', 
                    label=f"ROC curve class {index}(area = {roc_auc:.2f})")
            index += 1

        self.ax.plot([0,1],[0,1],"k--",label="Random")
        self.ax.set_xlim([-0.05, 1.05])
        self.ax.set_ylim([-0.05, 1.05])
        self.ax.set_xlabel('False Positive Rate')
        self.ax.set_ylabel('True Positive Rate')
        self.ax.set_title('ROC Curve')
        self.ax.legend()

        self.canvas.fig.set_tight_layout("rect")
        self.canvas.draw()

