from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.button import Toggle
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from matplotlib.collections import PathCollection
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import CmapCollection
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Scatter (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Scatter'))
        layout.addWidget(SeparateHLine())

        self.sizes = SpinBox(
            min  = 1,
            max  = 1000,
            step = 2,
            text = "sizes"
        )
        self.sizes.button.setValue(self.get_sizes())
        self.sizes.button.valueChanged.connect(self.set_sizes)
        layout.addWidget(self.sizes)

        collection = CmapCollection(self.gid, self.canvas)
        collection.onChanged.connect(self.onChanged.emit)
        layout.addWidget(collection)
    
    def find_obj (self) -> list[PathCollection]:
        return find_mpl_object(
            source=self.canvas.fig,
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
        return int(self.find_obj()[0].sizes)

class Scatter3D (Scatter):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('3D Scatter'))
        layout.addWidget(SeparateHLine())

        self.depthshade = Toggle(text="Depth Shade")
        self.depthshade.button.setChecked(self.get_depthshade())
        self.depthshade.button.checkedChanged.connect(self.set_depthshade)
        layout.addWidget(self.depthshade)

        self.sizes = SpinBox(
            min  = 1,
            max  = 1000,
            step = 2,
            text = "sizes"
        )
        self.sizes.button.setValue(self.get_sizes())
        self.sizes.button.valueChanged.connect(self.set_sizes)
        layout.addWidget(self.sizes)

        collection = CmapCollection(self.gid, self.canvas)
        collection.onChanged.connect(self.onChanged.emit)
        layout.addWidget(collection)
    
    def set_depthshade(self, value:bool):
        try:
            self.props.update(depthshade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_depthshade(self) -> bool:
        return self.find_obj()[0].depthshade