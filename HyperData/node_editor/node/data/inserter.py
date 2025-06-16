from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import Toggle
from ui.base_widgets.spinbox import TransparentSpinBox

DEBUG = False

class DataInserter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
        
        self._config = dict(
            loc=0,
            allow_duplicates=True,
        )
    
    def config(self):
        dialog = Dialog(title="Insert Data", parent=self.parent)

        loc = TransparentSpinBox(
            text="Column index",
            text2="Insertion index",
            getter=lambda: self._config["loc"],
            layout=dialog.main_layout
        )
        try: loc.button.setMaximum(len(self.node.input_sockets[0].socket_data.columns))
        except: loc.button.setMaximum(0)

        allow_duplicates = Toggle(
            text="Allow duplicates",
            text2="If not selected, the execution " \
            "will raise error if column is already contained in the DataFrame",
            getter=lambda: self._config["allow_duplicates"],
            layout=dialog.main_layout
        )

        if dialog.exec():
            self._config["loc"] = loc.button.value()
            self._config["allow_duplicates"] = allow_duplicates.button.isChecked()
            self.exec()    
        
    def func(self):
        if DEBUG or GLOBAL_DEBUG:
            from sklearn import datasets
            data = datasets.load_iris()
            df = pd.DataFrame(data=data.data, columns=data.feature_names)
            df["target_names"] = pd.Series(data.target).map({i: name for i, name in enumerate(data.target_names)})
            self.node.input_sockets[0].socket_data = df
            self.node.input_sockets[1].socket_data = df
            print('data in', self.node.input_sockets[0].socket_data, self.node.input_sockets[1].socket_data)

        try:
            data = self.node.input_sockets[0].socket_data.copy(deep=True)
            loc = self._config["loc"]
            for col in self.node.input_sockets[1].socket_data.columns:
                data.insert(
                    value=self.node.input_sockets[1].socket_data[col], 
                    column=col,
                    loc=loc,
                    allow_duplicates=self._config["allow_duplicates"]
                )
                loc += 1
            
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            node1 = self.node.input_sockets[0].edges[0].start_socket.node
            node2 = self.node.input_sockets[1].edges[0].start_socket.node
            logger.info(f"{self.name} {self.node.id}: insert data from {node2} {node2.id} into {node1} {node1.id} successfully.")
           
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
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()  
        self.node.input_sockets[1].socket_data = pd.DataFrame()  
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data