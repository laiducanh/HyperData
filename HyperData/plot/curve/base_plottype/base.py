from PySide6.QtWidgets import QWidget
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from ui.base_widgets.list import TreeWidget

class PlotConfigBase (QWidget):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, treeview:TreeWidget):
        super().__init__(treeview)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.treeview = treeview
        self.props = dict()

    def update_props(self):
        pass

    def update_plot(self):
        self.treeview.sig_onChange.emit()
        self.plot.plotting(**self.props)


