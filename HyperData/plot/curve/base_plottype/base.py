from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas

class PlotConfigBase (QWidget):
    onChanged = Signal()
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.props = dict()

    def update_props(self):
        pass

    def update_plot(self):
        self.onChanged.emit()
        self.plot.plotting(**self.props)


