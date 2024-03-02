from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsSceneHoverEvent
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainterPath, QColor, QPen, QPainter
from node_editor.base.node_graphics_node import NodeGraphicsSocket
import math

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2
EDGE_CP_ROUNDNESS = 100
LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
DEBUG = False

class NodeGraphicsEdge(QGraphicsPathItem):
    def __init__(self, start_socket:NodeGraphicsSocket=None, end_socket:NodeGraphicsSocket=None, parent=None):
        super().__init__(parent)

        self._color = QColor("#616161")
        self._color_selected = QColor("#252525")
        self._color_hovered = QColor("#FF37A6FF")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_dragging.setStyle(Qt.PenStyle.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(3.0)
        self._pen_dragging.setWidthF(3.0)
        self._pen_hovered.setWidthF(5.0)

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.hovered = False
        self.id = id(self)

        if self.start_socket != None: self.start_socket.addEdge(self)
        if self.end_socket != None: self.end_socket.addEdge(self)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if self.hovered and self.end_socket is not None:
            painter.setPen(self._pen_hovered)
            painter.drawPath(self.path())

        if self.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        
        painter.drawPath(self.path())
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hovered = False
        self.update()


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

        if (s[0] > d[0] and sspos in (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and sspos in (LEFT_BOTTOM, LEFT_TOP)):
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
