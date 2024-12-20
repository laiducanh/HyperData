from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QBrush, QColor, QPainter
from ui.utils import isDark

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
CONNECTOR_IN = 7
CONNECTOR_OUT = 8
DEBUG = False

class SocketItem (QGraphicsItem):
    def __init__(self, socket_type, parent=None):
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 2.5
        self._colors = [
            QColor("#FFA04D"),
            QColor("#FA6D6D"),
            QColor("#6DAFFA"),
            QColor("#6DFA8D"),
            QColor("#f0f1f2"),
            QColor("#f0f1f2"),
            QColor("#F2F209"),
            QColor("#F2F209"),
        ]
        self._color_background = self._colors[socket_type-1]
        self._color_outline = QColor("#FF000000")

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.socket_type = socket_type
        self.hovered = False
        self.id = id(self)

        self._pen_default = QPen(self._color_outline)
        self._pen_default.setWidthF(self.outline_width)
        self._pen_hovered = QPen(self._color_outline)
        self._pen_hovered.setWidthF(self.outline_width+1)
        self._brush = QBrush(self._color_background)    
        self._text = QGraphicsTextItem(self)   
        self._text.hide()     
        self.setTitle()

    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        # painting circle
        painter.setBrush(self._brush)
        
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
        else:
            painter.setPen(self._pen_default)
            painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
        
        if isDark():
            self._text.setDefaultTextColor(Qt.GlobalColor.white)
        else:
            self._text.setDefaultTextColor(Qt.GlobalColor.black)
        
    def boundingRect(self):
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )

    def setTitle(self, title = None):
        if not title:
            if self.socket_type == SINGLE_IN:
                self.title = 'Single Input'
            elif self.socket_type == MULTI_IN:
                self.title = 'Multiple Inputs'
            elif self.socket_type == SINGLE_OUT:
                self.title = 'Single Output'
            elif self.socket_type == MULTI_OUT:
                self.title = 'Multiple Outputs'
            elif self.socket_type in [PIPELINE_IN, PIPELINE_OUT]:
                self.title = "Pipeline"
            elif self.socket_type in [CONNECTOR_IN, CONNECTOR_OUT]:
                self.title = "Connector"
        else:
            self.title = title
        
        self._text.setPlainText(self.title)
        self._text.setPos(16,-13)

    def getSocketPosition(self):
        pass

    def addEdge(self, edge):
        pass

    def removeEdge(self, edge):
        pass

    def removeAllEdges(self):
        pass

    def hasEdge(self):
        pass

    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass