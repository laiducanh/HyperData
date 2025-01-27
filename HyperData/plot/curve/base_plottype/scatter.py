from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.button import Toggle
from matplotlib.collections import PathCollection
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import CmapCollection
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Scatter(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        super().initUI()

        self.sizes = SpinBox(min=1,max=1000,step=2,text="sizes")
        self.sizes.button.setValue(self.get_sizes())
        self.sizes.button.valueChanged.connect(self.set_sizes)
        self._layout.addWidget(self.sizes)

        self.collection = CmapCollection(self.gid, self.canvas, self.parent())
        self.collection.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.collection)

        self._layout.addStretch()
    
    def find_obj (self) -> list[PathCollection]:
        return find_mpl_object(
            figure=self.canvas.fig,
            match=[PathCollection],
            gid=self.gid
        )

    def update_prop(self):
        self.sizes.button.setValue(self.get_sizes())
    
    def set_sizes(self, value:int):
        try:
            self.props.update(sizes = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_sizes(self) -> int:
        return int(self.obj[0].sizes)
    
class Scatter3D (Scatter):
    def __init__(self, gid, canvas, plot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        super().initUI()

        self.depthshade = Toggle(text="Depth Shade")
        self.depthshade.button.setChecked(self.get_depthshade())
        self.depthshade.button.checkedChanged.connect(self.set_depthshade)
        self._layout.addWidget(self.depthshade)
    
    def update_prop(self):
        self.depthshade.button.setChecked(self.get_depthshade())
    
    def set_depthshade(self, value:bool):
        try:
            self.props.update(depthshade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_depthshade(self) -> bool:
        return self.obj[0].depthshade