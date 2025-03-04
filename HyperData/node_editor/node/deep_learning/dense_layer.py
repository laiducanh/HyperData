from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from keras import layers
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.node.deep_learning.base import DLBase
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from config.settings import logger, GLOBAL_DEBUG

DEBUG = True

class DenseLayer (DLBase):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            units = 1,
            activation = 'relu',
            use_bias = True,
            kernel_initializer = "glorot_uniform",
            bias_initializer = "zeros",
            kernel_regularizer = None,
            bias_regularizer = None,
            kernel_constraint = None,
            bias_constraint = None,
            name = f"{self.name}_{self.node.id}"
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        units = SpinBox(min=1, text="Units")
        units.button.setValue(self._config["units"])
        dialog.main_layout.addWidget(units)

        activation = ComboBox(items=["elu","exponential","gelu","hard_sigmoid","linear",
                                     "relu","selu","sigmoid","softmax","softplus","softsign",
                                     "swish","tank"], text="Activation function")
        activation.button.setCurrentText(self._config["activation"])
        dialog.main_layout.addWidget(activation)

        use_bias = Toggle(text="Use Bias")
        use_bias.button.setChecked(self._config["use_bias"])
        dialog.main_layout.addWidget(use_bias)

         

        if dialog.exec():
            self._config.update(
                units = units.button.value(),
                activation = activation.button.currentText(),
                use_bias = use_bias.button.isChecked()
            )
            self.exec()
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            pass

        try:
            # unpack data from input socket
            cv, X, Y, input_layer, output_layer = self.node.input_sockets[0].socket_data
            # create layer
            output_layer = layers.Dense(**self._config)(output_layer)
            print(output_layer.shape)
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