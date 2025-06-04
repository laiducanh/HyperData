from PySide6.QtWidgets import QVBoxLayout, QStackedLayout, QWidget
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
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

        self.bins = SpinBox(text="Bins",min=1)
        self.bins.button.setValue(self.get_bins())
        self.bins.button.valueChanged.connect(self.set_bins)
        layout.addWidget(self.bins)

        self.density = Toggle(text="Density")
        self.density.button.setChecked(self.get_density())
        self.density.button.checkedChanged.connect(self.set_density)
        layout.addWidget(self.density)

        self.cumulative = Toggle(text="Cumulative")
        self.cumulative.button.setChecked(self.get_cumulative())
        self.cumulative.button.checkedChanged.connect(self.set_cumulative)
        layout.addWidget(self.cumulative)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        # self.histtype = ComboBox(
        #     items = ['bar', 'barstacked', 'step', 'stepfilled'],
        #     text  = "Histtype"
        # )
        # self.histtype.button.setCurrentText(self.get_histtype())
        # self.histtype.button.currentTextChanged.connect(self.set_histtype)
        # self._layout.addWidget(self.histtype)

        self.align = ComboBox(
            items = ["left","mid","right"],
            text  = "Alignment"
        )
        self.align.button.setCurrentText(self.get_alignment())
        self.align.button.currentTextChanged.connect(self.set_alignment)
        layout.addWidget(self.align)

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.rwidth = DoubleSpinBox(
            text = 'Bar Width',
            min  = 0,
            max  = 5,
            step = 0.1
        )
        self.rwidth.button.setValue(self.get_rwidth())
        self.rwidth.button.valueChanged.connect(self.set_rwidth)
        layout.addWidget(self.rwidth)

        self.log = Toggle(text="Log")
        self.log.button.setChecked(self.get_log())
        self.log.button.checkedChanged.connect(self.set_log)
        layout.addWidget(self.log)

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

        self.showbox = Toggle(text="Show boxes")
        self.showbox.button.setChecked(self.get_showbox())
        self.showbox.button.checkedChanged.connect(self.set_showbox)
        layout_boxes.addWidget(self.showbox)

        self.notch = Toggle(text="Notch")
        self.notch.button.setChecked(self.get_notch())
        self.notch.button.checkedChanged.connect(self.set_notch)
        layout_boxes.addWidget(self.notch)

        self.vert = ComboBox(items=["vertical","horizontal"], text="Orientation")
        self.vert.button.setCurrentText(self.get_vert())
        self.vert.button.currentTextChanged.connect(self.set_vert)
        layout_boxes.addWidget(self.vert)

        self.widths = DoubleSpinBox(text="Widths", step=0.25)
        self.widths.button.setValue(self.get_widths())
        self.widths.button.valueChanged.connect(self.set_widths)
        layout_boxes.addWidget(self.widths)

        self.boxes = Rectangle(f"{self.gid}/boxes", self.canvas, self.parent())
        self.boxes.onChanged.connect(self.onChanged.emit)
        layout_boxes.addWidget(self.boxes)

        # Whiskers
        whiskers = QWidget()
        layout_whiskers = QVBoxLayout(whiskers)
        layout_whiskers.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(whiskers)

        self.whis = DoubleSpinBox(text="Whis")
        self.whis.button.setValue(self.get_whis())
        self.whis.button.valueChanged.connect(self.set_whis)
        layout_whiskers.addWidget(self.whis)

        self.autorange = Toggle(text="Autorange")
        self.autorange.button.setChecked(self.get_autorange())
        self.autorange.button.checkedChanged.connect(self.set_autorange)
        layout_whiskers.addWidget(self.autorange)

        self.whiskers = Line(f"_{self.gid}/whiskers", self.canvas)
        self.whiskers.onChanged.connect(self.onChanged.emit)
        layout_whiskers.addWidget(self.whiskers)
        
        # Caps
        caps = QWidget()
        layout_caps = QVBoxLayout(caps)
        layout_caps.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(caps)

        self.showcaps = Toggle(text="Show Caps")
        self.showcaps.button.setChecked(self.get_showcaps())
        self.showcaps.button.checkedChanged.connect(self.set_showcaps)
        layout_caps.addWidget(self.showcaps)

        self.capwidths = DoubleSpinBox(text="Capwidth", step=0.25)
        self.capwidths.button.setValue(self.get_capwidths())
        self.capwidths.button.valueChanged.connect(self.set_capwidths)
        layout_caps.addWidget(self.capwidths)

        self.caps = Line(f"_{self.gid}/caps", self.canvas)
        self.caps.onChanged.connect(self.onChanged.emit)
        layout_caps.addWidget(self.caps)

        # Fliers
        fliers = QWidget()
        layout_fliers = QVBoxLayout(fliers)
        layout_fliers.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(fliers)

        self.showfliers = Toggle(text="Show Fliers")
        self.showfliers.button.setChecked(self.get_showfliers())
        self.showfliers.button.checkedChanged.connect(self.set_showfliers)
        layout_fliers.addWidget(self.showfliers)

        self.fliers = Marker(f"_{self.gid}/fliers", self.canvas)
        self.fliers.onChanged.connect(self.onChanged.emit)
        layout_fliers.addWidget(self.fliers)

        # Medians 
        medians = QWidget()
        layout_medians = QVBoxLayout(medians)
        layout_medians.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(medians)

        self.bootstrap = SpinBox(text="Bootstrap", max=100000, step=1000)
        self.bootstrap.button.setValue(self.get_bootstrap())
        self.bootstrap.button.valueChanged.connect(self.set_bootstrap)
        layout_medians.addWidget(self.bootstrap)

        self.medians = Line(f"_{self.gid}/medians", self.canvas)
        self.medians.onChanged.connect(self.onChanged.emit)
        layout_medians.addWidget(self.medians)

        # Means
        means = QWidget()
        layout_mean = QVBoxLayout(means)
        layout_mean.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(means)

        self.showmeans = Toggle(text="Show Means")
        self.showmeans.button.setChecked(self.get_showmeans())
        self.showmeans.button.checkedChanged.connect(self.set_showmeans)
        layout_mean.addWidget(self.showmeans)

        self.meanline = Toggle(text="Meanline")
        self.meanline.button.setChecked(self.get_meanline())
        self.meanline.button.checkedChanged.connect(self.set_meanline)
        layout_mean.addWidget(self.meanline)

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

        self.vert = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.vert.button.setCurrentText(self.get_vert())
        self.vert.button.currentTextChanged.connect(self.set_vert)
        layout_bodies.addWidget(self.vert)

        self.widths = DoubleSpinBox(text="Widths")
        self.widths.button.setValue(self.get_widths())
        self.widths.button.valueChanged.connect(self.set_widths)
        layout_bodies.addWidget(self.widths)

        self.points = SpinBox(text="Num of Points")
        self.points.button.setValue(self.get_points())
        self.points.button.valueChanged.connect(self.set_points)
        layout_bodies.addWidget(self.points)

        self.bw_method = ComboBox(items=["scott","silverman"],text="Bandwidth Method")
        self.bw_method.button.setCurrentText(self.get_bw_method())
        self.bw_method.button.currentTextChanged.connect(self.set_bw_method)
        layout_bodies.addWidget(self.bw_method)

        self.bodies = SingleColorCollection(f"{self.gid}/bodies", self.canvas)
        self.bodies.onChanged.connect(self.onChanged.emit)
        layout_bodies.addWidget(self.bodies)

        # Means
        cmeans = QWidget()
        layout_cmeans = QVBoxLayout(cmeans)
        layout_cmeans.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmeans)

        self.showmeans = Toggle(text="Show Means")
        self.showmeans.button.setChecked(self.get_showmeans())
        self.showmeans.button.checkedChanged.connect(self.set_showmeans)
        layout_cmeans.addWidget(self.showmeans)

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

        self.showextrema = Toggle(text="Show Extrema")
        self.showextrema.button.setChecked(self.get_showextrema())
        self.showextrema.button.checkedChanged.connect(self.set_showextrema)
        layout_cbars.addWidget(self.showextrema)

        self.cbars = LineCollection(f"_{self.gid}/cbars", self.canvas)
        self.cbars.onChanged.connect(self.onChanged.emit)
        layout_cbars.addWidget(self.cbars)

        # Medians
        cmedians = QWidget()
        layout_cmedians = QVBoxLayout(cmedians)
        layout_cmedians.setContentsMargins(0,0,0,0)
        self.stackedlayout.addWidget(cmedians)

        self.showmedians = Toggle(text="Show Medians")
        self.showmedians.button.setChecked(self.get_showmedians())
        self.showmedians.button.checkedChanged.connect(self.set_showmedians)
        layout_cmedians.addWidget(self.showmedians)

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

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.lineoffsets = DoubleSpinBox(text="Line Offsets")
        self.lineoffsets.button.setValue(self.get_lineoffsets())
        self.lineoffsets.button.valueChanged.connect(self.set_lineoffsets)
        layout.addWidget(self.lineoffsets)

        self.linelengths = DoubleSpinBox(
            text = "Line Lengths",
            step = 0.25
        )
        self.linelengths.button.setValue(self.get_linelengths())
        self.linelengths.button.valueChanged.connect(self.set_linelengths)
        layout.addWidget(self.linelengths)

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

        self.binx = SpinBox(text="Bins X")
        self.binx.button.setValue(self.get_binx())
        self.binx.button.valueChanged.connect(self.set_binx)
        layout.addWidget(self.binx)

        self.biny = SpinBox(text="Spin Y")
        self.biny.button.setValue(self.get_biny())
        self.biny.button.valueChanged.connect(self.set_biny)
        layout.addWidget(self.biny)

        self.density = Toggle(text="Density")
        self.density.button.setChecked(self.get_density())
        self.density.button.checkedChanged.connect(self.set_density)
        layout.addWidget(self.density)

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

        capsize = DoubleSpinBox(text="Cap Size")
        capsize.button.setValue(self.get_capsize())
        capsize.button.valueChanged.connect(self.set_capsize)
        layout_err.addWidget(capsize)

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