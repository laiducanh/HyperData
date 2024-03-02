from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent, QResizeEvent, QColor
import qfluentwidgets

class MessageBox (qfluentwidgets.dialog.MaskDialogBase):
    def __init__(self, parent):
        super().__init__(parent)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self.widget.setStyleSheet("""#centerWidget{background-color:white;
                                        border: 1px solid rgb(144, 144, 142);
                                        border-radius: 10px;}""")
        self.widget.setFixedSize(200,200)
        self.viewLayout = QVBoxLayout(self.widget)
        
        self.viewLayout.addWidget(qfluentwidgets.StrongBodyLabel('qocis'))