from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.node.data import *
from node_editor.node.figure import *

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4

class Node(NodeGraphicsNode):
    def __init__(self, title="Undefined Node"):
        if title == 'Undefined Node':
            super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[SINGLE_OUT, MULTI_OUT])
            self.content = NodeContentWidget(self)
        elif title == 'Figure':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[])
            self.content = Figure(self)
        elif title == 'Logistic Regression':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = NodeContentWidget(self)
        elif title == 'Data Holder':
            super().__init__(title=title, inputs=[], outputs=[MULTI_OUT])
            self.content = DataHolder(self)
        elif title == 'Data Concator':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = DataConcator(self)

        self.set_Content(self.content)

        
    

    