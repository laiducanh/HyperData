import numpy as np
import pandas as pd
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HPrimaryComboBox, HTransparentComboBox, SegmentedWidget
from ui.base_widgets.text import BodyLabel
from ui.base_widgets.frame import SeparateHLine
from plot.canvas import Canvas
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout
from PySide6.QtCore import Qt
from sklearn import cluster
from sklearn.metrics import (rand_score, adjusted_rand_score, mutual_info_score, fowlkes_mallows_score,
                             adjusted_mutual_info_score, homogeneity_score, completeness_score,
                             silhouette_score,calinski_harabasz_score, davies_bouldin_score)
import matplotlib.pyplot as plt

def scoring(X, labels_true, labels_pred, metric='Rand Index'):
    try:
        if metric == 'Rand Index':
            return f"{rand_score(labels_true, labels_pred):.2f}"
        elif metric == 'Adjusted Rand Index':
            return f"{adjusted_rand_score(labels_true, labels_pred):.2f}"
        elif metric == 'Mutual Information Score':
            return f"{mutual_info_score(labels_true, labels_pred):.2f}"
        elif metric == 'Adjusted Mutual Information Score':
            return f"{adjusted_mutual_info_score(labels_true, labels_pred):.2f}"
        elif metric == 'Homogeneity':
            return f"{homogeneity_score(labels_true, labels_pred):.2f}"
        elif metric == 'Completeness':
            return f"{completeness_score(labels_true, labels_pred):.2f}"
        elif metric == 'Fowlkes-Mallows Score':
            return f"{fowlkes_mallows_score(labels_true, labels_pred):.2f}"
        elif metric == 'Silhouette Coefficient':
            return f"{silhouette_score(X, labels_pred):.2f}"
        elif metric == 'Calinski-Harabasz Index':
            return f"{calinski_harabasz_score(X, labels_pred):.2f}"
        elif metric == 'Davies-Douldin Index':
            return f"{davies_bouldin_score(X, labels_pred):.2f}"
    except Exception as e:
        logger.exception(e)
        return '--'

def attributes(model):
    attrs = {
        "Number of samples": len(model.labels_),
        "Number of features": model.n_features_in_,
        "Number of clusters": len(set(model.labels_)),
    }
    if isinstance(model, cluster.KMeans):
        attrs.update({
            # "Cluster centers": str(model.cluster_centers_),
            "Inertial": model.inertia_,
            "Iterations run": model.n_iter_,
            "Converged": len(set(model.labels_)) == model.cluster_centers_.shape[0]
        })
    elif isinstance(model, cluster.AffinityPropagation):
        attrs.update({
            # "Cluster centers": str(model.cluster_centers_),
            # "Affinity matrix": str(model.affinity_matrix_),
            "Iterations run": model.n_iter_,
            "Converged": len(set(model.labels_)) == model.cluster_centers_.shape[0]
        })
    elif isinstance(model, cluster.AgglomerativeClustering):
        attrs.update({
            "Number of leaves": model.n_leaves_,
            "Number of connected components": model.n_connected_components_,
        })
    elif isinstance(model, cluster.MeanShift):
        attrs.update({
            # "Cluster centers": str(model.cluster_centers_),
            "Iterations run": model.n_iter_,
            "Converged": len(set(model.labels_)) == model.cluster_centers_.shape[0]
        })
    elif isinstance(model, cluster.OPTICS):
        attrs.update({
            "Noisy samples": np.sum(model.labels_==-1),
        })
    elif isinstance(model, cluster.DBSCAN):
        pass
    elif isinstance(model, cluster.HDBSCAN):
        attrs.update({
            "Noisy samples": np.sum(model.labels_==-1),
            "Infinite samples": np.sum(model.labels_==-2),
            "Missing data samples": np.sum(model.labels_==-3),
        })
    elif isinstance(model, cluster.SpectralClustering):
        attrs.update({
            # "Affinity matrix": str(model.affinity_matrix_),
        })
    elif isinstance(model, cluster.Birch):
        attrs.update({
            # "Centroids of all subclusters": str(model.subcluster_centers_),
        })
    elif isinstance(model, cluster.BisectingKMeans):
        attrs.update({
            # "Cluster centers": str(model.cluster_centers_),
            "Inertial": model.inertia_,
            "Converged": len(set(model.labels_)) == model.cluster_centers_.shape[0]
        })
    
    return attrs

