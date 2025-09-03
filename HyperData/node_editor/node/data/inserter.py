from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.button import HToggle, HGroupRadioButton
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.window import Dialog
from ui.base_widgets.text import TitleLabel, BodyLabel
from ui.base_widgets.frame import SeparateHLine, VFrame

DEBUG = False

class DataInserter(NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = list()
        self._config = dict(
            axis='index',
            join='outer',
            loc=0,
            ignore_index=False,
            sort=False
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        dialog.setMinimumSize(600, 400)
        dialog.main_layout.addWidget(TitleLabel("Data Insertion"))
        dialog.main_layout.addWidget(BodyLabel("Insert a DataFrame into another DataFrame at "
                                               "a specific location along a particular axis"))
        dialog.main_layout.addWidget(SeparateHLine())
        fr = VFrame(dialog.main_layout)
        axis = HGroupRadioButton(
            items=["index","columns"], 
            label='Axis',
            label2='Choose axis to concatenate along',
            getter=lambda: self._config['axis'],
            layout=fr.vlayout
        )
        join = HGroupRadioButton(
            items=['inner','outer'],
            label='Join',
            label2='How to handle indexes on other axis',
            getter=lambda: self._config['join'],
            layout=fr.vlayout
        )
        fr = VFrame(dialog.main_layout)
        loc = HTransparentSpinBox(
            label="Location",
            label2="Insertion index",
            getter=lambda: self._config["loc"],
            layout=fr.vlayout
        )
        ignore_index = HToggle(
            label="Do not use the index values along the concatenation axis", 
            getter=lambda: self._config['ignore_index'],
            layout=fr.vlayout
        )
        sort = HToggle(
            label='Sort non-concatenation axis if it is not already aligned',
            getter=lambda: self._config["sort"],
            layout=fr.vlayout
        )

        if dialog.exec(): 
            self._config["axis"] = axis.get_value()
            self._config["join"] = join.get_value()
            self._config["loc"] = loc.button.value()
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
            df1 = self.node.input_sockets[0].socket_data.copy(deep=True)
            df2 = self.node.input_sockets[1].socket_data.copy(deep=True)
            loc = self._config['loc']
            if self._config['axis'] == 'index':
                top = df1.iloc[:loc]
                bot = df1.iloc[loc:]
                data = pd.concat(
                    objs=[top, df2, bot],
                    join=self._config['join'],
                    axis=self._config['axis'],
                    ignore_index=self._config['ignore_index'],
                    sort=self._config['sort']
                )
            else:
                left = df1.iloc[:, :loc]
                right = df1.iloc[:, loc:]
                data = pd.concat(
                    objs=[left, df2, right],
                    join=self._config['join'],
                    axis=self._config['axis'],
                    ignore_index=self._config['ignore_index'],
                    sort=self._config['sort']
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
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        self.node.input_sockets[1].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data