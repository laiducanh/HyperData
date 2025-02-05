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
from sklearn.decomposition import PCA
from sklearn.metrics import (rand_score, adjusted_rand_score, mutual_info_score, fowlkes_mallows_score,
                             adjusted_mutual_info_score, homogeneity_score, completeness_score,
                             silhouette_score,calinski_harabasz_score, davies_bouldin_score)
import matplotlib.pyplot as plt

class Variance(QWidget):
    def __init__(self, model:PCA, parent=None):
        super().__init__(parent)

        self.model = model

        layout = QVBoxLayout(self)

        self.plot = PrimaryComboBox(items=["Explained variance","Explained variance ratio",
                                           "Singular values"], text="Plot Type")
        self.plot.button.currentTextChanged.connect(self.draw_plot)
        layout.addWidget(self.plot)

        self.canvas = Canvas()
        layout.addWidget(self.canvas)
        self.draw_plot()
    
    def draw_plot(self):
        # clear plot
        self.canvas.fig.clear()

        # add axis
        self.ax = self.canvas.fig.add_subplot()

        n_components = self.model.n_components_
        if self.plot.button.currentText() == "Explained variance":
            explained_variance_ = self.model.explained_variance_
            self.ax.bar(
                range(1, n_components+1), 
                explained_variance_,
                label="Individual explained variance",
            )
            self.ax.set_xlabel("Principal components")
            self.ax.set_ylabel("Explained variance")
        elif self.plot.button.currentText() == "Explained variance ratio":
            explained_variance_ratio_ = self.model.explained_variance_ratio_
            cum_var = np.cumsum(explained_variance_ratio_)
            self.ax.bar(
                range(1, n_components+1), 
                explained_variance_ratio_,
                label="Individual explained variance ratio"
            )
            self.ax.plot(
                range(1, n_components+1),
                cum_var,
                color="red",
                label="Cumulative explained variance ratio"
            )
            self.ax.set_xlabel("Principal components")
            self.ax.set_ylabel("Explained variance ratio")
        elif self.plot.button.currentText() == "Singular values":
            singular_values_ = self.model.singular_values_
            self.ax.bar(
                range(1, n_components+1),
                singular_values_,
                label="Individual singular value"
            )
            self.ax.set_xlabel("Principal components")
            self.ax.set_ylabel("Singular value")
        
        self.ax.legend()
        self.canvas.draw_idle()

class Projection(QWidget):
    def __init__(self, X_reduced:np.ndarray, Y, parent=None):
        super().__init__(parent)

        self.X_reduced = X_reduced
        self.Y = Y

        layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.plot = PrimaryComboBox(items=["2D projection","3D projection"], text="Plot Type")
        self.plot.button.currentTextChanged.connect(self.change_plot)
        btn_layout.addWidget(self.plot)

        self.x_btn = ComboBox(items=[f"Eigenvector {i+1}" for i in range(self.X_reduced.shape[1])],
                              text="X")
        self.x_btn.button.currentTextChanged.connect(self.change_plot)
        btn_layout.addWidget(self.x_btn)

        self.y_btn = ComboBox(items=[f"Eigenvector {i+1}" for i in range(self.X_reduced.shape[1])],
                              text="Y")
        self.y_btn.button.currentTextChanged.connect(self.change_plot)
        btn_layout.addWidget(self.y_btn)

        self.z_btn = ComboBox(items=[f"Eigenvector {i+1}" for i in range(self.X_reduced.shape[1])],
                              text="Z")
        self.z_btn.button.currentTextChanged.connect(self.change_plot)
        btn_layout.addWidget(self.z_btn)

        self.canvas = Canvas()
        layout.addWidget(self.canvas)
        self.change_plot()
    
    def change_plot(self):
        # clear plot
        self.canvas.fig.clear()

        if self.plot.button.currentText() == "2D projection":
            self.z_btn.hide()
            self.ax = self.canvas.fig.add_subplot()
        elif self.plot.button.currentText() == "3D projection":
            self.z_btn.show()
            self.ax = self.canvas.fig.add_subplot(projection="3d")

        self.draw_plot()
    
    def draw_plot(self):
        if self.plot.button.currentText() == "2D projection":
            scatter = self.ax.scatter(
                self.X_reduced[:, self.x_btn.button.currentIndex()],
                self.X_reduced[:, self.y_btn.button.currentIndex()],
                c=self.Y,
            )
        elif self.plot.button.currentText() == "3D projection":
            scatter = self.ax.scatter(
                self.X_reduced[:, self.x_btn.button.currentIndex()],
                self.X_reduced[:, self.y_btn.button.currentIndex()],
                self.X_reduced[:, self.z_btn.button.currentIndex()],
                c=self.Y
            )
            self.ax.set(zlabel=f"Eigenvector {self.z_btn.button.currentIndex()+1}")
            self.ax.zaxis.set_ticklabels([])

        self.ax.set_xlabel(f"Eigenvector {self.x_btn.button.currentIndex()+1}")
        self.ax.set_ylabel(f"Eigenvector {self.y_btn.button.currentIndex()+1}")
        self.ax.xaxis.set_ticklabels([])
        self.ax.yaxis.set_ticklabels([])

        # Add a legend
        legend1 = self.ax.legend(
            scatter.legend_elements()[0],
            self.Y[0].unique(),
            title="Classes",
        )
        self.ax.add_artist(legend1)
        self.canvas.draw_idle()

class Report(Dialog):
    def __init__(self, model, X_reduced, Y, parent=None):
        super().__init__(title="Clustering",parent=parent)

        self.segment_widget = SegmentedWidget()
        self.main_layout.addWidget(self.segment_widget)

        self.segment_widget.addButton(text='Explained Variance', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment_widget.addButton(text='Projection', func=lambda: self.stackedlayout.setCurrentIndex(1))
        

        self.stackedlayout = QStackedLayout()
        self.main_layout.addLayout(self.stackedlayout)

        self.variance = Variance(model, self)
        self.stackedlayout.addWidget(self.variance)

        self.projection = Projection(X_reduced, Y, self)
        self.stackedlayout.addWidget(self.projection)

        self.stackedlayout.setCurrentIndex(0)
        self.segment_widget.setCurrentWidget("Explained Variance")