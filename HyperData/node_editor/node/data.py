from node_editor.base.node_graphics_content import NodeContentWidget
import pandas as pd
from PyQt6.QtWidgets import QFileDialog
DEBUG = True

class DataHolder (NodeContentWidget):
    def __init__(self, node=None):
        super().__init__(node)
        self.exec_btn.setText('Load data')
        self.exec_btn.clicked.connect(self.exec)
        
    def exec (self):
        import_dlg = QFileDialog()
        import_dlg.setWindowTitle("Import data")

        if import_dlg.exec():
            selectedFiles = import_dlg.selectedFiles()[0]
            self.node.data_out = pd.read_csv(selectedFiles)
            self.label.setText(f'Shape: {str(self.node.data_out.shape)}')
            for socket in self.node.output_sockets:
                for edge in socket.edges:
                    edge.end_socket.node.content.eval()
                    pass

class DataConcator (NodeContentWidget):
    def __init__(self, node=None):
        super().__init__(node)
        self.exec_btn.pressed.connect(self.exec)
        self.node.data_out = pd.DataFrame()
    
    def exec(self):
        if self.node.data_in != []: self.node.data_out = pd.concat(self.node.data_in,axis=1)
        self.label.setText(f'Shape: {str(self.node.data_out.shape)}')
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                edge.end_socket.node.content.eval()
                pass
    def eval(self):
        self.node.data_in = list()
        for i in self.node.input_sockets[0].edges:
            self.node.data_in.append(i.start_socket.node.data_out)