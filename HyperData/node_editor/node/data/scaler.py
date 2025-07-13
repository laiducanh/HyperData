from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import preprocessing
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HToggle, HPrimaryComboBox, HTransparentComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox, HTransparentSpinBox
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

DEBUG = False

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
        # Remove all child widgets from the layout
        while self.vlayout.count():
            item = self.vlayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
    
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
    
        self.with_mean = HToggle(
            label="Center data",
            getter=lambda: self._config["with_mean"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.with_std = HToggle(
            label="Unit variance",
            getter=lambda: self._config["with_std"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config["with_mean"] = self.with_mean.button.isChecked()
        self._config["with_std"] = self.with_std.button.isChecked()

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
    
        self.min = HTransparentDoubleSpinBox(
            label="Min",
            getter=lambda: self._config["feature_range"][0],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.max = HTransparentDoubleSpinBox(
            label="Max",
            getter=lambda: self._config["feature_range"][1],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.clip = HToggle(
            label="Clip",
            getter=lambda: self._config["clip"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config["feature_range"][0] = self.min.button.value()
        self._config["feature_range"][1] = self.max.button.value()
        self._config["clip"] = self.clip.button.isChecked()

class MaxAbsScaler(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)

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
    
        self.with_centering = HToggle(
            label="Center data",
            getter=lambda: self._config["with_centering"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.unit_variance = HToggle(
            label="Unit variance",
            getter=lambda: self._config["unit_variance"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.with_scaling = HToggle(
            label="Scale to interquartile",
            getter=lambda: self._config["with_scaling"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config["with_centering"] = self.with_centering.button.isChecked()
        self._config["with_scaling"] = self.with_scaling.button.isChecked()
        self._config["unit_variance"] = self.unit_variance.button.isChecked()

class QuantileTransfomer(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_quantiles = 1000,
            output_distribution = "uniform",
            subsample = 10000
        )
        else: self._config = config
    
        self.n_quantiles = HTransparentSpinBox(
            minimum=1, maximum=10000, singleStep=1000,
            label="Number of quantiles",
            getter=lambda: self._config["n_quantiles"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.output_distribution = HTransparentComboBox(
            items=["uniform","normal"], 
            label="Distribution",
            getter=lambda: self._config["output_distribution"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.subsampleOn = HToggle(
            text="Subsample",
            getter=lambda: True if self._config["subsample"] else False,
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.subsample = HTransparentSpinBox(
            minimum=1, maximum=100000, singleStep=10000, 
            label="Number of subsamples",
            getter=lambda: self._config["subsample"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config["n_quantiles"] = self.n_quantiles.button.value()
        self._config["output_distribution"] = self.output_distribution.button.currentText()
        self._config["subsample"] = self.subsample.button.value()

class PowerTransformer(ScalerBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            method = "yeo-johnson",
            standardize = True
        )
        else: self._config = config
    
        self.method = HTransparentComboBox(
            items=["yeo-johnson","box-cox"], 
            label="Method",
            getter=lambda: self._config["method"],
            setter=self.set_estimator,
            layout=self.vlayout
        )

        self.standardize = HToggle(
            label="Standardize",
            getter=lambda: self._config["standardize"],
            setter=self.set_estimator,
            layout=self.vlayout
        )
    
    def set_estimator(self):
        self._config["method"] = self.method.button.currentText()
        self._config["standardize"] = self.standardize.button.isChecked()

class DataScaler (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            scaler = "Standard Scaler",
            config = dict(),
        )
        
        self.scaler_list = ["Standard Scaler","Min-Max Scaler","Maximum Absolute Scaler",
                            "Robust Scaler","Quantile Transformer","Power Transformer"]
            
    def currentWidget(self) -> ScalerBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Data Scaling", self.parent)
        scaler = HPrimaryComboBox(items=self.scaler_list,label="Scaler")
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
        self.stackedlayout.addWidget(QuantileTransfomer())
        self.stackedlayout.addWidget(PowerTransformer())
        self.stackedlayout.setCurrentIndex(self.scaler_list.index(scaler.button.currentText()))
        self.currentWidget().set_config(self._config["config"])
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                scaler = scaler.button.currentText()
            )
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
            if self._config["scaler"] == "Standard Scaler":
                self.scaler = preprocessing.StandardScaler(**self._config["config"])
            elif self._config["scaler"] == "Min-Max Scaler":
                self.scaler = preprocessing.MinMaxScaler(**self._config["config"])
            elif self._config["scaler"] == "Maximum Absolute Scaler":
                self.scaler = preprocessing.MaxAbsScaler(**self._config["config"])
            elif self._config["scaler"] == "Robust Scaler":
                self.scaler = preprocessing.RobustScaler(**self._config["config"])
            elif self._config["scaler"] == "Quantile Transformer":
                self.scaler = preprocessing.QuantileTransformer(**self._config["config"])
            elif self._config["scaler"] == "Power Transformer":
                self.scaler = preprocessing.PowerTransformer(**self._config["config"])
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
        self.resetNode()
        # reset socket data
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        # update input sockets
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
