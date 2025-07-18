from PySide6.QtWidgets import (QGraphicsItem, QGraphicsRectItem, QGraphicsScene, QGraphicsLineItem, QGraphicsTextItem, QGraphicsObject)
from PySide6.QtGui import QColor, QBrush, QPolygonF, QPainter, QPen
from PySide6.QtCore import Signal, Qt, QPointF
import numpy as np
from typing import Literal
from config.settings import config

class MarginIndicator(QGraphicsObject):
    onMoved = Signal()
    def __init__(self, indicator:Literal['vertical_top','vertical_bottom','horizontal_left','horizontal_right'],
                 width, height, length=800, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setZValue(10)
        self.indicator = indicator
        self.length = length
        self.fraction = 0

        if self.indicator in ['vertical_top','vertical_bottom']:
            self.triangle = QPolygonF([
                QPointF(width, 0),
                QPointF(2*width, -height),
                QPointF(2*width, height)
            ])
        else:
            self.triangle = QPolygonF([
                QPointF(0, height),
                QPointF(width, 2*height),
                QPointF(-width, 2*height)
            ])
    
    def paint(self, painter:QPainter, option, widget=None):
        painter.setBrush(QBrush(QColor(config["themecolor"])))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(self.triangle)
    
    def boundingRect(self):
        return self.triangle.boundingRect()
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            pos:QPointF = value
            if self.indicator == 'vertical_top':
                vertical_bottom: MarginIndicator = self.scene().left_margin_bot
                y = max(0, min(pos.y(), self.length, vertical_bottom.length*(vertical_bottom.fraction-0.1)))
                self.fraction = y/self.length
                return QPointF(self.x(), y)
            elif self.indicator == 'vertical_bottom':
                vertical_top: MarginIndicator = self.scene().left_margin_top
                y = max(vertical_top.length*(vertical_top.fraction+0.1), min(pos.y(), self.length))
                self.fraction = y/self.length
                return QPointF(self.x(), y)
            elif self.indicator == 'horizontal_left':
                horizontal_right: MarginIndicator = self.scene().top_margin_right
                x = max(0, min(pos.x(), self.length, horizontal_right.length*(horizontal_right.fraction-0.1)))
                self.fraction = x/self.length
                return QPointF(x, self.y())
            elif self.indicator == 'horizontal_right':
                horizontal_left: MarginIndicator = self.scene().top_margin_left
                x = max(horizontal_left.length*(horizontal_left.fraction+0.1), min(pos.x(), self.length))
                self.fraction = x/self.length
                return QPointF(x, self.y())
                
        return super().itemChange(change, value)

    def _setPos(self, fraction):
        self.fraction = fraction
        if self.indicator in ['vertical_top','vertical_bottom']:
            return super().setPos(self.x(), fraction*self.length)
        else:
            return super().setPos(fraction*self.length, self.y())
    
    def update_length(self, length):
        self.length = length
        self._setPos(self.fraction)
    
    def mouseReleaseEvent(self, event):
        self.onMoved.emit()
        return super().mouseReleaseEvent(event)

class Crosshair(QGraphicsLineItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setZValue(15)
    
    def paint(self, painter:QPainter, option, /, widget = ...):
        if config['plot_crosshair']:
            pen = QPen(QColor(config['themecolor']))
            if config['plot_crosshair_style'] == 'solid':
                pen.setStyle(Qt.PenStyle.SolidLine)
            elif config['plot_crosshair_style'] == 'dash':
                pen.setStyle(Qt.PenStyle.DashLine)
            elif config['plot_crosshair_style'] == 'dot':
                pen.setStyle(Qt.PenStyle.DotLine)
            elif config['plot_crosshair_style'] == 'dash dot':
                pen.setStyle(Qt.PenStyle.DashDotLine)
            elif config['plot_crosshair_style'] == 'dash dot dot':
                pen.setStyle(Qt.PenStyle.DashDotDotLine)
            painter.setPen(pen)
            painter.drawLine(self.line())
        # return super().paint(painter, option, widget)

class GraphicsScene(QGraphicsScene):
    margin_updated = Signal()
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.rulerOn = False
        self.draw_crosshair()
    
    def draw_crosshair(self):
        self.vcross = Crosshair()
        self.addItem(self.vcross)

        self.hcross = Crosshair()
        self.addItem(self.hcross)
    
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
        self.top_margin_left = MarginIndicator(width=10, height=self.ruler_height, indicator='horizontal_left')
        self.top_margin_left.onMoved.connect(self.margin_updated.emit)
        self.addItem(self.top_margin_left)

        self.top_margin_right = MarginIndicator(width=10, height=self.ruler_height, indicator='horizontal_right')
        self.top_margin_right.onMoved.connect(self.margin_updated.emit)
        self.addItem(self.top_margin_right)

        # Add margin indicator on left ruler
        self.left_margin_top = MarginIndicator(width=self.ruler_width, height=10, indicator='vertical_top')
        self.left_margin_top.onMoved.connect(self.margin_updated.emit)
        self.addItem(self.left_margin_top)

        self.left_margin_bot = MarginIndicator(width=self.ruler_width, height=10, indicator='vertical_bottom')
        self.left_margin_bot.onMoved.connect(self.margin_updated.emit)
        self.addItem(self.left_margin_bot)

        self.update_rulers()
    
    def _best_interval(self, length:float):
        interval = 1
        while length/(10*(interval+1)) > 20:
            interval += 1
        return interval if interval % 2 == 0 else interval + 1
    
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
        interval = self._best_interval(width)
        for ind, x in enumerate(np.linspace(0, width, int(interval*10+1), endpoint=True)):
            if ind % int(interval) == 0:
                text = QGraphicsTextItem(str(round(x/width, 1)))
                text.setDefaultTextColor('black')
                text.setPos(x-text.boundingRect().width()/2, self.ruler_height/2 - text.boundingRect().height()/2)
                self.addItem(text)
                self.top_ticks.append(text)
            elif ind % int(interval) == interval/2:
                line_big = QGraphicsLineItem(x, 7, x, self.ruler_height-7)
                self.addItem(line_big)
                self.top_ticks.append(line_big)
            else:
                line_small = QGraphicsLineItem(x, 9, x, self.ruler_height-9)
                self.addItem(line_small)
                self.top_ticks.append(line_small)

        # Draw new left ruler ticks
        interval = self._best_interval(height)
        for ind, y in enumerate(np.linspace(0, height, int(interval*10+1), endpoint=True)):
            if ind % int(interval) == 0:
                text = QGraphicsTextItem(str(round(y/height, 1)))
                text.setDefaultTextColor('black')
                text.setTransformOriginPoint(text.boundingRect().center())
                text.setRotation(270)
                text.setPos(self.ruler_width/2-text.boundingRect().width()/2, y - text.boundingRect().height()/2)
                self.addItem(text)
                self.left_ticks.append(text)
            elif ind % int(interval) == interval/2:
                line_big = QGraphicsLineItem(7, y, self.ruler_width-7, y)
                self.addItem(line_big)
                self.left_ticks.append(line_big)
            else:
                line_small = QGraphicsLineItem(9, y, self.ruler_width-9, y)
                self.addItem(line_small)
                self.left_ticks.append(line_small)

        self.top_margin_left.update_length(width)
        self.top_margin_right.update_length(width)
        self.left_margin_top.update_length(height)
        self.left_margin_bot.update_length(height)

        self.toggle_ruler(self.rulerOn)

    def toggle_ruler(self, enable:bool):
        self.rulerOn = enable
        if enable:
            self.top_margin_left.show()
            self.top_margin_right.show()
            self.left_margin_bot.show()
            self.left_margin_top.show()
            self.left_ruler.show()
            self.top_ruler.show()
            for item in self.top_ticks + self.left_ticks:
                item.show()
        else:
            self.top_margin_left.hide()
            self.top_margin_right.hide()
            self.left_margin_bot.hide()
            self.left_margin_top.hide()
            self.left_ruler.hide()
            self.top_ruler.hide()
            for item in self.top_ticks + self.left_ticks:
                item.hide()
