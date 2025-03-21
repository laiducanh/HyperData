from PySide6.QtWidgets import QColorDialog
from PySide6.QtCore import Signal, QThreadPool, Qt
from PySide6.QtGui import QBrush
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.graphics.graphics_content import ContentItem
from config.threadpool import Worker
from config.settings import logger

class NodeContentWidget(ContentItem):
    sig = Signal()
    def __init__(self, node: NodeGraphicsNode,parent=None): # parent is an instance of "NodeGraphicsView"
        super().__init__()
        
        self.node = node
        self.parent = parent
        self.threadpool = QThreadPool().globalInstance()
        self.num_signal_pipeline = 0

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        """ use for threadpool run """
        self.progress.setValue(0)
        self.worker = Worker(self.func, *args, **kwargs)
        self.worker.signals.finished.connect(self.exec_done)
        self.threadpool.start(self.worker)
    
    def exec (self, *args, **kwargs):
        """ use to process data_out
         this function will be called when pressing execute button """
        self.num_signal_pipeline = 0 # reset number of pipeline signal
        for edge in self.node.socket_pipeline_out.edges: # reset data for the connected nodes
            edge.end_socket.node.content.resetStatus()
        self.timerStart()
        self.run_threadpool(*args, **kwargs)

    def func(self, *args, **kwargs):
        """ main function of the node """
        # make sure to properly process data_in
        # before executing the main function
        self.eval()

    def eval (self):
        """ use to process data_in """
        self.resetStatus()
    
    def exec_done(self):
        """ this function will be called when threadpool finishes running"""
        self.timer.stop()
        self.label.setText(f"Shape: {self.data_to_view.shape}")    
        
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e:
                    # write log
                    logger.warning(f"{self.name} {self.node.id}: could not evaluate the connected node {edge.end_socket.node.id}.")
                    logger.exception(e)
        
        self.pipeline()
        self.progress.setValue(100)

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.pipeline_signal()
    
    def pipeline_signal (self):
        self.num_signal_pipeline += 1
        if self.num_signal_pipeline >= len(self.node.socket_pipeline_in.edges):
            self.exec()
    
    def showColorDialog(self):
        dialog = QColorDialog(self.node._brush_background.color(), self.parent)
        dialog.colorSelected.connect(self.onColorChanged)
        dialog.exec()
    
    def onColorChanged(self, color):
        self.node._brush_background = QBrush(color)






    