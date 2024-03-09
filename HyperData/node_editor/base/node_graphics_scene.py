from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent
from PyQt6.QtGui import QColor, QKeyEvent, QPen
from PyQt6.QtCore import pyqtSignal, Qt
from node_editor.base.node_graphics_node import NodeGraphicsSocket, NodeGraphicsNode
from node_editor.base.node_graphics_edge import NodeGraphicsEdgeBezier, NodeGraphicsEdgeDirect, NodeGraphicsEdge
from node_editor.node_node import Node
from config.settings import logger

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6

class NodeGraphicsScene(QGraphicsScene):
    sig = pyqtSignal(object)
    sig_keyPressEvent = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)

        # settings
        self.gridSize = 20
        self.gridSquares = 5
        self.parent = parent

        self._color_background = QColor("white")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.id = id(self)

        self.initUI()
    
    def initUI(self):
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2,
                                  self.scene_width, self.scene_height)

    
    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent | None) -> None:
        pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.sig_keyPressEvent.emit(event)
        return super().keyPressEvent(event)

    def addNode(self, node:Node):
        self.addItem(node)
        self.nodes.append(node)
        node.content.sig.connect(lambda: self.sig.emit(node))
        logger.info(f"Scene::addNode: add node {node.id}.")

    def addEdge(self, edge:NodeGraphicsEdge):
        self.addItem(edge)
        self.edges.append(edge)
        logger.info(f"Scene::addEdge: add edge {edge.id}.")

    def removeNode(self, node:Node):
        if node in self.nodes: 
            self.nodes.remove(node)
            self.removeItem(node)
            logger.info(f"Scene::removeNode: remove node {node.id}.")
        else: logger.warn(f"Scene::removeNode: wanna remove node {node.id} from self.nodes but it's not in the list!")

    def removeEdge(self, edge:NodeGraphicsEdge):
        if edge in self.edges: 
            self.edges.remove(edge)
            self.removeItem(edge)
            edge.remove()
            logger.info(f"Scene::removeEdgge: remove edge {edge.id}.")
        else: logger.warn(f"Scene::removeEdge: wanna remove edge {edge.id} from self.edges but it's not in the list!") 
    
    def clear(self):
        for i in self.items():
            if isinstance(i,(NodeGraphicsNode,NodeGraphicsEdge)):
                self.removeItem(i)
                logger.info(f"Scene::clear: remove item {i.id}.")
        self.nodes = []
        self.edges = []
        logger.info(f"Scene::clear: reset self.nodes and self.edges.")

    def serialize(self):
        nodes, edges = dict(), dict()
        for node in self.nodes: nodes[node.id] = node.serialize()
        for edge in self.edges: edges[edge.id] = edge.serialize()
        return {"id":self.id,
                "scene_width":self.scene_width,
                "scene_height":self.scene_height,
                "nodes":nodes,
                "edges":edges}
    
    def deserialize(self, data, hashmap={}):
        self.clear()
        hashmap = {}
        self.id = data['id']
        
        # create nodes
        nodes = data['nodes']
        for node_id in nodes.keys():
            node = Node(nodes[node_id]['title'],self.parent)
            self.addNode(node)
            node.deserialize(nodes[node_id], hashmap)

        # create edges
        edges = data['edges']
        for edge_id in edges.keys():
            start_socket = hashmap[edges[edge_id]['start']]
            end_socket = hashmap[edges[edge_id]['end']]
            edge = NodeGraphicsEdgeBezier(start_socket, end_socket)
            if edge.start_socket.socket_type in [PIPELINE_IN, PIPELINE_OUT]: edge.setColor(Qt.GlobalColor.green)
            edge.updatePositions()
            self.addEdge(edge)
            edge.deserialize(edges[edge_id], hashmap)
            


        return True

