from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.spinbox import HTransparentSpinBox
from ui.base_widgets.button import HTransparentComboBox, HToggle
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import QuadMesh
from plot.curve.base_elements.line import Line
from plot.utilis import find_mpl_object
from plot.curve.base_plottype.base import PlotConfigBase
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import collections
from matplotlib.pyplot import colormaps
import matplotlib

DEBUG = False

class Heatmap (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Mesh', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        qm = QuadMesh(self.gid, self.canvas)
        qm.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(qm)

class Contour (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)
        
        self.fillmesh = HToggle(
            label="Fill Color",
            getter=self.get_fillmesh,
            setter=self.set_fillmesh,
            layout=self.general.addlayout
        )

        self.cmap = HTransparentComboBox(
            items = colormaps(), 
            label  = "Colormap",
            getter=self.get_cmap,
            setter=self.set_cmap,
            layout=self.general.addlayout
        )

        self.norm = HTransparentComboBox(
            items = ['linear', 'log', 'logit', 'symlog','asinh'], 
            label = "Norm",
            getter=self.get_norm,
            setter=self.set_norm,
            layout=self.general.addlayout
        )

        self.alpha = HTransparentSpinBox(
            label = 'Transparency',
            minimum = 0, maximum = 100, singleStep = 10,
            getter=self.get_alpha,
            setter=self.set_alpha,
            layout=self.general.addlayout
        )

        line = Line(self.gid, self.canvas)
        line.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line)

    def find_object(self) -> list[collections.QuadMesh]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[collections.QuadMesh],
            gid=self.gid,
        )

    def set_fillmesh(self, value:bool):
        try:
            self.plot.props.update(fill = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_fillmesh(self) -> bool:
        try: return self.plot.props["fill"]
        except: return False
    
    def set_cmap (self, value:str):
        try:
            self.plot.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap(self) -> str:
        try:
            return self.plot.props["cmap"].name
        except: return matplotlib.rcParams["image.cmap"]
    
    def set_norm(self, value:str):
        try:
            self.plot.props.update(norm = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_norm(self) -> str:
        try: return self.plot.props["norm"]
        except: return "linear"
    
    def set_alpha(self, value: float):
        try:
            for obj in self.find_object():
                obj.set_alpha(value/100)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        try:
            if self.find_object()[0].get_alpha() != None:
                return int(self.find_object()[0].get_alpha()*100)
            return 100
        except: return 100
