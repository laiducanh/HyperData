from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath
from node_editor.graphics.graphics_socket import GraphicsSocket
from node_editor.graphics.graphics_edge import GraphicsEdge
from config.settings import logger, config
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
    def __init__(self, start_socket:GraphicsSocket = None, end_socket:GraphicsSocket = None, parent = None):
        super().__init__(start_socket, end_socket, parent)

        self.start_socket = start_socket
        self.end_socket = end_socket

        if self.start_socket: self.start_socket.addEdge(self)
        if self.end_socket: self.end_socket.addEdge(self)
    

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]
    
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
        self.update()
    
    def remove(self):
        logger.info(f"NodeGraphicsEdge::remove: edge {self.id} will be removed, related sockets will remove the edge.")
        if self.start_socket: self.start_socket.removeEdge(self)
        if self.end_socket: self.end_socket.removeEdge(self)

    def serialize(self):
        return {"id":self.id,
                "start":self.start_socket.id,
                "end":self.end_socket.id}

    def deserialize(self, data, hashmap={}):
        self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]

    def updatePath(self):

        x1, y1 = self.posSource
        x2, y2 = self.posDestination
        path = QPainterPath(QPointF(x1, y1))
        style = config['nodeview_edgestyle']
        radius = min(config['nodeview_edgeradius'], abs(y2 - y1) / 2)

        if style == 'Straight': 
            path.lineTo(self.posDestination[0], self.posDestination[1])
        
        elif style == 'Bezier':
            dist = (x2 - x1) * 0.5
            cpx_s = +dist
            cpx_d = -dist
            cpy_s = 0
            cpy_d = 0

            sspos = self.start_socket.socket_type

            if (x1 > x2 and sspos in (SINGLE_OUT, MULTI_OUT, PIPELINE_OUT, CONNECTOR_OUT)) or (x1 < x2 and sspos in (SINGLE_IN, MULTI_IN, PIPELINE_IN, CONNECTOR_IN)):
                cpx_d *= -1
                cpx_s *= -1

                cpy_d = (
                    (y1 - y2) / math.fabs(
                        (y1 - y2) if (y1 - y2) != 0 else 0.00001
                    )
                ) * radius
                cpy_s = (
                    (y2 - y1) / math.fabs(
                        (y2 - y1) if (y2 - y1) != 0 else 0.00001
                    )
                ) * radius

            path.cubicTo(x1 + cpx_s, y1 + cpy_s, x2 + cpx_d, y2 + cpy_d, x2, y2)
        
        elif style == 'Orthogonal':
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            if x2 > x1:
                path.lineTo(mid_x - radius, y1)
                if y2 > y1:
                    path.arcTo(mid_x - radius, y1, radius, radius, 90, -90)
                    path.lineTo(mid_x, y2 - radius)
                    path.arcTo(mid_x, y2 - radius, radius, radius, 180, 90)
                else:
                    path.arcTo(mid_x - radius, y1 - radius, radius, radius, -90, 90)
                    path.lineTo(mid_x, y2 + radius)
                    path.arcTo(mid_x, y2, radius, radius, 180, -90)
            else:
                if y2 > y1:
                    path.arcTo(x1, y1, radius, radius, 90, -90)
                    path.lineTo(x1 + radius, mid_y - radius)
                    path.arcTo(x1, mid_y - radius, radius, radius, 0, -90)
                    path.lineTo(x2, mid_y)
                    path.arcTo(x2 - radius, mid_y, radius, radius, 90, 90)
                    path.lineTo(x2 - radius, y2 - radius)
                    path.arcTo(x2 - radius, y2 - radius, radius, radius, 180, 90)
                else:
                    path.arcTo(x1, y1 - radius, radius, radius, -90, 90)
                    path.lineTo(x1 + radius, mid_y + radius)
                    path.arcTo(x1, mid_y, radius, radius, 0, 90)
                    path.lineTo(x2, mid_y)
                    path.arcTo(x2 - radius, mid_y - radius, radius, radius, -90, -90)
                    path.lineTo(x2 - radius, y2 + radius)
                    path.arcTo(x2 - radius, y2, radius, radius, 180, -90)
            path.lineTo(x2, y2) 

        self.setPath(path)