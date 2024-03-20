from PyQt6.QtCore import pyqtSignal, Qt, QThreadPool
from PyQt6.QtWidgets import (QHBoxLayout,QVBoxLayout, QTextEdit, QScrollArea, QComboBox,
                             QWidget)

from ui.base_widgets.text import StrongBodyLabel, TextEdit
from ui.base_widgets.separator import SeparateHLine
from plot.curve.base_plottype.line import Line, Step, Area
from plot.curve.base_plottype.scatter import Scatter
from plot.canvas import Canvas
from plot.insert_plot.insert_plot import NewPlot
import qfluentwidgets, matplotlib
from matplotlib.artist import Artist

class Curve (QWidget):
    sig = pyqtSignal() # fire signal when plot updated
    def __init__(self, gid:str, canvas:Canvas, plot: NewPlot, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        #layout.setContentsMargins(0,0,0,0)
        self.parent = parent
        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_object()
        self.plot = plot

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
        self.set_legend()
        self.canvas.draw()

    def get_label (self):
        if "_child" in self.obj.get_label():
            return str()
        return self.obj.get_label()
    
    def set_legend(self):
        _leg = list()
        for obj in self.canvas.fig.findobj():
            if obj._gid != None and "graph" in obj._gid:
                _leg.append(obj)
        self.canvas.axesx2.legend(handles=_leg,draggable=True)
    
    def get_legend(self):
        return self.canvas.axesx2.get_legend()


    def update_plot (self):
        if self.get_legend(): self.set_legend()
        self.canvas.draw()
        self.sig.emit()

    def initialize_layout(self):
        plot_type = self.obj.plot_type
        if plot_type == "2d line":
            widget = Line(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type == "2d step":
            widget = Step(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type == "2d area":
            widget = Area(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type == "2d scatter":
            widget = Scatter(self.gid, self.canvas, self.plot, self.parent)

        widget.sig.connect(self.update_plot)
        self.layout2.addWidget(widget)
    