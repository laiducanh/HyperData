from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import numpy as np
import platform
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle, _ComboBox, _TransparentToolButton, _TransparentPushButton
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.line_edit import CompleterLineEdit, Completer, TextEdit
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from data_processing.data_window import TableModel
from config.settings import logger, encode
from PySide6.QtWidgets import QFileDialog, QWidget, QStackedLayout, QVBoxLayout, QTableView, QHBoxLayout, QApplication, QMainWindow
from PySide6.QtCore import QFileSystemWatcher

DEBUG = True
    
class DataReader (NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Load data')
        self.node.output_sockets[0].socket_data = pd.DataFrame()
        self._config = dict(
            nrows=100000,
            delimiter=",",
            header=0,
            skip_blank_lines=True,
            encoding="utf_8",
            auto_update=True
            )
        self.selectedFiles = None
        self.filetype = "csv"
        self.isReadable = True
        self.watcher = QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.update_data)
    
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
        
        dialog = Dialog("Configuration", self.parent)
        auto_update = Toggle(text="Auto update")
        dialog.main_layout.addWidget(auto_update)
        auto_update.button.setChecked(self._config["auto_update"])
        nrows = SpinBox(max=100000, text="Number of rows")
        dialog.main_layout.addWidget(nrows)
        nrows.button.setValue(self._config["nrows"])
        self.delimiter = ComboBox(items=["Tab","Semicolon","Comma","Space"],
                             text="Delimiter",text2="abc")
        self._delimiterDict = dict(Tab="\t",Semicolon=";",Comma=",",Space=" ")
        self.delimiter.button.setCurrentText(list(self._delimiterDict.keys())
                                        [list(self._delimiterDict.values()).index(self._config["delimiter"])])
        dialog.main_layout.addWidget(self.delimiter)
        self.delimiter.button.currentTextChanged.connect(self.update_preview)
        self.header = Toggle(text="Header")
        self.header.button.setChecked(not self._config["header"])
        dialog.main_layout.addWidget(self.header)
        self.header.button.checkedChanged.connect(self.update_preview)
        self.skip_blank_lines = Toggle(text="Skip blank lines")
        self.skip_blank_lines.button.setChecked(self._config["skip_blank_lines"])
        dialog.main_layout.addWidget(self.skip_blank_lines)
        self.skip_blank_lines.button.checkedChanged.connect(self.update_preview)
        self.encoding = ComboBox(items=encode,text="Encoding",text2="abc")
        dialog.main_layout.addWidget(self.encoding)
        self.encoding.button.setCurrentText(self._config["encoding"])
        self.encoding.button.currentTextChanged.connect(self.update_preview)
        self.sheet_name = ComboBox(text="Sheet name",text2="abc")
        dialog.main_layout.addWidget(self.sheet_name)
        self.sheet_name.button.currentTextChanged.connect(self.update_preview)
        if self.filetype == "excel":
            self.sheet_name.button.addItems(pd.ExcelFile(self.selectedFiles).sheet_names)

        dialog.main_layout.addWidget(BodyLabel("Preview"))
        dialog.main_layout.addWidget(SeparateHLine())
        self.preview = QTableView()
        self.update_preview()
        dialog.main_layout.addWidget(self.preview)
        

        if dialog.exec(): 
            self._config["nrows"] = nrows.button.value()
            self._config["delimiter"] = self._delimiterDict[self.delimiter.button.currentText()]
            self._config["header"] = 0 if self.header.button.isChecked() else None
            self._config["encoding"] = self.encoding.button.currentText()
            self._config["sheet_name"] = self.sheet_name.button.currentText()
            self._config["auto_update"] = auto_update.button.isChecked()
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

    def update_data(self):
        # update the path in case some text editors replace the file with a new one
        # so the watcher will stop watching the old file
        self.watcher.addPath(self.selectedFiles)
        if self._config["auto_update"]:
            super().exec(self.selectedFiles)
            self.worker.signals.finished.connect(lambda: self.view.update_data(self.data_to_view))
            
    def exec (self):    
        
        importDialog = QFileDialog(caption="Import data")
        # MacOS has a bug that prevents native dialog from properly working
        # then use the option of DontUseNativeDialog
        if platform.system() == "Darwin":
            importDialog.setOption(QFileDialog.Option.DontUseNativeDialog)

        if importDialog.exec():
            self.selectedFiles = importDialog.selectedFiles()[0]      
            # add file path for watcher
            self.watcher.addPath(self.selectedFiles)
            # write log
            logger.info(f"DataReader {self.node.id}: Selected {self.selectedFiles}.")
            # reset Shape label before executing the main function
            self.label.setText('Shape: (--, --)') 
            # execute main function
            super().exec(self.selectedFiles)
    
    def func (self, selectedFiles):
        
        if self.isReadable:
            match self.filetype:
                case "csv":
                    data = pd.read_csv(selectedFiles, 
                                       nrows=self._config["nrows"],
                                       header=self._config["header"],
                                       delimiter=self._config["delimiter"],
                                       skip_blank_lines=self._config["skip_blank_lines"],
                                       encoding=self._config["encoding"])
                    # write log
                    logger.info(f"DataReader {self.node.id}: Loaded a csv file.")

                case "excel":
                    data = pd.read_excel(selectedFiles, 
                                         nrows=self._config["nrows"],
                                         header=self._config["header"])
                    # write log
                    logger.info(f"DataReader {self.node.id}: Loaded an excel file.")
        else:
            data = pd.DataFrame()
            # write log
            logger.warning(f"DataReader {self.node.id}: Couldn't read data file, return an empty DataFrame.")
            logger.info(f"DataReader {self.node.id}: failed, file format is not supported.")
        
        self.node.output_sockets[0].socket_data = data
        self.data_to_view = data


