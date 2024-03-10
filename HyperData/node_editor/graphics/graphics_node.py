from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsProxyWidget, QWidget, QGraphicsPathItem
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPen, QFont, QBrush, QColor, QPainterPath, QPainter, QTextOption, QAction
import qfluentwidgets

SINGLE_IN = 1
MULTI_IN = 2
SINGLE_OUT = 3
MULTI_OUT = 4
PIPELINE_IN = 5
PIPELINE_OUT = 6
DEBUG = False

class GraphicsNode (QGraphicsItem):
    def __init__(self, title:str, parent=None):
        super().__init__(parent)

        self._title_font = QFont("Monospace", 10, 700)
        self.title = title
        self.edge_size = 5.0
        self.title_height = 24.0
        self._padding = 4.0
        self.socket_spacing = 22
        self.width = 180
        self.height = 100
        self.hovered = False
        self.id = id(self)
        self.content_change = False

        self.setColor()

        self.setTitle()
        

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        self.wasMoved = False

    def setColor(self):
        
        self._color = QColor("#7F000000")
        self._color_selected = QColor("#252525")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        if qfluentwidgets.isDarkTheme():
            self._brush_background = QBrush(QColor("#232323"))
            self._brush_title = QBrush(QColor("#F5F5F5"))
            self._title_color = Qt.GlobalColor.black
            self._title_color_hovered = Qt.GlobalColor.darkGray
        else:
            self._brush_background = QBrush(Qt.GlobalColor.white)
            self._brush_title = QBrush(QColor("#434343"))
            self._title_color = Qt.GlobalColor.lightGray
            self._title_color_hovered = Qt.GlobalColor.white

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()     

    def setTitle(self):
        self.title_item = QGraphicsTextItem(self.title.upper(),parent=self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        #self.title_item.setPos(self._padding, 0)
        self.title_item.document().setDefaultTextOption(QTextOption(Qt.AlignmentFlag.AlignCenter))
        self.title_item.setTextWidth(self.width)
    
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverEnterEvent(event)
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        super().hoverLeaveEvent(event)
        self.hovered = False
        self.update()

    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        #self.updateConnectedEdges() # already implemented in node_graphics_view class
        self.wasMoved = True
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self.wasMoved:
            self.wasMoved = False
            if DEBUG: print('node moved')

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        super().mousePressEvent(event)


    def paint(self, painter:QPainter, QStyleOptionGraphicsItem, widget=None):

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0,0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            self.title_item.setDefaultTextColor(self._title_color_hovered)
            
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())
            self.title_item.setDefaultTextColor(self._title_color)

        



    

