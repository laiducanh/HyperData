from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.button import HToggle
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

        self.segment.addButton(text='Scatter', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.sizes = HTransparentSpinBox(
            minimum = 1, maximum = 1000, singleStep = 2,
            label = "sizes",
            getter=self.get_sizes,
            setter=self.set_sizes,
            layout=self.general.addlayout
        )

        collection = CmapCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)
    
    def find_obj (self) -> list[PathCollection]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[PathCollection],
            gid=self.gid
        )

    def update_prop(self):
        self.sizes.button.setValue(self.get_sizes())
    
    def set_sizes(self, value:int):
        try:
            self.plot.props.update(sizes = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_sizes(self) -> int:
        return int(self.plot.props["sizes"])

class Scatter3D (Scatter):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        self.segment.addButton(text='Scatter', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.depthshade = HToggle(
            label="Depth Shade",
            getter=self.get_depthshade,
            setter=self.set_depthshade,
            layout=self.general.addlayout
        )

        self.sizes = HTransparentSpinBox(
            minimum = 1, maximum = 1000, singleStep = 2,
            label = "sizes",
            getter=self.get_sizes,
            setter=self.set_sizes,
            layout=self.general.addlayout
        )

        collection = CmapCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)
    
    def set_depthshade(self, value:bool):
        try:
            self.plot.props.update(depthshade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_depthshade(self) -> bool:
        return self.plot.props["depthshade"]