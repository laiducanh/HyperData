from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QThreadPool
from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.graphics.graphics_content import ContentItem
from config.threadpool import Worker
from config.settings import logger

class NodeContentWidget(ContentItem):
    sig = pyqtSignal()
    def __init__(self, node: NodeGraphicsNode,parent=None): # parent is an instance of "NodeGraphicsView"
        super().__init__()
        
        self.node = node
        self.parent = parent
        self.threadpool = parent.threadpool
        self.threadpool: QThreadPool
        self.num_signal_pipeline = 0

    def config(self):
        pass

    def run_threadpool(self, *args, **kwargs):
        """ use for threadpool run """
        self.progress.setValue(0)
        self.progress._setValue(0)
        worker = Worker(self.func, *args, **kwargs)
        worker.signals.finished.connect(self.exec_done)
        self.threadpool.start(worker)
        self.timerStart()
        self.progress.setValue(30)
    
    def exec (self, *args, **kwargs):
        """ use to process data_out
         this function will be called when pressing execute button """
        self.num_signal_pipeline = 0 # reset number of pipeline signal
        self.run_threadpool(*args, **kwargs)

    def func(self, *args, **kwargs):
        """ main function of the node """
        pass
    
    def exec_done(self):
        
        self.timer.stop()
        self.label.setText(f"Shape: {self.data_to_view.shape}")    
        
        for socket in self.node.output_sockets:
            for edge in socket.edges:
                try: edge.end_socket.node.content.eval()
                except Exception as e: print(e)

        self.pipeline()
        self.progress.setValue(100)

    def pipeline (self):

        for edge in self.node.socket_pipeline_out.edges:
            edge.end_socket.node.content.pipeline_signal()
    
    def pipeline_signal (self):
        self.num_signal_pipeline += 1
        if self.num_signal_pipeline >= len(self.node.socket_pipeline_in.edges):
            self.exec()






    