class DataHolder (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)
        
    def func(self):
        try:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.copy(deep=True)
            # write log
            connect_to_edge = self.node.input_sockets[0].edges[0]
            connect_to_node = connect_to_edge.start_socket.node
            logger.info(f"{self.name} {self.node.id}: copied data from {connect_to_node.content.name} {connect_to_node.id} successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
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
            # write log
            connect_to_edge = self.node.input_sockets[0].edges[0]
            connect_to_node = connect_to_edge.start_socket.node
            logger.info(f"{self.name} {self.node.id}: transposed data from {connect_to_node.content.name} {connect_to_node.id} successfully.")
        except Exception as e: 
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
        
    def eval (self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()            


class DataConcator (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode,parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = list()
        self._config = dict(
            axis='index',
            join='outer',
            ignore_index=False
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        axis = ComboBox(items=["index","columns"], text='Axis')
        axis.button.setCurrentText(self._config['axis'])
        dialog.main_layout.addWidget(axis)
        join = ComboBox(items=['inner','outer'],text='Join')
        join.button.setCurrentText(self._config['join'])
        dialog.main_layout.addWidget(join)
        ignore_index = Toggle("Ignore index")
        ignore_index.button.setChecked(self._config['ignore_index'])
        dialog.main_layout.addWidget(ignore_index)
        if dialog.exec(): 
            self._config["axis"] = axis.button.currentText()
            self._config["join"] = join.button.currentText()
            self._config["ignore_index"] = ignore_index.button.isChecked()
            self.exec()
    
    def func(self):
        
        if self.node.input_sockets[0].socket_data != []: 
            try: 
                self.node.output_sockets[0].socket_data = pd.concat(
                    objs=self.node.input_sockets[0].socket_data,
                    **self._config
                    )
                # write log
                connectedEdges = self.node.input_sockets[0].edges
                connectedNodes = [edge.start_socket.node for edge in connectedEdges]
                logger.info(f"{self.name} {self.node.id}: concated data from {connectedNodes} {[node.id for node in connectedNodes]} successfully.")
            except Exception as e:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
                # write log
                logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
                logger.exception(e)
        else:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.info(f"{self.name} {self.node.id}: Not enough input, return an empty DataFrame.")
        
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
        self._config = dict(
            func="minimum",
            overwrite=True
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)
        function = ComboBox(items=["take smaller","minimum"],text="Function")
        dialog.main_layout.addWidget(function)
        function.button.setCurrentText(self._config["func"])
        overwrite = Toggle(text="Overwrite")
        dialog.main_layout.addWidget(overwrite)
        overwrite.button.setChecked(self._config["overwrite"])

        if dialog.exec():
            self._config["func"] = function.button.currentText()
            self._config["overwrite"] = overwrite.button.isChecked()
            self.exec()
    
    def func(self):
        self.node.output_sockets[0].socket_data = pd.DataFrame()
        if self._config["func"] == "take smaller":
            func = lambda s1, s2: s1 if s1.sum() < s2.sum() else s2
        else:
            func = np.minimum
        overwrite = self._config["overwrite"]
        try:
            for data in self.node.input_sockets[0].socket_data:
                self.node.output_sockets[0].socket_data = self.node.output_sockets[0].socket_data.combine(data, func=func, overwrite=overwrite)
            # write log
            connectedEdges = self.node.input_sockets[0].edges
            connectedNodes = [edge.start_socket.node for edge in connectedEdges]
            logger.info(f"{self.name} {self.node.id}: combined data from {connectedNodes} {[node.id for node in connectedNodes]} successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
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
            if self.node.input_sockets[0].socket_data and self.node.input_sockets[1].socket_data:
                data_left = self.node.input_sockets[0].socket_data
                data_right = self.node.input_sockets[1].socket_data
                self.node.output_sockets[0].socket_data = data_left.merge(data_right)
            elif self.node.input_sockets[0].socket_data:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            elif self.node.input_sockets[1].socket_data:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[1].socket_data
            else:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            node1 = self.node.input_sockets[0].edges[0].start_socket.node
            node2 = self.node.input_sockets[1].edges[0].start_socket.node
            logger.info(f"{self.name} {self.node.id}: merged data from {node1} {node1.id} and {node2} {node2.id} successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
        self.data_to_view = self.node.output_sockets[0].socket_data        
    
    def eval(self):
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
        for edge in self.node.input_sockets[1].edges:
            self.node.input_sockets[1].socket_data = edge.start_socket.socket_data

class DataCompare (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            align_axis="columns",
            keep_shape=False,
            keep_equal=False
            )
    
    def config(self):
        dialog = Dialog(title="configuration", parent=self.parent)
        align_axis = ComboBox(items=["index","columns"],text="Axis")
        dialog.main_layout.addWidget(align_axis)
        align_axis.button.setCurrentText(self._config["align_axis"])
        keep_shape = Toggle(text="Keep shape")
        dialog.main_layout.addWidget(keep_shape)
        keep_shape.button.setChecked(self._config["keep_shape"])
        keep_equal = Toggle(text="Keep equal")
        dialog.main_layout.addWidget(keep_equal)
        keep_equal.button.setChecked(self._config["keep_equal"])

        if dialog.exec():
            self._config["align_axis"] = align_axis.button.currentText()
            self._config["keep_shape"] = keep_shape.button.isChecked()
            self._config["keep_equal"] = keep_equal.button.isChecked()
            self.exec()
    
    def func(self):
        try:
            if self.node.input_sockets[0].socket_data and self.node.input_sockets[1].socket_data:
                data_left = self.node.input_sockets[0].socket_data
                data_right = self.node.input_sockets[1].socket_data
                self.node.output_sockets[0].socket_data = data_left.compare(data_right,**self._config)
            elif self.node.input_sockets[0].socket_data:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            elif self.node.input_sockets[1].socket_data:
                self.node.output_sockets[0].socket_data = self.node.input_sockets[1].socket_data
            else:
                self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            node1 = self.node.input_sockets[0].edges[0].start_socket.node
            node2 = self.node.input_sockets[1].edges[0].start_socket.node
            logger.info(f"{self.name} {self.node.id}: compared data from {node1} {node1.id} and {node2} {node2.id} successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = pd.DataFrame()
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return an empty DataFrame.")
            logger.exception(e)
        
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
            self._config = dict(
                type="columns",
                column_from=None,
                column_to=None,
                row_from=None,
                row_to=None
                )
        else:
            self._config = dict(
                type="columns",
                column_from=self.node.input_sockets[0].socket_data.columns[0],
                column_to=self.node.input_sockets[0].socket_data.columns[-1],
                row_from=1,
                row_to=self.node.input_sockets[0].socket_data.shape[0]
                )

    def config(self):
        dialog = Dialog("Configuration", self.parent)

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
            # write log
            logger.info(f"{self.name} {self.node.id}: located data successfully.")

        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
            
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

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._config = dict(
            axis="columns",
            type="items",
            apply=str()
            )
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        def func1():
            try:
                if axis.button.currentText().lower() == "columns":
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.columns])) 
                else:
                    labels.button.setCompleter(Completer([str(i) for i in self.node.input_sockets[0].socket_data.index])) 
            except: pass

        axis = ComboBox(items=["columns","index"], text="Filter by")
        axis.button.setCurrentText(self._config["axis"])
        axis.button.currentTextChanged.connect(func1)
        dialog.main_layout.addWidget(axis)

        type = ComboBox(items=["items","contains","regular expression"], text="filter type")
        type.button.setCurrentText(self._config["type"])
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
            self._config["axis"] = axis.button.currentText()
            self._config["type"] = type.button.currentText()
            self._config["apply"] = apply.button.toPlainText().split(",")
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
            # write log
            logger.info(f"{self.name} {self.node.id}: filtered data successfully.")

        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
        
        self.data_to_view = self.node.output_sockets[0].socket_data
    
    def eval(self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
            

class DataSorter (NodeContentWidget):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)

        self.node.input_sockets[0].socket_data = pd.DataFrame()
        self._config = dict(
            by=[""],
            ascending=[True]
            )
        
    
    def config(self):
        dialog = Dialog("Configuration", self.parent)

        self.widget_index = 0
        
        class ShorterWidget(QWidget):
            def __init__(self, data:pd.DataFrame, by:str, order:bool, parent=None):
                super().__init__(parent)
                self.hlayout = QHBoxLayout(self)
                self.hlayout.setContentsMargins(0,0,0,0)

                self.col = _ComboBox(parent=dialog)
                self.col.setObjectName("by")
                if not data.empty: self.col.addItems(data.columns)
                self.col.setCurrentText(by)
                self.hlayout.addWidget(self.col)

                self.ascending = _ComboBox(["ascending","descending"],dialog)
                self.ascending.setObjectName("ascending")
                if order: self.ascending.setCurrentText("ascending")
                else: self.ascending.setCurrentText("descending")
                self.hlayout.addWidget(self.ascending)

                delete = _TransparentToolButton(dialog)
                delete.setIcon("delete.png")
                delete.pressed.connect(self.onDelete)
                self.hlayout.addWidget(delete)
            
            def onDelete(self):
                dialog.main_layout.removeWidget(self)
                self.deleteLater()
                QApplication.processEvents()
                dialog.adjustSize()
        
        def add(by="", order=True):
            widget = ShorterWidget(self.node.input_sockets[0].socket_data, by, order)
            dialog.main_layout.insertWidget(self.widget_index, widget)
            self.widget_index += 1

        for by, order in zip(self._config.get("by"), self._config.get("ascending")):
            add(by, order)

        add_btn = _TransparentPushButton(self)
        add_btn.setIcon("add.png")
        add_btn.pressed.connect(add)
        dialog.main_layout.addWidget(add_btn)

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
        try:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data.sort_values(**self._config)
            # write log
            logger.info(f"{self.name} {self.node.id}: sorted data successfully.")
        except Exception as e:
            self.node.output_sockets[0].socket_data = self.node.input_sockets[0].socket_data
            # write log
            logger.error(f"{self.name} {self.node.id}: failed, return the original DataFrame.") 
            logger.exception(e)
        
        self.data_to_view = self.node.output_sockets[0].socket_data

    def eval(self):
        if self.node.input_sockets[0].hasEdge():
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        else: self.node.input_sockets[0].socket_data = pd.DataFrame()