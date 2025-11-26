from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.clustering.report import Report, scoring
from node_editor.node.clustering.base import MethodBase
from node_editor.node.clustering.kmeans import KMeans
from node_editor.node.clustering.affinity import AffinityPropagation
from node_editor.node.clustering.mean_shift import MeanShift
from node_editor.node.clustering.spectral import SpectralClustering
from node_editor.node.clustering.agglomerative import AgglomerativeClustering
from node_editor.node.clustering.bisecting_kmeans import BisectingKMeans
from node_editor.node.clustering.dbscan import DBSCAN
from node_editor.node.clustering.hdbscan import HDBSCAN
from node_editor.node.clustering.optics import OPTICS
from node_editor.node.clustering.birch import Birch
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentPushButton, HPrimaryComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from PySide6.QtWidgets import QStackedLayout
from PySide6.QtGui import QAction
from sklearn import cluster

DEBUG = False
        
class Clustering(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Features")
        self.node.input_sockets[1].setSocketLabel("Labels")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Rand Index"

        self._config = dict(
            method = "K-Means",
            config = dict(),
        )

        self.method_list = ["K-Means","Affinity Propagation","Mean Shift","Spectral Clustering",
                            "Agglomerative Clustering","Bisecting K-Means","Density-based Clustering",
                            "Hierarchical Density-based Clustering","OPTICS","Birch"]

        self.model = cluster.KMeans(**self._config["config"])
        self.X = pd.DataFrame()
    
    def initMenu(self):
        action = QAction("Execute Card",self.menu)
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = QAction("View Output",self.menu)
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        action = QAction("Configuration",self.menu)
        action.triggered.connect(self.config)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Score", self.menu)
        action.triggered.connect(self.score_dialog)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Show Comment",self.menu)
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = QAction("Hide Comment",self.menu)
        action.triggered.connect(self.comment.hide)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Save Data", self.menu)
        action.triggered.connect(self.saveData)
        self.menu.addAction(action)
        action = QAction("Delete Card",self.menu)
        action.triggered.connect(lambda: self.parent.deleteSelected())
        self.menu.addAction(action)

    
    def currentWidget(self) -> MethodBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        method = HPrimaryComboBox(
            items=self.method_list,label="Method",
            getter=lambda: self._config['method'],
            setter=lambda s: self.stackedlayout.setCurrentIndex(self.method_list.index(s)),
            layout=dialog.main_layout
        )
        method.button.setMinimumWidth(250)
        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(KMeans())
        self.stackedlayout.addWidget(AffinityPropagation())
        self.stackedlayout.addWidget(MeanShift())
        self.stackedlayout.addWidget(SpectralClustering())
        self.stackedlayout.addWidget(AgglomerativeClustering())
        self.stackedlayout.addWidget(BisectingKMeans())
        self.stackedlayout.addWidget(DBSCAN())
        self.stackedlayout.addWidget(HDBSCAN())
        self.stackedlayout.addWidget(OPTICS())
        self.stackedlayout.addWidget(Birch())
        self.stackedlayout.setCurrentIndex(self.method_list.index(method.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                method = method.button.currentText()
            )
            self.model = self.currentWidget().method
            self.exec()


    def func(self):
        # reset UI
        self.score_btn.setText(f"Score: --")
        self.label.setText('Shape: (--, --)') 
        self.progress.changeColor('success')
        self.data_to_view = pd.DataFrame()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection
            X, Y = datasets.make_blobs(
                n_samples=300, 
                centers=3, 
                n_features=10, 
                cluster_std=[1.0, 2.5, 0.5],  # different spread for each cluster
                random_state=42
            )
            self.node.input_sockets[0].socket_data = pd.DataFrame(X)
            self.node.input_sockets[1].socket_data = pd.DataFrame(Y)
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            columms = self.node.input_sockets[0].socket_data.columns
            self.X = self.node.input_sockets[0].socket_data
            self.model.fit(self.X)
            self.X["Prediction"] = self.model.labels_
            data = self.X.copy()

            score = scoring(
                self.X, 
                self.node.input_sockets[1].socket_data.to_numpy().ravel(),
                self.model.labels_,
                self.score_function
            )
            self.score_btn.setText(f"Score: {score}")
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.model.__class__.__name__} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            self.score_btn.setText(f"Score: --")
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = self.model
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def score_dialog(self):
        dialog = Report(
            self.model, 
            self.X, 
            self.node.input_sockets[1].socket_data.to_numpy().ravel(),
            self.score_function
        )
        if dialog.exec():
            self.score_function = dialog.metrics.score_function
            score = scoring(
                self.X, 
                self.node.input_sockets[1].socket_data.to_numpy().ravel(),
                self.model.labels_, 
                self.score_function
            )
            self.score_btn.setText(f"Score: {score}")
        
    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
    
    def resetNode(self):
        try: self.score_btn.setText(f"Score: --")
        except: pass
        return super().resetNode()