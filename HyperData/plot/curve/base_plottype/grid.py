from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.collection import QuadMesh
from plot.curve.base_elements.line import Marker, Line, LineCollection
from plot.utilis import find_mpl_object
from plot.curve.base_plottype.base import PlotConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from matplotlib import patches, colors, lines, collections
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as Poly3D
import numpy as np
import matplotlib

DEBUG = False

class Heatmap (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.quadmesh = QuadMesh(self.gid, self.canvas)
        self.quadmesh.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.quadmesh)

class Contour(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas, plot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.fillmesh = Toggle(text="Fill Color")
        self.fillmesh.button.setChecked(self.get_fillmesh())
        self.fillmesh.button.checkedChanged.connect(self.set_fillmesh)
        self._layout.addWidget(self.fillmesh)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        self._layout.addWidget(self.cmap)

        self.norm = ComboBox(items=['linear', 'log', 'logit', 'symlog','asinh'], text="Norm")
        self.norm.button.setCurrentText(self.get_norm())
        self.norm.button.currentTextChanged.connect(self.set_norm)
        self._layout.addWidget(self.norm)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self._layout.addWidget(self.alpha)

        self.line = Line(self.gid, self.canvas)
        self.line.color.hide()
        self.line.onChange.connect(self.update_plot)
        self._layout.addWidget(self.line)
    
    def find_object(self) -> list[collections.QuadMesh]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.QuadMesh],
            gid=self.gid,
        )

    def set_fillmesh(self, value:bool):
        try:
            self.props.update(fill = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_fillmesh(self) -> bool:
        try: return self.obj[0].fill
        except: return False
    
    def set_cmap (self, value:str):
        try:
            self.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap(self) -> str:
        try:
            return self.obj[0].cmap.name
        except: return matplotlib.rcParams["image.cmap"]
    
    def set_norm(self, value:str):
        try:
            self.props.update(norm = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_norm(self) -> str:
        try: return self.obj[0].norm_
        except: return "linear"
    
    def set_alpha(self, value: float):
        try:
            for obj in self.obj:
                obj.set_alpha(value/100)
            self.canvas.draw_idle()
        except Exception as e:
            logger.exception(e)
    
    def get_alpha (self):
        try:
            if self.obj[0].get_alpha() != None:
                return int(self.obj[0].get_alpha()*100)
            return 100
        except: return 100

    
