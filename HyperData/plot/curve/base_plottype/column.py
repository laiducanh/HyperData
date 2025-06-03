from PySide6.QtWidgets import QVBoxLayout
from ui.base_widgets.line_edit import LineEdit
from ui.base_widgets.spinbox import DoubleSpinBox, SpinBox
from ui.base_widgets.button import ComboBox, Toggle
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
from config.settings import GLOBAL_DEBUG, logger
from matplotlib import patches, colors, lines
from matplotlib.pyplot import colormaps
from mpl_toolkits.mplot3d.art3d import Poly3DCollection as Poly3D
import numpy as np

DEBUG = False

class Column (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Bar'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        self.barwidth = DoubleSpinBox(
            text = 'Bar Width',
            min  = 0, 
            max  = 5, 
            step = 0.1
        )
        self.barwidth.button.setValue(self.get_barwidth())
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        layout.addWidget(self.barwidth)

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self.onChanged.emit)
        layout.addWidget(rect)

        layout.addWidget(TitleLabel('Connecting lines'))
        layout.addWidget(SeparateHLine())
        
        collection = LineCollection(f"_{self.gid.split('.')[0]}", self.canvas)
        collection.onChanged.connect(self.onChanged.emit)
        layout.addWidget(collection)
        
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle],
            gid=self.gid
        )

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation
    
    def set_bottom (self, value:str):
        try:
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.find_object()[0].bottom)

    def set_barwidth (self, value:float):
        try: 
            self.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.find_object()[0].width

class Column3D (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Column 3D'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["x","y","z"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        self.dx = DoubleSpinBox(
            text = 'Dx',
            min  = 0,
            max  = 5,
            step = 0.1
        )
        self.dx.button.setValue(self.get_dx())
        self.dx.button.valueChanged.connect(self.set_dx)
        layout.addWidget(self.dx)

        self.dy = DoubleSpinBox(
            text = "Dy",
            min  = 0,
            max  = 5,
            step = 0.1
        )
        self.dy.button.setValue(self.get_dy())
        self.dy.button.valueChanged.connect(self.set_dy)
        layout.addWidget(self.dy)

        self.color = ColorDropdown(
            text  = "Color", 
            color = self.get_color()
        )
        self.color.button.colorChanged.connect(self.set_color)
        layout.addWidget(self.color)

        self.shade = Toggle(text="Shade") 
        self.shade.button.setChecked(self.get_shade())
        self.shade.button.checkedChanged.connect(self.set_shade)
        layout.addWidget(self.shade)

        collection = Poly3DCollection(self.gid, self.canvas)
        collection.onChanged.connect(self.onChanged.emit)
        layout.addWidget(collection)
    
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
        return self.find_object()[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.find_object()[0].bottom)

    def set_dx (self, value:float):
        try: 
            self.props.update(Dx = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dx (self) -> float:
        return self.find_object()[0].Dx
    
    def set_dy(self, value:float):
        try:
            self.props.update(Dy = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_dy(self) -> float:
        return self.find_object()[0].Dy
    
    def set_color(self, value:str):
        try:
            self.props.update(color = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_color(self) -> str:
        _color = self.find_object()[0].color
        if not _color:
            color = np.max(self.find_object()[0].get_facecolor(),axis=0)
            return colors.to_hex(color)
        return _color
    
    def set_shade(self, value:bool):
        try:
            self.props.update(shade = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_shade(self) -> bool:
        return self.find_object()[0].shade
    
class Dot (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Dot'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        marker = Marker(self.gid, self.canvas)
        marker.onChanged.connect(self.onChanged.emit)
        layout.addWidget(marker)

        alpha = SpinBox(
            text = 'Transparent',
            step = 10
        )
        alpha.button.setValue(self.get_alpha())
        alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(alpha)

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
        return self.find_object()[0].orientation
    
    def set_bottom (self, value:str):
        try:
            if value == "": value = 0
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.find_object()[0].bottom)
    
    def set_alpha(self, value:int):
        for obj in self.find_object():
            obj.set_alpha(value/100)
        self.onChanged.emit()
        self.canvas.draw_idle()
    
    def get_alpha(self) -> int:
        if not self.find_object()[0].get_alpha():
            return 100
        return int(self.find_object()[0].get_alpha()*100)

class ClusteredColumn (Column):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Bar'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        self.barwidth = DoubleSpinBox(
            text = 'Bar Width',
            min  = 0, 
            max  = 5, 
            step = 0.1
        )
        self.barwidth.button.setValue(self.get_barwidth())
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        layout.addWidget(self.barwidth)

        self.distance = SpinBox(
            min  = 0,
            max  = 100,
            step = 10,
            text = "Distance"
        )
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        layout.addWidget(self.distance)

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self.onChanged.emit)
        layout.addWidget(rect)
    
    def set_distance(self, value:int):
        try:
            self.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.find_object()[0].distance*100)

class ClusteredDot (Dot):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Dot'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        self.distance = SpinBox(
            min  = 0,
            max  = 100,
            step = 10,
            text = "Distance"
        )
        self.distance.button.setValue(self.get_distance())
        self.distance.button.valueChanged.connect(self.set_distance)
        layout.addWidget(self.distance)

        marker = Marker(self.gid, self.canvas)
        marker.onChanged.connect(self.onChanged.emit)
        layout.addWidget(marker)

        alpha = SpinBox(
            text = 'Transparent',
            step = 10
        )
        alpha.button.setValue(self.get_alpha())
        alpha.button.valueChanged.connect(self.set_alpha)
        layout.addWidget(alpha)
    
    def set_distance(self, value:int):
        try:
            self.props.update(distance = float(value/100))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_distance(self) -> int:
        return int(self.find_object()[0].distance*100)

