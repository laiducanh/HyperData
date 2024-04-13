from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsSceneHoverEvent
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainterPath, QColor, QPen, QPainter
from node_editor.base.node_graphics_node import NodeGraphicsSocket
from node_editor.graphics.graphics_edge import GraphicsEdge
import math

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_CP_ROUNDNESS = 100
SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8
DEBUG = False

class NodeGraphicsEdge(GraphicsEdge):
    def __init__(self, start_socket:NodeGraphicsSocket=None, 
                 end_socket:NodeGraphicsSocket=None, parent=None):
        super().__init__(start_socket, end_socket, parent)

        self.start_socket = start_socket
        self.end_socket = end_socket

        if self.start_socket != None: self.start_socket.addEdge(self)
        if self.end_socket != None: self.end_socket.addEdge(self)
    

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]
    
    def updatePath(self):
        """ Will handle drawing QPainterPath from Point A to B """
        raise NotImplemented("This method has to be overriden in a child class")

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()        
        source_pos[0] = self.start_socket.scenePos().x()
        source_pos[1] = self.start_socket.scenePos().y()
        self.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] = self.end_socket.scenePos().x()
            end_pos[1] = self.end_socket.scenePos().y()
            self.setDestination(*end_pos)
        else:
            self.setDestination(*source_pos)
        #if DEBUG: print('Source pos', source_pos, 'End pos', end_pos)
        if DEBUG: print(" SS:", self.start_socket)
        if DEBUG: print(" ES:", self.end_socket)
        self.update()
    
    def remove(self):
        if self.start_socket != None: self.start_socket.removeEdge(self)
        if self.end_socket != None: self.end_socket.removeEdge(self)

    def serialize(self):
        return {"id":self.id,
                "start":self.start_socket.id,
                "end":self.end_socket.id}

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]



class NodeGraphicsEdgeDirect(NodeGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class NodeGraphicsEdgeBezier(NodeGraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0]) * 0.5
        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        sspos = self.start_socket.socket_type

        if (s[0] > d[0] and sspos in (SINGLE_OUT, MULTI_OUT, PIPELINE_OUT, CONNECTOR_OUT)) or (s[0] < d[0] and sspos in (SINGLE_IN, MULTI_IN, PIPELINE_IN, CONNECTOR_IN)):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                    (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS
            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                    (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS


        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])
        self.setPath(path)
