from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from config.settings import logger, encode, GLOBAL_DEBUG
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import _ComboBox, _TransparentToolButton, _TransparentPushButton
from PySide6.QtWidgets import QHBoxLayout, QWidget, QApplication

DEBUG = False

class SorterWidget(QWidget):
    def __init__(self, data:pd.DataFrame, by:str, order:bool, parent:Dialog):
        super().__init__(parent)
        self.hlayout = QHBoxLayout(self)
        self.hlayout.setContentsMargins(0,0,0,0)

        idx = parent.main_layout.count()-1
        parent.main_layout.insertWidget(idx, self)

        self.col = _ComboBox(parent=parent)
        self.col.setObjectName("by")
        if not data.empty: self.col.addItems(data.columns)
        self.col.setCurrentText(by)
        self.hlayout.addWidget(self.col)

        self.ascending = _ComboBox(["ascending","descending"],parent=parent)
        self.ascending.setObjectName("ascending")
        if order: self.ascending.setCurrentText("ascending")
        else: self.ascending.setCurrentText("descending")
        self.hlayout.addWidget(self.ascending)

        delete = _TransparentToolButton(parent=parent)
        delete.setIcon("delete.png")
        delete.pressed.connect(self.onDelete)
        self.hlayout.addWidget(delete)

    def onDelete(self):
        self.parent().main_layout.removeWidget(self)
        self.deleteLater()
        QApplication.processEvents()
        self.parent().adjustSize()

class DataSorter (NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.initConfig()
    
    def initConfig(self):
        if self.node.input_sockets[0].socket_data.empty:
            by = [""]
        else: by = self.node.input_sockets[0].socket_data.columns[0]

        self._config = dict(
            by = by,
            ascending = [True],
        )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        
        def add(by="", order=True):
            SorterWidget(self.node.input_sockets[0].socket_data, by, order, dialog)

        add_btn = _TransparentPushButton(self)
        add_btn.setIcon("add.png")
        add_btn.pressed.connect(add)
        dialog.main_layout.addWidget(add_btn)

        for by, order in zip(self._config.get("by"), self._config.get("ascending")):
            add(by, order)

        if dialog.exec():
            # reset self._config
            self._config = dict(by=[],ascending=[])
            for btn in dialog.findChildren(_ComboBox):
                btn : _ComboBox
                if btn.objectName() == "by":
                    self._config["by"].append(btn.currentText())
                if btn.objectName() == "ascending":
                    self._config["ascending"].append(True if btn.currentText()=="ascending" else False)
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
            data: pd.DataFrame = self.node.input_sockets[0].socket_data.sort_values(**self._config)
            # change progressbar's color
            self.progress.changeColor('success')
            # write log
            logger.info(f"{self.name} {self.node.id}: sorted data successfully.")
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