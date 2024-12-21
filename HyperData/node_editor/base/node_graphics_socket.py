from PySide6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent
from node_editor.graphics.graphics_item import GraphicsSocket, GraphicsEdge, GraphicsNode
import pandas as pd

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8
DEBUG = False

class NodeGraphicsSocket (GraphicsSocket):
    def __init__(self, node:GraphicsNode, index=0, socket_type=SINGLE_IN, data:pd.DataFrame=None, parent=None):
        super().__init__(node, socket_type, parent)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.node = node # node that socket is attached to so that we can get socket position from 'NodeGraphicsNode' class
        self.index = index
        self.edges: list[GraphicsEdge] = list() # assigns a list of edges connected to (self) socket, init with an empty list, has type of list[GraphicsEdge]
        self.socket_data = data

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.show()
        if self.node.content: self.node.content.hide()
        self.hovered = True
        self.update()
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self._text.hide()
        if self.node.content: self.node.content.show()
        self.hovered = False
        self.update()

    def getSocketPosition(self):
        """ This method use getSocketPosition method in NodeGraphicsNode to calculate the position of socket for drawing edges """
        """ return a list contains x, y """
        pos = self.node.getSocketPosition(self.index, self.socket_type)
        return pos
    
    def addEdge(self, edge:GraphicsEdge):   
        self.edges.append(edge)
        if DEBUG: print('Add edge', edge, 'from node', edge.start_socket.node, 'to node', edge.end_socket.node)
        if DEBUG: print(self.edges)
        if self.socket_type in [SINGLE_IN, MULTI_IN]: edge.end_socket.node.content.eval()
          
    def removeEdge(self, edge:GraphicsEdge):
        if edge in self.edges: 
            if self.socket_type in [SINGLE_IN, MULTI_IN]: edge.end_socket.node.content.eval()
            self.edges.remove(edge)
            

        else: print("Socket::removeEdge", "wanna remove edge", edge, "from self.edges but it's not in the list!")

    def removeAllEdges(self):
        for edge in self.edges:
            self.edges.remove(edge)
            if self.socket_type in [SINGLE_IN, MULTI_IN]: edge.end_socket.node.content.eval()
        if DEBUG: print("Socket::removeAllEdges", "the edge list is", self.edges)

    def hasEdge(self) -> bool:
        """ return True if there is at least one edge attached to the socket """
        return self.edges is not []    
    
    def serialize(self):
        return {"id":self.id,
                "index":self.index,
                "socket_type":self.socket_type}

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        hashmap[data['id']] = self
        return True