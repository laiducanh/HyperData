from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle, ComboBox
from ui.base_widgets.spinbox import SpinBox

DEBUG = False

class DataComputation (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
        
        self._config = dict(
            function = "addition"
        )
    
    def config(self):
        dialog = Dialog(title="Configuration", parent=self.parent)
        
        func = ComboBox(items=["addition","subtraction","multiplication","floating division",
                               "integer division","modulo","exponential power","dot product"],
                               text="Function")
        func.button.setCurrentText(self._config["function"])
        dialog.main_layout.addWidget(func)

        if dialog.exec():
            self._config.update(
                function = func.button.currentText()
            )
            self.exec()    
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data.copy(deep=True)
            data_other = self.node.input_sockets[1].socket_data.copy(deep=True)
            if self._config["function"] == "addition":
                data = data.add(data_other)
            elif self._config["function"] == "substraction":
                data = data.sub(data_other)
            elif self._config["function"] == "multiplication":
                data = data.mul(data_other)
            elif self._config["function"] == "floating division":
                data = data.div(data_other)
            elif self._config["function"] == "integer division":
                data = data.floordiv(data_other)
            elif self._config["function"] == "modulo":
                data = data.mod(data_other)
            elif self._config["function"] == "exponential power":
                data = data.pow(data_other)
            elif self._config["function"] == "dot product":
                data = data.dot(data_other)
           
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if not DEBUG and not GLOBAL_DEBUG:
                node1 = self.node.input_sockets[0].edges[0].start_socket.node
                node2 = self.node.input_sockets[1].edges[0].start_socket.node
                logger.info(f"{self.name} {self.node.id}: compute data from {node2} {node2.id} and {node1} {node1.id} successfully.")
           
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
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