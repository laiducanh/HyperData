from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
import platform
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.button import ComboBox, Toggle
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import BodyLabel
from data_processing.data_window import TableModel
from config.settings import logger, encode, GLOBAL_DEBUG
from PySide6.QtWidgets import QFileDialog, QTableView
from PySide6.QtCore import QFileSystemWatcher

DEBUG = False

class DataReader (NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node,parent)

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
                data = pd.read_csv(
                    self.selectedFiles, 
                    nrows=10,
                    header=header,
                    delimiter=delimiter,
                    skip_blank_lines=skip_blank_lines,
                    encoding=encoding
                )
            elif self.filetype == "excel":
                data = pd.read_excel(
                    self.selectedFiles, 
                    nrows=10,
                    header=header,
                    sheet_name=sheet_name
                )
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
            # check filetype for reading
            self.check_filetype(self.selectedFiles)
            # write log
            logger.info(f"DataReader {self.node.id}: Selected {self.selectedFiles}.")
            # reset status of the node before executing the main function
            self.resetStatus()
            # execute main function
            super().exec(self.selectedFiles)
    
    def func (self, selectedFiles):
        if self.isReadable:
            match self.filetype:
                case "csv":
                    data = pd.read_csv(
                        selectedFiles, 
                        nrows=self._config["nrows"],
                        header=self._config["header"],
                        delimiter=self._config["delimiter"],
                        skip_blank_lines=self._config["skip_blank_lines"],
                        encoding=self._config["encoding"]
                    )
                    # write log
                    logger.info(f"DataReader {self.node.id}: Loaded a csv file.")

                case "excel":
                    data = pd.read_excel(
                        selectedFiles, 
                        nrows=self._config["nrows"],
                        header=self._config["header"]
                    )
                    # write log
                    logger.info(f"DataReader {self.node.id}: Loaded an excel file.")
            
            # change progressbar's color
            self.progress.changeColor('success')
        else:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.warning(f"DataReader {self.node.id}: Couldn't read data file, return an empty DataFrame.")
            logger.info(f"DataReader {self.node.id}: failed, file format is not supported.")
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
