from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QDialog
from ui.base_widgets.frame import ScrollArea
from plot.canvas import Canvas
from plot.insert_plot.insert_plot import NewPlot
from plot.curve.base_plottype.line import Line, Step, Stem, Stem3d, Area, StackedArea, StackedArea100
from plot.curve.base_plottype.column import (Column, Column3D, Dot, ClusteredColumn, ClusteredDot, Dumbbell,
                                             Marimekko, Treemap, WaterFall)
from plot.curve.base_plottype.scatter import Scatter, Scatter3D
from plot.curve.base_plottype.pie import (Pie, Doughnut, Coxcomb, SemicircleDoughnut, MultilevelDoughnut,
                                          Radar)
from plot.curve.base_plottype.stats import (Histogram, Boxplot, Violinplot, Eventplot, Hist2d, 
                                            ErrorBar, Pareto, Andrews, CovEllipse)
from plot.curve.base_plottype.grid import Heatmap, Contour
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Curve(QDialog):
    sig = Signal() # fire signal when plot updated
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.setWindowTitle(self.plot.plot_type.title())
        self.initUI()
    
    def initUI(self):
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        try:
            plot_type = self.plot.plot_type
            args = [self.gid.split('/')[0], self.canvas, self.plot]

            if   plot_type == '2d line':                widget = Line(*args)
            elif plot_type == "2d step":                widget = Step(*args)
            elif plot_type == '2d stem':                widget = Stem(*args)
            elif plot_type == "2d area":                widget = Area(*args)
            elif plot_type == "fill between":           widget = Area(*args)
            elif plot_type == "2d stacked area":        widget = StackedArea(*args)
            elif plot_type == "2d 100% stacked area":   widget = StackedArea100(*args)
            elif plot_type == "2d scatter":             widget = Scatter(*args)
            elif plot_type == "2d bubble":              widget = Scatter(*args)
            elif plot_type == "2d column":              widget = Column(*args)
            elif plot_type == "dot":                    widget = Dot(*args)
            elif plot_type == "dumbbell":               widget = Dumbbell(*args)
            elif plot_type == "2d stacked column":      widget = Column(*args)
            elif plot_type == "stacked dot":            widget = Dot(*args)
            elif plot_type == "2d 100% stacked column": widget = Column(*args)
            elif plot_type == "2d clustered column":    widget = ClusteredColumn(*args)
            elif plot_type == "2d waterfall column":    widget = WaterFall(*args)
            elif plot_type == "clustered dot":          widget = ClusteredDot(*args)
            elif plot_type == "marimekko":              widget = Marimekko(*args)
            elif plot_type == "treemap":                widget = Treemap(*args)
            elif plot_type == "pie":                    widget = Pie(*args)
            elif plot_type == "coxcomb":                widget = Coxcomb(*args)
            elif plot_type == "doughnut":               widget = Doughnut(*args)
            elif plot_type == "multilevel doughnut":    widget = MultilevelDoughnut(*args)
            elif plot_type == "semicircle doughnut":    widget = SemicircleDoughnut(*args)
            elif plot_type == "radar":                  widget = Radar(*args)
            elif plot_type == "histogram":              widget = Histogram(*args)
            elif plot_type == "stacked histogram":      widget = Histogram(*args)
            elif plot_type == "boxplot":                widget = Boxplot(*args)
            elif plot_type == "violinplot":             widget = Violinplot(*args)
            elif plot_type == "eventplot":              widget = Eventplot(*args)
            elif plot_type == "hist2d":                 widget = Hist2d(*args)
            elif plot_type == "error bar":              widget = ErrorBar(*args)
            elif plot_type == "pareto":                 widget = Pareto(*args)
            elif plot_type == "andrews plot":           widget = Andrews(*args)
            elif plot_type == "covariance ellipse":     widget = CovEllipse(*args)
            elif plot_type == "heatmap":                widget = Heatmap(*args)
            elif plot_type == "contour":                widget = Contour(*args)

            elif plot_type == "3d line":                widget = Line(*args)
            elif plot_type == "3d step":                widget = Step(*args)
            elif plot_type == "3d stem":                widget = Stem3d(*args)
            elif plot_type == "3d column":              widget = Column3D(*args)
            elif plot_type == "3d scatter":             widget = Scatter3D(*args)
            elif plot_type == "3d bubble":              widget = Scatter3D(*args)

            widget.onChanged.connect(self.sig.emit)
            self.vlayout.addWidget(widget)

        except Exception as e:
            logger.exception(e)