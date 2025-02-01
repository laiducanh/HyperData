from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import preprocessing
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle, PrimaryComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import DoubleSpinBox
from node_editor.node.train_test_split.train_test_split import TrainTestSplitter
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

DEBUG = True

class ScalerBase(QWidget):
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
        self.scaler = None

        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()

class StandardScaler (ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            with_mean = True,
            with_std = True
        )
        else: self._config = config
        self.scaler = preprocessing.StandardScaler(**self._config)
    
        self.with_mean = Toggle(text="Center data")
        self.with_mean.button.setChecked(self._config["with_mean"])
        self.vlayout.addWidget(self.with_mean)

        self.with_std = Toggle(text="Unit variance")
        self.with_std.button.setChecked(self._config["with_std"])
        self.vlayout.addWidget(self.with_std)
    
    def set_estimator(self):
        self._config["with_mean"] = self.with_mean.button.isChecked()
        self._config["with_std"] = self.with_std.button.isChecked()
        self.scaler = preprocessing.StandardScaler(**self._config)

class MinMaxScaler(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            feature_range=(0,1),
            clip = False
        )
        else: self._config = config
        self.scaler = preprocessing.MinMaxScaler(**self._config)
    
        self.min = DoubleSpinBox(text="Min")
        self.min.button.setValue(self._config["feature_range"][0])
        self.vlayout.addWidget(self.min)

        self.max = DoubleSpinBox(text="Max")
        self.max.button.setValue(self._config["feature_range"][1])
        self.vlayout.addWidget(self.max)

        self.clip = Toggle(text="Clip")
        self.clip.button.setChecked(self._config["clip"])
        self.vlayout.addWidget(self.clip)
    
    def set_estimator(self):
        self._config["feature_range"][0] = self.min.button.value()
        self._config["feature_range"][1] = self.max.button.value()
        self._config["clip"] = self.clip.button.isChecked()
        self.scaler = preprocessing.MinMaxScaler(**self._config)

class MaxAbsScaler(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):
        self.clear_layout()
    
    def set_estimator(self):
        self.scaler = preprocessing.MaxAbsScaler(**self._config)

class RobustScaler(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            with_centering = True,
            with_scaling = True,
            unit_variance = False
        )
        else: self._config = config
        self.scaler = preprocessing.RobustScaler(**self._config)
    
        self.with_centering = Toggle(text="Center data")
        self.with_centering.button.setChecked(self._config["with_centering"])
        self.vlayout.addWidget(self.with_centering)

        self.unit_variance = Toggle(text="Unit variance")
        self.unit_variance.button.setChecked(self._config["unit_variance"])
        self.vlayout.addWidget(self.unit_variance)

        self.with_scaling = Toggle(text="Scale to interquartile")
        self.with_scaling.button.setChecked(self._config["with_scaling"])
        self.vlayout.addWidget(self.with_scaling)
    
    def set_estimator(self):
        self._config["with_centering"] = self.with_centering.button.isChecked()
        self._config["with_scaling"] = self.with_scaling.button.isChecked()
        self._config["unit_variance"] = self.unit_variance.button.isChecked()
        self.scaler = preprocessing.RobustScaler(**self._config)

class DataScaler (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            scaler = "Standard Scaler",
            config = dict(),
        )
        
        self.scaler_list = ["Standard Scaler","Min-Max Scaler","Maximum Absolute Scaler","Robust Scaler"]
        
        self.scaler = preprocessing.StandardScaler(**self._config["config"])
    
    def currentWidget(self) -> ScalerBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        scaler = PrimaryComboBox(items=self.scaler_list,text="Scaler")
        scaler.button.setMinimumWidth(250)
        scaler.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.scaler_list.index(s)))
        dialog.main_layout.addWidget(scaler)
        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(StandardScaler())
        self.stackedlayout.addWidget(MinMaxScaler())
        self.stackedlayout.addWidget(MaxAbsScaler())
        self.stackedlayout.addWidget(RobustScaler())
        self.stackedlayout.setCurrentIndex(self.scaler_list.index(scaler.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                scaler = scaler.button.currentText()
            )
            self.scaler = self.currentWidget().scaler
            self.exec()

    def func(self):
        self.eval()

        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data.copy()
            columns = data.columns
            X = data.to_numpy()
            data_transformed = self.scaler.fit_transform(X)
            data = pd.DataFrame(data_transformed, columns=columns)
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.scaler} run successfully.")

            
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color   
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty Dataframe.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
     
    def eval (self):
        self.resetStatus()
        # reset socket data
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
