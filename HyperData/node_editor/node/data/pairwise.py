from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, Toggle, PrimaryComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import DoubleSpinBox
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QStackedLayout
from PySide6.QtCore import Qt
from sklearn.metrics import pairwise

DEBUG = False

class MethodBase(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        _layout = QVBoxLayout()
        _layout.setContentsMargins(0,0,0,0)
        self.setLayout(_layout)
        self.scroll_area = QScrollArea(parent)
        _layout.addWidget(self.scroll_area)
        
        self.widget = QWidget()
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0,0,0,0)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setLayout(self.vlayout)
        self.scroll_area.setWidget(self.widget)
        self.scroll_area.setWidgetResizable(True)

        self._config = dict()
        self.method = None # ClassifierMixin

        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()

class PairwiseDistances(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            metric = "euclidean"
        )
        else: self._config = config
        self.method = pairwise.pairwise_distances

        self.metric_ = ComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan",
                                      "braycurtis","canberra","chebyshev","correlation","dice",
                                      "hamming","jaccard","kulsinski","mahalanobis","rogerstanimoto",
                                      "russellrao","seuclidean","sokalmichener","sokalsneath","sqeuclidean",
                                      "yule"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
        
    def set_estimator(self):
        self._config.update(
            metric = self.metric_.button.currentText()
        )

class PairwiseDistancesArgmin(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            metric = "euclidean"
        )
        else: self._config = config
        self.method = pairwise.pairwise_distances_argmin

        self.metric_ = ComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan",
                                      "braycurtis","canberra","chebyshev","correlation","dice",
                                      "hamming","jaccard","kulsinski","mahalanobis","rogerstanimoto",
                                      "russellrao","seuclidean","sokalmichener","sokalsneath","sqeuclidean",
                                      "yule"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
        
    def set_estimator(self):
        self._config.update(
            metric = self.metric_.button.currentText()
        )

class PairedDistances(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            metric = "euclidean"
        )
        else: self._config = config
        self.method = pairwise.paired_distances

        self.metric_ = ComboBox(items=["cityblock","cosine","euclidean","l1","l2","manhattan"], text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
        
    def set_estimator(self):
        self._config.update(
            metric = self.metric_.button.currentText()
        )

class HaversineDistance(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        self._config = dict()
        self.method = pairwise.haversine_distances
   
class PairwiseKernel(MethodBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        self._config = dict(
            metric = "linear"
        )
        self.method = pairwise.pairwise_kernels

        self.metric_ = ComboBox(items=["additive_chi2","chi2","linear","quadratic","cubic",
                                         "quartic","rbf","laplacian","sigmoid","cosine"],
                                         text="Metric")
        self.metric_.button.setCurrentText(self._config["metric"])
        self.metric_.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.metric_)
    
    def set_estimator(self):
        self._config.update(
            metric = self.metric_.button.currentText()
        )


class PairwiseMeasurer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            method = "Pairwise Distances",
            config = dict(),
        )

        self.method_list = ["Pairwise Distances","Pairwise Distances Argmin",
                            "Paired Distances","Haversine Distances","Pairwise Kernel"]

        self.method = pairwise.pairwise_distances
    
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
        self.stackedlayout.addWidget(PairwiseDistances())
        self.stackedlayout.addWidget(PairwiseDistancesArgmin())
        self.stackedlayout.addWidget(PairedDistances())
        self.stackedlayout.addWidget(HaversineDistance())
        self.stackedlayout.addWidget(PairwiseKernel())
        self.stackedlayout.setCurrentIndex(self.method_list.index(method.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                method = method.button.currentText()
            )
            self.method = self.currentWidget().method
            self.exec()


    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            data = self.method(
                self.node.input_sockets[0].socket_data,
                self.node.input_sockets[1].socket_data,
                **self._config["config"]
            )
            data = pd.DataFrame(data)
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.method} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.node.input_sockets[1].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data