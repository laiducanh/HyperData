from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QResizeEvent, QColor
import qfluentwidgets

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
