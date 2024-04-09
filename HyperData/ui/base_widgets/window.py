from PyQt6.QtWidgets import (QProgressBar, QVBoxLayout, QProgressDialog, QDialog, QHBoxLayout)
from PyQt6.QtCore import pyqtSignal, Qt, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QResizeEvent, QColor, QPainter
import math
from ui.base_widgets.button import _PrimaryPushButton, _PushButton

class Dialog (QDialog):
    def __init__(self, title:str=None, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.Dialog)   
        self.setWindowTitle(title)  
        
        self.vlayout = QVBoxLayout(self)
        self.main_layout = QVBoxLayout()
        self.vlayout.addLayout(self.main_layout)

        self.groupButton = QHBoxLayout()
        self.vlayout.addLayout(self.groupButton)
        self.ok_btn = _PrimaryPushButton("OK")
        self.ok_btn.setMinimumWidth(200)
        self.ok_btn.clicked.connect(self.accept)
        self.groupButton.addWidget(self.ok_btn)
        self.cancel_btn = _PushButton("Cancel")
        self.cancel_btn.setMinimumWidth(200)
        self.cancel_btn.clicked.connect(self.reject)
        self.groupButton.addWidget(self.cancel_btn)
    
class ProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self._val = 0

        self.lightBackgroundColor = QColor(0, 0, 0, 155)
        self.darkBackgroundColor = QColor(255, 255, 255, 155)
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
        painter.setBrush(QColor("#0085f1"))
        w = int(self.val / (self.maximum() - self.minimum()) * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(0, 0, w, self.height(), r, r)

    val = pyqtProperty(int, _value, _setValue)
        
class ProgressDialog (QProgressDialog):
    def __init__(self, text=None, cancel_btn=None, parent=None):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setLabelText(text)
        self.setCancelButton(cancel_btn)
        self.progressbar = ProgressBar(self)
        self.setBar(self.progressbar)