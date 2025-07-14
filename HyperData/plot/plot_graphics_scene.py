from PySide6.QtWidgets import (QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem)
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import QRectF, Signal, Qt, QPointF

class MarginIndicator(QGraphicsRectItem):
    def __init__(self, x, y, width=4, height=20, orientation='vertical', length=800, *args, **kwargs):
        super().__init__(x, y, width, height, *args, **kwargs)
        self.setBrush(QBrush(Qt.GlobalColor.red))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.orientation = orientation
        self.length = length
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            pos:QPointF = value
            if self.orientation == 'vertical':
                # Constrain x position within ruler length, lock y position
                x = max(0, min(pos.x(), self.length - self.rect().width()))
                pos = QPointF(x, self.y())
            else:
                # Constrain y position within ruler length, lock x position
                y = max(0, min(pos.y(), self.length - self.rect().height()))
                pos = QPointF(self.x(), y)
            return pos
        return super().itemChange(change, value)

class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
    
    def draw_ruler(self):

        # Draw top ruler
        self.ruler_height = 20
        self.top_ruler = QGraphicsRectItem(0, 0, 800, self.ruler_height)
        self.top_ruler.setBrush(QBrush(QColor(230, 230, 230)))
        self.addItem(self.top_ruler)

        # Draw left ruler
        self.ruler_width = 20
        self.left_ruler = QGraphicsRectItem(0, 0, self.ruler_width, 600)
        self.left_ruler.setBrush(QBrush(QColor(230, 230, 230)))
        self.addItem(self.left_ruler)

        # Keep track of tick items to delete them later on resize
        self.top_ticks = []
        self.left_ticks = []

        # Add margin indicator on top ruler
        self.top_margin = MarginIndicator(100, 0, width=4, height=self.ruler_height, orientation='vertical')
        self.addItem(self.top_margin)

        # Add margin indicator on left ruler
        self.left_margin = MarginIndicator(0, 100, width=self.ruler_width, height=4, orientation='horizontal')
        self.addItem(self.left_margin)

        self.update_rulers()
    
    def update_rulers(self):
        width = self.views()[0].viewport().width()
        height = self.views()[0].viewport().height()
  
        # Update ruler sizes
        self.top_ruler.setRect(0, 0, width, self.ruler_height)
        self.left_ruler.setRect(0, 0, self.ruler_width, height)

        # Remove old tick marks
        for item in self.top_ticks + self.left_ticks:
            self.removeItem(item)
        self.top_ticks.clear()
        self.left_ticks.clear()

        # Draw new top ruler ticks
        tick_interval = 50
        for x in range(0, int(width), tick_interval):
            line = QGraphicsLineItem(x, 0, x, self.ruler_height)
            self.addItem(line)
            text = QGraphicsTextItem(str(x))
            text.setPos(x + 2, 2)
            self.addItem(text)
            self.top_ticks.extend([line, text])

        # Draw new left ruler ticks
        for y in range(0, int(height), tick_interval):
            line = QGraphicsLineItem(0, y, self.ruler_width, y)
            self.addItem(line)
            text = QGraphicsTextItem(str(y))
            text.setPos(2, y + 2)
            self.addItem(text)
            self.left_ticks.extend([line, text])
        
        self.top_margin.length = width
        self.left_margin.length = height