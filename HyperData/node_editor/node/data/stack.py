from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from itertools import compress
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import ComboBox
from ui.base_widgets.window import Dialog

DEBUG = False

class DataStack (NodeContentWidget):
    """ Stack columns to index """
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            level = -1,
            future_stack = True
        )
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def config(self):
        data = self.node.input_sockets[0].socket_data
        dialog = Dialog(title="configuration", parent=self.parent)
        level = ComboBox(items=[str(i) for i in range(-1,data.columns.nlevels)], text="Level")
        level.button.setCurrentText(str(self._config["level"]))
        dialog.main_layout.addWidget(level)

        if dialog.exec():
            self._config.update(level = int(level.button.currentText()))
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            multicol1 = pd.MultiIndex.from_tuples([('weight', 'kg'),
                                       ('weight', 'pounds')])
            df = pd.DataFrame([[1, 2], [2, 4]],
                                     index=['cat', 'dog'],
                                    columns=multicol1)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data
            data = data.stack(**self._config)
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

class DataUnstack (NodeContentWidget):
    """ Unstack indexes to column """
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            level = -1,
        )
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def config(self):
        data = self.node.input_sockets[0].socket_data
        dialog = Dialog(title="configuration", parent=self.parent)
        level = ComboBox(items=[str(i) for i in range(-1,data.index.nlevels)], text="Level")
        level.button.setCurrentText(str(self._config["level"]))
        dialog.main_layout.addWidget(level)

        if dialog.exec():
            self._config.update(level = int(level.button.currentText()))
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            index = pd.MultiIndex.from_tuples([('one', 'a'), ('one', 'b'),
                                   ('two', 'a'), ('two', 'b')])
            df = pd.Series(range(1, 5), index=index)
            self.node.input_sockets[0].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data
            data = data.unstack(**self._config)
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
