from node_editor.base.node_graphics_content import NodeContentWidget
from plot.canvas import Canvas, Canvas3D
import pandas as pd
from ui.base_widgets.menu import Action
class Figure2D (NodeContentWidget):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Open Figure')
        self.canvas = Canvas()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def initMenu(self):
        action = Action("Open Figurre",self.menu)
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = Action("View Data",self.menu)
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = Action("Show Comment",self.menu)
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = Action("Hide Comment",self.menu)
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

class Figure3D (NodeContentWidget):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)
        self.exec_btn.setText('Open Figure')
        self.canvas = Canvas3D()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
    
    def initMenu(self):
        action = Action("Open Figurre",self.menu)
        action.triggered.connect(self.exec)
        self.menu.addAction(action)
        action = Action("View Data",self.menu)
        action.triggered.connect(self.viewData)
        self.menu.addAction(action)
        self.menu.addSeparator()
        action = Action("Show Comment",self.menu)
        action.triggered.connect(self.comment.show)
        self.menu.addAction(action)
        action = Action("Hide Comment",self.menu)
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