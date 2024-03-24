from node_editor.base.node_graphics_content import NodeContentWidget, NodeComment
import pandas as pd
import numpy as np
import qfluentwidgets, pathlib
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.text import EditableComboBox, Completer, TextEdit
from config.settings import logger
from config.threadpool import Worker
from PyQt6.QtWidgets import QFileDialog, QWidget, QStackedLayout, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QThreadPool

DEBUG = True
    
class DataReader (NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Load data')
        self.node.output_sockets[0].socket_data = pd.DataFrame()
        
    def exec (self):    
        
        import_dlg = QFileDialog()
        import_dlg.setWindowTitle("Import data")

        if import_dlg.exec():
            selectedFiles = import_dlg.selectedFiles()[0]
            logger.info(f"Select {selectedFiles}.")

            self.run_threadpool(selectedFiles)
    
    def func (self, selectedFiles):
        suffix = pathlib.Path(selectedFiles).suffix
        if suffix == ".csv":
            self.node.output_sockets[0].socket_data = pd.read_csv(selectedFiles)
            logger.info(f"Load a csv file.")
        elif suffix in [".xls", ".xlsx"]:
            self.node.output_sockets[0].socket_data = pd.read_excel(selectedFiles)
            logger.info(f"Load an excel file.")
        else:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.warning("Cannot read data file, return an empty DataFrame.")
    
    
        self.data_to_view = self.node.output_sockets[0].socket_data
        

class DataHolder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def func(self):
        try:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.copy(deep=True)
            logger.info(f"{self.name} run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data

    def eval(self):
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data

class DataTranspose (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def func(self):
        try: 
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.transpose()
            logger.info(f"{self.name} run successfully.")
        except Exception as e: 
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
        
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data


class DataConcator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__(node, parent)
        self.node.input_sockets[0].socket_data = list()
        self._config = dict(axis='index',join='outer',ignore_index=False)
    
    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)
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
    
    def func(self):
        
        if self.node.input_sockets[0].socket_data != []: 
            try: 
                self.node.output_sockets[0].socket_data = pd.concat(objs=self.node.input_sockets[0].socket_data,
                                           axis=self._config["axis"],
                                           join=self._config["join"],
                                           ignore_index=self._config["ignore_index"])
                logger.info(f"{self.name} run successfully.")
            except Exception as e:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
                logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        else:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.info(f"{self.name} Not enough input, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data

    def eval(self):
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data.append(edge.start_socket.socket_data)

class DataCombiner (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.exec_btn.setText('Combine')
        self.node.input_sockets[0].socket_data = list()
    
    def func(self):
        self.node.output_sockets[0].socket_data = pd.DataFrame()
        try:
            for data in self.node.input_sockets[0].socket_data:
                self.node.output_sockets[0].socket_data = self.node.output_sockets[0].socket_data.combine(data, np.minimum)
            logger.info(f"{self.name} run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data        

    def eval(self):
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data.append(edge.start_socket.socket_data)

class DataMerge (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.exec_btn.setText('Merge')

    def func(self):
        try:
            if self.node.input_sockets[0].socket_data != None and self.node.input_sockets[1].socket_data != None:
                data_left = self.node.input_sockets[0].socket_data
                data_right = self.node.input_sockets[1].socket_data
                self.node.output_sockets[0].socket_data = data_left.merge(data_right)
            elif self.node.input_sockets[0].socket_data != None:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            elif self.node.input_sockets[1].socket_data != None:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[1].socket_data
            else:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.info(f"{self.name} run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval(self):
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data

class DataCompare (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
    
    def func(self):
        try:
            if self.node.input_sockets[0].socket_data != None and self.node.input_sockets[1].socket_data != None:
                data_left = self.node.input_sockets[0].socket_data
                data_right = self.node.input_sockets[1].socket_data
                self.node.output_sockets[0].socket_data = data_left.compare(data_right)
            elif self.node.input_sockets[0].socket_data != None:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            elif self.node.input_sockets[1].socket_data != None:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[1].socket_data
            else:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.info(f"{self.name} run successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {repr(e)}, return an empty DataFrame.")
        
        self.data_to_view = self.node.output_sockets[0].socket_data
    
    def eval(self):
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data

class DataLocator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self.initConfig()
        
    def initConfig (self):
        if self.node.input_sockets[0].socket_data.empty:
            self._config = dict(type="columns",
                            column_from=None,column_to=None,
                            row_from=None,row_to=None)
        else:
            self._config = dict(type="columns",
                            column_from=self.node.input_sockets[0].socket_data.columns[0],
                            column_to=self.node.input_sockets[0].socket_data.columns[-1],
                            row_from=1,row_to=self.node.input_sockets[0].socket_data.shape[0])

    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)

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
        col_from.button.setCompleter(completer=Completer(self.node.input_sockets[0].socket_data.columns))
        col_from.button.setText(str(self._config["column_from"]))
        col_layout.addWidget(col_from)

        col_to = EditableComboBox(text="to column")
        col_to.button.setCompleter(completer=Completer(self.node.input_sockets[0].socket_data.columns))
        col_to.button.setText(str(self._config["column_to"]))
        col_layout.addWidget(col_to)

        row = QWidget()
        row_layout = QVBoxLayout()
        row.setLayout(row_layout)
        stacklayout.addWidget(row)

        row_from = EditableComboBox(text="from row")
        row_from.button.setCompleter(completer=Completer([str(i) for i in range(1,1+self.node.input_sockets[0].socket_data.shape[0])]))
        row_from.button.setText(str(self._config["row_from"]))
        row_layout.addWidget(row_from)

        row_to = EditableComboBox(text="to row")
        row_to.button.setCompleter(completer=Completer([str(i) for i in range(1,1+self.node.input_sockets[0].socket_data.shape[0])]))
        row_to.button.setText(str(self._config["row_to"]))
        row_layout.addWidget(row_to)

        stacklayout.setCurrentIndex(type.button.currentIndex())

        if dialog.exec():
            self._config["type"] = type.button.currentText().lower()
            self._config["column_from"] = col_from.button.text()
            self._config["column_to"] = col_to.button.text()
            self._config["row_from"] = row_from.button.text()
            self._config["row_to"] = row_to.button.text()
            self.exec()

    def func(self):
        try:

            if self._config["type"] == "columns":
                col_from = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_from"])
                col_to = self.node.input_sockets[0].socket_data.columns.get_loc(self._config["column_to"])+1
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.iloc[:,col_from:col_to]

            elif self._config["type"] == "rows":
                row_from = int(self._config["row_from"])-1
                row_to = int(self._config["row_to"])
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.iloc[row_from:row_to,:]

            logger.info(f"{self.name} run successfully.")

        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            logger.error(f"{self.name} {repr(e)}, return the original DataFrame.") 
            
        self.data_to_view = self.node.output_sockets[0].socket_data
    
    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data

        self.initConfig()

class DataFilter (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(axis="columns",type="items",apply=str())
    
    def config(self):
        dialog = Dialog("Configuration", self.parent.parent)

        def func1():
            if axis.button.currentText().lower() == "columns":
                labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.columns])) 
            else:
                labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.index])) 

        axis = ComboBox(items=["columns","index"], text="Filter by")
        axis.button.setCurrentText(self._config["axis"].title())
        axis.button.currentTextChanged.connect(func1)
        dialog.textLayout.addWidget(axis)

        type = ComboBox(items=["items","contains","regular expression"], text="filter type")
        type.button.setCurrentText(self._config["type"].title())
        dialog.textLayout.addWidget(type)

        def func2 ():
            if type.button.currentText().lower() == "items":
                if apply.button.toPlainText() == '':
                    string = list()
                else:
                    string = apply.button.toPlainText().split(",")
                string.append(labels.button.text())
                apply.button.setText(",".join(string))
            else:
                apply.button.setText(labels.button.text())
            labels.button.clear()

        labels = EditableComboBox(text="labels")
        labels.button.returnPressed.connect(func2)
        func1()
        dialog.textLayout.addWidget(labels)

        apply = TextEdit(text="Keep labels")
        apply.button.setText(",".join(self._config["apply"]))
        dialog.textLayout.addWidget(apply)

        

        if dialog.exec():
            self._config["axis"] = axis.button.currentText().lower()
            self._config["type"] = type.button.currentText().lower()
            self._config["apply"] = apply.button.toPlainText().split(",")
            print(self._config)
            self.exec()
    

    def func(self):
        try:
            if self._config["type"] == "items":
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.filter(axis=self._config["axis"],
                                                                                                        items=self._config["apply"])
            elif self._config["type"] == "contains":
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.filter(axis=self._config["axis"],
                                                                                                        like=self._config["apply"][0])
            elif self._config["type"] == "regular expression":
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.filter(axis=self._config["axis"],
                                                                                                        regex=self._config["apply"][0])
                
            logger.info(f"{self.name} run successfully.")

        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            logger.error(f"{self.name} {repr(e)}, return the original DataFrame.") 
        
        self.data_to_view = self.node.output_sockets[0].socket_data
    
    def eval(self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        