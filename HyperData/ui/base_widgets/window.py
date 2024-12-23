from PySide6.QtWidgets import (QProgressBar, QVBoxLayout, QProgressDialog, QDialog, QHBoxLayout)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, Property, QSize, QEasingCurve
from PySide6.QtGui import QResizeEvent, QColor, QPainter, QRegion, QPainterPath, QBrush
import math, typing
from ui.base_widgets.button import _PrimaryPushButton, _PushButton
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from ui.utils import isDark

class Dialog (QDialog):
    def __init__(self, title:str=None, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.setWindowTitle(title)  
        
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vlayout.setContentsMargins(20,30,20,10)
        self.vlayout.addWidget(TitleLabel(title))
        self.vlayout.addWidget(SeparateHLine())

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vlayout.addLayout(self.main_layout)

        self.groupButton = QHBoxLayout()
        self.vlayout.addLayout(self.groupButton)
        self.ok_btn = _PrimaryPushButton("Save Changes")
        self.ok_btn.setMinimumWidth(200)
        self.ok_btn.clicked.connect(self.accept)
        self.groupButton.addWidget(self.ok_btn)
        self.cancel_btn = _PushButton("Cancel")
        self.cancel_btn.setMinimumWidth(200)
        self.cancel_btn.clicked.connect(self.reject)
        self.groupButton.addWidget(self.cancel_btn)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)
       
        # Fill the dialog background
        if isDark():
            painter.fillPath(path, QBrush(QColor(32,32,32)))
        else:
            painter.fillPath(path, QBrush(Qt.GlobalColor.white))
    
    def showEvent(self, event):
        

        # # Get the current geometry of the dialog
        # start_geometry = self.geometry()

        # # Create a new geometry with a smaller size
        # end_geometry = QRect(start_geometry.center() - QRect(0, 0, 10, 10).center(),
        #                      start_geometry.size())

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(100)  # Adjust duration as needed
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
        super().showEvent(event)

    
class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self._val = 0

        self.lightBackgroundColor = QColor(0, 0, 0, 155)
        self.darkBackgroundColor = QColor(255, 255, 255, 155)
        self.color = QColor("#0085f1")
        self.ani = QPropertyAnimation(self, b'val', self)
        self.setValue(self._val)
        self.valueChanged.connect(self._onValueChanged)
    
    def _setValue(self, value: int) -> None:
        self._val = value
        self.update()
    
    def _value(self) -> int:
        return self._val

    def _onValueChanged(self, value):
        self.ani.stop()
        self.ani.setEndValue(value)
        self.ani.setDuration(300)
        self.ani.start()
        super().setValue(value)
    
    def changeColor(self, colortype:typing.Literal["fail", "success"]):
        if colortype == "fail":
            self.color = QColor("#e03131")
        elif colortype == "success":
            self.color = QColor("#0085f1")

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # draw background
        bc = self.lightBackgroundColor
        painter.setPen(bc)
        y =  math.floor(self.height() / 2)
        painter.drawLine(0, y, self.width(), y)

        if self.minimum() >= self.maximum():
            return

        # draw bar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.color)
        w = int(self.val / (self.maximum() - self.minimum()) * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(0, 0, w, self.height(), r, r)

    val = Property(int, _value, _setValue)
        
class ProgressDialog (QProgressDialog):
    def __init__(self, text=None, cancel_btn=None, parent=None):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setLabelText(text)
        self.setCancelButton(cancel_btn)
        self.progressbar = ProgressBar(self)
        self.setBar(self.progressbar)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(self.rect().toRectF(), 10, 10)

        # Fill the dialog background
        if isDark:
            painter.fillPath(path, QBrush(QColor(32,32,32)))
        else:
            painter.fillPath(path, QBrush(Qt.GlobalColor.white))