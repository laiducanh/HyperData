from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
import platform
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.line_edit import CompleterLineEdit, Completer, TextEdit
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from data_processing.data_window import TableModel
from config.settings import logger, encode
from PyQt6.QtWidgets import QFileDialog, QWidget, QStackedLayout, QVBoxLayout, QTableView


DEBUG = True
    
class DataReader (NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Load data')
        self.node.output_sockets[0].socket_data = pd.DataFrame()
        self.parent = parent
        self._config = dict(nrows=100000,delimiter=",",header=0,
                            skip_blank_lines=True,encoding="utf_8")
        self.selectedFiles = None
        self.filetype = "csv"
        self.isReadable = True
    
    def check_filetype (self, file):
        functionList = [pd.read_csv, pd.read_excel]
        filetypeList= ["csv","excel"]
        
        read = 0
        for func, self.filetype in zip(functionList,filetypeList):
            try:
                self.node.output_sockets[0].socket_data = func(file,nrows=1)
                self.isReadable = True
                break
            except: read += 1
        if read == len(functionList):
            self.isReadable = False
        
    def config(self):
        # Note that this configuration works for csv file
        
        dialog = Dialog("Configuration", self.parent.parent)
        nrows = SpinBox(max=100000, text="Number of rows")
        dialog.main_layout.addWidget(nrows)
        nrows.button.setValue(self._config["nrows"])
        self.delimiter = ComboBox(items=["Tab","Semicolon","Comma","Space"],
                             text="Delimiter")
        self._delimiterDict = dict(Tab="\t",Semicolon=";",Comma=",",Space=" ")
        self.delimiter.button.setCurrentText(list(self._delimiterDict.keys())
                                        [list(self._delimiterDict.values()).index(self._config["delimiter"])])
        dialog.main_layout.addWidget(self.delimiter)
        self.delimiter.button.currentTextChanged.connect(self.update_preview)
        self.header = Toggle(text="Header")
        if self._config["header"] == 0:
            self.header.button.setChecked(True)
        else: self.header.button.setChecked(False)
        dialog.main_layout.addWidget(self.header)
        self.header.button.checkedChanged.connect(self.update_preview)
        self.skip_blank_lines = Toggle(text="Skip blank lines")
        self.skip_blank_lines.button.setChecked(self._config["skip_blank_lines"])
        dialog.main_layout.addWidget(self.skip_blank_lines)
        self.skip_blank_lines.button.checkedChanged.connect(self.update_preview)
        self.encoding = ComboBox(items=encode,text="Encoding")
        dialog.main_layout.addWidget(self.encoding)
        self.encoding.button.setCurrentText(self._config["encoding"])
        self.encoding.button.currentTextChanged.connect(self.update_preview)
        self.sheet_name = ComboBox(text="Sheet name")
        dialog.main_layout.addWidget(self.sheet_name)
        self.sheet_name.button.currentTextChanged.connect(self.update_preview)
        if self.filetype == "excel":
            self.sheet_name.button.addItems(pd.ExcelFile(self.selectedFiles).sheet_names)

        dialog.main_layout.addWidget(BodyLabel("Data Preview"))
        dialog.main_layout.addWidget(SeparateHLine())
        self.preview = QTableView()
        self.update_preview()
        dialog.main_layout.addWidget(self.preview)
        

        if dialog.exec(): 
            self._config["nrows"] = nrows.button.value()
            self._config["delimiter"] = self._delimiterDict[self.delimiter.button.currentText()]
            self._config["header"] = "infer" if self.header.button.isChecked() else None
            self._config["encoding"] = self.encoding.button.currentText()
            self._config["sheet_name"] = self.sheet_name.button.currentText()
            super().exec(self.selectedFiles)
    
    def update_preview (self):
        delimiter = self._delimiterDict[self.delimiter.button.currentText()]
        header = self.header.button.isChecked()
        skip_blank_lines = self.skip_blank_lines.button.isChecked()
        encoding = self.encoding.button.currentText()
        sheet_name = self.sheet_name.button.currentText()
        
        if header: header=0
        else: header=None

        data = pd.DataFrame()

        if self.selectedFiles and self.isReadable:
            if self.filetype == "csv":
                data = pd.read_csv(self.selectedFiles, nrows=10,header=header,
                                   delimiter=delimiter,skip_blank_lines=skip_blank_lines,
                                   encoding=encoding)
            elif self.filetype == "excel":
                data = pd.read_excel(self.selectedFiles, nrows=10,header=header,
                                     sheet_name=sheet_name)
        self.model = TableModel(data, self.parent)
        self.preview.setModel(self.model)
            
    def exec (self):    
        
        import_dlg = QFileDialog()
        if platform.system() == "Darwin":
            # MacOS has a bug that prevents native dialog from properly working
            # then use the option of DontUseNativeDialog
            import_dlg.setOption(QFileDialog.Option.DontUseNativeDialog)
        import_dlg.setWindowTitle("Import data")

        if import_dlg.exec():
            self.selectedFiles = import_dlg.selectedFiles()[0]
            logger.info(f"{self.name} {self.node.id}::Select {self.selectedFiles}.")
            self.label.setText(f'Shape: (--, --)') # reset Shape label
            super().exec(self.selectedFiles)
    
    def func (self, selectedFiles):
        
        if self.isReadable:
            if self.filetype == "csv":
                data = pd.read_csv(selectedFiles, nrows=self._config["nrows"],
                                   header=self._config["header"],
                                   delimiter=self._config["delimiter"],
                                   skip_blank_lines=self._config["skip_blank_lines"],
                                   encoding=self._config["encoding"])
                logger.info(f"{self.name} {self.node.id}::Load a csv file.")
            elif self.filetype == "excel":
                data = pd.read_excel(selectedFiles, nrows=self._config["nrows"],
                                     header=self._config["header"])
                logger.info(f"{self.name} {self.node.id}::Load an excel file.")
        else:
            data = pd.DataFrame()
            logger.warning(f"{self.name} {self.node.id}::Cannot read data file, return an empty DataFrame.")
        
        self.node.output_sockets[0].socket_data = data
    
        self.data_to_view = data
    
    def eval(self):
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data


class DataHolder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
        
    def func(self):
        try:
            connect_to_edge = self.node.input_sockets[0].edges[0]
            connect_to_node = connect_to_edge.start_socket.node
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.copy(deep=True)
            logger.info(f"{self.name} {self.node.id}::copy data from {connect_to_node.content.name} {connect_to_node.id} successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            logger.error(f"{self.name} {self.node.id}::{repr(e)}, return an empty DataFrame.")
        
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
        dialog.main_layout.addWidget(axis)
        join = ComboBox(items=['inner','outer'],text='Join')
        join.button.setCurrentText(self._config['join'].title())
        dialog.main_layout.addWidget(join)
        ignore_index = Toggle("Ignore index")
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.main_layout.addWidget(ignore_index)
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
        type.button.setCurrentText(self._config["type"])
        type.button.currentTextChanged.connect(lambda: stacklayout.setCurrentIndex(type.button.currentIndex()))
        dialog.main_layout.addWidget(type)

        dialog.main_layout.addWidget(SeparateHLine())

        stacklayout = QStackedLayout()
        dialog.main_layout.addLayout(stacklayout)

        col = QWidget()
        col_layout = QVBoxLayout()
        col_layout.setContentsMargins(0,0,0,0)
        col.setLayout(col_layout)
        stacklayout.addWidget(col)

        col_from = CompleterLineEdit(text="from column")
        col_layout.addWidget(col_from)

        col_to = CompleterLineEdit(text="to column")
        col_layout.addWidget(col_to)

        row = QWidget()
        row_layout = QVBoxLayout()
        row_layout.setContentsMargins(0,0,0,0)
        row.setLayout(row_layout)
        stacklayout.addWidget(row)

        row_from = CompleterLineEdit(text="from row")
        row_layout.addWidget(row_from)

        row_to = CompleterLineEdit(text="to row")
        row_layout.addWidget(row_to)
        
        if self.node.input_sockets[0].socket_data.shape[0] < 1000:
            try:
                row_from.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.index+1)))
                row_to.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.index+1)))
            except: pass
        if self.node.input_sockets[0].socket_data.shape[1] < 1000:
            try:
                col_from.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.columns)))
                col_to.button._addItems(items=list(map(str, self.node.input_sockets[0].socket_data.columns)))
            except: pass

        col_from.button.setCurrentText(str(self._config["column_from"]))
        col_to.button.setCurrentText(str(self._config["column_to"]))
        row_from.button.setCurrentText(str(self._config["row_from"]))
        row_to.button.setCurrentText(str(self._config["row_to"]))

        stacklayout.setCurrentIndex(type.button.currentIndex())
        
        if dialog.exec():
            self._config["type"] = type.button.currentText()
            self._config["column_from"] = col_from.button.currentText()
            self._config["column_to"] = col_to.button.currentText()
            self._config["row_from"] = row_from.button.currentText()
            self._config["row_to"] = row_to.button.currentText()
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
            try:
                if axis.button.currentText().lower() == "columns":
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.columns])) 
                else:
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.index])) 
            except: pass

        axis = ComboBox(items=["columns","index"], text="Filter by")
        axis.button.setCurrentText(self._config["axis"].title())
        axis.button.currentTextChanged.connect(func1)
        dialog.main_layout.addWidget(axis)

        type = ComboBox(items=["items","contains","regular expression"], text="filter type")
        type.button.setCurrentText(self._config["type"].title())
        dialog.main_layout.addWidget(type)

        def func2 ():
            if type.button.currentText().lower() == "items":
                if apply.button.toPlainText() == '':
                    string = list()
                else:
                    string = apply.button.toPlainText().split(",")
                string.append(labels.button.currentText())
                apply.button.setText(",".join(string))
            else:
                apply.button.setText(labels.button.currentText())
            labels.button.clear()

        labels = CompleterLineEdit(text="labels")
        labels.button.lineedit.returnPressed.connect(func2)
        func1()
        dialog.main_layout.addWidget(labels)

        apply = TextEdit(text="Keep labels")
        apply.button.setText(",".join(self._config["apply"]))
        dialog.main_layout.addWidget(apply)

        

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
        