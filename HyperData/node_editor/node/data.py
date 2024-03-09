from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
import qfluentwidgets, pathlib
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.text import EditableComboBox, Completer
from config.settings import logger
from PyQt6.QtWidgets import QFileDialog, QWidget, QStackedLayout, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

DEBUG = True
    
class DataHolder (NodeContentWidget):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Load data')
        
    def exec (self):
        import_dlg = QFileDialog()
        import_dlg.setWindowTitle("Import data")

        if import_dlg.exec():
            selectedFiles = import_dlg.selectedFiles()[0]
            logger.info(f"Select {selectedFiles}.")
            suffix = pathlib.Path(selectedFiles).suffix
            if suffix == ".csv":
                self.node.data_out = pd.read_csv(selectedFiles)
                logger.info(f"Load a csv file.")
            elif suffix in [".xls", ".xlsx"]:
                self.node.data_out = pd.read_excel(selectedFiles)
                logger.info(f"Load an excel file.")
            else:
                self.node.data_out = pd.DataFrame()
                logger.warning("Cannot read data file, return an empty DataFrame.")
            
            self.node.data_in = self.node.data_out
            
        
        super().exec()
        logger.info("DataHolder run successfully.")

class DataTranspose (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def exec(self):
        try: self.node.data_out = self.node.data_in.transpose()
        except Exception as e: 
            self.node.data_out = pd.DataFrame()
            logger.error(f"{repr(e)}, return an empty DataFrame.")

        super().exec()
        logger.info("DataTranspose run successfully.")
        
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.data_in = pd.DataFrame()
        else:
            self.node.data_in = self.node.input_sockets[0].edges[0].start_socket.node.data_out
        

class DataConcator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__(node, parent)
        self.node.data_out = pd.DataFrame()
        self.node.data_in = list()
        self._config = dict(axis='index',join='outer',ignore_index=False)
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        axis = ComboBox(items=["index","columns"], text='Axis')
        axis.button.setCurrentText(self._config['axis'].title())
        dialog.textLayout.addWidget(axis)
        join = ComboBox(items=['inner','outer'],text='Join')
        join.button.setCurrentText(self._config['join'].title())
        dialog.textLayout.addWidget(join)
        ignore_index = Toggle("Ignore index")
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.textLayout.addWidget(ignore_index)
        if dialog.exec(): 
            self._config["axis"] = axis.button.currentText().lower()
            self._config["join"] = join.button.currentText().lower()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()
    
    def exec(self):
        
        if self.node.data_in != []: 
            try: self.node.data_out = pd.concat(objs=self.node.data_in,
                                           axis=self._config["axis"],
                                           join=self._config["join"],
                                           ignore_index=self._config["ignore_index"])
            except Exception as e:
                self.node.data_out = pd.DataFrame()
                logger.error(f"{repr(e)}, return an empty DataFrame.")
        else:
            self.node.data_out = pd.DataFrame()
        
        super().exec()
        logger.info("DataConcator run successfully.")

    def eval(self):
        self.node.data_in = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.data_in.append(edge.start_socket.node.data_out)

class DataCombiner (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.exec_btn.setText('Combine')
        self.node.data_out = pd.DataFrame()
        self.node.data_in = list()
    
    def exec(self):
        self.node.data_out = pd.DataFrame()
        try:
            for data in self.node.data_in:
                self.node.data_out = self.node.data_out.combine(data, np.minimum)
        except Exception as e:
            self.node.data_out = pd.DataFrame()
            logger.error(f"{repr(e)}, return an empty DataFrame.")

        super().exec()
        logger.info("DataCombiner run successfully.")

    def eval(self):
        self.node.data_in = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.data_in.append(edge.start_socket.node.data_out)

class DataMerge (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.exec_btn.setText('Merge')
        self.node.data_out = pd.DataFrame()
        self.node.data_in = list()
    
    def exec(self):
        try:
            if len(self.node.data_in) == 2:
                data_left = self.node.data_in[0]
                data_right = self.node.data_in[1]
                self.node.data_out = data_left.merge(data_right)
            elif len(self.node.data_in) == 1:
                self.node.data_out = self.node.data_in[0]
            else:
                self.node.data_out = pd.DataFrame()
        except Exception as e:
            self.node.data_out = pd.DataFrame()
            logger.error(f"{repr(e)}, return an empty DataFrame.")

        super().exec()
        if DEBUG: print("DataMerge run successfully")
    
    def eval(self):
        self.node.data_in = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.data_in.insert(0,edge.start_socket.node.data_out)
        for edge in self.node.input_sockets[1].edges:
            self.node.data_in.insert(1,edge.start_socket.node.data_out)

class DataCompare (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.data_out = pd.DataFrame()
        self.node.data_in = list()
    
    def exec(self):
        try:
            if len(self.node.data_in) == 2:
                data_left = self.node.data_in[0]
                data_right = self.node.data_in[1]
                self.node.data_out = data_left.compare(data_right)
            elif len(self.node.data_in) == 1:
                self.node.data_out = self.node.data_in[0]
            else:
                self.node.data_out = pd.DataFrame()
        except Exception as e:
            self.node.data_out = pd.DataFrame()
            logger.error(f"{repr(e)}, return an empty DataFrame.")

        super().exec()
        logger.info("DataCompare run successfully.")
    
    def eval(self):
        self.node.data_in = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.data_in.insert(0,edge.start_socket.node.data_out)
        for edge in self.node.input_sockets[1].edges:
            self.node.data_in.insert(1,edge.start_socket.node.data_out)

class DataSplitter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        if self.node.data_in.empty:
            self._config = dict(type="columns",
                            column_from=None,column_to=None,
                            row_from=1,row_to=None)
        else:
            self._config = dict(type="columns",
                            column_from=self.node.data_in.columns[0],
                            column_to=self.node.data_in.columns[-1],
                            row_from=1,row_to=1+self.node.data_in.shape[0])

    def config(self):
        dialog = Dialog("Configuration", self.parent)

        type = ComboBox(items=["columns","rows"], text="type")
        type.button.setCurrentText(self._config["type"].title())
        type.button.currentTextChanged.connect(lambda: stacklayout.setCurrentIndex(type.button.currentIndex()))
        dialog.textLayout.addWidget(type)

        stacklayout = QStackedLayout()
        dialog.textLayout.addLayout(stacklayout)

        col = QWidget()
        col_layout = QVBoxLayout()
        col.setLayout(col_layout)
        stacklayout.addWidget(col)

        col_from = EditableComboBox(text="from column")
        col_from.button.setCompleter(completer=Completer(self.node.data_in.columns))
        col_from.button.setCurrentText(self._config["column_from"])
        col_layout.addWidget(col_from)

        col_to = EditableComboBox(text="to column")
        col_to.button.setCompleter(completer=Completer(self.node.data_in.columns))
        col_to.button.setCurrentText(self._config["column_to"])
        col_layout.addWidget(col_to)

        row = QWidget()
        row_layout = QVBoxLayout()
        row.setLayout(row_layout)
        stacklayout.addWidget(row)

        row_from = EditableComboBox(text="from row")
        row_from.button.setCompleter(completer=Completer([str(i) for i in range(1,1+self.node.data_in.shape[0])]))
        row_from.button.setCurrentText(self._config["row_from"])
        row_layout.addWidget(row_from)

        row_to = EditableComboBox(text="to row")
        row_to.button.setCompleter(completer=Completer([str(i) for i in range(1,1+self.node.data_in.shape[0])]))
        row_to.button.setCurrentText(self._config["row_to"])
        row_layout.addWidget(row_to)

        stacklayout.setCurrentIndex(type.button.currentIndex())

        if dialog.exec():
            self._config["type"] = type.button.currentText().lower()
            self._config["column_from"] = col_from.button.text()
            self._config["column_to"] = col_to.button.text()
            self._config["row_from"] = row_from.button.text()
            self._config["row_to"] = row_to.button.text()
            self.exec()

    def exec(self):
        try:

            if self._config["type"] == "columns":
                col_from = self.node.data_in.columns.get_loc(self._config["column_from"])
                col_to = self.node.data_in.columns.get_loc(self._config["column_to"])+1
                self.node.data_out = self.node.data_in.iloc[:,col_from:col_to]

            elif self._config["type"] == "rows":
                row_from = int(self._config["row_from"])-1
                row_to = int(self._config["row_to"])
                self.node.data_out = self.node.data_in.iloc[row_from:row_to,:]

            if DEBUG: print("DataSplitter run successfully")

        except Exception as e:
            logger.error(f"{repr(e)}, return the original DataFrame.") 
            self.node.data_out = self.node.data_in

        super().exec()
        logger.infor("DataSplitter run successfully.")
    
    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.data_in = pd.DataFrame()
        else:
            self.node.data_in = self.node.input_sockets[0].edges[0].start_socket.node.data_out