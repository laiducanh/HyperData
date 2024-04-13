from PyQt6.QtCore import pyqtSignal, Qt, QTimer
from PyQt6.QtWidgets import QVBoxLayout,  QScrollArea, QWidget, QSizePolicy
from PyQt6.QtGui import QPaintEvent
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import TextEdit
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.window import ProgressBar
from plot.curve.base_plottype.line import Line, Step, Area
from plot.curve.base_plottype.scatter import Scatter
from plot.curve.base_plottype.column import Column, ClusteredColumn, Marimekko
from plot.canvas import Canvas
from plot.insert_plot.insert_plot import NewPlot
from matplotlib.artist import Artist
from typing import List

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

        self.progressbar = ProgressBar()

        layout.addWidget(TitleLabel(str(self.gid).title()))
        layout.addWidget(self.progressbar)
                
        self.scroll_widget = Frame()
        self.scroll_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.setLayout(self.layout2)
        
        self.scroll_area = QScrollArea(parent)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.verticalScrollBar().setValue(1900)
        layout.addWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_widget)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.set_label)

        self.layout2.addWidget(TitleLabel('Label'))
        self.layout2.addWidget(SeparateHLine())
        self.legend = TextEdit()
        self.legend.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.legend.button.setPlainText(self.get_label())
        self.legend.setFixedHeight(100)
        self.layout2.addWidget(self.legend)
        self.legend.button.textChanged.connect(lambda: self.timer.start(300))
        self.legend.button.textChanged.connect(lambda: self.progressbar.setValue(0))
        self.initialize_layout()

        self.progressbar.setValue(100)

    def find_object (self) -> List[Artist]:
        obj_list = list()
        for obj in self.canvas.fig.findobj(match=Artist):
            if obj._gid != None and obj._gid == self.gid:
                obj_list.append(obj)
        return obj_list
        
    def set_label (self):
        self.progressbar.setValue(0)
        self.progressbar._setValue(0)
        _label = self.legend.button.toPlainText()
        if _label == "":
            _label = "_"
        for obj in self.obj:
            obj.set_label(_label)
        self.set_legend()
        self.canvas.draw()
        self.progressbar.setValue(100)

    def get_label (self):
        # skip label if starts with "_"
        for obj in self.obj:
            if obj.get_label().startswith("_"):
                return None
            return obj.get_label()
    
    def set_legend(self):
        _artist = list()
        _gid = list()
        _label = list()
        for obj in self.canvas.fig.findobj(match=Artist):
            if obj._gid != None and "graph" in obj._gid and obj._gid not in _gid:
                _gid.append(obj._gid)
                _artist.append(obj)
                _label.append(obj._label)
        for ind, val in enumerate(_label):
            if val.startswith("_"):
                _label.pop(ind)
                _artist.pop(ind)
        if self.get_legend(): self.get_legend().remove()
        if _artist != []:
            self.canvas.axesleg.legend(handles=_artist,draggable=True)
    
    def get_legend(self):
        return self.canvas.axesleg.get_legend()


    def update_plot (self):
        self.progressbar.setValue(0)
        self.progressbar._setValue(0)
        if self.get_legend(): self.set_legend()
        self.canvas.draw()
        self.sig.emit()
        self.progressbar.setValue(100)

    def initialize_layout(self):
        plot_type = self.obj[0].plot_type
        if plot_type in ["2d line"]:
            widget = Line(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type in ["2d step"]:
            widget = Step(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type in ["2d area"]:
            widget = Area(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type == "2d scatter":
            widget = Scatter(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type in ["2d column","2d stacked column", "2d 100% stacked column"]:
            widget = Column(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type in ["2d clustered column"]:
            widget = ClusteredColumn(self.gid, self.canvas, self.plot, self.parent)
        elif plot_type in ["marimekko"]:
            widget = Marimekko(self.gid, self.canvas, self.plot, self.parent)

        widget.sig.connect(self.update_plot)
        self.layout2.addWidget(widget)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)