from PySide6.QtWidgets import (QProgressBar, QVBoxLayout, QProgressDialog, QDialog, 
                               QHBoxLayout, QFileDialog, QWidget,)
from PySide6.QtCore import (Qt, QPropertyAnimation, Property, QEasingCurve
                            ,QParallelAnimationGroup, QSequentialAnimationGroup)
from PySide6.QtGui import QColor, QPainter, QPainterPath, QBrush
import math, typing
from ui.base_widgets.button import PushButton, TransparentPushButton
from ui.utils import isDark
from typing import Literal

class Dialog (QDialog):
    def __init__(self, title:str=None, parent=None):
        super().__init__(parent)

        # self.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle(title)  
        
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # self.vlayout.setContentsMargins(0,0,0,0)
        # self.vlayout.addWidget(TitleLabel(title))
        # self.vlayout.addWidget(SeparateHLine())

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vlayout.addLayout(self.main_layout)

        self.vlayout.addStretch()

        widget = QWidget()
        # widget.setAutoFillBackground(True)
        # widget.setPalette(Qt.GlobalColor.gray)
        self.groupButton = QHBoxLayout(widget)
        self.vlayout.addWidget(widget)
        self.groupButton.addStretch()
        self.ok_btn = PushButton(
            text="Save Changes",
            icon="accept.png",
            setter=self.accept,
            layout=self.groupButton
        )
        self.cancel_btn = TransparentPushButton(
            text="Cancel",
            icon="close.png",
            setter=self.reject,
            layout=self.groupButton
        )
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Create rounded rectangle path
        # path = QPainterPath()
        # path.addRoundedRect(self.rect().toRectF(), 10, 10)

        # Fill the dialog background
        # if isDark():
        #     painter.fillPath(path, QBrush(QColor(32,32,32)))
        # else:
        #     painter.fillPath(path, QBrush(QColor(250,250,250)))
        super().paintEvent(event)
    
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
    def __init__(self, progresstype:Literal['normal','indeterminate']='normal', 
                 parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self.progresstype = progresstype

        self.lightBackgroundColor = QColor(0, 0, 0, 155)
        self.darkBackgroundColor = QColor(255, 255, 255, 155)
        self.color = QColor("#0085f1")

        self._val = 0
        self.ani = QPropertyAnimation(self, b'val', self)
        self.setValue(self._val)
        self.valueChanged.connect(self._onValueChanged)

        self._shortPos = 0
        self._longPos = 0

        self.shortBarAni = QPropertyAnimation(self, b'shortPos', self)
        self.longBarAni = QPropertyAnimation(self, b'longPos', self)

        self.aniGroup = QParallelAnimationGroup(self)
        self.longBarAniGroup = QSequentialAnimationGroup(self)

        self.shortBarAni.setDuration(833)
        self.longBarAni.setDuration(1167)
        self.shortBarAni.setStartValue(0)
        self.longBarAni.setStartValue(0)
        self.shortBarAni.setEndValue(1.45)
        self.longBarAni.setEndValue(1.75)
        self.longBarAni.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.aniGroup.addAnimation(self.shortBarAni)
        self.longBarAniGroup.addPause(785)
        self.longBarAniGroup.addAnimation(self.longBarAni)
        self.aniGroup.addAnimation(self.longBarAniGroup)
        self.aniGroup.setLoopCount(-1)

        if self.progresstype == 'indeterminate': self.start()
    
    def set_type(self, progresstype:Literal['normal','indeterminate']):
        self.progresstype = progresstype
        if self.progresstype == 'indeterminate': self.start()
    
    def set_value(self, value: int) -> None:
        self._val = value
        self.update()
    
    def get_value(self) -> int:
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
    
    def get_shortPos(self):
        return self._shortPos
   
    def set_shortPos(self, p):
        self._shortPos = p
        self.update()
    
    def get_longPos(self):
        return self._longPos
    
    def set_longPos(self, p):
        self._longPos = p
        self.update()

    def start(self):
        self._shortPos = 0
        self._longPos = 0
        self.aniGroup.start()
        self.update()

    def stop(self):
        self.aniGroup.stop()
        self._shortPos = 0
        self._longPos = 0
        self.update()

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

        # normal progress bar
        if self.progresstype == 'normal':
            w = int(self.val / (self.maximum() - self.minimum()) * self.width())
            r = self.height() / 2
            painter.drawRoundedRect(0, 0, w, self.height(), r, r)

        else: # draw indeterminate progress bar
            # draw short bar
            x = int((self.shortPos - 0.4) * self.width())
            w = int(0.4 * self.width())
            r = self.height() / 2
            painter.drawRoundedRect(x, 0, w, self.height(), r, r)

            # draw long bar
            x = int((self.longPos - 0.6) * self.width())
            w = int(0.6 * self.width())
            r = self.height() / 2
            painter.drawRoundedRect(x, 0, w, self.height(), r, r)

    val = Property(int, get_value, set_value)
    shortPos = Property(float, get_shortPos, set_shortPos)
    longPos = Property(float, get_longPos, set_longPos)
        
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
        path.addRoundedRect(self.rect().toRectF(), 6, 6)

        # Fill the dialog background
        if isDark():
            painter.fillPath(path, QBrush(QColor(32,32,32)))
        else:
            painter.fillPath(path, QBrush(QColor(200,200,200)))

class FileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MacOS has a bug that prevents native dialog from properly working
        # then use the option of DontUseNativeDialog
        # if platform.system() == "Darwin":
        #     self.setOption(QFileDialog.Option.DontUseNativeDialog)


