from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from ui.base_widgets.spinbox import SpinBox
from ui.base_widgets.button import Toggle
from matplotlib.collections import PathCollection
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import CmapCollection
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Scatter(QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_obj()
        self.props = dict(sizes = 1)

        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.sizes = SpinBox(min=1,max=1000,step=2,text="sizes")
        self.sizes.button.setValue(self.get_sizes())
        self.sizes.button.valueChanged.connect(self.set_sizes)
        self._layout.addWidget(self.sizes)

        self.collection = CmapCollection(self.gid, self.canvas, self.parent())
        self.collection.sig.connect(self.sig.emit)
        self._layout.addWidget(self.collection)

        self._layout.addStretch()
    
    def find_obj (self) -> list[PathCollection]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[PathCollection],
                               gid=self.gid)

    def update_prop(self, button=None):
        if button != self.sizes.button:
            self.sizes.button.setValue(self.get_sizes())
        self.collection.update_props()
    
    def update_plot(self, *args, **kwargs):
        self.sig.emit()
        self.plot.plotting(**self.props)
        self.update_prop(*args, **kwargs)
    
    def set_sizes(self, value:int):
        try:
            self.props.update(sizes = value)
            self.update_plot(self.sizes.button)
        except Exception as e:
            logger.exception(e)
    
    def get_sizes(self) -> int:
        return int(self.obj[0].sizes)

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)
    
class Scatter3D (Scatter):
    def __init__(self, gid, canvas, plot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.props.update(depthshade = True)
    
    def initUI(self):
        super().initUI()

        self.depthshade = Toggle(text="Depth Shade")
        self.depthshade.button.setChecked(self.get_depthshade())
        self.depthshade.button.checkedChanged.connect(self.set_depthshade)
        self._layout.addWidget(self.depthshade)
    
    def update_prop(self, button=None):
        if button != self.depthshade.button:
            self.depthshade.button.setChecked(self.get_depthshade())
        return super().update_prop(button)
    
    def set_depthshade(self, value:bool):
        try:
            self.props.update(depthshade = value)
            self.update_plot(self.depthshade.button)
        except Exception as e:
            logger.exception(e)
    
    def get_depthshade(self) -> bool:
        return self.obj[0].depthshade