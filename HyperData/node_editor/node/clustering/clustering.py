from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.clustering.report import Report, scoring
from node_editor.node.clustering.base import MethodBase
from node_editor.node.clustering.kmeans import KMeans
from node_editor.node.clustering.minibatch_kmeans import MiniBatchKMeans
from node_editor.node.clustering.affinity import AffinityPropagation
from node_editor.node.clustering.mean_shift import MeanShift
from node_editor.node.clustering.spectral import SpectralClustering
from node_editor.node.clustering.agglomerative import AgglomerativeClustering
from node_editor.node.clustering.bisecting_kmeans import BisectingKMeans
from node_editor.node.clustering.dbscan import DBSCAN
from node_editor.node.clustering.hdbscan import HDBSCAN
from node_editor.node.clustering.optics import OPTICS
from node_editor.node.clustering.birch import Birch
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import _TransparentPushButton, Toggle, PrimaryComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QStackedLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from sklearn import cluster

DEBUG = True
        
class Clustering (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Features")
        self.node.input_sockets[1].setSocketLabel("Labels")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self.score_btn = _TransparentPushButton()
        self.score_btn.setText(f"Score: --")
        self.score_btn.released.connect(self.score_dialog)
        self.vlayout.insertWidget(2,self.score_btn)
        self.score_function = "Rand Index"

        self._config = dict(
            method = "K-Means",
            config = dict(),
        )

        self.method_list = ["K-Means","Mini-Batch K-Means","Affinity Propagation",
                            "Mean Shift","Spectral Clustering","Agglomerative Clustering",
                            "Bisecting K-Means","DBSCAN","HDBSCAN","OPTICS","Birch"]

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
        action = QAction("Visualization", self.menu)
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
        method = PrimaryComboBox(items=self.method_list,text="Method")
        method.button.setMinimumWidth(250)
        method.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.method_list.index(s)))
        dialog.main_layout.addWidget(method)
        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(KMeans())
        self.stackedlayout.addWidget(MiniBatchKMeans())
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
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets, model_selection, preprocessing
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            #X = df.iloc[:,:4]
            random_state = np.random.RandomState(0)
            n_samples, n_features = data.data.shape
            X = np.concatenate([data.data, random_state.randn(n_samples, 200 * n_features)], axis=1)
            X = pd.DataFrame(X)
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
                        
            self.node.input_sockets[0].socket_data = X
            self.node.input_sockets[1].socket_data = Y
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            columms = self.node.input_sockets[0].socket_data.columns
            self.X = self.node.input_sockets[0].socket_data
            self.model.fit(self.X)
            data = pd.DataFrame(self.model.cluster_centers_, columns=columms)

            score = scoring(
                self.X, 
                self.node.input_sockets[1].socket_data.to_numpy().ravel(),
                self.model.labels_
            )
            self.score_btn.setText(f"Score: {score[self.score_function]}")
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.model} run successfully.")

            
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
        dialog = Report(self.model, self.X, self.node.input_sockets[1].socket_data.to_numpy().ravel())
        if dialog.exec():
            self.score_function = dialog.metrics.score_function
        
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
    
    def resetStatus(self):
        try: self.score_btn.setText(f"Score: --")
        except: pass
        return super().resetStatus()