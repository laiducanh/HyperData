from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from itertools import compress
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox, Toggle, ListCheckBox
from ui.base_widgets.window import Dialog

DEBUG = False

class DataPivot(NodeContentWidget):
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
        dialog = Dialog(title="Data Pivot", parent=self.parent)
        aggfunc = TransparentComboBox(
            items=["mean","sum","min","max"],
            text="Function",
            text2='Function will be used to calculate the partial aggregates',
            getter=lambda: self._config["aggfunc"],
            layout=dialog.main_layout
        )

        margins = Toggle(
            text="Margins",
            text2='Add aggregate columns and rows across the categories',
            getter=lambda: self._config["margins"],
            layout=dialog.main_layout
        )

        dropna = Toggle(
            text="Drop NaN",
            text2='Do not include columns whose entries are all NaN',
            getter=lambda: self._config["dropna"],
            layout=dialog.main_layout
        )

        sort = Toggle(
            text="Sort",
            text2='Specifies if the result should be sorted',
            getter=lambda: self._config["sort"],
            layout=dialog.main_layout
        )

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
            rawdata = self.node.input_sockets[0].socket_data.copy(deep=True)
            _data = pd.pivot_table(rawdata,**self._config)
            
            if self._config['margins']:
                _columns = _data.columns[:-1]
                _index = _data.index[:-1]
            else:
                _columns = _data.columns
                _index = _data.index
            if isinstance(_data.columns, pd.MultiIndex):
                columns = [' \u2192 '.join(col) for col in _columns]
            else:
                columns = _data.columns
            if isinstance(_data.index, pd.MultiIndex):
                index = [' \u2192 '.join(idx) for idx in _index]
            else:
                index = _data.index
            if self._config['margins']:
                columns.append(self._config['aggfunc'].title())
                index.append(self._config['aggfunc'].title())

            data = pd.DataFrame(data=_data.values, columns=columns, index=index)
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
        self.resetNode()
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
        dialog = Dialog(title="Data Unpivot", parent=self.parent)

        ignore_index = Toggle(
            text="Ignore index",
            getter=lambda: self._config["ignore_index"],
            layout=dialog.main_layout
        )
     
        id_vars = ListCheckBox(
            data.columns, 
            text="Columns",
            states=[i in self._config["id_vars"] for i in data.columns]
        )
        dialog.main_layout.addWidget(id_vars)
        value_vars = ListCheckBox(
            data.columns, 
            text="Values",
            states=[i in self._config["value_vars"] for i in data.columns]
        )
        dialog.main_layout.addWidget(value_vars)

        if dialog.exec():
            self._config.update(
                id_vars = list(compress(data.columns, id_vars.states)),
                value_vars = list(compress(data.columns, value_vars.states)),
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
        self.resetNode()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data