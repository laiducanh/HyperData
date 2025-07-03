from PySide6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsTextItem, QGraphicsProxyWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QFont, QBrush, QColor, QPainterPath, QPainter, QTextOption
from ui.utils import isDark
from config.settings import config
from node_editor.graphics.graphics_content import GraphicsContent

DEBUG = False

class GraphicsNode(QGraphicsItem):
    def __init__(self, title:str, parent=None):
        super().__init__(parent)

        self._title_font = QFont("Arial", 10.5, 700)
        self.title = title
        self._edge_size = 5.0
        self._title_height = 28.0
        self._padding = 4.0
        self._socket_spacing = 22
        self._width = 180
        self._height = 50
        self.hovered = False
        self.id = id(self)
        self.content = None

        self.setColor()

        self.setTitle()
        
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def setColor(self):
        
        if isDark():
            self._color = QColor("#c8c8c8")
            self._color_selected = QColor(config["themecolor"])
            self._color_hovered = QColor(config["themecolor"])
            self._brush_background = QBrush(QColor("#232323"))
            self._title_color = Qt.GlobalColor.white
        else:
            self._color = QColor("#7F000000")
            self._color_selected = QColor(config["themecolor"])
            self._color_hovered = QColor(config["themecolor"])
            self._brush_background = QBrush(Qt.GlobalColor.white)
            self._title_color = Qt.GlobalColor.black

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(1.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self._width,
            self._height
        ).normalized()     

    def setTitle(self):
        for obj in self.childItems():
            if isinstance(obj, QGraphicsTextItem):
                obj.deleteLater()
        self.title_item = QGraphicsTextItem(self.title.upper(),parent=self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        #self.title_item.setPos(self._padding, 0)
        self.title_item.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
        self.title_item.setTextWidth(self._width)
    
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverLeaveEvent(event)
        self.hovered = False
        self.update()


    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):
        
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0,0, self._width, self._title_height, self._edge_size, self._edge_size)
        path_title.addRect(0, self._title_height - self._edge_size, self._edge_size, self._edge_size)
        path_title.addRect(self._width - self._edge_size, self._title_height - self._edge_size, self._edge_size, self._edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_title.simplified())
        self.title_item.setDefaultTextColor(self._title_color)
        painter.setPen(self._pen_default)
        painter.drawLine(10, self._title_height, self._width-10, self._title_height)


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self._title_height, self._width, self._height - self._title_height, self._edge_size, self._edge_size)
        path_content.addRect(0, self._title_height, self._edge_size, self._edge_size)
        path_content.addRect(self._width - self._edge_size, self._title_height, self._edge_size, self._edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self._width, self._height, self._edge_size, self._edge_size)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())
    
    def set_Content(self, content: GraphicsContent):
        self.content = content
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self._edge_size)+10, int(self._title_height + self._edge_size),
                                 int(self._width - 2*self._edge_size-20), int(self._height - 2*self._edge_size-self._title_height))
        self.grContent.setWidget(content)
        self._height = max(self._height, self._title_height + self.content.height() + 2*self._padding)

    def updateConnectedEdges(self):
        pass

    def getSocketPosition(self, index, socket_type):
        pass

    def addSocket(self, index, socket_type):
        pass

    def removeSocket(self, index, socket_type, socket):
        pass

    def serialize(self):
        pass

    def deserialize(self, data, hashmap={}):
        pass

    def _update(self):
        self.setColor()
        return super().update()


    

