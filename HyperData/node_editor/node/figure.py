from node_editor.base.node_graphics_content import NodeContentWidget
from plot.canvas import Canvas
import pandas as pd
from PyQt6.QtGui import QAction

class Figure (NodeContentWidget):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Open Figure')
        self.canvas = Canvas()
    
    def initMenu(self):
        action = QAction("Open Figurre")
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = QAction("View Data")
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = QAction("Show Comment")
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = QAction("Hide Comment")
        action.triggered.connect(self.comment.hide)
        self.menu.addAction(action)
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.input_sockets[0].socket_data = pd.DataFrame()
        else:
            self.node.input_sockets[0].socket_data = self.node.input_sockets[0].edges[0].start_socket.socket_data
        self.label.setText(f'Shape: {str(self.node.input_sockets[0].socket_data.shape)}')
        self.data_to_view = self.node.input_sockets[0].socket_data
    
    def exec(self):
        self.sig.emit()
    
    def serialize(self):
        return {"figure":self.canvas.serialize(),
                "data":self.node.data_in.to_json(),}
            
    def deserialize(self, data, hashmap={}):
        pass