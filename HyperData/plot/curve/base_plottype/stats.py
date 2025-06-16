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

class Histogram (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Histogram'))
        layout.addWidget(SeparateHLine())

        self.bins = TransparentSpinBox(
            text="Bins",
            min=1, 
            getter=self.get_bins,
            setter=self.set_bins,
            layout=layout
        )

        self.density = Toggle(
            text="Density",
            getter=self.get_density,
            setter=self.set_density,
            layout=layout
        )

        self.cumulative = Toggle(
            text="Cumulative",
            getter=self.get_cumulative,
            setter=self.set_cumulative,
            layout=layout
        )

        self.bottom = LineEdit(
            text="Bottom",
            getter=self.get_bottom,
            layout=layout
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
            layout=layout
        )

        self.orientation = TransparentComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=layout
        )

        self.rwidth = TransparentDoubleSpinBox(
            text = 'Bar Width',
            min  = 0, max  = 5, step = 0.1,
            getter=self.get_rwidth,
            setter=self.set_rwidth,
            layout=layout
        )

        self.log = Toggle(
            text="Log",
            getter=self.get_log,
            setter=self.set_log,
            layout=layout
        )

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self.onChanged.emit)
        layout.addWidget(rect)
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig, 
            match=[patches.Rectangle], 
            gid=self.gid
        )

    def set_bins(self, value:int):
        try:
            self.props.update(bins = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bins(self) -> int:
        return self.find_object()[0].bins

    def set_density(self, value:bool):
        try:
            self.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.find_object()[0].density

    def set_cumulative(self, value:bool):
        try:
            self.props.update(cumulative = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cumulative(self) -> bool:
        return self.find_object()[0].cumulative

    def set_histtype(self, value:str):
        try:
            self.props.update(histtype = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_histtype(self) -> str:
        return self.find_object()[0].histtype
    
    def set_alignment (self, value:str):
        try: 
            self.props.update(align = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_alignment(self) -> str:
        return self.find_object()[0].align

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value: value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.find_object()[0].bottom)
 
    def set_rwidth (self, value):
        try: 
            self.props.update(rwidth = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rwidth (self):
        if not self.find_object()[0].rwidth:
            return 0
        return self.find_object()[0].rwidth

    def set_log(self, value:bool):
        try:
            self.props.update(log = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_log(self) -> bool:
        return self.find_object()[0].log

class Boxplot (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        
        self.choose_component = SegmentedWidget()
        layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Boxes', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Whiskers', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_component.addButton(text='Caps', func=lambda: self.stackedlayout.setCurrentIndex(2) )
        self.choose_component.addButton(text='Fliers', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.choose_component.addButton(text='Medians', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.choose_component.addButton(text='Means', func=lambda: self.stackedlayout.setCurrentIndex(5))

        self.choose_component.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        # Boxes
        boxes = QWidget()
        layout_boxes = QVBoxLayout(boxes)
        layout_boxes.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(boxes)

        self.showbox = Toggle(
            text="Show boxes",
            getter=self.get_showbox,
            setter=self.set_showbox,
            layout=layout
        )

        self.notch = Toggle(
            text="Notch",
            getter=self.get_notch,
            setter=self.set_notch,
            layout=layout
        )

        self.vert = TransparentComboBox(
            items=["vertical","horizontal"], 
            text="Orientation",
            getter=self.get_vert,
            setter=self.set_vert,
            layout=layout
        )

        self.widths = TransparentDoubleSpinBox(
            text="Widths", 
            step=0.25,
            getter=self.get_widths,
            setter=self.set_widths,
            layout=layout
        )

        self.boxes = Rectangle(f"{self.gid}/boxes", self.canvas, self.parent())
        self.boxes.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.autorange = Toggle(
            text="Autorange",
            getter=self.get_autorange,
            setter=self.set_autorange,
            layout=layout
        )

        self.whiskers = Line(f"_{self.gid}/whiskers", self.canvas)
        self.whiskers.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.capwidths = TransparentDoubleSpinBox(
            text="Capwidth", 
            step=0.25,
            getter=self.get_capwidths,
            setter=self.set_capwidths,
            layout=layout
        )

        self.caps = Line(f"_{self.gid}/caps", self.canvas)
        self.caps.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.fliers = Marker(f"_{self.gid}/fliers", self.canvas)
        self.fliers.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.medians = Line(f"_{self.gid}/medians", self.canvas)
        self.medians.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.meanline = Toggle(
            text="Meanline",
            getter=self.get_meanline,
            setter=self.set_meanline,
            layout=layout
        )

        self.means = Line(f"_{self.gid}/means", self.canvas)
        self.means.onChanged.connect(self.onChanged.emit)
        layout_mean.addWidget(self.means)
    
    def find_object(self) -> list[Union[lines.Line2D, patches.PathPatch]]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D, patches.PathPatch],
            gid=self.gid,
        )

    def set_showbox(self, value:bool):
        try:
            self.props.update(showbox = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showbox(self) -> bool:
        return self.find_object()[0].showbox
    
    def set_notch(self, value:bool):
        try:
            self.props.update(notch = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_notch(self) -> bool:
        return self.find_object()[0].notch

    def set_vert(self, value:str):
        try:
            if value == "vertical": self.props.update(vert = True)
            else: self.props.update(vert = False)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        if self.find_object()[0].vert: return "vertical"
        return "horizontal"
    
    def set_widths(self, value:float):
        try:
            self.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.find_object()[0].widths

    def set_whis(self, value:float):
        try:
            self.props.update(whis = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_whis(self) -> float:
        return self.find_object()[0].whis 
    
    def set_autorange(self, value:bool):
        try:
            self.props.update(autorange = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_autorange(self) -> bool:
        return self.find_object()[0].autorange

    def set_showcaps(self, value:bool):
        try:
            self.props.update(showcaps = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showcaps(self) -> bool:
        return self.find_object()[0].showcaps
    
    def set_capwidths(self, value:float):
        try:
            self.props.update(capwidths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_capwidths(self) -> float:
        return self.find_object()[0].capwidths
    
    def set_showfliers(self, value:bool):
        try:
            self.props.update(showfliers = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showfliers(self) -> bool:
        return self.find_object()[0].showfliers
    
    def set_bootstrap(self, value:int):
        try:
            self.props.update(bootstrap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bootstrap(self) -> int:
        return self.find_object()[0].bootstrap
    
    def set_showmeans(self, value:bool):
        try:
            self.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.find_object()[0].showmeans
    
    def set_meanline(self, value:bool):
        try:
            self.props.update(meanline = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_meanline(self) -> bool:
        return self.find_object()[0].meanline

class Violinplot (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        
        self.choose_component = SegmentedWidget()
        layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Bodies', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Means', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_component.addButton(text='Min', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_component.addButton(text='Max', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.choose_component.addButton(text='Bars', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.choose_component.addButton(text='Medians', func=lambda: self.stackedlayout.setCurrentIndex(5))
        self.choose_component.addButton(text='Quantiles', func=lambda: self.stackedlayout.setCurrentIndex(6))

        self.choose_component.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

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
            layout=layout
        )

        self.widths = TransparentDoubleSpinBox(
            text="Widths",
            getter=self.get_widths,
            setter=self.set_widths,
            layout=layout
        )

        self.points = TransparentSpinBox(
            text="Num of Points",
            getter=self.get_points,
            setter=self.set_points,
            layout=layout
        )

        self.bw_method = TransparentComboBox(
            items=["scott","silverman"],
            text="Bandwidth Method",
            getter=self.get_bw_method,
            setter=self.set_bw_method,
            layout=layout
        )

        self.bodies = SingleColorCollection(f"{self.gid}/bodies", self.canvas)
        self.bodies.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.cmeans = LineCollection(f"_{self.gid}/cmeans",self.canvas)
        self.cmeans.onChanged.connect(self.onChanged.emit)
        layout_cmeans.addWidget(self.cmeans)

        # Mins
        cmins = QWidget()
        layout_cmins = QVBoxLayout(cmins)
        layout_cmins.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmins)

        self.cmins = LineCollection(f"_{self.gid}/cmins", self.canvas)
        self.cmins.onChanged.connect(self.onChanged.emit)
        layout_cmins.addWidget(self.cmins)

        # Maxes
        cmaxes = QWidget()
        layout_cmaxes = QVBoxLayout(cmaxes)
        layout_cmaxes.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmaxes)

        self.cmaxes = LineCollection(f"_{self.gid}/cmaxes", self.canvas)
        self.cmaxes.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.cbars = LineCollection(f"_{self.gid}/cbars", self.canvas)
        self.cbars.onChanged.connect(self.onChanged.emit)
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
            layout=layout
        )

        self.cmedians = LineCollection(f"_{self.gid}/cmedians", self.canvas)
        self.cmedians.onChanged.connect(self.onChanged.emit)
        layout_cmedians.addWidget(self.cmedians)

        # Quantiles
        cquantiles = QWidget()
        layout_cquantiles = QVBoxLayout(cquantiles)
        layout_cquantiles.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cquantiles)
        
        self.cquantiles = SingleColorCollection(f"_{self.gid}/cquantiles", self.canvas)
        self.cquantiles.onChanged.connect(self.onChanged.emit)
        layout_cquantiles.addWidget(self.cquantiles)
    
    def find_object(self) -> list[Union[collections.PolyCollection, collections.LineCollection]]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.PolyCollection, collections.LineCollection],
            gid=self.gid,
        )

    def set_vert(self, value:str):
        try:
            self.props.update(orientation = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        return self.find_object()[0].orientation
    
    def set_widths(self, value:float):
        try:
            self.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.find_object()[0].widths

    def set_points(self, value:int):
        try:
            self.props.update(points = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_points(self) -> int:
        return self.find_object()[0].points
    
    def set_bw_method(self, value:str):
        try:
            self.props.update(bw_method = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bw_method(self) -> str:
        return self.find_object()[0].bw_method
    
    def set_showmeans(self, value:bool):
        try:
            self.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.find_object()[0].showmeans

    def set_showextrema(self, value:bool):
        try:
            self.props.update(showextrema = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showextrema(self) -> bool:
        return self.find_object()[0].showextrema

    def set_showmedians(self, value:bool):
        try:
            self.props.update(showmedians = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmedians(self) -> bool:
        return self.find_object()[0].showmedians

class Eventplot (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Eventplot'))
        layout.addWidget(SeparateHLine())

        self.orientation = TransparentComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation",
            getter=self.get_orientation,
            setter=self.set_orientation,
            layout=layout
        )

        self.lineoffsets = TransparentDoubleSpinBox(
            text="Line Offsets",
            getter=self.get_lineoffsets,
            setter=self.set_lineoffsets,
            layout=layout
        )

        self.linelengths = TransparentDoubleSpinBox(
            text = "Line Lengths",
            step = 0.25,
            getter=self.get_linelengths,
            setter=self.set_linelengths,
            layout=layout
        )

        collection = LineCollection(self.gid, self.canvas)
        collection.onChanged.connect(self.onChanged.emit)
        layout.addWidget(collection)
    
    def find_object(self) -> list[collections.EventCollection]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.EventCollection],
            gid=self.gid,
        )

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation

    def set_lineoffsets(self, value:float):
        try:
            self.props.update(lineoffsets = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_lineoffsets(self) -> float:
        return self.find_object()[0].lineoffsets
    
    def set_linelengths(self, value:float):
        try:
            self.props.update(linelengths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_linelengths(self) -> float:
        return self.find_object()[0].linelengths

class Hist2d (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(TitleLabel('Histogram 2D'))
        layout.addWidget(SeparateHLine())

        self.binx = TransparentSpinBox(
            text="Bins X",
            getter=self.get_binx,
            setter=self.set_binx,
            layout=layout
        )

        self.biny = TransparentSpinBox(
            text="Spin Y",
            getter=self.get_biny,
            setter=self.set_biny,
            layout=layout
        )

        self.density = Toggle(
            text="Density",
            getter=self.get_density,
            setter=self.set_density,
            layout=layout
        )

        qm = QuadMesh(self.gid, self.canvas)
        qm.onChanged.connect(self.onChanged.emit)
        layout.addWidget(qm)

    def find_object(self) -> list[collections.QuadMesh]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[collections.QuadMesh],
            gid=self.gid,
        )
    
    def set_binx(self, value:int):
        try:
            self.props.update(binx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_binx(self) -> int:
        return self.find_object()[0].binx
    
    def set_biny(self, value:int):
        try:
            self.props.update(biny = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_biny(self) -> int:
        return self.find_object()[0].biny
    
    def set_density(self, value:bool):
        try:
            self.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.find_object()[0].density

class ErrorBar (PlotConfigBase):
    def __init__(self, gid, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.choose_component = SegmentedWidget()
        layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Data line', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Error bars', func=lambda: self.stackedlayout.setCurrentIndex(1))
        
        self.choose_component.setCurrentIndex(0)

        self.stackedlayout = QStackedLayout()
        layout.addLayout(self.stackedlayout)

        data_line = QWidget()
        layout_data = QVBoxLayout(data_line)
        layout_data.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(data_line)

        data_line = Line(f'{self.gid}/dataline', self.canvas)
        data_line.onChanged.connect(self.onChanged.emit)
        layout_data.addWidget(data_line)

        marker = Marker(f'{self.gid}/dataline', self.canvas)
        marker.onChanged.connect(self.onChanged.emit)
        layout_data.addWidget(marker)

        err = QWidget()
        layout_err = QVBoxLayout(err)
        layout_err.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(err)

        capsize = TransparentDoubleSpinBox(
            text="Cap Size",
            getter=self.get_capsize,
            setter=self.set_capsize,
            layout=layout
        )

        err = ErrorBarCollection(f'_{self.gid}/err', self.canvas)
        err.onChanged.connect(self.onChanged.emit)
        layout_err.addWidget(err)
    
    def find_object(self) -> lines.Line2D:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[lines.Line2D],
            gid=self.gid,
        )

    def set_capsize(self, value:float):
        try:
            self.props.update(capsize = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_capsize(self) -> float:
        return self.find_object()[0].capsize