from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QProgressDialog
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QResizeEvent, QColor, QPainter
import qfluentwidgets, math

class _Dialog (qfluentwidgets.dialog.MaskDialogBase):
    def __init__(self, parent):
        super().__init__(parent)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self.widget.setStyleSheet("""#centerWidget{background-color:white;
                                        border: 1px solid rgb(144, 144, 142);
                                        border-radius: 10px;}""")
        #self.widget.setFixedSize(200,200)
        self.viewLayout = QVBoxLayout(self.widget)


class Dialog (qfluentwidgets.MessageBox):
    def __init__(self, title, parent):
        super().__init__(title,"",parent)

        self.textLayout.removeWidget(self.contentLabel)



class ProgressBar(qfluentwidgets.ProgressBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setFixedHeight(4)
        
        self.lightBackgroundColor = QColor(0, 0, 0, 155)
        self.darkBackgroundColor = QColor(255, 255, 255, 155)
    
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # draw background
        bc = self.darkBackgroundColor if qfluentwidgets.isDarkTheme() else self.lightBackgroundColor
        painter.setPen(bc)
        y =  math.floor(self.height() / 2)
        painter.drawLine(0, y, self.width(), y)

        if self.minimum() >= self.maximum():
            return

        # draw bar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(qfluentwidgets.themeColor())
        w = int(self.value() / (self.maximum() - self.minimum()) * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(0, 0, w, self.height(), r, r)
        
class ProgressDialog (QProgressDialog):
    def __init__(self, text=None, cancel_btn=None, parent=None):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setLabelText(text)
        self.setCancelButton(cancel_btn)
        self.setBar(ProgressBar(self))