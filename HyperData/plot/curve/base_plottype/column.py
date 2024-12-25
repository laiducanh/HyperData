from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QWidget, QStackedLayout
from ui.base_widgets.frame import SeparateHLine
from ui.base_widgets.text import TitleLabel
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox, Slider
from ui.base_widgets.button import ComboBox, Toggle, SegmentedWidget
from ui.base_widgets.color import ColorDropdown
from plot.insert_plot.insert_plot import NewPlot
from plot.canvas import Canvas
from plot.curve.base_elements.patches import Rectangle
from plot.curve.base_elements.collection import Poly3DCollection
from plot.curve.base_elements.line import Marker, Line, DumbbellMarker
from plot.utilis import find_mpl_object
from config.settings import GLOBAL_DEBUG, logger, linestyle_lib
from matplotlib import patches, colors, lines, collections
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as Poly3D
import numpy as np

DEBUG = False

class Column (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.prop = dict(
            orientation = "vertical",
            bottom      = 0,
            align       = "center",
            width       = 0.8
        )

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel("Column"))
        self._layout.addWidget(SeparateHLine())

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

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.sig.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()

    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[patches.Rectangle],
                               gid=self.gid)
    
    def update_plot(self):
        # self.sig.emit()
        self.plot.plotting(**self.prop)
        
    def set_orientation(self, value:str):
        try:
            self.prop.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.prop.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_barwidth (self, value:float):
        try: 
            self.prop.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.obj[0].width

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)
    
class Column3D (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.prop = dict(
            orientation = "z",
            bottom      = 0,
            Dx          = 0.5,
            Dy          = 0.5,
            shade       = True,
            zsort       = "average",
            color       = self.get_color(),
        )

        self.initUI()

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
        self.column.sig.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()

    def find_object (self) -> list[Poly3D]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[Poly3D],
                               gid=self.gid)
    
    def update_plot(self):
        # self.sig.emit()
        self.plot.plotting(**self.prop)
        
    def set_orientation(self, value:str):
        try:
            self.prop.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.prop.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)

    def set_dx (self, value:float):
        try: 
            self.prop.update(Dx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dx (self) -> float:
        return self.obj[0].Dx
    
    def set_dy(self, value:float):
        try:
            self.prop.update(Dy = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dy(self) -> float:
        return self.obj[0].Dy
    
    def set_color(self, value:str):
        try:
            self.prop.update(color = value)
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
            self.prop.update(shade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_shade(self) -> bool:
        return self.obj[0].shade

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class Dot(QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.prop = dict()

        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel("Dot"))
        self._layout.addWidget(SeparateHLine())

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
        self.dot.sig.connect(self.sig.emit)
        self._layout.addWidget(self.dot)

        self._layout.addStretch()
    
    def find_object(self):
        return find_mpl_object(
            self.canvas.fig,
            [lines.Line2D],
            gid=self.gid
        )
    
    def update_plot(self):
        # self.sig.emit()
        self.plot.plotting(**self.prop)
    
    def set_orientation(self, value:str):
        try:
            self.prop.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.prop.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.obj[0].bottom)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class ClusteredColumn(Column):
    def __init__(self, gid, canvas: Canvas, plot: NewPlot = None, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.prop.update(distance = 1)
    
    def initUI(self):
        super().initUI()

        self._layout.insertWidget(0, TitleLabel("Clustered Column"))
        self._layout.insertWidget(1, SeparateHLine())

        self.distance = SpinBox(min=0,max=100,step=10,text="Distance")
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        self._layout.insertWidget(2, self.distance)

    def set_distance(self, value:int):
        try:
            self.prop.update(distance = float(value/100))
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

        self._layout.insertWidget(0, TitleLabel("Clustered Column"))
        self._layout.insertWidget(1, SeparateHLine())

        self.distance = SpinBox(min=0,max=100,step=10,text="Distance")
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        self._layout.insertWidget(2, self.distance)
    
    def set_distance(self, value:int):
        try:
            self.prop.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.obj[0].distance*100)

class Dumbbell(QWidget):
    sig = Signal()
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        if "." in gid:
            self.gid = gid.split(".")[0]
        else: self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.props = dict()
        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel("Lines"))
        self._layout.addWidget(SeparateHLine())

        self.line = Line(self.gid, self.canvas)
        self._layout.addWidget(self.line)

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self._layout.addWidget(TitleLabel("Head 1"))
        self._layout.addWidget(SeparateHLine())

        self.head1 = DumbbellMarker(f"{self.gid}.1", self.canvas)
        self._layout.addWidget(self.head1)

        self._layout.addWidget(TitleLabel("Head 2"))
        self._layout.addWidget(SeparateHLine())

        self.head1 = DumbbellMarker(f"{self.gid}.2", self.canvas)
        self._layout.addWidget(self.head1)

    def find_object(self):
        return find_mpl_object(self.canvas.fig, [lines.Line2D], self.gid)

    def update_plot(self):
        self.plot.plotting(**self.props)

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.obj[0].orientation

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class Marimekko (QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)
        
        self.gid = gid
        self.canvas = canvas
        self.plot = plot
        self.obj = self.find_object()
        self.prop = dict(orientation = "vertical")

        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self._layout.addWidget(TitleLabel("Column"))
        self._layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(items=["vertical","horizontal"],text="Orientation")
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        self._layout.addWidget(self.orientation)

        self.column = Rectangle(self.gid, self.canvas, self.parent())
        self.column.sig.connect(self.sig.emit)
        self._layout.addWidget(self.column)

        self._layout.addStretch()
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[patches.Rectangle],
                               gid=self.gid)
    
    def update_plot(self):
        # self.sig.emit()
        self.plot.plotting(**self.prop)
    
    def set_orientation(self, value:str):
        try:
            self.prop.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_orientation(self) -> str:
        return self.obj[0].orientation
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

