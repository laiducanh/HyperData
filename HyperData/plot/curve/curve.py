from PyQt6.QtCore import pyqtSignal, Qt, QThreadPool
from PyQt6.QtWidgets import (QHBoxLayout,QVBoxLayout, QTextEdit, QScrollArea, QComboBox,
                             QWidget)

from ui.base_widgets.text import StrongBodyLabel, TextEdit
from ui.base_widgets.separator import SeparateHLine
from plot.curve.base_plottype.line import Line
from plot.canvas import Canvas
import qfluentwidgets, matplotlib
from matplotlib.artist import Artist

class Curve (QWidget):
    sig = pyqtSignal() # when want to the whole graph
    sig_legend = pyqtSignal() # when editing legend only
    def __init__(self, gid:str, canvas:Canvas, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        #layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_object()

        layout.addWidget(StrongBodyLabel(str(self.gid).title()))

        layout.addWidget(SeparateHLine())
                
        self.scroll_widget = qfluentwidgets.CardWidget()
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.setLayout(self.layout2)
        
        self.scroll_area = QScrollArea(parent)
        self.scroll_area.setObjectName('QScrollArea')
        self.scroll_area.setStyleSheet('QScrollArea {border: none; background-color:transparent}')
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.verticalScrollBar().setValue(1900)
        layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        self.layout2.addWidget(StrongBodyLabel('Label'))
        self.layout2.addWidget(SeparateHLine())
        self.legend = TextEdit()
        self.legend.button.setPlainText(self.get_label())
        self.legend.setFixedHeight(100)
        self.layout2.addWidget(self.legend)
        self.legend.button.textChanged.connect(self.set_label)

        self.initialize_layout()

    def find_object (self) -> Artist:
        for obj in self.canvas.fig.findobj(match=Artist):
            if obj._gid != None and obj._gid == self.gid:
                return obj
        
    def set_label (self):
        self.obj.set_label(self.legend.button.toPlainText())
        self.canvas.axes.legend()
        self.canvas.draw_idle()
    
    def get_label (self):
        if "_child" in self.obj.get_label():
            return str()
        return self.obj.get_label()

    def initialize_layout(self):
        
        if isinstance(self.obj, matplotlib.lines.Line2D):
            line = Line(self.gid, self.canvas)
            self.layout2.addWidget(line)
        

    