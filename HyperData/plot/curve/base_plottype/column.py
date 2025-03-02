from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.color import ColorDropdown
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.collection import Poly3DCollection
from plot.curve.base_elements.line import Marker, Line, LineCollection
from plot.utilis import find_mpl_object
from plot.curve.base_plottype.base import PlotConfigBase
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from matplotlib import patches, colors, lines, collections
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as Poly3D
import numpy as np

DEBUG = False

class Column (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
        
    def initUI(self):
        super().initUI()

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        self._layout.addWidget(self.bottom)

        self.barwidth = DoubleSpinBox(text='Bar Width',min=0,max=5,step=0.1)
        self.barwidth.button.setValue(self.get_barwidth())
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        self._layout.addWidget(self.barwidth)

        self.connected_lines = LineCollection(f"_{self.gid.split('.')[0]}", self.canvas)
        self.connected_lines.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.connected_lines)

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()

    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle],
            gid=self.gid
        )

    def update_props(self):
        self.orientation.button.setCurrentText(self.get_orientation())
        self.bottom.button.setText(self.get_bottom())
        self.barwidth.button.setValue(self.get_barwidth())
        
    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_barwidth (self, value:float):
        try: 
            self.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.obj[0].width
    
class Column3D (PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.orientation = ComboBox(items=["x","y","z"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        self._layout.addWidget(self.bottom)

        self.dx = DoubleSpinBox(text='Dx',min=0,max=5,step=0.1)
        self.dx.button.setValue(self.get_dx())
        self.dx.button.valueChanged.connect(self.set_dx)
        self._layout.addWidget(self.dx)

        self.dy = DoubleSpinBox(text="Dy",min=0,max=5,step=0.1)
        self.dy.button.setValue(self.get_dy())
        self.dy.button.valueChanged.connect(self.set_dy)
        self._layout.addWidget(self.dy)

        self.color = ColorDropdown(text="Color", color=self.get_color(), parent=self.parent())
        self.color.button.colorChanged.connect(self.set_color)
        self._layout.addWidget(self.color)

        self.shade = Toggle(text="Shade") 
        self.shade.button.setChecked(self.get_shade())
        self.shade.button.checkedChanged.connect(self.set_shade)
        self._layout.addWidget(self.shade) 

        self.column = Poly3DCollection(self.gid, self.canvas, self.parent())
        self.column.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()

    def find_object (self) -> list[Poly3D]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[Poly3D],
            gid=self.gid
        )
        
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
            if value == "": value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_dx (self, value:float):
        try: 
            self.props.update(Dx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dx (self) -> float:
        return self.obj[0].Dx
    
    def set_dy(self, value:float):
        try:
            self.props.update(Dy = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dy(self) -> float:
        return self.obj[0].Dy
    
    def set_color(self, value:str):
        try:
            self.props.update(color = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_color(self) -> str:
        _color = self.obj[0].color
        if not _color:
            color = np.max(self.obj[0].get_facecolor(),axis=0)
            return colors.to_hex(color)
        return _color
    
    def set_shade(self, value:bool):
        try:
            self.props.update(shade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_shade(self) -> bool:
        return self.obj[0].shade

class Dot(PlotConfigBase):
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

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        self._layout.addWidget(self.bottom)

        self.dot = Marker(self.gid, self.canvas, self.parent())
        self.dot.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.dot)

        self._layout.addStretch()
    
    def find_object(self):
        return find_mpl_object(
            self.canvas.fig,
            [lines.Line2D],
            gid=self.gid
        )
    
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
            if value == "": value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

class ClusteredColumn(Column):
    def __init__(self, gid, canvas: Canvas, plot: NewPlot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        super().initUI()

        self.distance = SpinBox(min=0,max=100,step=10,text="Distance")
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        self._layout.insertWidget(2, self.distance)

    def set_distance(self, value:int):
        try:
            self.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.obj[0].distance*100)

class ClusteredDot(Dot):
    def __init__(self, gid, canvas, plot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        super().initUI()

        self.distance = SpinBox(min=0,max=100,step=10,text="Distance")
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        self._layout.insertWidget(2, self.distance)
    
    def set_distance(self, value:int):
        try:
            self.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.obj[0].distance*100)

class Dumbbell(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
        
        if "." in gid:
            self.gid = gid.split(".")[0]
        else: self.gid = gid
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel("Lines"))
        self._layout.addWidget(SeparateHLine())

        self.line = Line(self.gid, self.canvas)
        self.line.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.line)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self._layout.addWidget(TitleLabel("Head 1"))
        self._layout.addWidget(SeparateHLine())

        self.head1 = Marker(f"{self.gid}.1", self.canvas)
        self.head1.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.head1)

        self._layout.addWidget(TitleLabel("Head 2"))
        self._layout.addWidget(SeparateHLine())

        self.head2 = Marker(f"{self.gid}.2", self.canvas)
        self.head2.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.head1)

    def find_object(self):
        return find_mpl_object(self.canvas.fig, [lines.Line2D], self.gid)

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation

class Marimekko (PlotConfigBase):
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

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle],
            gid=self.gid
        )

    def update_props(self):
        self.orientation.button.setCurrentText(self.get_orientation())
    
    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_orientation(self) -> str:
        return self.obj[0].orientation

