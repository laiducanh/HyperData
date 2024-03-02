from node_editor.base.node_graphics_content import NodeContentWidget
from plot.canvas import Canvas
import pandas as pd

class Figure (NodeContentWidget):
    def __init__(self, node=None):
        super().__init__(node)
        self.exec_btn.setText('Open Figure')
        self.exec_btn.pressed.connect(self.exec)
        self.canvas = Canvas()
    
    def eval (self):
        if self.node.input_sockets[0].edges == []:
            self.node.data_in = pd.DataFrame()
        else:
            self.node.data_in = self.node.input_sockets[0].edges[0].start_socket.node.data_out
        self.label.setText(f'Shape: {str(self.node.data_in.shape)}')
    
    def exec(self):
        self.sig.emit()
    
    def serialize(self):
        return {"figure":self.canvas.serialize(),
                "data":self.node.data_in.to_json(),}
            
    def deserialize(self, data, hashmap={}):
        pass