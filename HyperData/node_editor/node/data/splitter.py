from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.line_edit import CompleterLineEdit
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout

DEBUG = False

class DataSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._data = pd.DataFrame()
        self.initConfig()
        
    def initConfig (self):
        if self.node.input_sockets[0].socket_data.empty:
            # reset _config if the input data is empty Dataframe
            self._config = dict(
                type="columns",
                row = -1,
                col = -1
            )
        elif not self._data.equals(self.node.input_sockets[0].socket_data):
            # update _config according to the new input data
            self._config = dict(
                type="columns",
                row = self.node.input_sockets[0].socket_data.shape[0],
                col = self.node.input_sockets[0].socket_data.columns[-1]
            )

        self._data = self.node.input_sockets[0].socket_data.copy()
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        type = ComboBox(items=["columns","rows"], text="type")
        type.button.setCurrentText(self._config["type"])
        type.button.currentTextChanged.connect(lambda: stacklayout.setCurrentIndex(type.button.currentIndex()))
        dialog.main_layout.addWidget(type)

        dialog.main_layout.addWidget(SeparateHLine())

        stacklayout = QStackedLayout()
        dialog.main_layout.addLayout(stacklayout)

        col = CompleterLineEdit(text="Column")
        stacklayout.addWidget(col)

        row = CompleterLineEdit(text="Row")
        stacklayout.addWidget(row)
        
        if self.node.input_sockets[0].socket_data.shape[0] < 1000:
            try: row.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.index+1)))
            except: pass
        if self.node.input_sockets[0].socket_data.shape[1] < 1000:
            try: col.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.columns)))
            except: pass

        col.button.setCurrentText(str(self._config["col"]))
        row.button.setCurrentText(str(self._config["row"]))

        stacklayout.setCurrentIndex(type.button.currentIndex())
        
        if dialog.exec():
            self._config["type"] = type.button.currentText()
            self._config["col"] = col.button.currentText()
            self._config["row"] = row.button.currentText()
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

            if self._config["type"] == "columns":
                col = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["col"])+1
                data1 = self.node.input_sockets[0].socket_data.iloc[:,:col]
                data2 = self.node.input_sockets[0].socket_data.iloc[:,col:]

            elif self._config["type"] == "rows":
                row = int(self._config["row"])
                data1 = self.node.input_sockets[0].socket_data.iloc[:row,:]
                data2 = self.node.input_sockets[0].socket_data.iloc[row:,:]
           
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: located data successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data1.copy()
        self.node.output_sockets[1].socket_data = data2.copy()
        self.data_to_view = self.node.input_sockets[0].socket_data.copy()
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

        self.initConfig()
    