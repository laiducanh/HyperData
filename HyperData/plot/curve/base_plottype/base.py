from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout
from PySide6.QtCore import Signal
from plot.insert_plot.insert_plot import InsertPlot
from plot.canvas import Canvas
from ui.base_widgets.button import SegmentedWidget, TransparentComboBox, Toggle
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from plot.utilis import find_mpl_object
from matplotlib import artist

AXES = 0
AXES_Y2 = 1
AXES_X2 = 2
AXES_PIE = 3

class PlotConfigBase (QWidget):
    onChanged = Signal()
    def __init__(self, gid:str, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.props = dict()

        self.vlayout = QVBoxLayout(self)
        self.vlayout.setContentsMargins(0,0,0,0)
        self.segment = SegmentedWidget(parent)
        self.vlayout.addWidget(self.segment)

        self.stackedlayout = QStackedLayout()
        self.vlayout.addLayout(self.stackedlayout)

    def update_props(self):
        pass

    def update_plot(self):
        self.onChanged.emit()
        self.plot.plotting(**self.props)

class AxesPlot(QWidget):
    def __init__(self, gid:str, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.props = dict()
        self.ax = self.canvas.fig.axes.index(self.find_obj()[0].axes)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.choose_axis1 = TransparentComboBox(
            text="Horizontal Axis",
            items=["Bottom","Top"],
            setter=self.set_ax,
            getter=lambda: self.get_ax()[0],
            layout=layout
        )
        
        self.choose_axis2 = TransparentComboBox(
            text="Vertical Axis",
            items=["Left","Right"],
            setter=self.set_ax,
            getter=lambda: self.get_ax()[1],
            layout=layout
        )

        layout.addWidget(SeparateHLine())

        clip = Toggle(
            text="Clipping",
            setter=self.set_clip,
            getter=self.get_clip,
            layout=layout
        )
    
    def get_ax(self):
        if self.ax == AXES:
            return ["Bottom","Left"]
        elif self.ax == AXES_X2:
            return ["Top","Left"]
        elif self.ax == AXES_Y2:
            return ["Bottom","Right"]
    
    def set_ax(self):
        _ax1 = self.choose_axis1.button.currentText()
        _ax2 = self.choose_axis2.button.currentText()
        if _ax1 == "Bottom" and _ax2 == "Left":
            self.plot.plotting(_ax=AXES)
    
    def find_obj(self):
        return find_mpl_object(
            source=self.canvas.fig,
            match=[artist.Artist],
            gid=self.gid,
        )

    def set_clip(self, bool):
        for obj in self.find_obj():
            obj.set_clip_on(bool)
    
    def get_clip(self) -> bool:
        return self.find_obj()[0].get_clip_on()