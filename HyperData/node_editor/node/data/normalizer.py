from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from sklearn.preprocessing import normalize
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.frame import VFrame

DEBUG = False

class DataNormalizer (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            norm = "l2",
            axis = 1,
        )
    
    def config(self):
        dialog = Dialog("Data Normalization", self.parent)
        dialog.setMinimumSize(600, 400)

        fr = VFrame(dialog.main_layout)

        norm = HTransparentComboBox(
            label="Norm",
            items=["l1","l2","max"],
            getter=lambda: self._config["norm"],
            layout=fr.vlayout
        )

        axis = HTransparentComboBox(
            items=["row","column"],
            label="Axis",
            getter=lambda: "row" if self._config["axis"] else "column",
            layout=fr.vlayout
        )

        if dialog.exec():
            self._config["norm"] = norm.button.currentText()
            self._config["axis"] = 1 if axis.button.currentText() == "row" else 2
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            columns = self.node.input_sockets[0].socket_data.columns
            X = self.node.input_sockets[0].socket_data.to_numpy()
            data = pd.DataFrame(normalize(X,**self._config), columns=columns)
           
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: normalize data successfully.")
           
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return an empty DataFrame.")
            logger.exception(e)

        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()

    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data