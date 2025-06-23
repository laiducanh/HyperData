from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QWidget
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import TransparentDoubleSpinBox, TransparentSpinBox
from ui.base_widgets.button import TransparentComboBox, Toggle, SegmentedWidget
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.frame import SeparateHLine
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.line import LineCollection, Line, Marker, ErrorBarCollection
from plot.curve.base_elements.collection import SingleColorCollection, QuadMesh
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches, lines, collections
from typing import Union

DEBUG = False

class Histogram(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Rectangle', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.bins = TransparentSpinBox(
            text="Bins",
            min=1, 
            getter=self.get_bins,
            setter=self.set_bins,
            layout=self.general.addlayout
        )

        self.density = Toggle(
            text="Density",
            getter=self.get_density,
            setter=self.set_density,
            layout=self.general.addlayout
        )

        self.cumulative = Toggle(
            text="Cumulative",
            getter=self.get_cumulative,
            setter=self.set_cumulative,
            layout=self.general.addlayout
        )

        self.bottom = LineEdit(
            text="Bottom",
            getter=self.get_bottom,
            layout=self.general.addlayout
        )
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))

        # self.histtype = ComboBox(
        #     items = ['bar', 'barstacked', 'step', 'stepfilled'],
        #     text  = "Histtype"
        # )
        # self.histtype.button.setCurrentText(self.get_histtype())
        # self.histtype.button.currentTextChanged.connect(self.set_histtype)
        # self._layout.addWidget(self.histtype)

        self.align = TransparentComboBox(
            items = ["left","mid","right"],
            text  = "Alignment",
            getter=self.get_alignment,
            setter=self.set_alignment,
            layout=self.general.addlayout
        )

        self.orientation = TransparentComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.rwidth = TransparentDoubleSpinBox(
            text = 'Bar Width',
            min  = 0, max  = 5, step = 0.1,
            getter=self.get_rwidth,
            setter=self.set_rwidth,
            layout=self.general.addlayout
        )

        self.log = Toggle(
            text="Log",
            getter=self.get_log,
            setter=self.set_log,
            layout=self.general.addlayout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(rect)
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.figure, 
            match=[patches.Rectangle], 
            gid=self.gid
        )

    def set_bins(self, value:int):
        try:
            self.plot.props.update(bins = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bins(self) -> int:
        return self.plot.props["bins"]

    def set_density(self, value:bool):
        try:
            self.plot.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.plot.props["density"]

    def set_cumulative(self, value:bool):
        try:
            self.plot.props.update(cumulative = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cumulative(self) -> bool:
        return self.plot.props["cumulative"]

    def set_histtype(self, value:str):
        try:
            self.plot.props.update(histtype = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_histtype(self) -> str:
        return self.plot.props["histtype"]
    
    def set_alignment (self, value:str):
        try: 
            self.plot.props.update(align = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_alignment(self) -> str:
        return self.plot.props["align"]

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]
    
    def set_bottom (self, value:str):
        try:
            if value: value = 0
            self.plot.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.plot.props["bottom"])
 
    def set_rwidth (self, value):
        try: 
            self.plot.props.update(rwidth = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rwidth (self):
        if not self.plot.props["rwidth"]:
            return 0
        return self.plot.props["rwidth"]

    def set_log(self, value:bool):
        try:
            self.plot.props.update(log = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_log(self) -> bool:
        return self.plot.props["log"]

class Boxplot(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Boxes', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Whiskers', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Caps', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.addButton(text='Fliers', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.segment.addButton(text='Medians', func=lambda: self.stackedlayout.setCurrentIndex(5))
        self.segment.addButton(text='Means', func=lambda: self.stackedlayout.setCurrentIndex(6))
        self.segment.setCurrentIndex(0)

        # Boxes
        boxes = QWidget()
        layout_boxes = QVBoxLayout(boxes)
        layout_boxes.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(boxes)

        self.showbox = Toggle(
            text="Show boxes",
            getter=self.get_showbox,
            setter=self.set_showbox,
            layout=layout_boxes
        )

        self.notch = Toggle(
            text="Notch",
            getter=self.get_notch,
            setter=self.set_notch,
            layout=layout_boxes
        )

        self.vert = TransparentComboBox(
            items=["vertical","horizontal"], 
            text="Orientation",
            getter=self.get_vert,
            setter=self.set_vert,
            layout=layout_boxes
        )

        self.widths = TransparentDoubleSpinBox(
            text="Widths", 
            step=0.25,
            getter=self.get_widths,
            setter=self.set_widths,
            layout=layout_boxes
        )

        self.boxes = Rectangle(f"{self.gid}/boxes", self.canvas, self.parent())
        self.boxes.onChanged.connect(self._onChange)
        layout_boxes.addWidget(self.boxes)

        # Whiskers
        whiskers = QWidget()
        layout_whiskers = QVBoxLayout(whiskers)
        layout_whiskers.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(whiskers)

        self.whis = TransparentDoubleSpinBox(
            text="Whis",
            getter=self.get_whis,
            setter=self.set_whis,
            layout=layout_whiskers
        )

        self.autorange = Toggle(
            text="Autorange",
            getter=self.get_autorange,
            setter=self.set_autorange,
            layout=layout_whiskers
        )

        self.whiskers = Line(f"_{self.gid}/whiskers", self.canvas)
        self.whiskers.onChanged.connect(self._onChange)
        layout_whiskers.addWidget(self.whiskers)
        
        # Caps
        caps = QWidget()
        layout_caps = QVBoxLayout(caps)
        layout_caps.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(caps)

        self.showcaps = Toggle(
            text="Show Caps",
            getter=self.get_showcaps,
            setter=self.set_showcaps,
            layout=layout_caps
        )

        self.capwidths = TransparentDoubleSpinBox(
            text="Capwidth", 
            step=0.25,
            getter=self.get_capwidths,
            setter=self.set_capwidths,
            layout=layout_caps
        )

        self.caps = Line(f"_{self.gid}/caps", self.canvas)
        self.caps.onChanged.connect(self._onChange)
        layout_caps.addWidget(self.caps)

        # Fliers
        fliers = QWidget()
        layout_fliers = QVBoxLayout(fliers)
        layout_fliers.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(fliers)

        self.showfliers = Toggle(
            text="Show Fliers",
            getter=self.get_showfliers,
            setter=self.set_showfliers,
            layout=layout_fliers
        )

        self.fliers = Marker(f"_{self.gid}/fliers", self.canvas)
        self.fliers.onChanged.connect(self._onChange)
        layout_fliers.addWidget(self.fliers)

        # Medians 
        medians = QWidget()
        layout_medians = QVBoxLayout(medians)
        layout_medians.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(medians)

        self.bootstrap = TransparentSpinBox(
            text="Bootstrap", 
            max=100000, step=1000,
            getter=self.get_bootstrap,
            setter=self.set_bootstrap,
            layout=layout_medians
        )

        self.medians = Line(f"_{self.gid}/medians", self.canvas)
        self.medians.onChanged.connect(self._onChange)
        layout_medians.addWidget(self.medians)

        # Means
        means = QWidget()
        layout_mean = QVBoxLayout(means)
        layout_mean.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(means)

        self.showmeans = Toggle(
            text="Show Means",
            getter=self.get_showmeans,
            setter=self.set_showmeans,
            layout=layout_mean
        )

        self.meanline = Toggle(
            text="Meanline",
            getter=self.get_meanline,
            setter=self.set_meanline,
            layout=layout_mean
        )

        self.means = Line(f"_{self.gid}/means", self.canvas)
        self.means.onChanged.connect(self._onChange)
        layout_mean.addWidget(self.means)
    
    def find_object(self) -> list[Union[lines.Line2D, patches.PathPatch]]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[lines.Line2D, patches.PathPatch],
            gid=self.gid,
        )

    def set_showbox(self, value:bool):
        try:
            self.plot.props.update(showbox = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showbox(self) -> bool:
        return self.plot.props["showbox"]
    
    def set_notch(self, value:bool):
        try:
            self.plot.props.update(notch = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_notch(self) -> bool:
        return self.plot.props["notch"]

    def set_vert(self, value:str):
        try:
            if value == "vertical": self.plot.props.update(vert = True)
            else: self.plot.props.update(vert = False)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        if self.plot.props["vert"]: return "vertical"
        return "horizontal"
    
    def set_widths(self, value:float):
        try:
            self.plot.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.plot.props["widths"]

    def set_whis(self, value:float):
        try:
            self.plot.props.update(whis = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_whis(self) -> float:
        return self.plot.props["whis"]
    
    def set_autorange(self, value:bool):
        try:
            self.plot.props.update(autorange = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_autorange(self) -> bool:
        return self.plot.props["autorange"]

    def set_showcaps(self, value:bool):
        try:
            self.plot.props.update(showcaps = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showcaps(self) -> bool:
        return self.plot.props["showcaps"]
    
    def set_capwidths(self, value:float):
        try:
            self.plot.props.update(capwidths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_capwidths(self) -> float:
        return self.plot.props["capwidths"]
    
    def set_showfliers(self, value:bool):
        try:
            self.plot.props.update(showfliers = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showfliers(self) -> bool:
        return self.plot.props["showfliers"]
    
    def set_bootstrap(self, value:int):
        try:
            self.plot.props.update(bootstrap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bootstrap(self) -> int:
        return self.plot.props["bootstrap"]
    
    def set_showmeans(self, value:bool):
        try:
            self.plot.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.plot.props["showmeans"]
    
    def set_meanline(self, value:bool):
        try:
            self.plot.props.update(meanline = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_meanline(self) -> bool:
        return self.plot.props["meanline"]

class Violinplot(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Bodies', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Means', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.addButton(text='Min', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.segment.addButton(text='Max', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.segment.addButton(text='Bars', func=lambda: self.stackedlayout.setCurrentIndex(5))
        self.segment.addButton(text='Medians', func=lambda: self.stackedlayout.setCurrentIndex(6))
        self.segment.addButton(text='Quantiles', func=lambda: self.stackedlayout.setCurrentIndex(7))
        self.segment.setCurrentIndex(0)        

        # Bodies
        bodies = QWidget()
        layout_bodies = QVBoxLayout(bodies)
        layout_bodies.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(bodies)

        self.vert = TransparentComboBox(
            items=["vertical","horizontal"],
            text="Orientation",
            getter=self.get_vert,
            setter=self.set_vert,
            layout=layout_bodies
        )

        self.widths = TransparentDoubleSpinBox(
            text="Widths",
            getter=self.get_widths,
            setter=self.set_widths,
            layout=layout_bodies
        )

        self.points = TransparentSpinBox(
            text="Num of Points",
            getter=self.get_points,
            setter=self.set_points,
            layout=layout_bodies
        )

        self.bw_method = TransparentComboBox(
            items=["scott","silverman"],
            text="Bandwidth Method",
            getter=self.get_bw_method,
            setter=self.set_bw_method,
            layout=layout_bodies
        )

        self.bodies = SingleColorCollection(f"{self.gid}/bodies", self.canvas)
        self.bodies.onChanged.connect(self._onChange)
        layout_bodies.addWidget(self.bodies)

        # Means
        cmeans = QWidget()
        layout_cmeans = QVBoxLayout(cmeans)
        layout_cmeans.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmeans)

        self.showmeans = Toggle(
            text="Show Means",
            getter=self.get_showmeans,
            setter=self.set_showmeans,
            layout=layout_cmeans
        )

        self.cmeans = LineCollection(f"_{self.gid}/cmeans",self.canvas)
        self.cmeans.onChanged.connect(self._onChange)
        layout_cmeans.addWidget(self.cmeans)

        # Mins
        cmins = QWidget()
        layout_cmins = QVBoxLayout(cmins)
        layout_cmins.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmins)

        self.cmins = LineCollection(f"_{self.gid}/cmins", self.canvas)
        self.cmins.onChanged.connect(self._onChange)
        layout_cmins.addWidget(self.cmins)

        # Maxes
        cmaxes = QWidget()
        layout_cmaxes = QVBoxLayout(cmaxes)
        layout_cmaxes.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmaxes)

        self.cmaxes = LineCollection(f"_{self.gid}/cmaxes", self.canvas)
        self.cmaxes.onChanged.connect(self._onChange)
        layout_cmaxes.addWidget(self.cmaxes)

        # Bars
        cbars = QWidget()
        layout_cbars = QVBoxLayout(cbars)
        layout_cbars.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cbars)

        self.showextrema = Toggle(
            text="Show Extrema",
            getter=self.get_showextrema,
            setter=self.set_showextrema,
            layout=layout_cbars
        )

        self.cbars = LineCollection(f"_{self.gid}/cbars", self.canvas)
        self.cbars.onChanged.connect(self._onChange)
        layout_cbars.addWidget(self.cbars)

        # Medians
        cmedians = QWidget()
        layout_cmedians = QVBoxLayout(cmedians)
        layout_cmedians.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmedians)

        self.showmedians = Toggle(
            text="Show Medians",
            getter=self.get_showmedians,
            setter=self.set_showmedians,
            layout=layout_cmedians
        )

        self.cmedians = LineCollection(f"_{self.gid}/cmedians", self.canvas)
        self.cmedians.onChanged.connect(self._onChange)
        layout_cmedians.addWidget(self.cmedians)

        # Quantiles
        cquantiles = QWidget()
        layout_cquantiles = QVBoxLayout(cquantiles)
        layout_cquantiles.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cquantiles)
        
        self.cquantiles = SingleColorCollection(f"_{self.gid}/cquantiles", self.canvas)
        self.cquantiles.onChanged.connect(self._onChange)
        layout_cquantiles.addWidget(self.cquantiles)
    
    def find_object(self) -> list[Union[collections.PolyCollection, collections.LineCollection]]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[collections.PolyCollection, collections.LineCollection],
            gid=self.gid,
        )

    def set_vert(self, value:str):
        try:
            self.plot.props.update(orientation = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        return self.plot.props["orientation"]
    
    def set_widths(self, value:float):
        try:
            self.plot.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.plot.props["widths"]

    def set_points(self, value:int):
        try:
            self.plot.props.update(points = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_points(self) -> int:
        return self.plot.props["points"]
    
    def set_bw_method(self, value:str):
        try:
            self.plot.props.update(bw_method = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bw_method(self) -> str:
        return self.plot.props["bw_method"]
    
    def set_showmeans(self, value:bool):
        try:
            self.plot.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.plot.props["showmeans"]

    def set_showextrema(self, value:bool):
        try:
            self.plot.props.update(showextrema = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showextrema(self) -> bool:
        return self.plot.props["showextrema"]

    def set_showmedians(self, value:bool):
        try:
            self.plot.props.update(showmedians = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmedians(self) -> bool:
        return self.plot.props["showmedians"]

class Eventplot(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.orientation = TransparentComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=self.general.addlayout
        )

        self.lineoffsets = TransparentDoubleSpinBox(
            text="Line Offsets",
            getter=self.get_lineoffsets,
            setter=self.set_lineoffsets,
            layout=self.general.addlayout
        )

        self.linelengths = TransparentDoubleSpinBox(
            text = "Line Lengths",
            step = 0.25,
            getter=self.get_linelengths,
            setter=self.set_linelengths,
            layout=self.general.addlayout
        )

        collection = LineCollection(self.gid, self.canvas)
        collection.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(collection)
    
    def find_object(self) -> list[collections.EventCollection]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[collections.EventCollection],
            gid=self.gid,
        )

    def set_orientation(self, value:str):
        try:
            self.plot.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.plot.props["orientation"]

    def set_lineoffsets(self, value:float):
        try:
            self.plot.props.update(lineoffsets = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_lineoffsets(self) -> float:
        return self.plot.props["lineoffsets"]
    
    def set_linelengths(self, value:float):
        try:
            self.plot.props.update(linelengths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_linelengths(self) -> float:
        return self.plot.props["linelengths"]

class Hist2d(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Mesh', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.setCurrentIndex(0)

        self.binx = TransparentSpinBox(
            text="Bins X",
            getter=self.get_binx,
            setter=self.set_binx,
            layout=self.general.addlayout
        )

        self.biny = TransparentSpinBox(
            text="Spin Y",
            getter=self.get_biny,
            setter=self.set_biny,
            layout=self.general.addlayout
        )

        self.density = Toggle(
            text="Density",
            getter=self.get_density,
            setter=self.set_density,
            layout=self.general.addlayout
        )

        qm = QuadMesh(self.gid, self.canvas)
        qm.onChanged.connect(self._onChange)
        self.stackedlayout.addWidget(qm)

    def find_object(self) -> list[collections.QuadMesh]:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[collections.QuadMesh],
            gid=self.gid,
        )
    
    def set_binx(self, value:int):
        try:
            self.plot.props.update(binx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_binx(self) -> int:
        return self.plot.props["binx"]
    
    def set_biny(self, value:int):
        try:
            self.plot.props.update(biny = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_biny(self) -> int:
        return self.plot.props["biny"]
    
    def set_density(self, value:bool):
        try:
            self.plot.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.plot.props["density"]

class ErrorBar(PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        self.segment.addButton(text='Data line', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.segment.addButton(text='Error bars', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.segment.setCurrentIndex(0)

        data_line = QWidget()
        layout_data = QVBoxLayout(data_line)
        layout_data.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(data_line)

        data_line = Line(f'{self.gid}/dataline', self.canvas)
        data_line.onChanged.connect(self._onChange)
        layout_data.addWidget(data_line)

        marker = Marker(f'{self.gid}/dataline', self.canvas)
        marker.onChanged.connect(self._onChange)
        layout_data.addWidget(marker)

        err = QWidget()
        layout_err = QVBoxLayout(err)
        layout_err.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(err)

        capsize = TransparentDoubleSpinBox(
            text="Cap Size",
            getter=self.get_capsize,
            setter=self.set_capsize,
            layout=layout_err
        )

        err = ErrorBarCollection(f'_{self.gid}/err', self.canvas)
        err.onChanged.connect(self._onChange)
        layout_err.addWidget(err)
    
    def find_object(self) -> lines.Line2D:
        return find_mpl_object(
            source=self.canvas.figure,
            match=[lines.Line2D],
            gid=self.gid,
        )

    def set_capsize(self, value:float):
        try:
            self.plot.props.update(capsize = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_capsize(self) -> float:
        return self.plot.props["capsize"]