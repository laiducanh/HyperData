from PySide6.QtGui import QKeyEvent, QPaintEvent, QShowEvent
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDockWidget, QMainWindow
from PySide6.QtCore import Signal, Qt
from node_editor.base.node_graphics_view import NodeGraphicsView
from node_editor.base.node_graphics_scene import NodeGraphicsScene
from node_editor.node_node import Node
from node_editor.base.node_graphics_node import NodeEditor
from node_editor.base.node_graphics_edge import NodeGraphicsEdge
from node_editor.graphics.graphics_item import GraphicsSocket
from ui.base_widgets.list import Draggable_TreeWidget
from ui.base_widgets.line_edit import _SearchBox
from ui.base_widgets.button import _TransparentToolButton
from config.settings import config

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8

class NodeView (QMainWindow):
    sig = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.nodelist = {
            "Data Processing": ["Data Reader", "Data Concator", "Data Transpose", "Data Inserter",
                                "Data Combiner", "Data Merge", "Data Compare","Data Correlator",
                                "Data Locator","Data Splitter","Data Filter", "Data Holder","Data Sorter",
                                "Data Pivot","Data Unpivot","Data Stack","Data Unstack","Data Computation",
                                "Data Overwriter","Curve Fitter",
                                "Data Scaler","Data Normalizer","Pairwise Measurer",
                                "Nan Eliminator", "Nan Imputer", "Drop Duplicate",
                                ],
            "Machine Learning": ["Classifier","Bagging-Classifier","Voting-Classifier",
                                "Regressor", "Clustering","Decomposition",
                                "CV Splitter","Train/Test Splitter",
                                "Predictor","Feature Expander","Feature Selector",
                                "Label Encoder","Label Binarizer","Ordinal Encoder","One-Hot Encoder",
                                ],
            "Deep Learning": ["Input Layer","Dense Layer","Normalization Layer","DL Model"],
            "Visualization": ["Figure 2D", "Figure 3D","Multi-Figure"],
            "Misc": ["Executor", "Looper", "Undefined Node"]
        }

        self.setup_layout()
    
    def setup_layout (self):
        self.mainlayout = QHBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainlayout)
        self.setCentralWidget(self.central_widget)

        self.list_widget = QWidget()
        self.list_widget_layout = QVBoxLayout()
        self.list_widget.setLayout(self.list_widget_layout)
        self.mainlayout.addWidget(self.list_widget)

        self.static_layout = QHBoxLayout()
        self.list_widget_layout.addLayout(self.static_layout)

        self.search_box = _SearchBox(parent=self.parent)
        self.search_box.setPlaceholderText("Type / to search")
        self.static_layout.addWidget(self.search_box)

        self.nodesListWidget = Draggable_TreeWidget()
        self.nodesListWidget.setData(self.nodelist)
        self.nodesListWidget.sig_doubleClick.connect(self.addNode)
        self.list_widget_layout.addWidget(self.nodesListWidget)
        self.search_box.set_TreeView(self.nodesListWidget)

        self.nodesDock = QDockWidget("Cards")
        self.nodesDock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.nodesDock.setTitleBarWidget(QWidget())        
        self.nodesDock.setWidget(self.list_widget)       

        self.grScene = NodeGraphicsScene(self.parent)
        self.node_view = NodeGraphicsView(self.grScene, self.parent)
        self.grScene.sig.connect(lambda s: self.sig.emit(s))
        self.grScene.sig_keyPressEvent.connect(lambda s: self.keyPressEvent(s))
        self.mainlayout.addWidget(self.node_view)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        dock_area = config["dock area"]
        if dock_area == "Left":
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.nodesDock)
        elif dock_area == "Right":
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.nodesDock)
        elif dock_area == "Top":
            self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.nodesDock)
        elif dock_area == "Bottom":
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.nodesDock)
        return super().paintEvent(a0)
        
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
            
        return super().keyPressEvent(event)

    def addNode (self, title):
        try:
            node = Node(title,self.node_view)
            self.grScene.addNode(node)
        except:pass


class NodeUserDefine (NodeView):
    sig_back_to_grScene = Signal()
    def __init__(self, main_node:Node=None, parent=None):
        super().__init__(parent)

        self.graphicscreen_btn = _TransparentToolButton()
        self.graphicscreen_btn.setIcon("stack.png")
        self.graphicscreen_btn.pressed.connect(self.sig_back_to_grScene.emit)
        self.graphicscreen_btn.setToolTip("Node View")
        self.static_layout.insertWidget(0, self.graphicscreen_btn)

        self.main_node = main_node
        self.first_show = True

        main_node.content.sig_redraw.connect(self.drawConnectionCard)
    
    def drawConnectionCard (self):
        
        self.inputs = self.main_node.content.socket_in
        self.outputs = self.main_node.content.socket_out
        x, y = 20, 20

        for node in self.grScene.items():
            if isinstance(node, NodeEditor):
                self.grScene.removeNode(node)
        # also delete edges if connected node has been deleted        
        for item in self.grScene.items():
            if isinstance(item, NodeGraphicsEdge):
                if item.start_socket not in self.grScene.items() or item.end_socket not in self.grScene.items():
                    self.grScene.removeEdge(item)
                    item.remove()

        for ind, _ in enumerate(self.inputs):
            node = NodeEditor(f"Input {str(ind+1)}", CONNECTOR_OUT)
            _x, _y = x + ind*30, y
            node.setPos(self.node_view.mapToScene(_x, _y))
            self.grScene.addNode(node)
        if len(self.inputs) >= 1:
            y += 65
        for ind, _ in enumerate(self.outputs):
            node = NodeEditor(f"Output {str(ind+1)}", CONNECTOR_IN)
            _x, _y = x + ind*30, y
            node.setPos(self.node_view.mapToScene(_x, _y))
            self.grScene.addNode(node)
        if len(self.outputs) >= 1:
            y += 65
        
        node = NodeEditor("Pipeline In", PIPELINE_OUT)
        node.setPos(self.node_view.mapToScene(x, y))
        self.grScene.addNode(node)

        node = NodeEditor("Pipeline Out", PIPELINE_IN)
        x += 30
        node.setPos(self.node_view.mapToScene(x, y))
        self.grScene.addNode(node)
    

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)

        if self.first_show: self.drawConnectionCard()
        self.first_show = False
        

        