class Treemap(QWidget):
    sig = Signal()
    def __init__(self, gid, canvas:Canvas, plot:NewPlot=None, parent=None):
        super().__init__(parent)

        self.gid = gid
        self.canvas = canvas
        self.setParent(parent)
        self.plot = plot
        self.obj = self.find_object()
        self.props = dict(
            pad   = 0,
            cmap  = "tab10",
            alpha = 1)
        self.initUI()
    
    def initUI(self):
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0,0,0)

        self.rounded = Toggle(text="Rounded")
        self.rounded.button.setChecked(self.get_rounded())
        self.rounded.button.checkedChanged.connect(self.set_rounded)
        self._layout.addWidget(self.rounded)

        self.pad = DoubleSpinBox(min=0,max=20,step=0.5,text="Padding")
        self.pad.button.setValue(self.get_pad())
        self.pad.button.valueChanged.connect(self.set_pad)
        self._layout.addWidget(self.pad)

        self.cmap = ComboBox(items=colormaps(), text="Colormap")
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        self._layout.addWidget(self.cmap)

        self.alpha = Slider(text='Transparency',min=0,max=100)
        self.alpha.button.setValue(self.get_alpha())
        self.alpha.button.valueChanged.connect(self.set_alpha)
        self._layout.addWidget(self.alpha)
        
        self._layout.addStretch()
    def find_object(self) -> list[patches.Rectangle|patches.FancyBboxPatch]:
        return find_mpl_object(figure=self.canvas.fig,
                               match=[patches.Rectangle,patches.FancyBboxPatch],
                               gid=self.gid)
 
    
    def update_plot(self):
        # self.sig.emit()
        self.plot.plotting(**self.props)
    
    def set_rounded(self, value:bool):
        try:
            self.props.update(rounded=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rounded(self) -> bool:
        return self.obj[0].rounded

    def set_pad(self, value:float):
        try:
            self.props.update(pad = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return float(self.obj[0].pad)
          
    def set_cmap(self, value:str):
        try:
            self.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_cmap(self) -> str:
        return self.obj[0].cmap

    def set_alpha (self, value:float):
        try: 
            self.props.update(alpha = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_alpha (self):
        if self.obj[0].get_alpha() != None:
            return int(self.obj[0].get_alpha()*100)
        return 100

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.obj = self.find_object()
        return super().paintEvent(a0)