class Visualization(QWidget):
    def __init__(self, model, X:pd.DataFrame, parent=None):
        super().__init__(parent)

        self.model = model
        self.X = X

        layout = QVBoxLayout(self)

        hlayout = QHBoxLayout()
        layout.addLayout(hlayout)

        self.x_btn = HTransparentComboBox(items=list(self.X.columns[:-1]), label="X")
        self.x_btn.button.currentIndexChanged.connect(self.draw_plot)
        hlayout.addWidget(self.x_btn)

        self.y_btn = HTransparentComboBox(items=list(self.X.columns[:-1]), label="Y")
        self.y_btn.button.setCurrentIndex(1)
        self.y_btn.button.currentIndexChanged.connect(self.draw_plot)
        hlayout.addWidget(self.y_btn)

        self.canvas = Canvas()
        layout.addWidget(self.canvas)
        self.draw_plot()
    
    def draw_plot(self):
        # clear plot
        self.canvas.figure.clear()

        # add axis
        self.ax = self.canvas.figure.add_subplot()

        n_clusters = len(set(self.model.labels_))
        colors = plt.cycler("color", plt.cm.viridis(np.linspace(0, 1, n_clusters)))

        for k, col in zip(range(n_clusters), colors):
            class_members = self.model.labels_ == k
            self.ax.scatter(
                self.X.iloc[class_members, self.x_btn.button.currentIndex()], 
                self.X.iloc[class_members, self.y_btn.button.currentIndex()],
                color=col["color"],
                alpha=0.7,
                label=f"Cluster {k+1}"
            )              

        self.ax.set_xlabel(self.x_btn.button.currentText())
        self.ax.set_ylabel(self.y_btn.button.currentText())
        self.ax.set_title("Clustering")
        self.ax.legend(
            loc='upper left', 
            bbox_to_anchor=(0, -0.1, 1, -0.), 
            ncols=np.ceil(n_clusters/3),
            mode='expand',
            frameon=False
        )
        self.canvas.figure.tight_layout()
        self.canvas.draw_idle()
    
class Metrics(QWidget):
    def __init__(self, model, X:pd.DataFrame, labels_true, score_function, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.model = model
        self.score_function = score_function
        self.X = X
        self.labels_true = labels_true

        metric_to_show = HPrimaryComboBox(
            items=["Rand Index","Adjusted Rand Index","Mutual Information Score",
                   "Adjusted Mutual Information Score","Homogeneity","Completeness",
                   "Fowlkes-Mallows Score","Silhouette Coefficient",
                   "Calinski-Harabasz Index","Davies-Douldin Index"],
            getter=lambda: self.score_function,
            setter=self.change_metric,
            label="Metric",
            layout=layout
        )
        metric_to_show.button.setMinimumWidth(250)
        layout.addWidget(SeparateHLine())

        self.score = BodyLabel(f'Score: {scoring(X, labels_true, model.labels_, self.score_function)}')
        layout.addWidget(self.score)

        for key, value in attributes(model).items():
            layout.addWidget(SeparateHLine())
            layout.addWidget(BodyLabel(f'{key}: {value}'))

    def change_metric(self, metric:str):
        self.score_function = metric
        self.score.setText(f'Score: {scoring(self.X, self.labels_true, self.model.labels_, self.score_function)}')

class Report(Dialog):
    def __init__(self, model, X:pd.DataFrame, labels_true, score_function, parent=None):
        super().__init__(title="Clustering",parent=parent)

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Metrics', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Plot', func=lambda: self.stackedlayout.setCurrentIndex(1))
        

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        self.metrics = Metrics(model, X, labels_true, score_function, self)
        self.stackedlayout.addWidget(self.metrics)

        self.visualization = Visualization(model, X, self)
        self.stackedlayout.addWidget(self.visualization)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Metrics")



        
    

        