from node_editor.base.node_graphics_content import NodeContentWidget
from plot.canvas import Canvas, Canvas3D, MultiFigureCanvas
import pandas as pd
from ui.base_widgets.menu import Action
from config.settings import logger
from plot.plot_view import PlotView
import pickle

class Figure2D (NodeContentWidget):
    def __init__(self, node, parent=None):
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
        return {"canvas":self.canvas.serialize(),
                "comment": self.comment.toPlainText()}
            
    def deserialize(self, data, hashmap={}):
        self.canvas.deserialize(data['canvas'], hashmap)
        self.comment.setText(data['comment'])


class Figure3D (Figure2D):
    def __init__(self, node, parent=None):
        super().__init__(node,parent)
    
    def initCanvas(self):
        self.canvas = Canvas3D()

class MultiFigure(Figure2D):
    def __init__(self, node, parent=None):
        super().__init__(node,parent)

        self.label.hide()
        self.node.input_sockets[0].socket_data = list()
    
    def initCanvas(self):
        self.canvas = MultiFigureCanvas()
    
    def eval (self):
        self.resetStatus()
        self.node.input_sockets[0].socket_data = list()
        for edge in self.node.input_sockets[0].edges:
            try: 
                self.node.input_sockets[0].socket_data.append(edge.start_socket.node.content.canvas)
            except Exception as e:
                logger.exception(e)
                print(e)
                    