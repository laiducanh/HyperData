from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit
from plot.curve.base_widget.line import LineBase
from plot.curve.base_widget.marker import MarkerBase
from ui.base_widgets.separator import SeparateHLine
from ui.base_widgets.text import TextEdit, StrongBodyLabel

class Line (QWidget):
    sig = pyqtSignal()
    sig_legend = pyqtSignal()
    def __init__(self, gid, canvas, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)
        #layout.setContentsMargins(0,0,0,0)
        #self.setStyleSheet('background-color:transparent')
        self.gid = gid
        self.canvas = canvas

        layout.addWidget(StrongBodyLabel('Line'))
        layout.addWidget(SeparateHLine())

        line = LineBase(gid, canvas)
        layout.addWidget(line)

        layout.addSpacing(10)

        layout.addWidget(StrongBodyLabel('Marker'))
        layout.addWidget(SeparateHLine())

        marker = MarkerBase(gid, canvas)
        layout.addWidget(marker)

        layout.addStretch()
    