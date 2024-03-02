from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
import qfluentwidgets

class SeparateHLine(QWidget):
    """ Horizontal separator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfluentwidgets.common.style_sheet.isDarkTheme():
            painter.setPen(QColor(255, 255, 255, 51))
        else:
            painter.setPen(QColor(0, 0, 0, 22))

        painter.drawLine(0, 1, self.width(), 1)

class SeparateVLine (qfluentwidgets.VerticalSeparator):
    def __init__(self):
        super().__init__()
