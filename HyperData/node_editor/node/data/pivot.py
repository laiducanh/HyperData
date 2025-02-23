from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from itertools import compress
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox, Toggle, ListCheckBox
from ui.base_widgets.window import Dialog

DEBUG = False

class DataPivot (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            aggfunc = "mean",
            margins = False,
            dropna = True,
            sort = True,
            values = [],
            index = [],
            columns = []
        )
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def config(self):
        data = self.node.input_sockets[0].socket_data
        dialog = Dialog(title="configuration", parent=self.parent)
        aggfunc = ComboBox(items=["mean","sum","min","max"],text="Function")
        aggfunc.button.setCurrentText(self._config["aggfunc"])
        dialog.main_layout.addWidget(aggfunc)
        margins = Toggle(text="Margins")
        margins.button.setChecked(self._config["margins"])
        dialog.main_layout.addWidget(margins)
        dropna = Toggle("Drop NaN")
        dropna.button.setChecked(self._config["dropna"])
        dialog.main_layout.addWidget(dropna)
        sort = Toggle(text="Sort")
        sort.button.setChecked(self._config["sort"])
        dialog.main_layout.addWidget(sort)
        values = ListCheckBox(data.columns, text="Values",
                              states=[i in self._config["values"] for i in data.columns])
        dialog.main_layout.addWidget(values)
        indexes = ListCheckBox(data.columns, text="Index",
                               states=[i in self._config["index"] for i in data.columns])
        dialog.main_layout.addWidget(indexes)
        columns = ListCheckBox(data.columns, text="Columns",
                               states=[i in self._config["columns"] for i in data.columns])
        dialog.main_layout.addWidget(columns)

        if dialog.exec():
            self._config.update(
                aggfunc = aggfunc.button.currentText(),
                margins = margins.button.isChecked(),
                dropna = dropna.button.isChecked(),
                sort = sort.button.isChecked(),
                values = list(compress(data.columns, values.states)),
                index = list(compress(data.columns, indexes.states)),
                columns = list(compress(data.columns, columns.states))
            )
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                          "bar", "bar", "bar", "bar"],
                    "B": ["one", "one", "one", "two", "two",
                          "one", "one", "two", "two"],
                    "C": ["small", "large", "large", "small",
                          "small", "large", "small", "small",
                          "large"],
                    "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                    "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]})
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data
            data = pd.pivot_table(data,**self._config)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")

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

class DataUnpivot(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            id_vars = [],
            value_vars = [],
            col_level = -1,
            ignore_index = True
        )
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def config(self):
        data = self.node.input_sockets[0].socket_data
        dialog = Dialog(title="configuration", parent=self.parent)
        col_level = ComboBox(items=[str(i) for i in range(-1,data.columns.nlevels)], text="Level")
        col_level.button.setCurrentText(str(self._config["col_level"]))
        dialog.main_layout.addWidget(col_level)
        ignore_index = Toggle(text="Ignore index")
        ignore_index.button.setChecked(self._config["ignore_index"])
        dialog.main_layout.addWidget(ignore_index)
        id_vars = ListCheckBox(data.columns, text="Columns",
                               states=[i in self._config["id_vars"] for i in data.columns])
        dialog.main_layout.addWidget(id_vars)
        value_vars = ListCheckBox(data.columns, text="Values",
                                  states=[i in self._config["value_vars"] for i in data.columns])
        dialog.main_layout.addWidget(value_vars)

        if dialog.exec():
            self._config.update(
                id_vars = list(compress(data.columns, id_vars.states)),
                value_vars = list(compress(data.columns, value_vars.states)),
                col_level = int(col_level.button.currentText()),
                ignore_index = ignore_index.button.isChecked()
            )
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            df = pd.DataFrame({'A': {0: 'a', 1: 'b', 2: 'c'},
                   'B': {0: 1, 1: 3, 2: 5},
                   'C': {0: 2, 1: 4, 2: 6}})
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data
            data = pd.melt(data,**self._config)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: run successfully.")

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