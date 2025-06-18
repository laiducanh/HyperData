from PySide6.QtWidgets import QVBoxLayout
from plot.curve.base_elements import line
from ui.base_widgets.button import TransparentComboBox
from ui.base_widgets.spinbox import TransparentDoubleSpinBox
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from matplotlib.collections import Collection
from matplotlib import lines, collections
from plot.insert_plot.insert_plot import InsertPlot
from plot.canvas import Canvas
from plot.curve.base_elements.collection import SingleColorCollection
from plot.curve.base_plottype.base import PlotConfigBase, AxesPlot
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger

DEBUG = False

class Line (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.segment.addButton(text='General', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.segment.addButton(text='Line 2D', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.setCurrentIndex(0)

        axesplot = AxesPlot(gid, canvas, plot, parent)
        self.stackedlayout.addWidget(axesplot)

        line2d = line.Line(gid, canvas, parent)
        line2d.onChanged.connect(self.onChanged.emit)
        self.stackedlayout.addWidget(line2d)

        marker = line.Marker(gid, canvas, parent)
        marker.onChanged.connect(self.onChanged.emit)
        self.stackedlayout.addWidget(marker)

class Step (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Step'))
        layout.addWidget(SeparateHLine())

        self.where = TransparentComboBox(
            items=['pre', 'post', 'mid'], 
            text="Where",
            getter=self.get_where,
            setter=self.set_where,
            layout=layout
        )

        layout.addWidget(TitleLabel('Line 2D'))
        layout.addWidget(SeparateHLine())
        line2d = line.Line(gid, canvas, parent)
        line2d.onChanged.connect(self.onChanged.emit)
        layout.addWidget(line2d)

        layout.addWidget(TitleLabel('Marker'))
        layout.addWidget(SeparateHLine())
        marker = line.Marker(gid, canvas, parent)
        marker.onChanged.connect(self.onChanged.emit)
        layout.addWidget(marker)

    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D],
            gid=self.gid,
        )

    def set_where (self, value:str):
        try:
            self.props.update(where = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_where (self) -> str:
        return self.find_object()[0].where

class Stem (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Stemline'))
        layout.addWidget(SeparateHLine())

        self.orientation = TransparentComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=layout
        )

        self.bottom = TransparentDoubleSpinBox(
            text="Bottom",
            getter=self.get_bottom,
            setter=self.set_bottom,
            layout=layout
        )

        self.stemline = line.LineCollection(f"{self.gid}/stemlines", self.canvas)
        self.stemline.onChanged.connect(self.onChanged.emit)
        layout.addWidget(self.stemline)

        layout.addWidget(TitleLabel('Marker'))
        layout.addWidget(SeparateHLine())
        marker = line.Marker(f"{self.gid}/markerline", self.canvas)
        marker.onChanged.connect(self.onChanged.emit)
        layout.addWidget(marker)

        layout.addWidget(TitleLabel('Baseline'))
        layout.addWidget(SeparateHLine())
        line2d = line.Line(f"{self.gid}/baseline", self.canvas)
        line2d.onChanged.connect(self.onChanged.emit)
        layout.addWidget(line2d)
    
    def find_object(self):
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D, collections.LineCollection],
            gid=self.gid
        )

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation
    
    def set_bottom(self, value:float):
        try:
            self.props.update(bottom = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom(self) -> float:
        return self.find_object()[0].bottom

class Stem3d (Stem):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
        self.props.update(orientation = "z")
        self.orientation.button.blockSignals(True)
        self.orientation.button.clear()
        self.orientation.button.addItems(["x","y","z"])
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.blockSignals(False)

class Area (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):
       
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        
        layout.addWidget(TitleLabel('Area'))
        layout.addWidget(SeparateHLine())

        self.step = TransparentComboBox(
            text='Step',
            items=['pre','post','mid','none'],
            getter=self.get_step,
            setter=self.set_step,
            layout=layout
        )

        self.orientation = TransparentComboBox(
            items=["vertical","horizontal"],
            text="Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=layout
        )

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(collection.onChanged.emit)
        layout.addWidget(collection)

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.props.update(step = value.lower())
            if value == "none": self.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.find_obj()[0].step

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_obj()[0].orientation
    
class StackedArea (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Stacked Area'))
        layout.addWidget(SeparateHLine())

        self.baseline = TransparentComboBox(
            text  = 'Baseline',
            items = ['zero','sym','wiggle','weighted_wiggle'],
            setter=self.set_baseline,
            getter=self.get_baseline,
            layout=layout
        )

        self.step = TransparentComboBox(
            text  = 'Step',
            items = ['pre','post','mid','none'],
            getter=self.get_step,
            setter=self.set_step,
            layout=layout
        )

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(collection.onChanged.emit)
        layout.addWidget(collection)
    
    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.props.update(step = value.lower())
            if value == "none": self.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        return self.find_obj()[0].step

    def set_baseline(self, value:str):
        try:
            self.props.update(baseline = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_baseline(self) -> str:
        return self.find_obj()[0].baseline

class StackedArea100 (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:InsertPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('100% Stacked Area'))
        layout.addWidget(SeparateHLine())

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(collection.onChanged.emit)
        layout.addWidget(collection)