class Dumbbell (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)
    
        if "." in gid:
            self.gid = gid.split(".")[0]
        else: self.gid = gid
    
        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Dumbbell'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        layout.addWidget(TitleLabel('Lines'))
        layout.addWidget(SeparateHLine())
        line = Line(f"{self.gid}/0", self.canvas)
        line.onChanged.connect(self.onChanged.emit)
        layout.addWidget(line)

        layout.addWidget(TitleLabel('Head 1'))
        layout.addWidget(SeparateHLine())
        head1 = Marker(f"_{self.gid}/1", self.canvas)
        head1.onChanged.connect(self.onChanged.emit)
        layout.addWidget(head1)

        layout.addWidget(TitleLabel('Head 2'))
        layout.addWidget(SeparateHLine())
        head2 = Marker(f"_{self.gid}/2", self.canvas)
        head2.onChanged.connect(self.onChanged.emit)
        layout.addWidget(head2)

    def find_object(self):
        return find_mpl_object(self.canvas.fig, [lines.Line2D], self.gid)

    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation

class Marimekko (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Marimekko'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self.onChanged.emit)
        layout.addWidget(rect)
        
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle],
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

class Treemap (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Treemap'))
        layout.addWidget(SeparateHLine())

        self.rounded = DoubleSpinBox(text="Rounding factor")
        self.rounded.button.setValue(self.get_rounded())
        self.rounded.button.valueChanged.connect(self.set_rounded)
        layout.addWidget(self.rounded)

        self.pad = DoubleSpinBox(
            min  = 0,
            max  = 20,
            step = 0.5,
            text = "Padding"
        )
        self.pad.button.setValue(self.get_pad())
        self.pad.button.valueChanged.connect(self.set_pad)
        layout.addWidget(self.pad)

        self.cmap_on = Toggle(text="Use colormap")
        self.cmap_on.button.setChecked(self.get_cmap_on())
        self.cmap_on.button.checkedChanged.connect(self.set_cmap_on)
        layout.addWidget(self.cmap_on)

        self.cmap = ComboBox(
            items = colormaps(), 
            text  = "Colormap"
        )
        self.cmap.button.setCurrentText(self.get_cmap())
        self.cmap.button.currentTextChanged.connect(self.set_cmap)
        layout.addWidget(self.cmap)

        rect = Rectangle(self.gid, self.canvas)
        rect.onChanged.connect(self.onChanged.emit)
        layout.addWidget(rect)
    
    def find_object(self) -> list[patches.FancyBboxPatch]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.FancyBboxPatch],
            gid=self.gid,
        )
    
    def set_rounded(self, value:float):
        try:
            self.props.update(rounded=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_rounded(self) -> float:
        return self.find_object()[0].rounded

    def set_pad(self, value:float):
        try:
            self.props.update(pad = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_pad(self) -> float:
        return float(self.find_object()[0].pad)
    
    def set_cmap_on(self, value:bool):
        try:
            self.props.update(cmap_on=value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_cmap_on(self) -> bool:
        return self.find_object()[0].cmap_on
          
    def set_cmap(self, value:str):
        try:
            self.props.update(cmap = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)

    def get_cmap(self) -> str:
        return self.find_object()[0].cmap

class WaterFall (PlotConfigBase):
    def __init__(self, gid:str, canvas:Canvas, plot:NewPlot, parent=None):
        super().__init__(gid, canvas, plot, parent)

        self.initUI()
    
    def initUI(self):
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        layout.addWidget(TitleLabel('Waterfall'))
        layout.addWidget(SeparateHLine())

        self.orientation = ComboBox(
            items = ["vertical","horizontal"],
            text  = "Orientation"
        )
        self.orientation.button.setCurrentText(self.get_orientation())
        self.orientation.button.currentTextChanged.connect(self.set_orientation)
        layout.addWidget(self.orientation)

        self.bottom = LineEdit(text="Bottom")
        self.bottom.button.setFixedWidth(150)
        self.bottom.button.setText(self.get_bottom())
        self.bottom.button.returnPressed.connect(lambda: self.set_bottom(self.bottom.button.text()))
        layout.addWidget(self.bottom)

        self.barwidth = DoubleSpinBox(
            text = 'Bar Width',
            min  = 0,
            max  = 5,
            step = 0.1
        )
        self.barwidth.button.setValue(self.get_barwidth())
        self.barwidth.button.valueChanged.connect(self.set_barwidth)
        layout.addWidget(self.barwidth)

        layout.addWidget(TitleLabel('Positive Bars'))
        layout.addWidget(SeparateHLine())
        pbars = Rectangle(f"{self.gid}/positive", self.canvas)
        pbars.onChanged.connect(self.onChanged.emit)
        layout.addWidget(pbars)

        layout.addWidget(TitleLabel('Negative Bars'))
        layout.addWidget(SeparateHLine())
        nbars = Rectangle(f"{self.gid}/negative", self.canvas)
        nbars.onChanged.connect(self.onChanged.emit)
        layout.addWidget(nbars)

        layout.addWidget(TitleLabel('Connected Lines'))
        layout.addWidget(SeparateHLine())
        cline = LineCollection(f"_{self.gid}/line", self.canvas)
        cline.onChanged.connect(self.onChanged.emit)
        layout.addWidget(cline)
    
    def find_object (self) -> list[patches.Rectangle]:
        return find_mpl_object(
            source=self.canvas.fig,
            match=[patches.Rectangle],
            gid=self.gid
        )
    
    def set_orientation(self, value:str):
        try:
            self.props.update(orientation = value.lower())
            self.update_plot()
        except Exception as e:
            logger.exception(e)
            self.plot.progressbar.changeColor()
    
    def get_orientation(self) -> str:
        return self.find_object()[0].orientation
    
    def set_bottom (self, value:str):
        try:
            self.props.update(bottom = float(value))
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_bottom (self) -> str:
        return str(self.find_object()[0].bottom)

    def set_barwidth (self, value:float):
        try: 
            self.props.update(width = value)
            self.update_plot()
        except Exception as e:
            logger.exception(e)
    
    def get_barwidth (self) -> float:
        return self.find_object()[0].width