from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.decomposition.report import Report
from node_editor.node.decomposition.base import MethodBase
from node_editor.node.decomposition.pca import PCA
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import _TransparentPushButton, Toggle, PrimaryComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QStackedLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from sklearn import decomposition

DEBUG = True
        
class Decomposition (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].setSocketLabel("Features")
        self.node.input_sockets[1].setSocketLabel("Labels")
        self.node.output_sockets[0].setSocketLabel("Model")
        self.node.output_sockets[1].setSocketLabel("Data out")

        self._config = dict(
            method = "Principal Component Analysis",
            config = dict(),
        )

        self.method_list = ["Principal Component Analysis"]

        self.model = decomposition.PCA(**self._config["config"])
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
        action.triggered.connect(self.visualize_dialog)
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
        self.stackedlayout.addWidget(PCA())
        
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
            X = df.iloc[:,:4]
            random_state = np.random.RandomState(0)
            n_samples, n_features = data.data.shape
            #X = np.concatenate([data.data, random_state.randn(n_samples, 200 * n_features)], axis=1)
            X = pd.DataFrame(X)
            Y = preprocessing.LabelEncoder().fit_transform(df.iloc[:,4])
            Y = pd.DataFrame(data=Y)
                        
            self.node.input_sockets[0].socket_data = X
            self.node.input_sockets[1].socket_data = Y
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            columms = self.node.input_sockets[0].socket_data.columns
            self.X = self.node.input_sockets[0].socket_data
            data = self.model.fit_transform(self.X)
            data = pd.DataFrame(
                data, 
                columns=[f"Principal component {i+1}" for i in range(self.model.n_components_)]
            )
        
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.model} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = self.model
        self.node.output_sockets[1].socket_data = data.copy()
        self.data_to_view = data.copy()

    def visualize_dialog(self):
        dialog = Report(self.model, self.node.output_sockets[1].socket_data, self.node.input_sockets[1].socket_data)
        dialog.exec()
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data
