from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import TransparentComboBox, Toggle
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine

DEBUG = False

class DataConcator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = list()
        self._config = dict(
            axis='index',
            join='outer',
            ignore_index=False,
            sort=False
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.main_layout.addWidget(TitleLabel("Concatenation"))
        dialog.main_layout.addWidget(SeparateHLine())
        axis = TransparentComboBox(
            items=["index","columns"], 
            text='Axis',
            text2='Choose axis to concatenate along')
        axis.button.setCurrentText(self._config['axis'])
        dialog.main_layout.addWidget(axis)
        
        dialog.main_layout.addWidget(TitleLabel("Index"))
        dialog.main_layout.addWidget(SeparateHLine())
        join = TransparentComboBox(
            items=['inner','outer'],
            text='Join',
            text2='How to handle indexes on other axis')
        join.button.setCurrentText(self._config['join'])
        dialog.main_layout.addWidget(join)
        ignore_index = Toggle(
            text="Ignore index", 
            text2="The index along the concatenation axis will be ignored")
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.main_layout.addWidget(ignore_index)
        sort = Toggle(
            text="Sort", 
            text2='Sort non-concatenation axis if it is not already aligned')
        sort.button.setChecked(self._config["sort"])
        dialog.main_layout.addWidget(sort)

        if dialog.exec(): 
            self._config["axis"] = axis.button.currentText()
            self._config["join"] = join.button.currentText()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self._config["sort"] = sort.button.isChecked()
            self.exec()
    
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data.append(df)
            self.node.input_sockets[0].socket_data.append(df)
            print('data in', self.node.input_sockets[0].socket_data)

        try: 
            data: pd.DataFrame = pd.concat(
                objs=self.node.input_sockets[0].socket_data,
                **self._config
            )
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            connectedEdges = self.node.input_sockets[0].edges
            connectedNodes = [edge.start_socket.node for edge in connectedEdges]
            logger.info(f"{self.name} {self.node.id}: concated data from {connectedNodes} {[node.id for node in connectedNodes]} successfully.")
        
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
        self.resetNode()
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data.append(edge.start_socket.socket_data)