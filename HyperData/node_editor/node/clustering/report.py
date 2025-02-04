import numpy as np
import pandas as pd
from sklearn import metrics, preprocessing
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import (PrimaryComboBox, ComboBox, Toggle, SegmentedWidget,
                                    TransparentPushButton)
from ui.base_widgets.text import BodyLabel
from plot.canvas import Canvas
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout, QApplication)
from PySide6.QtCore import Qt
from sklearn.cluster import KMeans
from sklearn.metrics import (rand_score, adjusted_rand_score, mutual_info_score, fowlkes_mallows_score,
                             adjusted_mutual_info_score, homogeneity_score, completeness_score,
                             silhouette_score,calinski_harabasz_score, davies_bouldin_score)
import matplotlib.pyplot as plt

def scoring(X, labels_true, labels_pred):
    return {
            "Rand Index": f"{rand_score(labels_true, labels_pred):.2f}",
            "Adjusted Rand Index": f"{adjusted_rand_score(labels_true, labels_pred):.2f}",
            "Mutual Information Score": f"{mutual_info_score(labels_true, labels_pred):.2f}",
            "Adjusted Mutual Information Score": f"{adjusted_mutual_info_score(labels_true, labels_pred):.2f}",
            "Homogeneity": f"{homogeneity_score(labels_true, labels_pred):.2f}",
            "Completeness": f"{completeness_score(labels_true, labels_pred):.2f}",
            "Fowlkes-Mallows Score": f"{fowlkes_mallows_score(labels_true, labels_pred):.2f}",
            "Silhouette Coefficient": f"{silhouette_score(X, labels_pred):.2f}",
            "Calinski-Harabasz Index": f"{calinski_harabasz_score(X, labels_pred):.2f}",
            "Davies-Douldin Index": f"{davies_bouldin_score(X, labels_pred):.2f}"
        }

class Visualization(QWidget):
    def __init__(self, model:KMeans, X:pd.DataFrame, parent=None):
        super().__init__(parent)

        self.model = model
        self.X = X

        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.plot = PrimaryComboBox(items=["Scatter","Fireworks"], text="Plot Type")
        self.plot.button.currentTextChanged.connect(self.draw_plot)
        btn_layout.addWidget(self.plot)

        self.x_btn = ComboBox(items=list(self.X.columns), text="X")
        self.x_btn.button.currentTextChanged.connect(self.draw_plot)
        btn_layout.addWidget(self.x_btn)

        self.y_btn = ComboBox(items=list(self.X.columns), text="Y")
        self.y_btn.button.setCurrentIndex(1)
        self.y_btn.button.currentTextChanged.connect(self.draw_plot)
        btn_layout.addWidget(self.y_btn)

        self.legend_toggle = Toggle(text="Label")
        self.legend_toggle.button.checkedChanged.connect(self.draw_plot)
        btn_layout.addWidget(self.legend_toggle)

        self.canvas = Canvas()
        layout.addWidget(self.canvas)
        self.draw_plot()
    
    def draw_plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        n_clusters = len(set(self.model.labels_))
        colors = plt.cycler("color", plt.cm.viridis(np.linspace(0, 1, n_clusters)))

        if self.plot.button.currentText() == "Scatter":
            for k, col in zip(range(n_clusters), colors):
                class_members = self.model.labels_ == k
                self.ax.scatter(
                    self.X.iloc[class_members, self.x_btn.button.currentIndex()], 
                    self.X.iloc[class_members, self.y_btn.button.currentIndex()],
                    color=col["color"],
                    alpha=0.7,
                    label=f"Cluster {k+1}"
                )
            self.ax.scatter(
                self.model.cluster_centers_[:, self.x_btn.button.currentIndex()],
                self.model.cluster_centers_[:, self.y_btn.button.currentIndex()],
                c='black',
                s=300,
                marker='x',
            )
        elif self.plot.button.currentText() == "Fireworks":
            for k, col in zip(range(n_clusters), colors):
                class_members = self.model.labels_ == k

                self.ax.scatter(
                    self.X.iloc[class_members, self.x_btn.button.currentIndex()], 
                    self.X.iloc[class_members, self.y_btn.button.currentIndex()],
                    color=col["color"],
                    s=10,
                    label=f"Cluster {k+1}"
                )

                x0 = self.model.cluster_centers_[:, self.x_btn.button.currentIndex()][k]
                y0 = self.model.cluster_centers_[:, self.y_btn.button.currentIndex()][k]
                self.ax.scatter(
                    x0,
                    y0,
                    color=col["color"],
                    s=30,
                    marker='o'
                )
                for x, y in zip(
                    self.X.iloc[class_members, self.x_btn.button.currentIndex()],
                    self.X.iloc[class_members, self.y_btn.button.currentIndex()]
                ):
                    self.ax.plot(
                        [x0, x], [y0, y],
                        color=col["color"],
                        alpha=0.5
                    )

        self.ax.set_xlabel(self.x_btn.button.currentText())
        self.ax.set_ylabel(self.y_btn.button.currentText())
        self.ax.set_title("Clustering")
        if self.legend_toggle.button.isChecked(): self.ax.legend()
        self.canvas.draw_idle()
    
class Metrics(QWidget):
    def __init__(self, model:KMeans, X:pd.DataFrame, labels_true, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.score_function = "Rand Index"

        metric_to_show = PrimaryComboBox(
            items=["Rand Index","Adjusted Rand Index","Mutual Information Score",
                   "Adjusted Mutual Information Score","Homogeneity","Completeness",
                   "Fowlkes-Mallows Score","Silhouette Coefficient",
                   "Calinski-Harabasz Index","Davies-Douldin Index"], 
            text="Metric"
        )
        metric_to_show.button.setMinimumWidth(250)
        metric_to_show.button.currentTextChanged.connect(self.change_metric)
        layout.addWidget(metric_to_show)

        score = scoring(X, labels_true, model.labels_)
        for metric in score:
            _btn = TransparentPushButton(text=metric)
            _btn.button.setText(str(score[metric]))
            layout.addWidget(_btn)

    def change_metric(self, metric:str):
        self.score_function = metric

class Report(Dialog):
    def __init__(self, model:KMeans, X:pd.DataFrame, labels_true, parent=None):
        super().__init__(title="Clustering",parent=parent)

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Visualization', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(1))
        

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        self.visualization = Visualization(model, X, self)
        self.stackedlayout.addWidget(self.visualization)

        self.metrics = Metrics(model, X, labels_true, self)
        self.stackedlayout.addWidget(self.metrics)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")



        
    

        