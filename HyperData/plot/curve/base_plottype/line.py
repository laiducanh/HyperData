from plot.curve.base_elements import line
from ui.base_widgets.button import HTransparentComboBox
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
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
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.setCurrentIndex(0)

        line2d = line.Line(gid, canvas, parent)
        line2d.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line2d)

        marker = line.Marker(gid, canvas, parent)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)

class Step (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
        
        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.setCurrentIndex(0)

        self.where = HTransparentComboBox(
            items=['pre', 'post', 'mid'], 
            label="Where",
            getter=self.get_where,
            setter=self.set_where,
            layout=self.general.addlayout
        )

        line2d = line.Line(gid, canvas, parent)
        line2d.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line2d)
        
        marker = line.Marker(gid, canvas, parent)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)

    def find_object (self) -> list[lines.Line2D]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[lines.Line2D],
            gid=self.gid,
        )

    def set_where (self, value:str):
        try:
            self.plot.props.update(where = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_where (self) -> str:
        return self.plot.props["where"]

class Stem (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):

        self.segment.addButton(text='Stemline', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Baseline', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.setCurrentIndex(0)

        self.stemline = line.LineCollection(f"{self.gid}/stemlines", self.canvas)
        self.stemline.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(self.stemline)

        self.orientation = HTransparentComboBox(
            items = ["vertical","horizontal"],
            label = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
        )
        self.stemline.vlayout.insertWidget(0, self.orientation)

        line2d = line.Line(f"{self.gid}/baseline", self.canvas)
        line2d.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line2d)

        self.bottom = HTransparentDoubleSpinBox(
            label="Bottom",
            getter=self.get_bottom,
            setter=self.set_bottom,
        )
        line2d.vlayout.insertWidget(0, self.bottom)

        marker = line.Marker(f"{self.gid}/markerline", self.canvas)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)
    
    def find_object(self):
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[lines.Line2D, collections.LineCollection],
            gid=self.gid
        )

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom(self, value:float):
        try:
            self.plot.props.update(bottom = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom(self) -> float:
        return self.plot.props["bottom"]

class Stem3d (Stem):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
        self.plot.props.update(orientation = "z")
        self.orientation.button.blockSignals(True)
        self.orientation.button.clear()
        self.orientation.button.addItems(["x","y","z"])
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.blockSignals(False)

class Area (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):
       
        self.segment.addButton(text='Area', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)

        self.step = HTransparentComboBox(
            label='Step',
            items=['pre','post','mid','none'],
            getter=self.get_step,
            setter=self.set_step,
            layout=self.general.addlayout
        )

        self.orientation = HTransparentComboBox(
            items=["vertical","horizontal"],
            label="Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.plot.props.update(step = value.lower())
            if value == "none": self.plot.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        if self.plot.props["step"]:
            return self.plot.props["step"]
        else: return 'none'

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
class StackedArea (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):
        
        self.segment.addButton(text='Area', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)

        self.baseline = HTransparentComboBox(
            label = 'Baseline',
            items = ['zero','sym','wiggle','weighted_wiggle'],
            setter=self.set_baseline,
            getter=self.get_baseline,
            layout=self.general.addlayout
        )

        self.step = HTransparentComboBox(
            label = 'Step',
            items = ['pre','post','mid','none'],
            getter=self.get_step,
            setter=self.set_step,
            layout=self.general.addlayout
        )

    def find_obj (self) -> list[Collection]:
        return find_mpl_object(
            figure=self.canvas.figure,
            match=[Collection],
            gid=self.gid
        )
    
    def set_step(self, value:str):
        try:
            self.plot.props.update(step = value.lower())
            if value == "none": self.plot.props.update(step = None)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_step(self) -> str:
        if self.plot.props["step"]:
            return self.plot.props["step"]
        else: return 'none'

    def set_baseline(self, value:str):
        try:
            self.plot.props.update(baseline = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_baseline(self) -> str:
        return self.plot.props["baseline"]

class StackedArea100 (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()

    def initUI(self):

        self.segment.addButton(text='Area', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        collection = SingleColorCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)