from ui.base_widgets.line_edit import HLineEdit
from ui.base_widgets.spinbox import HTransparentDoubleSpinBox
from ui.base_widgets.button import HToggle
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.line import Line, Marker
from plot.curve.base_elements.patches import Wedge, MultiWedges, Polygon
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches

DEBUG = False

class Pie(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):   
        
        self.segment.addButton(text='Wedge', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.explode = HLineEdit(
            label="Explode",
            getter=self.get_explode,
            setter=self.set_explode,
            layout=self.general.addlayout
        )

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.radius = HTransparentDoubleSpinBox(
            label='Radius',
            getter=self.get_radius,
            setter=self.set_radius,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        self.counterclock = HToggle(
            label="Counterclock",
            getter=self.get_counterclock,
            setter=self.set_counterclock,
            layout=self.general.addlayout
        )

        self.rotatelabels = HToggle(
            label="Rotate Labels",
            getter=self.get_rotatelabels,
            setter=self.set_rotatelabels,
            layout=self.general.addlayout
        )

        self.normalize = HToggle(
            label="Normalize",
            getter=self.get_normalize,
            setter=self.set_normalize,
            layout=self.general.addlayout
        )

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(wedge)
    
    def find_object (self) -> list[patches.Wedge]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[patches.Wedge],
            gid=self.gid
        )

    def set_explode(self, value:str) -> None:
        try:
            if value == "": value = None
            else: value = [float(i) for i in value.split(",")]
            self.plot.props.update(explode = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_explode(self) -> str:
        if not self.plot.props["explode"]:
            return str()
        return str(self.plot.props["explode"])
    
    def set_labels(self, value:str) -> None:
        try:
            if value == "": value = None
            else: value = value.split(",")
            self.plot.props.update(labels = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_labels(self) -> str:
        if not self.plot.props["labels"]:
            return str()
        return str(self.plot.props["labels"])

    def get_radius(self) -> float:
        return self.find_object()[0].r
    
    def set_radius(self, value: float):
        try:
            self.plot.props.update(radius = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def set_startangle(self, value:float) -> None:
        try:
            self.plot.props.update(startangle = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_startangle(self) -> float:
        return float(self.plot.props["startangle"])
    
    def set_counterclock(self, value:bool) -> None:
        try:
            self.plot.props.update(counterclock = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_counterclock(self) -> bool:
        return self.plot.props["counterclock"]

    def set_rotatelabels(self, value:bool) -> None:
        try:
            self.plot.props.update(rotatelabels = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rotatelabels(self) -> bool:
        return self.plot.props["rotatelabels"]
    
    def set_normalize(self, value:bool) -> None:
        try:
            self.plot.props.update(normalize = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_normalize(self) -> bool:
        return self.plot.props["normalize"]

class Coxcomb(Pie):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):   

        self.segment.addButton(text='Wedge', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.explode = HLineEdit(
            label="Explode",
            getter=self.get_explode,
            setter=self.set_explode,
            layout=self.general.addlayout
        )

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        self.radius = HTransparentDoubleSpinBox(
            label = "Radius",
            singleStep = 0.2,
            getter=self.get_radius,
            setter=self.set_radius,
            layout=self.general.addlayout
        )

        self.counterclock = HToggle(
            label="Counterclock",
            getter=self.get_counterclock,
            setter=self.set_counterclock,
            layout=self.general.addlayout
        )

        self.rotatelabels = HToggle(
            label="Rotate Labels",
            getter=self.get_rotatelabels,
            setter=self.set_rotatelabels,
            layout=self.general.addlayout
        )

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(wedge)

class Doughnut(Pie):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        self.segment.addButton(text='Wedge', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.wedgewidth = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 1, singleStep = 0.1,
            label = "Width",
            getter=self.get_wedgewidth,
            setter=self.set_wedgewidth,
            layout=self.general.addlayout
        )

        self.explode = HLineEdit(
            label="Explode",
            getter=self.get_explode,
            setter=self.set_explode,
            layout=self.general.addlayout
        )

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        self.radius = HTransparentDoubleSpinBox(
            label = "Radius",
            singleStep = 0.2,
            getter=self.get_radius,
            setter=self.set_radius,
            layout=self.general.addlayout
        )

        self.counterclock = HToggle(
            label="Counterclock",
            getter=self.get_counterclock,
            setter=self.set_counterclock,
            layout=self.general.addlayout
        )

        self.rotatelabels = HToggle(
            label="Rotate Labels",
            getter=self.get_rotatelabels,
            setter=self.set_rotatelabels,
            layout=self.general.addlayout
        )

        self.normalize = HToggle(
            label="Normalize",
            getter=self.get_normalize,
            setter=self.set_normalize,
            layout=self.general.addlayout
        )

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(wedge)
    
    def set_wedgewidth(self, value:float):
        try:
            self.plot.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_wedgewidth(self) -> float:
        return self.plot.props["width"]

class SemicircleDoughnut(Doughnut):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        
        self.segment.addButton(text='Wedge', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.explode = HLineEdit(
            label="Explode",
            getter=self.get_explode,
            setter=self.set_explode,
            layout=self.general.addlayout
        )

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.radius = HTransparentDoubleSpinBox(
            label = "Radius",
            singleStep = 0.2,
            getter=self.get_radius,
            setter=self.set_radius,
            layout=self.general.addlayout
        )

        self.counterclock = HToggle(
            label="Counterclock",
            getter=self.get_counterclock,
            setter=self.set_counterclock,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        self.rotatelabels = HToggle(
            label="Rotate Labels",
            getter=self.get_rotatelabels,
            setter=self.set_rotatelabels,
            layout=self.general.addlayout
        )

        wedge = Wedge(self.gid, self.canvas)
        wedge.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(wedge)
    
class MultilevelDoughnut(Doughnut):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):

        self.segment.addButton(text='Wedge', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.wedgewidth = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 1, singleStep = 0.1,
            label = "Width",
            getter=self.get_wedgewidth,
            setter=self.set_wedgewidth,
            layout=self.general.addlayout
        )

        self.explode = HLineEdit(
            label="Explode",
            getter=self.get_explode,
            setter=self.set_explode,
            layout=self.general.addlayout
        )

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        self.radius = HTransparentDoubleSpinBox(
            label = "Radius",
            singleStep = 0.2,
            getter=self.get_radius,
            setter=self.set_radius,
            layout=self.general.addlayout
        )

        self.counterclock = HToggle(
            label="Counterclock",
            getter=self.get_counterclock,
            setter=self.set_counterclock,
            layout=self.general.addlayout
        )

        self.rotatelabels = HToggle(
            label="Rotate Labels",
            getter=self.get_rotatelabels,
            setter=self.set_rotatelabels,
            layout=self.general.addlayout
        )

        self.normalize = HToggle(
            label="Normalize",
            getter=self.get_normalize,
            setter=self.set_normalize,
            layout=self.general.addlayout
        )

        self.pad = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 1, singleStep = 0.01,
            label = "Padding",
            getter=self.get_pad,
            setter=self.set_pad,
            layout=self.general.addlayout
        )
        
        mw = MultiWedges(self.gid, self.canvas)
        mw.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(mw)
    
    def set_pad(self, pad:float):
        try:
            self.plot.props.update(pad=pad)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return self.plot.props["pad"]

class Radar(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):   
        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Marker', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Fill', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.setCurrentIndex(0)

        self.labels = HLineEdit(
            label="Labels",
            getter=self.get_labels,
            setter=self.set_labels,
            layout=self.general.addlayout
        )

        self.startangle = HTransparentDoubleSpinBox(
            minimum = 0, maximum = 360, singleStep = 30,
            label = "Start angle",
            getter=self.get_startangle,
            setter=self.set_startangle,
            layout=self.general.addlayout
        )

        line2d = Line(f'{self.gid}/line', self.canvas)
        line2d.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(line2d)

        marker = Marker(f'{self.gid}/line', self.canvas)
        marker.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(marker)

        fill = Polygon(f'{self.gid}/fill', self.canvas)
        fill.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(fill)

    def set_labels(self, value:str) -> None:
        try:
            if value == "": value = None
            else: value = value.split(",")
            self.plot.props.update(labels = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_labels(self) -> str:
        if not self.plot.props["labels"]:
            return str()
        return str(self.plot.props["labels"])

    def set_startangle(self, value:float) -> None:
        try:
            self.plot.props.update(startangle = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_startangle(self) -> float:
        return float(self.plot.props["startangle"])