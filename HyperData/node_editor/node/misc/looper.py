from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.base.node_graphics_node import NodeGraphicsNode
from ui.base_widgets.window import Dialog
from ui.base_widgets.spinbox import SpinBox

class Looper (NodeContentWidget):
    def __init__(self, node: NodeGraphicsNode, parent=None):
        super().__init__(node, parent)

        self._config = dict(
            n=10,
            current_iter=0,
        )
        self.label.setText(f"Iteration: {self._config["current_iter"]}")
    
    def config(self):
        dialog = Dialog(title="configuration", parent=self.parent)
        n = SpinBox(min=1, max=10000, step=10, text="Number of iterations")
        n.button.setValue(self._config["n"])
        dialog.main_layout.addWidget(n)

        if dialog.exec():
            self._config.update(
                n=n.button.value()
            )
    
    def exec(self):
        self._config.update(
            n=10,
            current_iter=0,
        )
        self.pipeline()    
        self.progress.setValue(int(1/self._config["n"]*100))
        self.label.setText(f"Iteration: 1")                 
    
    def pipeline_signal(self):
        self._config["current_iter"] += 1
        self.timerStart()
    
    def timerStop(self, step = 10):
        if self._config["current_iter"] < self._config["n"]:
            self.pipeline()
            self.label.setText(f"Iteration: {self._config["current_iter"]+1}")
            self.progress.setValue(int((self._config["current_iter"]+1)/self._config["n"]*100))     
                
    def resetStatus(self):
        self.progress.setValue(0)
        self.progress.changeColor("success")
