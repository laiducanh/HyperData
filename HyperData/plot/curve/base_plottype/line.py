from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from plot.curve.base_elements.line import Line2D, LineCollection, Marker
from plot.curve.base_elements.line import Line as LineBase
from ui.base_widgets.button import Toggle, ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from matplotlib.collections import Collection
from matplotlib import lines, collections
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import SingleColorCollection
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Line (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
        
    def initUI(self):
        super().initUI()

        self.line = Line2D(self.gid, self.canvas, self.parent())
        self.line.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.line)

        self._layout.addStretch()
    
    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D],
            gid=self.gid
        )
 
class Step (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        super().initUI()

        self.where = ComboBox(items=['pre', 'post', 'mid'], text="Where")
        self.where.button.setCurrentText(self.get_where())
        self.where.button.currentTextChanged.connect(self.set_where)
        self._layout.addWidget(self.where)
        self.line = Line2D(self.gid, self.canvas, self.parent())
        self.line.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.line)

        self._layout.addStretch()
    
    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D],
            gid=self.gid,
        )
    
    def update_props(self):
        self.where.button.setCurrentText(self.get_where())

    def set_where (self, value:str):
        try:
            self.props.update(where = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_where (self) -> str:
        return self.obj[0].where

class Stem(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        super().initUI()
        
        self.choose_component = SegmentedWidget()
        self._layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Stemline', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Baseline', func=lambda: self.stackedlayout.setCurrentIndex(1))

        self.stackedlayout = QStackedLayout()
        self._layout.addLayout(self.stackedlayout)
        self.choose_component.setCurrentWidget("Stemline")

        stemline = QWidget()
        layout_stemline = QVBoxLayout()
        layout_stemline.setContentsMargins(0,0,0,0)
        stemline.setLayout(layout_stemline)
        self.stackedlayout.addWidget(stemline)
        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout_stemline.addWidget(self.orientation)
        self.stemline = LineCollection(f"{self.gid}/stemlines", self.canvas)
        self.stemline.onChange.connect(self.sig.emit)
        layout_stemline.addWidget(self.stemline)
        self.markerline = Marker(f"{self.gid}/markerline", self.canvas)
        self.markerline.onChange.connect(self.sig.emit)
        layout_stemline.addWidget(self.markerline)

        baseline = QWidget()
        layout_baseline = QVBoxLayout()
        layout_baseline.setContentsMargins(0,0,0,0)
        baseline.setLayout(layout_baseline)
        self.stackedlayout.addWidget(baseline)
        self.bottom = DoubleSpinBox(text="Bottom")
        self.bottom.button.setValue(self.get_bottom())
        self.bottom.button.valueChanged.connect(self.set_bottom)
        layout_baseline.addWidget(self.bottom)
        self.baseline = LineBase(f"{self.gid}/baseline", self.canvas)
        self.baseline.onChange.connect(self.sig.emit)
        layout_baseline.addWidget(self.baseline)

    def find_object(self):
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D, collections.LineCollection],
            gid=self.gid
        )

    def update_props(self):
        self.orientation.button.setCurrentText(self.get_orientation())
        self.bottom.button.setValue(self.get_bottom())

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom(self, value:float):
        try:
            self.props.update(bottom = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom(self) -> float:
        return self.obj[0].bottom

class Stem3d (Stem):
    def __init__(self, gid, canvas, plot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.props.update(orientation = "z")
        self.orientation.button.blockSignals(True)
        self.orientation.button.clear()
        self.orientation.button.addItems(["x","y","z"])
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.blockSignals(False)

class Spline2d(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas, plot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        num = SpinBox(min=10, max=10000, step=100, text="Number of points")
        num.button.setValue(self.get_num())
        num.button.valueChanged.connect(self.set_num)
        self._layout.addWidget(num)

        order = SpinBox(min=1, text="B-spline degree")
        order.button.setValue(self.get_order())
        order.button.valueChanged.connect(self.set_order)
        self._layout.addWidget(order)

        bc_type = ComboBox(items=["clamped","natural","not-a-knot","periodic"], text="Boundary condition")
        bc_type.button.setCurrentText(self.get_bctype())
        bc_type.button.currentTextChanged.connect(self.set_bctype)
        self._layout.addWidget(bc_type)

        line = LineBase(f"{self.gid}/interp", self.canvas)
        line.onChange.connect(self.sig.emit)
        self._layout.addWidget(line)

        marker = Marker(f"{self.gid}/points", self.canvas)
        marker.onChange.connect(self.sig.emit)
        self._layout.addWidget(marker)
    
    def set_num(self, value:int):
        try:
            self.props.update(num = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_num(self) -> int:
        return self.obj[0].num

    def set_order(self, value:int):
        try:
            self.props.update(order = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_order(self):
        return self.obj[0].order
    
    def set_bctype(self, value:str):
        try:
            self.props.update(bc_type = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bctype(self) -> str:
        return self.obj[0].bc_type

class Area (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        super().initUI()

        self.step = ComboBox(text='Step',items=['pre','post','mid','none'])
        self.step.button.setCurrentText(self.get_step())
        self.step.button.currentTextChanged.connect(self.set_step)
        self._layout.addWidget(self.step)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self._layout.addSpacing(10)

        self.patch = SingleColorCollection(self.gid, self.canvas, self.parent())
        self.patch.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.patch)
        
        self._layout.addStretch()

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Collection],
            gid=self.gid
        )
    
    def update_props(self):
        self.step.button.setCurrentText(self.get_step())
        self.orientation.button.setCurrentText(self.get_orientation())
    
    def set_step(self, value:str):
        try:
            self.props.update(step = value.lower())
            if value == "none": self.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.obj[0].step

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
class StackedArea(Area):
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.baseline = ComboBox(text='Baseline',items=['zero','sym','wiggle','weighted_wiggle'])
        self.baseline.button.setCurrentText(self.get_baseline())
        self.baseline.button.currentTextChanged.connect(self.set_baseline)
        self._layout.addWidget(self.baseline)

        self.step = ComboBox(text='Step',items=['pre','post','mid','none'])
        self.step.button.setCurrentText(self.get_step())
        self.step.button.currentTextChanged.connect(self.set_step)
        self._layout.addWidget(self.step)

        self._layout.addSpacing(10)

        self.patch = SingleColorCollection(self.gid, self.canvas, self.parent())
        self.patch.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.patch)
        
        self._layout.addStretch()
        
    def set_baseline(self, value:str):
        try:
            self.props.update(baseline = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_baseline(self) -> str:
        return self.obj[0].baseline

    def update_props(self):
        self.step.button.setCurrentText(self.get_step())
        self.baseline.button.setCurrentText(self.get_baseline())

class StackedArea100 (Area):
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.patch = SingleColorCollection(self.gid, self.canvas, self.parent())
        self.patch.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.patch)
        
        self._layout.addStretch()