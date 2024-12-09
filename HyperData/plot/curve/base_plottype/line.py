from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from plot.curve.base_elements.line import Line2D, LineCollection, Marker
from plot.curve.base_elements.line import Line as LineBase
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.button import Toggle, ComboBox, SegmentedWidget
from ui.base_widgets.spinbox import DoubleSpinBox
from matplotlib.collections import Collection
from matplotlib import lines, collections
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import SingleColorCollection
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from typing import List

DEBUG = False

class Line (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.setParent(parent)
        self.plot = plot

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.line = Line2D(self.gid, self.canvas, self.parent())
        self.line.sig.connect(self.sig.emit)
        self._layout.addWidget(self.line)

        self._layout.addStretch()
 
class Step (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.setParent(parent)
        self.plot = plot
        self.obj = self.find_object()
        self.props = dict(where = "pre")

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.where = ComboBox(items=['pre', 'post', 'mid'], text="Where")
        self.where.button.setCurrentText(self.get_where())
        self.where.button.currentTextChanged.connect(self.set_where)
        self._layout.addWidget(self.where)
        self.line = Line2D(self.gid, self.canvas, self.parent())
        self.line.sig.connect(self.sig.emit)
        self._layout.addWidget(self.line)

        self._layout.addStretch()
    
    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[lines.Line2D],
                               gid=self.gid)

    def update_plot(self, *args, **kwargs):
        self.sig.emit()
        self.plot.plotting(**self.props)
        self.update_props(*args, **kwargs)
    
    def update_props(self, button=None):
        if button != self.where.button:
            self.where.button.setCurrentText(self.get_where())
        self.line.update_props()

    def set_where (self, value:str):
        try:
            self.props.update(where = value)
        except Exception as e:
            logger.exception(e)
        self.update_plot(self.where.button)
    
    def get_where (self) -> str:
        return self.obj[0].where
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class Stem(QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.setParent(parent)
        self.plot = plot
        self.obj = self.find_object()
        self.props = dict(
            orientation = "vertical",
            bottom = 0
        )

        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        
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
        self.stemline.sig.connect(self.sig.emit)
        layout_stemline.addWidget(self.stemline)
        self.markerline = Marker(f"{self.gid}/markerline", self.canvas)
        self.markerline.sig.connect(self.sig.emit)
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
        self.baseline.sig.connect(self.sig.emit)
        layout_baseline.addWidget(self.baseline)

    def find_object(self):
        return find_mpl_object(figure=self.canvas.fig,
                               match=[lines.Line2D, collections.LineCollection],
                               gid=self.gid)

    def update_plot(self, *args, **kwargs):
        self.sig.emit()
        self.plot.plotting(**self.props)
        self.update_props(*args, **kwargs)
    
    def update_props(self, button=None):
        if button != self.orientation.button:
            self.orientation.button.setCurrentText(self.get_orientation())
        if button != self.bottom.button:
            self.bottom.button.setValue(self.get_bottom())

        self.stemline.update_props()
        self.markerline.update_props()
        self.baseline.update_props()

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot(self.orientation.button)
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom(self, value:float):
        try:
            self.props.update(bottom = value)
            self.update_plot(self.bottom.button)
        except Exception as e:
            logger.exception(e)
    
    def get_bottom(self) -> float:
        return self.obj[0].bottom

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class Stem3d (Stem):
    def __init__(self, gid, canvas, plot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.props.update(orientation = "z")
        self.orientation.button.blockSignals(True)
        self.orientation.button.clear()
        self.orientation.button.addItems(["x","y","z"])
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.blockSignals(False)

class Area (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)
        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_obj()
        self.plot = plot
        self.prop = dict(step=None)

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel('Area'))
        self._layout.addWidget(SeparateHLine())

        self.step = ComboBox(text='Step',items=['pre','post','mid','none'])
        self.step.button.setCurrentText(self.get_step())
        self.step.button.currentTextChanged.connect(self.set_step)
        self._layout.addWidget(self.step)

        self._layout.addSpacing(10)

        self.patch = SingleColorCollection(self.gid, self.canvas, self.parent())
        self.patch.sig.connect(self.update_plot)
        self._layout.addWidget(self.patch)
        
        self._layout.addStretch()

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[Collection],
                               gid=self.gid)
    
    def update_plot(self, *args, **kwargs):
        self.sig.emit()
        self.plot.plotting(**self.prop)
        self.update_props(*args, **kwargs)  
    
    def update_props(self, button=None):
        if button != self.step.button:
            self.step.button.setCurrentText(self.get_step())
        self.patch.update_props()
    
    def set_step(self, value:str):
        try:
            self.prop.update(step = value.lower())
            if value == "none": self.prop.update(step = None)
            self.update_plot(self.step.button)
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.obj[0].step

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_obj()
        return super().paintEvent(a0)
    
class StackedArea(QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_obj()
        self.plot = plot
        self.step = None
        self.baseline = "zero"

        self._layout.addWidget(TitleLabel('Stacked Area'))
        self._layout.addWidget(SeparateHLine())

        base = ComboBox(text='baseline',items=['zero','sym','wiggle','weighted_wiggle'])
        base.button.currentTextChanged.connect(self.set_baseline)
        base.button.setCurrentText(self.get_baseline())
        self._layout.addWidget(base)

        step = ComboBox(text='Step',items=['pre','post','mid','none'])
        step.button.currentTextChanged.connect(self.set_step)
        step.button.setCurrentText(self.get_step())
        self._layout.addWidget(step)

        self._layout.addSpacing(10)

        patch = SingleColorCollection(gid, canvas, parent)
        patch.sig.connect(self.update_plot)
        self._layout.addWidget(patch)
        
        self._layout.addStretch()

    def find_obj(self):
        found = find_mpl_object(figure=self.canvas.fig,
                               match=[Collection],
                               gid=self.gid)
        return found[0]
    
    def update_plot(self, **kwargs):
        self.plot.plotting(step=self.step,
                           baseline=self.baseline,**kwargs)
        
        self.sig.emit()
    
    def set_step(self, value:str):
        self.step = value.lower()
        if self.step == 'none': self.step = None
        self.update_plot()
    
    def get_step(self) -> str:
        return self.obj.step

    def set_baseline(self, value:str):
        self.baseline = value.lower()
        self.update_plot(baseline=self.baseline)
    
    def get_baseline(self) -> str:
        return self.obj.baseline

class StackedArea100 (QWidget):
    sig = pyqtSignal()
    def __init__(self, gid, canvas: Canvas, plot:NewPlot, parent=None):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)
        self.gid = gid
        self.canvas = canvas
        self.obj = self.find_obj()
        self.plot = plot

        patch = SingleColorCollection(gid, canvas, parent)
        patch.sig.connect(self.update_plot)
        self._layout.addWidget(patch)
        
        self._layout.addStretch()

    def find_obj(self):
        found = find_mpl_object(figure=self.canvas.fig,
                               match=[Collection],
                               gid=self.gid)
        return found[0]
    
    def update_plot(self, **kwargs):
        self.plot.plotting(**kwargs)
        self.sig.emit()