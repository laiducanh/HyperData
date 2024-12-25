from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtWidgets import QVBoxLayout,  QScrollArea, QWidget, QSizePolicy
from PySide6.QtGui import QPaintEvent
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import TextEdit
from ui.base_widgets.frame import SeparateHLine, Frame
from ui.base_widgets.window import ProgressBar
from plot.curve.base_plottype.line import Line, Step, Stem, Stem3d, Area, StackedArea, StackedArea100
from plot.curve.base_plottype.scatter import Scatter, Scatter3D
from plot.curve.base_plottype.column import Column, Dot, Dumbbell, Column3D, ClusteredColumn, ClusteredDot, Marimekko, Treemap
from plot.curve.base_plottype.pie import Pie, Coxcomb, Doughnut, MultilevelDoughnut, SemicircleDoughnut
from plot.curve.base_plottype.stats import Histogram, Boxplot, Violinplot, Eventplot, Hist2d
from plot.canvas import Canvas
from plot.insert_plot.insert_plot import NewPlot
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from plot.plotting.plotting import set_legend, get_legend
from matplotlib.artist import Artist
from matplotlib import legend
from typing import List

DEBUG = True

class Curve (QWidget):
    sig = Signal() # fire signal when plot updated
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)
        
        self.setParent(parent)
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()

        self.progressbar = ProgressBar()

        self.initUI()

        self.progressbar.setValue(100)
    
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        #layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel(str(self.gid).title()))
        layout.addWidget(self.progressbar)
                
        self.scroll_widget = Frame()
        self.scroll_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_widget.setLayout(self.layout2)
        
        self.scroll_area = QScrollArea(self.parent())
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
        #self.legend.button.textChanged.connect(self.set_label)
        # self.legend.button.textChanged.connect(lambda: self.timer.start(1000))
        # self.legend.button.textChanged.connect(self.canvas.draw)
        
        self.initialize_layout()

    def find_object (self) -> List[Artist]:
        return find_mpl_object(self.canvas.fig,
                                   match=[Artist],
                                   gid=self.gid)
            
        
    def set_label (self):
        try:
            self.progressbar.setValue(0)
            self.progressbar._setValue(0)
            _label = self.legend.button.toPlainText()
            if _label == "":
                _label = "_"
            for obj in self.obj:
                obj.set_label(_label)
            set_legend(self.canvas)
            self.canvas.draw_idle()
            self.progressbar.setValue(100)
            
            
        except Exception as e:
            logger.exception(e)

    def get_label (self):
        # skip label if starts with "_"
        for obj in self.obj:
            if obj.get_label().startswith("_"):
                return None
            return obj.get_label()

    def update_plot (self):
        try:
            self.progressbar.setValue(0)
            self.progressbar._setValue(0)
            if get_legend(self.canvas): set_legend(self.canvas)
            self.canvas.draw_idle()
            self.sig.emit()
            self.progressbar.setValue(100)
        except Exception as e:
            logger.exception(e)

    def initialize_layout(self):
        try:
            plot_type = self.obj[0].plot_type
            args = [self.gid.split("/")[0], self.canvas, self.plot, self.parent()]

            match plot_type:
                case "2d line":                widget = Line(*args)
                case "2d step":                widget = Step(*args)
                case "2d stem":                widget = Stem(*args)
                case "2d area":                widget = Area(*args)
                case "fill between":           widget = Area(*args)
                case "2d stacked area":        widget = StackedArea(*args)
                case "2d 100% stacked area":   widget = StackedArea100(*args)
                case "2d scatter":             widget = Scatter(*args)
                case "2d bubble":              widget = Scatter(*args)
                case "2d column":              widget = Column(*args)
                case "dot":                    widget = Dot(*args)
                case "dumbbell":               widget = Dumbbell(*args)
                case "2d stacked column":      widget = Column(*args)
                case "stacked dot":            widget = Dot(*args)
                case "2d 100% stacked column": widget = Column(*args)
                case "2d clustered column":    widget = ClusteredColumn(*args)
                case "clustered dot":          widget = ClusteredDot(*args)
                case "marimekko":              widget = Marimekko(*args)
                case "treemap":                widget = Treemap(*args)
                case "pie":                    widget = Pie(*args)
                case "coxcomb":                widget = Coxcomb(*args)
                case "doughnut":               widget = Doughnut(*args)
                case "multilevel doughnut":    widget = MultilevelDoughnut(*args)
                case "semicircle doughnut":    widget = SemicircleDoughnut(*args)
                case "histogram":              widget = Histogram(*args)
                case "stacked histogram":      widget = Histogram(*args)
                case "boxplot":                widget = Boxplot(*args)
                case "violinplot":             widget = Violinplot(*args)
                case "eventplot":              widget = Eventplot(*args)
                case "hist2d":                 widget = Hist2d(*args)

                case "3d line":                widget = Line(*args)
                case "3d step":                widget = Step(*args)
                case "3d stem":                widget = Stem3d(*args)
                case "3d column":              widget = Column3D(*args)
                case "3d scatter":             widget = Scatter3D(*args)
                case "3d bubble":              widget = Scatter3D(*args)

            widget.sig.connect(self.update_plot)
            self.layout2.addWidget(widget)

        except Exception as e:
            logger.exception(e) 
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)