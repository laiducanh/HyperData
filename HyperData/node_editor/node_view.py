from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPaintEvent
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QDockWidget, 
                             QMainWindow)
from PyQt6.QtCore import pyqtSignal, Qt
from node_editor.base.node_graphics_view import NodeGraphicsView
from node_editor.base.node_graphics_scene import NodeGraphicsScene
from node_editor.node_node import Node
from ui.base_widgets.list import Draggable_TreeWidget
from ui.base_widgets.text import _Search_Box
from config.settings import config

class NodeView (QMainWindow):
    sig = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
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

        self.search_box = _Search_Box()
        self.list_widget_layout.addWidget(self.search_box)

        self.nodesListWidget = Draggable_TreeWidget()
        self.nodesListWidget.setData({"Data Processing": ["Data Reader", "Data Concator", "Data Transpose", 
                                                          "Data Combiner", "Data Merge", "Data Compare",
                                                          "Data Locator","Data Filter", "Data Holder",
                                                          "Nan Eliminator", "Nan Imputer", "Drop Duplicate",
                                                          ],
                                        "Machine Learning": ["Classifier","Train/Test Splitter",
                                                             "Label Encoder","Ordinal Encoder","One-Hot Encoder",],
                                        "Visualization": ["Figure"],
                                        "Misc": ["Executor", "Undefined Node"]})
        self.nodesListWidget.sig_doubleClick.connect(self.addNode)
        self.list_widget_layout.addWidget(self.nodesListWidget)
        self.search_box.set_TreeView(self.nodesListWidget)

        self.nodesDock = QDockWidget("Cards")
        self.nodesDock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.nodesDock.setTitleBarWidget(QWidget())        
        self.nodesDock.setWidget(self.list_widget)
        

        self.grScene = NodeGraphicsScene(self.parent)
        node_view = NodeGraphicsView(self.grScene, self.parent)
        self.grScene.sig.connect(lambda s: self.sig.emit(s))
        self.grScene.sig_keyPressEvent.connect(lambda s: self.keyPressEvent(s))
        self.mainlayout.addWidget(node_view)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        dock_area = config["dock area"]
        if dock_area == "left":
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.nodesDock)
        elif dock_area == "right":
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.nodesDock)
        elif dock_area == "top":
            self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.nodesDock)
        elif dock_area == "bottom":
            self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.nodesDock)
        return super().paintEvent(a0)
        
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Slash:
            self.search_box.setFocus()
            
        return super().keyPressEvent(event)

    def addNode (self, title):
        try:
            node = Node(title,self.grScene)
            self.grScene.addNode(node)
        except:pass
    