from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsItem, QGraphicsSceneHoverEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen, QPainter

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8

class GraphicsEdge(QGraphicsPathItem):
    def __init__(self, start_socket=None, end_socket=None, parent=None):
        super().__init__(parent)

        self.hovered = False
        self.id = id(self)

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)

        self.initUI()
    
    def initUI(self):
        if self.start_socket.socket_type in [PIPELINE_OUT]:
            self._color = Qt.GlobalColor.darkBlue
        else:
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

    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        self.updatePath()
        self.initUI()
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
        pass
    
    


