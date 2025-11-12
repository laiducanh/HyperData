from rdkit.Chem import PandasTools
import os
import pandas as pd
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from data_processing.data_window import MolDataView
from ui.base_widgets.window import FileDialog
from config.settings import logger, GLOBAL_DEBUG
from PySide6.QtWidgets import QFileDialog

DEBUG = False

class SDFReader(NodeContentWidget):
    def __init__(self, node:NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self.view = MolDataView(self.data_to_view, parent)
        self.selectedFiles = None

    def exec (self):    
        dialog = FileDialog(
            filter="""Structure Data File (*.sdf)""",
            acceptMode=QFileDialog.AcceptMode.AcceptOpen,
        )
        if self.selectedFiles: 
            dialog.setDirectory(os.path.dirname(self.selectedFiles))
            dialog.selectFile(self.selectedFiles)
        if dialog.exec():
            self.selectedFiles = dialog.selectedFiles()[0]
            # write log
            logger.info(f"{self.name} {self.node.id}: select {self.selectedFiles}.")
            # reset status of the node before executing the main function
            self.resetNode()
            # execute main function
            super().exec()
    
    def func(self):
        try:
            data = PandasTools.LoadSDF(self.selectedFiles, molColName='_molread')
            # write log
            logger.info(f"{self.name} {self.node.id}: load sdf file successfully.")
            # change progressbar's color
            self.progress.changeColor('success')
        except Exception as e:
            data = pd.DataFrame()
            # change progressbar's color
            self.progress.changeColor('fail')
            # write log
            logger.error(f"{self.name} {self.node.id}: fail, return an empty DataFrame.") 
            logger.exception(e)
        
        self.node.output_sockets[0].socket_data = data.copy()
        self.data_to_view = data.copy()
    
    def serialize(self):
        return {"comment": self.comment.toPlainText(),
                "selected_files":self.selectedFiles
                }

    def deserialize(self, data, hashmap={}):
        super().deserialize(data)
        self.selectedFiles = data['selected_files']
        self.comment.setText(data['comment'])