class Treemap(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.rounded = DoubleSpinBox(text="Rounded")
        self.rounded.button.setValue(self.get_rounded())
        self.rounded.button.valueChanged.connect(self.set_rounded)
        self._layout.addWidget(self.rounded)

        self.pad = DoubleSpinBox(min=0,max=20,step=0.5,text="Padding")
        self.pad.button.setValue(self.get_pad())
        self.pad.button.valueChanged.connect(self.set_pad)
        self._layout.addWidget(self.pad)

        self.cmap_on = Toggle(text="Use colormap")
        self.cmap_on.button.setChecked(self.get_cmap_on())
        self.cmap_on.button.checkedChanged.connect(self.set_cmap_on)
        self._layout.addWidget(self.cmap_on)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        self._layout.addWidget(self.cmap)

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.onChange.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self.column.facecolor.setEnabled(not self.get_cmap_on())
        self.cmap.setEnabled(self.get_cmap_on())
        
        self._layout.addStretch()
    def find_object(self) -> list[patches.FancyBboxPatch]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.FancyBboxPatch],
            gid=self.gid,
        )
    
    def update_props(self):
        self.rounded.button.setValue(self.get_rounded())
        self.pad.button.setValue(self.get_pad())
        self.cmap_on.button.setChecked(self.get_cmap_on())
        self.cmap.button.setCurrentText(self.get_cmap())
    
    def set_rounded(self, value:float):
        try:
            self.props.update(rounded=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rounded(self) -> float:
        return self.obj[0].rounded

    def set_pad(self, value:float):
        try:
            self.props.update(pad = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return float(self.obj[0].pad)
    
    def set_cmap_on(self, value:bool):
        try:
            self.props.update(cmap_on=value)
            self.update_plot()
            self.column.facecolor.setEnabled(not value)
            self.cmap.setEnabled(value)
        except Exception as e:
            logger.exception(e)
    
    def get_cmap_on(self) -> bool:
        return self.obj[0].cmap_on
          
    def set_cmap(self, value:str):
        try:
            self.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_cmap(self) -> str:
        return self.obj[0].cmap

class WaterFall(PlotConfigBase):
    sig = Signal()
    def __init__(self, gid, canvas, plot = None, parent=None):
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

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        self._layout.addWidget(self.bottom)

        self.barwidth = DoubleSpinBox(text='Bar Width',min=0,max=5,step=0.1)
        self.barwidth.button.setValue(self.get_barwidth())
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        self._layout.addWidget(self.barwidth)

        self.choose_component = SegmentedWidget()
        self._layout.addWidget(self.choose_component)

        self.choose_component.addButton(text='Positive Bars', func=lambda: self.stackedlayout.setCurrentIndex(0))
        self.choose_component.addButton(text='Negative Bars', func=lambda: self.stackedlayout.setCurrentIndex(1))
        self.choose_component.addButton(text='Connected Lines', func=lambda: self.stackedlayout.setCurrentIndex(2))

        self.stackedlayout = QStackedLayout()
        self._layout.addLayout(self.stackedlayout)

        self.choose_component.setCurrentWidget("Positive Bars")
        self.stackedlayout.setCurrentIndex(0)
    
        pos_bars = Rectangle(f"{self.gid}/positive", self.canvas)
        pos_bars.onChange.connect(self.sig.emit)
        self.stackedlayout.addWidget(pos_bars)

        neg_bars = Rectangle(f"{self.gid}/negative", self.canvas)
        neg_bars.onChange.connect(self.sig.emit)
        self.stackedlayout.addWidget(neg_bars)

        line = LineCollection(f"{self.gid}/line", self.canvas)
        line.onChange.connect(self.sig.emit)
        self.stackedlayout.addWidget(line)

    def update_props(self):
        self.orientation.button.setCurrentText(self.get_orientation())
        self.bottom.button.setText(self.get_bottom())
        self.barwidth.button.setValue(self.get_barwidth())
        
    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_barwidth (self, value:float):
        try: 
            self.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.obj[0].width