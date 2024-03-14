from node_editor.base.node_graphics_node import NodeGraphicsNode
from node_editor.base.node_graphics_content import NodeContentWidget
from node_editor.node.data import *
from node_editor.node.data_cleaning import *
from node_editor.node.data_encoder import *
from node_editor.node.machine_learning import *
from node_editor.node.figure import *
from node_editor.node.misc import *
from PyQt6.QtGui import QMouseEvent

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4

class Node(NodeGraphicsNode):
    def __init__(self, title="Undefined Node",parent=None):
        if title == 'Undefined Node':
            super().__init__(title=title, inputs=[SINGLE_IN, MULTI_IN], outputs=[SINGLE_OUT, MULTI_OUT, SINGLE_OUT, SINGLE_OUT])
            self.content = NodeContentWidget(self,parent)
        elif title == 'Figure':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[])
            self.content = Figure(self,parent)
        elif title == 'Data Holder':
            super().__init__(title=title, inputs=[], outputs=[MULTI_OUT])
            self.content = DataHolder(self,parent)
        elif title == "Data Transpose":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataTranspose(self, parent)
        elif title == 'Data Concator':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = DataConcator(self,parent)
        elif title == 'Data Combiner':
            super().__init__(title=title, inputs=[MULTI_IN], outputs=[MULTI_OUT])
            self.content = DataCombiner(self,parent)
        elif title == 'Data Merge':
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataMerge(self,parent)
        elif title == 'Data Compare':
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataCompare(self,parent)
        elif title == "Data Locator":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataLocator(self,parent)
        elif title == "Data Filter":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DataFilter(self,parent)
        elif title == 'Nan Eliminator':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = NAEliminator(self,parent)
        elif title == 'Nan Imputer':
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = NAImputer(self,parent)
        elif title == "Drop Duplicate":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = DropDuplicate(self,parent)
        elif title == "Label Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = LabelEncoder(self,parent)
        elif title == "Ordinal Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = OrdinalEncoder(self,parent)
        elif title == "One-Hot Encoder":
            super().__init__(title=title, inputs=[SINGLE_IN], outputs=[MULTI_OUT])
            self.content = OneHotEncoder(self,parent)
        elif title == "Data Splitter":
            super().__init__(title=title, inputs=[], outputs=[MULTI_OUT])
            self.content = DataSplitter(self,parent)
        elif title == "ML_Modeler":
            super().__init__(title=title, inputs=[SINGLE_IN, SINGLE_IN, SINGLE_IN], outputs=[MULTI_OUT, MULTI_OUT])
            self.content = MLModeler(self,parent)
        elif title == 'Executor':
            super().__init__(title=title, inputs=[], outputs=[])
            self.content = Executor(self,parent)
        
        self.menu = self.content.menu
        self.set_Content(self.content)

    

    