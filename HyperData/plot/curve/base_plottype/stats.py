from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.line import Line2D, LineCollection, Line, Marker
from plot.curve.base_elements.collection import SingleColorCollection, QuadMesh
from plot.curve.base_plottype.base import PlotConfigBase
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches, lines, collections

DEBUG = False

class Histogram (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.bins = SpinBox(text="Bins",min=1)
        self.bins.button.setValue(self.get_bins())
        self.bins.button.valueChanged.connect(self.set_bins)
        self._layout.addWidget(self.bins)

        self.density = Toggle(text="Density")
        self.density.button.setChecked(self.get_density())
        self.density.button.checkedChanged.connect(self.set_density)
        self._layout.addWidget(self.density)

        self.cumulative = Toggle(text="Cumulative")
        self.cumulative.button.setChecked(self.get_cumulative())
        self.cumulative.button.checkedChanged.connect(self.set_cumulative)
        self._layout.addWidget(self.cumulative)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        self._layout.addWidget(self.bottom)

        self.histtype = ComboBox(items=['bar', 'barstacked', 'step', 'stepfilled'],text="Histtype")
        self.histtype.button.setCurrentText(self.get_histtype())
        self.histtype.button.currentTextChanged.connect(self.set_histtype)
        # self._layout.addWidget(self.histtype)

        self.align = ComboBox(items=["left","mid","right"],text="Alignment")
        self.align.button.setCurrentText(self.get_alignment())
        self.align.button.currentTextChanged.connect(self.set_alignment)
        self._layout.addWidget(self.align)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.rwidth = DoubleSpinBox(text='Bar Width',min=0,max=5,step=0.1)
        self.rwidth.button.setValue(self.get_rwidth())
        self.rwidth.button.valueChanged.connect(self.set_rwidth)
        self._layout.addWidget(self.rwidth)

        self.log = Toggle(text="Log")
        self.log.button.setChecked(self.get_log())
        self.log.button.checkedChanged.connect(self.set_log)
        self._layout.addWidget(self.log)

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.sig.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()

    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            figure=self.canvas.fig, 
            match=[patches.Rectangle], 
            gid=self.gid
        )

    def update_props(self):
        self.bins.button.setValue(self.get_bins())
        self.density.button.setChecked(self.get_density())
        self.cumulative.button.setChecked(self.get_cumulative())
        self.histtype.button.setCurrentText(self.get_histtype())
        self.align.button.setCurrentText(self.get_alignment())
        self.orientation.button.setCurrentText(self.get_orientation())
        self.bottom.button.setText(self.get_bottom())
        self.rwidth.button.setValue(self.get_rwidth())
        self.log.button.setChecked(self.get_log())
    
    def set_bins(self, value:int):
        try:
            self.props.update(bins = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bins(self) -> int:
        return self.obj[0].bins

    def set_density(self, value:bool):
        try:
            self.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.obj[0].density

    def set_cumulative(self, value:bool):
        try:
            self.props.update(cumulative = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cumulative(self) -> bool:
        return self.obj[0].cumulative

    def set_histtype(self, value:str):
        try:
            self.props.update(histtype = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_histtype(self) -> str:
        return self.obj[0].histtype
    
    def set_alignment (self, value:str):
        try: 
            self.props.update(align = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_alignment(self) -> str:
        return self.obj[0].align

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value: value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)
 
    def set_rwidth (self, value):
        try: 
            self.props.update(rwidth = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rwidth (self):
        if not self.obj[0].rwidth:
            return 0
        return self.obj[0].rwidth

    def set_log(self, value:bool):
        try:
            self.props.update(log = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_log(self) -> bool:
        return self.obj[0].log
    
class Boxplot (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.choose_component = SegmentedWidget()
        self._layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Boxes', func=lambda: self.changeComponent("boxes"))
        self.choose_component.addButton(text='Whiskers', func=lambda: self.changeComponent("whiskers"))
        self.choose_component.addButton(text='Fliers', func=lambda: self.changeComponent("fliers"))
        self.choose_component.addButton(text='Medians', func=lambda: self.changeComponent("medians"))

        self.stackedlayout = QStackedLayout()
        self._layout.addLayout(self.stackedlayout)

        self._initBoxes = False
        self._initWhiskers = False
        self._initFliers = False
        self._initMedians = False

        self.choose_component.setCurrentWidget("Boxes")
        self.changeComponent("boxes")
    
    def initBoxes(self):
        boxes = QWidget()
        layout_boxes = QVBoxLayout()
        layout_boxes.setContentsMargins(0,0,0,0)
        boxes.setLayout(layout_boxes)
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
        self.boxes.sig.connect(self.sig.emit)
        layout_boxes.addWidget(self.boxes)

        self.stackedlayout.setCurrentWidget(boxes)
        self._initBoxes = True

    def initWhiskers(self):
        whiskers = QWidget()
        layout_whiskers = QVBoxLayout()
        layout_whiskers.setContentsMargins(0,0,0,0)
        whiskers.setLayout(layout_whiskers)
        self.stackedlayout.addWidget(whiskers)

        layout_whiskers.addWidget(TitleLabel("Whiskers"))
        layout_whiskers.addWidget(SeparateHLine())
        self.whis = DoubleSpinBox(text="Whis")
        self.whis.button.setValue(self.get_whis())
        self.whis.button.valueChanged.connect(self.set_whis)
        layout_whiskers.addWidget(self.whis)
        self.autorange = Toggle(text="Autorange")
        self.autorange.button.setChecked(self.get_autorange())
        self.autorange.button.checkedChanged.connect(self.set_autorange)
        layout_whiskers.addWidget(self.autorange)
        self.whiskers = Line(f"{self.gid}/whiskers", self.canvas)
        self.whiskers.sig.connect(self.sig.emit)
        layout_whiskers.addWidget(self.whiskers)

        layout_whiskers.addWidget(TitleLabel("Caps"))
        layout_whiskers.addWidget(SeparateHLine())
        self.showcaps = Toggle(text="Show Caps")
        self.showcaps.button.setChecked(self.get_showcaps())
        self.showcaps.button.checkedChanged.connect(self.set_showcaps)
        layout_whiskers.addWidget(self.showcaps)
        self.capwidths = DoubleSpinBox(text="Capwidth", step=0.25)
        self.capwidths.button.setValue(self.get_capwidths())
        self.capwidths.button.valueChanged.connect(self.set_capwidths)
        layout_whiskers.addWidget(self.capwidths)
        self.caps = Line(f"{self.gid}/caps", self.canvas)
        self.caps.sig.connect(self.sig.emit)
        layout_whiskers.addWidget(self.caps)

        self.stackedlayout.setCurrentWidget(whiskers)
        self._initWhiskers = True

    def initFliers(self):
        fliers = QWidget()
        layout_fliers = QVBoxLayout()
        layout_fliers.setContentsMargins(0,0,0,0)
        fliers.setLayout(layout_fliers)
        self.stackedlayout.addWidget(fliers)
        self.showfliers = Toggle(text="Show Fliers")
        self.showfliers.button.setChecked(self.get_showfliers())
        self.showfliers.button.checkedChanged.connect(self.set_showfliers)
        layout_fliers.addWidget(self.showfliers)
        self.fliers = Marker(f"{self.gid}/fliers", self.canvas)
        self.fliers.sig.connect(self.sig.emit)
        layout_fliers.addWidget(self.fliers)

        self.stackedlayout.setCurrentWidget(fliers)
        self._initFliers = True
    
    def initMedians(self):
        medians = QWidget()
        layout_medians = QVBoxLayout()
        layout_medians.setContentsMargins(0,0,0,0)
        medians.setLayout(layout_medians)
        self.stackedlayout.addWidget(medians)

        layout_medians.addWidget(TitleLabel("Medians"))
        layout_medians.addWidget(SeparateHLine())
        self.bootstrap = SpinBox(text="Bootstrap", max=100000, step=1000)
        self.bootstrap.button.setValue(self.get_bootstrap())
        self.bootstrap.button.valueChanged.connect(self.set_bootstrap)
        layout_medians.addWidget(self.bootstrap)
        self.medians = Line(f"{self.gid}/medians", self.canvas)
        self.medians.sig.connect(self.sig.emit)
        layout_medians.addWidget(self.medians)

        layout_medians.addWidget(TitleLabel("Means"))
        layout_medians.addWidget(SeparateHLine())
        self.showmeans = Toggle(text="Show Means")
        self.showmeans.button.setChecked(self.get_showmeans())
        self.showmeans.button.checkedChanged.connect(self.set_showmeans)
        layout_medians.addWidget(self.showmeans)
        self.meanline = Toggle(text="Meanline")
        self.meanline.button.setChecked(self.get_meanline())
        self.meanline.button.checkedChanged.connect(self.set_meanline)
        layout_medians.addWidget(self.meanline)
        self.means = Line2D(f"{self.gid}/means", self.canvas)
        self.means.sig.connect(self.sig.emit)
        layout_medians.addWidget(self.means)

        self.stackedlayout.setCurrentWidget(medians)
        self._initMedians = True

    def changeComponent(self, component:str):
        match component:
            case "boxes":
                if self._initBoxes: self.stackedlayout.setCurrentIndex(0)
                else: self.initBoxes()
            case "whiskers":
                if self._initWhiskers: self.stackedlayout.setCurrentIndex(1)
                else: self.initWhiskers()
            case "fliers":
                if self._initFliers: self.stackedlayout.setCurrentIndex(2)
                else: self.initFliers()
            case "medians":
                if self._initMedians: self.stackedlayout.setCurrentIndex(3)
                else: self.initMedians()

    def find_object(self) -> list[lines.Line2D | patches.PathPatch]:
        return find_mpl_object(
            figure=self.canvas.fig,
            match=[lines.Line2D, patches.PathPatch],
            gid=self.gid,
        )

    # def update_props(self):
    #     self.showbox.button.setChecked(self.get_showbox())
    #     self.notch.button.setChecked(self.get_notch())
    #     self.vert.button.setCurrentText(self.get_vert())
    #     self.widths.button.setValue(self.get_widths())
    #     self.whis.button.setValue(self.get_whis())
    #     self.autorange.button.setChecked(self.get_autorange())
    #     self.showcaps.button.setChecked(self.get_showcaps())
    #     self.capwidths.button.setValue(self.get_capwidths())
    #     self.showfliers.button.setChecked(self.get_showfliers())
    #     self.bootstrap.button.setValue(self.get_bootstrap())
    #     self.showmeans.button.setChecked(self.get_showmeans())
    #     self.meanline.button.setChecked(self.get_meanline())

    def set_showbox(self, value:bool):
        try:
            self.props.update(showbox = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showbox(self) -> bool:
        return self.obj[0].showbox
    
    def set_notch(self, value:bool):
        try:
            self.props.update(notch = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_notch(self) -> bool:
        return self.obj[0].notch

    def set_vert(self, value:str):
        try:
            if value == "vertical": self.props.update(vert = True)
            else: self.props.update(vert = False)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        if self.obj[0].vert: return "vertical"
        return "horizontal"
    
    def set_widths(self, value:float):
        try:
            self.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.obj[0].widths

    def set_whis(self, value:float):
        try:
            self.props.update(whis = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_whis(self) -> float:
        return self.obj[0].whis 
    
    def set_autorange(self, value:bool):
        try:
            self.props.update(autorange = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_autorange(self) -> bool:
        return self.obj[0].autorange

    def set_showcaps(self, value:bool):
        try:
            self.props.update(showcaps = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showcaps(self) -> bool:
        return self.obj[0].showcaps
    
    def set_capwidths(self, value:float):
        try:
            self.props.update(capwidths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_capwidths(self) -> float:
        return self.obj[0].capwidths
    
    def set_showfliers(self, value:bool):
        try:
            self.props.update(showfliers = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showfliers(self) -> bool:
        return self.obj[0].showfliers
    
    def set_bootstrap(self, value:int):
        try:
            self.props.update(bootstrap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bootstrap(self) -> int:
        return self.obj[0].bootstrap
    
    def set_showmeans(self, value:bool):
        try:
            self.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.obj[0].showmeans
    
    def set_meanline(self, value:bool):
        try:
            self.props.update(meanline = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_meanline(self) -> bool:
        return self.obj[0].meanline
    
class Violinplot (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.choose_component = SegmentedWidget()
        self._layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Bodies', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Means', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_component.addButton(text='Min', func=lambda: self.stackedlayout.setCurrentIndex(2))
        self.choose_component.addButton(text='Max', func=lambda: self.stackedlayout.setCurrentIndex(3))
        self.choose_component.addButton(text='Bars', func=lambda: self.stackedlayout.setCurrentIndex(4))
        self.choose_component.addButton(text='Medians', func=lambda: self.stackedlayout.setCurrentIndex(5))
        self.choose_component.addButton(text='Quantiles', func=lambda: self.stackedlayout.setCurrentIndex(6))

        self.choose_component.setCurrentWidget("Bodies")

        self.stackedlayout = QStackedLayout()
        self._layout.addLayout(self.stackedlayout)

        bodies = QWidget()
        layout_bodies = QVBoxLayout()
        layout_bodies.setContentsMargins(0,0,0,0)
        bodies.setLayout(layout_bodies)
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
        self.bodies.sig.connect(self.sig.emit)
        layout_bodies.addWidget(self.bodies)

        cmeans = QWidget()
        layout_cmeans = QVBoxLayout()
        layout_cmeans.setContentsMargins(0,0,0,0)
        cmeans.setLayout(layout_cmeans)
        self.stackedlayout.addWidget(cmeans)
        self.showmeans = Toggle(text="Show Means")
        self.showmeans.button.setChecked(self.get_showmeans())
        self.showmeans.button.checkedChanged.connect(self.set_showmeans)
        layout_cmeans.addWidget(self.showmeans)
        self.cmeans = LineCollection(f"{self.gid}/cmeans",self.canvas)
        self.cmeans.sig.connect(self.sig.emit)
        layout_cmeans.addWidget(self.cmeans)

        cmins = QWidget()
        layout_cmins = QVBoxLayout()
        layout_cmins.setContentsMargins(0,0,0,0)
        cmins.setLayout(layout_cmins)
        self.stackedlayout.addWidget(cmins)
        self.cmins = LineCollection(f"{self.gid}/cmins", self.canvas)
        self.cmins.sig.connect(self.sig.emit)
        layout_cmins.addWidget(self.cmins)

        cmaxes = QWidget()
        layout_cmaxes = QVBoxLayout()
        layout_cmaxes.setContentsMargins(0,0,0,0)
        cmaxes.setLayout(layout_cmaxes)
        self.stackedlayout.addWidget(cmaxes)
        self.cmaxes = LineCollection(f"{self.gid}/cmaxes", self.canvas)
        self.cmaxes.sig.connect(self.sig.emit)
        layout_cmaxes.addWidget(self.cmaxes)

        cbars = QWidget()
        layout_cbars = QVBoxLayout()
        layout_cbars.setContentsMargins(0,0,0,0)
        cbars.setLayout(layout_cbars)
        self.stackedlayout.addWidget(cbars)
        self.showextrema = Toggle(text="Show Extrema")
        self.showextrema.button.setChecked(self.get_showextrema())
        self.showextrema.button.checkedChanged.connect(self.set_showextrema)
        layout_cbars.addWidget(self.showextrema)
        self.cbars = LineCollection(f"{self.gid}/cbars", self.canvas)
        self.cbars.sig.connect(self.sig.emit)
        layout_cbars.addWidget(self.cbars)

        cmedians = QWidget()
        layout_cmedians = QVBoxLayout()
        layout_cmedians.setContentsMargins(0,0,0,0)
        cmedians.setLayout(layout_cmedians)
        self.stackedlayout.addWidget(cmedians)
        self.showmedians = Toggle(text="Show Medians")
        self.showmedians.button.setChecked(self.get_showmedians())
        self.showmedians.button.checkedChanged.connect(self.set_showmedians)
        layout_cmedians.addWidget(self.showmedians)
        self.cmedians = LineCollection(f"{self.gid}/cmedians", self.canvas)
        self.cmedians.sig.connect(self.sig.emit)
        layout_cmedians.addWidget(self.cmedians)

        cquantiles = QWidget()
        layout_cquantiles = QVBoxLayout()
        layout_cquantiles.setContentsMargins(0,0,0,0)
        cquantiles.setLayout(layout_cquantiles)
        self.stackedlayout.addWidget(cquantiles)
        self.cquantiles = SingleColorCollection(f"{self.gid}/cquantiles", self.canvas)
        self.cquantiles.sig.connect(self.sig.emit)
        layout_cquantiles.addWidget(self.cquantiles)
    
    def find_object(self) -> list[collections.PolyCollection, collections.LineCollection]:
        return find_mpl_object(
            figure=self.canvas.fig,
            match=[collections.PolyCollection, collections.LineCollection],
            gid=self.gid,
        )

    # def update_props(self, button=None):
    #     if button != self.vert.button:
    #         self.vert.button.setCurrentText(self.get_vert())
    #     if button != self.widths.button:
    #         self.widths.button.setValue(self.get_widths())
    #     if button != self.points.button:
    #         self.points.button.setValue(self.get_points())
    #     if button != self.bw_method.button:
    #         self.bw_method.button.setCurrentText(self.get_bw_method())
    #     if button != self.showmeans.button:
    #         self.showmeans.button.setChecked(self.get_showmeans())
    #     if button != self.showextrema.button:
    #         self.showextrema.button.setChecked(self.get_showextrema())
    #     if button != self.showmedians.button:
    #         self.showmedians.button.setChecked(self.get_showmedians())

    #     self.bodies.update_props()
    #     self.cmeans.update_props()
    #     self.cmins.update_props()
    #     self.cmaxes.update_props()
    #     self.cbars.update_props()
    #     self.cmedians.update_props()
    #     self.cquantiles.update_props()
    
    def set_vert(self, value:str):
        try:
            self.props.update(orientation = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_vert(self) -> str:
        return self.obj[0].orientation
    
    def set_widths(self, value:float):
        try:
            self.props.update(widths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_widths(self) -> float:
        return self.obj[0].widths

    def set_points(self, value:int):
        try:
            self.props.update(points = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_points(self) -> int:
        return self.obj[0].points
    
    def set_bw_method(self, value:str):
        try:
            self.props.update(bw_method = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bw_method(self) -> str:
        return self.obj[0].bw_method
    
    def set_showmeans(self, value:bool):
        try:
            self.props.update(showmeans = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmeans(self) -> bool:
        return self.obj[0].showmeans

    def set_showextrema(self, value:bool):
        try:
            self.props.update(showextrema = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showextrema(self) -> bool:
        return self.obj[0].showextrema

    def set_showmedians(self, value:bool):
        try:
            self.props.update(showmedians = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_showmedians(self) -> bool:
        return self.obj[0].showmedians
    
class Eventplot(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.lineoffsets = DoubleSpinBox(text="Line Offsets")
        self.lineoffsets.button.setValue(self.get_lineoffsets())
        self.lineoffsets.button.valueChanged.connect(self.set_lineoffsets)
        self._layout.addWidget(self.lineoffsets)

        self.linelengths = DoubleSpinBox(text="Line Lengths",step=0.25)
        self.linelengths.button.setValue(self.get_linelengths())
        self.linelengths.button.valueChanged.connect(self.set_linelengths)
        self._layout.addWidget(self.linelengths)

        self.eventcollection = LineCollection(self.gid, self.canvas)
        self.eventcollection.sig.connect(self.sig.emit)
        self._layout.addWidget(self.eventcollection)
    
    def find_object(self) -> list[collections.EventCollection]:
        return find_mpl_object(
            figure=self.canvas.fig,
            match=[collections.EventCollection],
            gid=self.gid,
        )

    # def update_props(self, button=None):
    #     if button != self.orientation.button:
    #         self.orientation.button.setCurrentText(self.get_orientation())
    #     if button != self.lineoffsets.button:
    #         self.lineoffsets.button.setValue(self.get_lineoffsets())
    #     if button != self.linelengths.button:
    #         self.linelengths.button.setValue(self.get_linelengths())
    #     if button != self.linewidths.button:
    #         self.linewidths.button.setValue(self.get_linewidths())

    #     self.eventcollection.update_props()

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation

    def set_lineoffsets(self, value:float):
        try:
            self.props.update(lineoffsets = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_lineoffsets(self) -> float:
        return self.obj[0].lineoffsets
    
    def set_linelengths(self, value:float):
        try:
            self.props.update(linelengths = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_linelengths(self) -> float:
        return self.obj[0].linelengths

class Hist2d (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.binx = SpinBox(text="Bins X")
        self.binx.button.setValue(self.get_binx())
        self.binx.button.valueChanged.connect(self.set_binx)
        self._layout.addWidget(self.binx)

        self.biny = SpinBox(text="Spin Y")
        self.biny.button.setValue(self.get_biny())
        self.biny.button.valueChanged.connect(self.set_biny)
        self._layout.addWidget(self.biny)

        self.density = Toggle(text="Density")
        self.density.button.setChecked(self.get_density())
        self.density.button.checkedChanged.connect(self.set_density)
        self._layout.addWidget(self.density)

        self.quadmesh = QuadMesh(self.gid, self.canvas)
        self.quadmesh.sig.connect(self.sig.emit)
        self._layout.addWidget(self.quadmesh)

    def find_object(self) -> list[collections.QuadMesh]:
        return find_mpl_object(
            figure=self.canvas.fig,
            match=[collections.QuadMesh],
            gid=self.gid,
        )
    
    # def update_props(self, button=None):
    #     if button != self.binx.button:
    #         self.binx.button.setValue(self.get_binx())
    #     if button != self.biny.button:
    #         self.biny.button.setValue(self.get_biny())
    #     if button != self.density.button:
    #         self.density.button.setChecked(self.get_density())

    #     self.quadmesh.update_props()

    def set_binx(self, value:int):
        try:
            self.props.update(binx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_binx(self) -> int:
        return self.obj[0].binx
    
    def set_biny(self, value:int):
        try:
            self.props.update(biny = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_biny(self) -> int:
        return self.obj[0].biny
    
    def set_density(self, value:bool):
        try:
            self.props.update(density = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_density(self) -> bool:
        return self.obj[0].density
