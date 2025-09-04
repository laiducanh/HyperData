from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import Signal, QThreadPool
from PySide6.QtGui import QBrush
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.graphics.graphics_content import GraphicsContent
from config.threadpool import Worker
from config.settings import logger
import pandas as pd

class NodeContentWidget(GraphicsContent):
    sig = Signal()
    def __init__(self, node: NodeGraphicsNode, parent=None): # parent is an instance of "NodeGraphicsView"
        super().__init__(parent)
  
        self.node = node
        self.parent = parent
        self.name = self.node.title
        self.threadpool = QThreadPool().globalInstance()
        self.num_signal_pipeline = 0
        self._config = dict()
        self.resetNode()

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        """ use for threadpool run """
        self.worker = Worker(self.func, *args, **kwargs)
        self.worker.signals.finished.connect(self.exec_done)
        self.threadpool.start(self.worker)
    
    def exec (self, *args, **kwargs):
        """ use to process data_out
         this function will be called when pressing execute button """
        self.num_signal_pipeline = 0 # reset number of pipeline signal
        for edge in self.node.socket_pipeline_out.edges: # reset data for the connected nodes
            edge.end_socket.node.content.resetNode()
        self.exec_btn.setIcon("stop.png")
        self.progress.set_type('indeterminate')
        self.progress.setValue(0)
        self.run_threadpool(*args, **kwargs)

    def func(self, *args, **kwargs):
        """ main function of the node """
        # make sure to properly process data_in before executing the main function
        self.eval()

    def eval (self):
        """ use to process data_in """
        self.resetNode()
    
    def exec_done(self):
        """ this function will be called when threadpool finishes running"""
        self.progress.set_type('normal')
        self.label.setText(f"Shape: {self.data_to_view.shape}")    
        
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e:
                    logger.warning(f"{self.name} {self.node.id}: could not evaluate the connected node {edge.end_socket.node.id}.")
                    logger.exception(e)
        
        self.pipeline()
        
        self.progress.setValue(100)
        self.exec_btn.setIcon("play.png")

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.pipeline_signal()
    
    def pipeline_signal (self):
        self.num_signal_pipeline += 1
        if self.num_signal_pipeline >= len(self.node.socket_pipeline_in.edges):
            self.exec()
    
    def resetNode(self):
        self.data_to_view = pd.DataFrame()
        for socket in self.node.output_sockets:
            socket.socket_data = None
        self.progress.setValue(0)
        self.progress.changeColor("success")
        self.label.setText('Shape: (--, --)') 
    
    def showColorDialog(self):
        dialog = QColorDialog(self.node._brush_background.color(), self.parent)
        dialog.colorSelected.connect(self.onColorChanged)
        dialog.exec()
    
    def onColorChanged(self, color):
        self.node._brush_background = QBrush(color)

    def _update(self):
        self.node._update()
        return super().update()

    def serialize(self):
        return {"config": self._config,
                "comment": self.comment.toPlainText()}
    
    def deserialize(self, data, hashmap=...):
        self._config = data['config']
        self.comment.setText(data['comment'])



    