from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import layers
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox 
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QStackedLayout)
from PySide6.QtCore import Qt

DEBUG = True

class LayerBase (QWidget):
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
        self.layer = None # ClassifierMixin

        self.set_config(config=None)
        
    def clear_layout (self):
        for widget in self.widget.findChildren(QWidget):
            self.vlayout.removeWidget(widget)
    
    def set_config(self, config=None):
        self.clear_layout()

class Normalization(LayerBase):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def set_config(self, config=None):
        self.clear_layout()

        if not config: self._config = dict(
            mean = None,
            variance = None
        )
        else: self._config = config
        self.layer = layers.Normalization(**self._config)

    def set_layer(self):
        self.layer = layers.Normalization(**self._config)

class NormalizationLayer (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            axis = -1,
            name = f"{self.name}_{self.node.id}"
        )

        self._config = dict(
            layer = "Normalization",
            config = dict(),
        )
        
        self.layer_list = ["Normalization","BatchNormalization","UnitNormalization",
                           "GroupNormalization","LayerNormalization","SpectralNormalization"]
        self.layer = layers.Normalization(**self._config["config"])
    
    def currentWidget(self) -> LayerBase:
        return self.stackedlayout.currentWidget()     

    def config(self):
        dialog = Dialog("Configuration", self.parent)
        method = ComboBox(items=self.layer_list,text="Normalization strategy")
        method.button.setCurrentText(self._config["layer"])
        dialog.main_layout.addWidget(method)
        
        self.stackedlayout = QStackedLayout()
        dialog.main_layout.addLayout(self.stackedlayout)
        self.stackedlayout.addWidget(Normalization())
        
        self.stackedlayout.setCurrentIndex(self.layer_list.index(method.button.currentText()))
 
        if dialog.exec():
            self._config.update(
                config    = self.currentWidget()._config,
                layer = method.button.currentText()
            )
            self.layer = self.currentWidget().layer
            self.exec()
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            pass

        try:
            # unpack data from input socket
            cv, X, Y, input_layer, output_layer = self.node.input_sockets[0].socket_data
            # create layer
            output_layer = self.layer(output_layer)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")
           
        except Exception as e:
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = [cv, X, Y, input_layer, output_layer]

    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = [None, None, None, None, None]
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data