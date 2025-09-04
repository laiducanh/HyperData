from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine, VFrame
from ui.base_widgets.text import TitleLabel, BodyLabel

DEBUG = False

class DataSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._data = pd.DataFrame()
        self.initConfig()
        
    def initConfig (self):
        try:
            if self.node.input_sockets[0].socket_data.empty:
                # reset _config if the input data is empty Dataframe
                self._config = dict(
                    type="columns",
                    idx = -1,
                )
            elif not self._data.equals(self.node.input_sockets[0].socket_data):
                # update _config according to the new input data
                self._config = dict(
                    type="columns",
                    idx=self.node.input_sockets[0].socket_data.shape[0]
                )
        except: 
            self._config = dict(
                    type="columns",
                    idx = -1,
                )
            
        self._data = self.node.input_sockets[0].socket_data.copy()
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.setMinimumSize(600, 200)
        dialog.main_layout.addWidget(TitleLabel("Split Data"))
        dialog.main_layout.addWidget(BodyLabel("Slide DataFrame along a column or a row"))
        dialog.main_layout.addWidget(SeparateHLine())

        fr = VFrame(dialog.main_layout)
        type = HTransparentComboBox(
            items=["columns","rows"], 
            label="Type",
            getter=lambda: self._config["type"],
            layout=fr.vlayout
        )

        idx = HTransparentSpinBox(
            minimum=0, maximum=1000000,
            label="Index",
            label2="Position of the slice",
            getter=lambda: self._config["idx"],
            layout=fr.vlayout
        )
        
        if dialog.exec():
            self._config["type"] = type.button.currentText()
            self._config["idx"] = idx.button.value()
            logger.info(f"{self.name} {self.node.id}: update config {self._config}")
            self.exec()

    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            self.initConfig()
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            idx = self._config['idx']
            if self._config["type"] == "columns":
                data1 = self.node.input_sockets[0].socket_data.iloc[:,:idx]
                data2 = self.node.input_sockets[0].socket_data.iloc[:,idx:]

            elif self._config["type"] == "rows":
                data1 = self.node.input_sockets[0].socket_data.iloc[:idx,:]
                data2 = self.node.input_sockets[0].socket_data.iloc[idx:,:]
           
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: split data successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return the original DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data1.copy()
        self.node.output_sockets[1].socket_data = data2.copy()
        self.data_to_view = self.node.input_sockets[0].socket_data.copy()
    
    def eval(self):
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

        #self.initConfig()
    