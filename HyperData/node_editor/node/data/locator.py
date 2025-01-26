from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.line_edit import CompleterLineEdit
from PySide6.QtWidgets import QStackedLayout, QWidget, QVBoxLayout

DEBUG = False

class DataLocator (NodeContentWidget):
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
                column_from=None,
                column_to=None,
                row_from=None,
                row_to=None
            )
        elif not self._data.equals(self.node.input_sockets[0].socket_data):
            # update _config according to the new input data
            self._config = dict(
                type="columns",
                column_from=self.node.input_sockets[0].socket_data.columns[0],
                column_to=self.node.input_sockets[0].socket_data.columns[-1],
                row_from=1,
                row_to=self.node.input_sockets[0].socket_data.shape[0]
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

        col = QWidget()
        col_layout = QVBoxLayout()
        col_layout.setContentsMargins(0,0,0,0)
        col.setLayout(col_layout)
        stacklayout.addWidget(col)

        col_from = CompleterLineEdit(text="from column")
        col_layout.addWidget(col_from)

        col_to = CompleterLineEdit(text="to column")
        col_layout.addWidget(col_to)

        row = QWidget()
        row_layout = QVBoxLayout()
        row_layout.setContentsMargins(0,0,0,0)
        row.setLayout(row_layout)
        stacklayout.addWidget(row)

        row_from = CompleterLineEdit(text="from row")
        row_layout.addWidget(row_from)

        row_to = CompleterLineEdit(text="to row")
        row_layout.addWidget(row_to)
        
        if self.node.input_sockets[0].socket_data.shape[0] < 1000:
            try:
                row_from.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.index+1)))
                row_to.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.index+1)))
            except: pass
        if self.node.input_sockets[0].socket_data.shape[1] < 1000:
            try:
                col_from.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.columns)))
                col_to.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.columns)))
            except: pass

        col_from.button.setCurrentText(str(self._config["column_from"]))
        col_to.button.setCurrentText(str(self._config["column_to"]))
        row_from.button.setCurrentText(str(self._config["row_from"]))
        row_to.button.setCurrentText(str(self._config["row_to"]))

        stacklayout.setCurrentIndex(type.button.currentIndex())
        
        if dialog.exec():
            self._config["type"] = type.button.currentText()
            self._config["column_from"] = col_from.button.currentText()
            self._config["column_to"] = col_to.button.currentText()
            self._config["row_from"] = row_from.button.currentText()
            self._config["row_to"] = row_to.button.currentText()
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
                col_from = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_from"])
                col_to = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_to"])+1
                data = self.node.input_sockets[0].socket_data.iloc[:,col_from:col_to]

            elif self._config["type"] == "rows":
                row_from = int(self._config["row_from"])-1
                row_to = int(self._config["row_to"])
                data = self.node.input_sockets[0].socket_data.iloc[row_from:row_to,:]
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            if DEBUG or GLOBAL_DEBUG: print('data out', data)
            else: logger.info(f"{self.name} {self.node.id}: located data successfully.")

        except Exception as e:
            data = self.node.input_sockets[0].socket_data
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

        self.initConfig()
    