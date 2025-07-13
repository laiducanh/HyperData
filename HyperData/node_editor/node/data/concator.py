from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HToggle, HGroupRadioButton
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel, BodyLabel
from ui.base_widgets.frame import SeparateHLine

DEBUG = False

class DataConcator(NodeContentWidget):
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
        dialog.main_layout.addWidget(BodyLabel("Concatenate DataFrames along a particular axis"))
        dialog.main_layout.addWidget(SeparateHLine())
        axis = HGroupRadioButton(
            items=["index","columns"], 
            label='Axis',
            label2='Choose axis to concatenate along',
            getter=lambda: self._config['axis'],
            layout=dialog.main_layout
        )
        join = HGroupRadioButton(
            items=['inner','outer'],
            label='Join',
            label2='How to handle indexes on other axis',
            getter=lambda: self._config['join'],
            layout=dialog.main_layout
        )
        ignore_index = HToggle(
            label="Do not use the index values along the concatenation axis", 
            getter=lambda: self._config['ignore_index'],
            layout=dialog.main_layout
        )
        sort = HToggle(
            label='Sort non-concatenation axis if it is not already aligned',
            getter=lambda: self._config["sort"],
            layout=dialog.main_layout
        )

        if dialog.exec(): 
            self._config["axis"] = axis.get_value()
            self._config["join"] = join.get_value()
            self._config["ignore_index"] = ignore_index.get_value()
            self._config["sort"] = sort.get_value()
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
            logger.info(f"{self.name} {self.node.id}: run successfully.")
        
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