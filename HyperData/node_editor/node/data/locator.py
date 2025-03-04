from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.line_edit import CompleterLineEdit

DEBUG = True

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
                column_from=None,
                column_to=None,
                row_from=None,
                row_to=None
            )
        elif not self._data.equals(self.node.input_sockets[0].socket_data):
            # update _config according to the new input data
            self._config = dict(
                column_from=self.node.input_sockets[0].socket_data.columns[0],
                column_to=self.node.input_sockets[0].socket_data.columns[-1],
                row_from=1,
                row_to=self.node.input_sockets[0].socket_data.shape[0]
            )

        self._data = self.node.input_sockets[0].socket_data.copy()
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        col_from = CompleterLineEdit(text="From column")
        dialog.main_layout.addWidget(col_from)

        col_to = CompleterLineEdit(text="To column")
        dialog.main_layout.addWidget(col_to)

        row_from = CompleterLineEdit(text="From row")
        dialog.main_layout.addWidget(row_from)

        row_to = CompleterLineEdit(text="To row")
        dialog.main_layout.addWidget(row_to)
        
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
        
        if dialog.exec():
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
            col_from = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_from"])
            col_to = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_to"])+1
            row_from = int(self._config["row_from"])-1
            row_to = int(self._config["row_to"])
            data = self.node.input_sockets[0].socket_data.iloc[row_from:row_to,col_from:col_to]
                
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
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def eval(self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

        self.initConfig()
    