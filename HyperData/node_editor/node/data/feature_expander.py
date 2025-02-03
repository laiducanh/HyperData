from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
from node_editor.base.node_graphics_node import NodeGraphicsNode
from sklearn import preprocessing
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle, PrimaryComboBox, ComboBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.spinbox import SpinBox
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout, QScrollArea
from PySide6.QtCore import Qt

DEBUG = False

class ExpanderBase(QWidget):
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
        self.expander = None

        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()

class PolynomialFeatures (ExpanderBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            degree = 2,
            interaction_only = False,
            include_bias = True,
        )
        else: self._config = config
        self.scaler = preprocessing.PolynomialFeatures(**self._config)
        
        self.degree = SpinBox(text="Degree")
        self.degree.button.setValue(self._config["degree"])
        self.vlayout.addWidget(self.degree)

        self.interaction_only = Toggle(text="Only interaction features")
        self.interaction_only.button.setChecked(self._config["interaction_only"])
        self.interaction_only.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.interaction_only)
        
        self.include_bias = Toggle(text="Include bias")
        self.include_bias.button.setChecked(self._config["include_bias"])
        self.include_bias.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.include_bias)
    
    def set_estimator(self):
        self._config["degree"] = self.degree.button.value()
        self._config["interaction_only"] = self.interaction_only.button.isChecked()
        self._config["include_bias"] = self.include_bias.button.isChecked()
        self.scaler = preprocessing.PolynomialFeatures(**self._config)

class SplineTransfomer(ExpanderBase):
    def __init__(self, parent=None):
        super().__init__(parent)

    def set_config(self, config=None):

        self.clear_layout()

        if not config: self._config = dict(
            n_knots = 5,
            degree = 3,
            knots = "uniform",
            extrapolation = "constant",
            include_bias = True,
        )
        else: self._config = config
        self.scaler = preprocessing.SplineTransformer(**self._config)
        
        self.n_knots = SpinBox(min=1, text="Number of knots")
        self.n_knots.button.setValue(self._config["n_knots"])
        self.n_knots.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.n_knots)

        self.degree = SpinBox(text="Degree")
        self.degree.button.setValue(self._config["degree"])
        self.degree.button.valueChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.degree)

        self.knots = ComboBox(items=["uniform","quantile"], text="Knot positions")
        self.knots.button.setCurrentText(self._config["knots"])
        self.knots.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.knots)

        self.extrapolation = ComboBox(items=["error","constant","linear","continue","periodic"],
                                      text="Extrapolation")
        self.extrapolation.button.setCurrentText(self._config["extrapolation"])
        self.extrapolation.button.currentTextChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.extrapolation)

        self.include_bias = Toggle(text="Include bias")
        self.include_bias.button.setChecked(self._config["include_bias"])
        self.include_bias.button.checkedChanged.connect(self.set_estimator)
        self.vlayout.addWidget(self.include_bias)
    
    def set_estimator(self):
        self._config.update(
            n_knots = self.n_knots.button.value(),
            degree = self.degree.button.value(),
            knots = self.knots.button.currentText(),
            extrapolation = self.extrapolation.button.currentText(),
            include_bias = self.include_bias.button.isChecked(),
        )
        self.scaler = preprocessing.SplineTransformer(**self._config)

class FeatureExpander (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            expander = "Polynomial expansion",
            config = dict(),
        )
        
        self.expander_list = ["Polynomial expansion","Univariate B-spline"]
        
        self.expander = preprocessing.PolynomialFeatures(**self._config["config"])
    
    def currentWidget(self) -> ExpanderBase:
        return self.stackedlayout.currentWidget()       

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        expander = PrimaryComboBox(items=self.expander_list,text="Scaler")
        expander.button.setMinimumWidth(250)
        expander.button.currentTextChanged.connect(lambda s: self.stackedlayout.setCurrentIndex(self.expander_list.index(s)))
        dialog.main_layout.addWidget(expander)
        dialog.main_layout.addWidget(SeparateHLine())
    
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(PolynomialFeatures())
        self.stackedlayout.addWidget(SplineTransfomer())
        self.stackedlayout.setCurrentIndex(self.expander_list.index(expander.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                expander = expander.button.currentText()
            )
            self.expander = self.currentWidget().expander
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
            X = data.to_numpy()
            data_transformed = self.expander.fit_transform(X, **self._config["config"])
            columns = [f"Expanded_feature {i+1}" for i in range(data_transformed.shape[1])]
            data = pd.DataFrame(data_transformed, columns=columns)
            
            # change progressbar's color   
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: {self.expander} run successfully.")

            
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
