from node_editor.base.node_graphics_content import NodeContentWidget
from plot.canvas import Canvas, Canvas3D
import pandas as pd
from ui.base_widgets.menu import Action
class Figure2D (NodeContentWidget):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)

        self.initCanvas()

    def initCanvas(self):
        self.canvas = Canvas()
       
    def eval (self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = pd.DataFrame()
        for edge in self.node.input_sockets[0].edges:
            self.node.input_sockets[0].socket_data = edge.start_socket.socket_data
                    
        self.label.setText(f'Shape: {str(self.node.input_sockets[0].socket_data.shape)}')
        self.data_to_view = self.node.input_sockets[0].socket_data
    
    def exec(self):
        self.sig.emit()
        self.eval()
    
    def serialize(self):
        return {"figure":self.canvas.serialize(),
                "data":self.node.data_in.to_json(),}
            
    def deserialize(self, data, hashmap={}):
        pass

class Figure3D (Figure2D):
    def __init__(self, node,parent=None):
        super().__init__(node,parent)
    
    def initCanvas(self):
        self.canvas = Canvas3D()
    
    def serialize(self):
        return {"figure":self.canvas.serialize(),
                "data":self.node.data_in.to_json(),}
            
    def deserialize(self, data, hashmap={}):
        pass