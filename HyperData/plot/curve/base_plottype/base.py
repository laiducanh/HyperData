from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPaintEvent
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.utilis import find_mpl_object
from plot.curve.base_elements.base import ArtistConfigBase
from matplotlib.artist import Artist

class PlotConfigBase(QWidget):
    onChange = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.props = dict()

        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
    
    def find_object (self) -> list[Artist]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Artist],
            gid=self.gid
        )

    def update_props(self):
        pass

    def update_plot(self):
        # self.onChange.emit()
        self.plot.plotting(**self.props)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        for obj in self.obj:
            if obj.stale:
                self.update_props()
                for widget in self.findChildren(ArtistConfigBase):
                    widget.update_props()
                self.canvas.draw_idle()   
                break 
        return super().paintEvent(a0)

